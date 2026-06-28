from django.apps import AppConfig


class SupabaseConfig(AppConfig):
    name = "megaone.supabase"
    verbose_name = "Supabase Integration"

    def ready(self):
        pass
