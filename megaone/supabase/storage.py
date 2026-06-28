import io
import mimetypes
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from supabase import create_client


def get_supabase_client():
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY,
    )


def get_supabase_service_client():
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_ROLE_KEY,
    )


@deconstructible
class SupabaseStorage(Storage):
    def __init__(self, bucket_name=None, public=False, **kwargs):
        self.bucket_name = bucket_name or settings.SUPABASE_STORAGE_BUCKET
        self.public = public
        self._client = None
        self._service_client = None

    @property
    def client(self):
        if self._client is None:
            self._client = get_supabase_client()
        return self._client

    @property
    def service_client(self):
        if self._service_client is None:
            self._service_client = get_supabase_service_client()
        return self._service_client

    def _get_storage(self):
        return self.client.storage.from_(self.bucket_name)

    def _get_service_storage(self):
        return self.service_client.storage.from_(self.bucket_name)

    def _open(self, name, mode="rb"):
        if mode != "rb":
            raise ValueError("SupabaseStorage only supports rb mode")
        try:
            data = self._get_service_storage().download(name)
            return File(io.BytesIO(data), name)
        except Exception as e:
            raise FileNotFoundError(f"File not found: {name}") from e

    def _save(self, name, content):
        content.seek(0)
        file_bytes = content.read()
        content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
        self._get_service_storage().upload(
            path=name,
            file=file_bytes,
            file_options={"content-type": content_type, "upsert": "true"},
        )
        return name

    def exists(self, name):
        try:
            self._get_service_storage().info(name)
            return True
        except Exception:
            return False

    def url(self, name):
        if self.public:
            return self._get_storage().get_public_url(name)
        signed_url = self._get_service_storage().create_signed_url(name, expires_in=3600)
        if isinstance(signed_url, dict):
            return signed_url.get("signedURL", signed_url.get("url", ""))
        return signed_url

    def delete(self, name):
        try:
            self._get_service_storage().remove([name])
        except Exception:
            pass

    def listdir(self, path=""):
        try:
            items = self._get_service_storage().list(path)
            dirs, files = [], []
            for item in items:
                name = item.get("name", "")
                if item.get("id") is None:
                    dirs.append(name)
                else:
                    files.append(name)
            return dirs, files
        except Exception:
            return [], []

    def size(self, name):
        try:
            info = self._get_service_storage().info(name)
            if isinstance(info, dict):
                return info.get("metadata", {}).get("size", 0) or info.get("size", 0)
            return info.size if hasattr(info, "size") else 0
        except Exception:
            return 0

    def get_accessed_time(self, name):
        from django.utils.timezone import now
        return now()

    def get_created_time(self, name):
        from django.utils.timezone import now
        return now()

    def get_modified_time(self, name):
        from django.utils.timezone import now
        return now()
