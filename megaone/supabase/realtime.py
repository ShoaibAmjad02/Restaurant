import json
import logging

from django.conf import settings
from supabase import create_client

logger = logging.getLogger(__name__)


def get_supabase_client():
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY,
    )


def get_realtime_client():
    client = get_supabase_client()
    return client.realtime


def subscribe_to_orders(callback, channel_name="order-updates", table="kitchen_orders", filter_column=None, filter_value=None):
    client = get_supabase_client()
    channel = client.channel(channel_name)

    def handle_change(payload):
        try:
            callback(payload)
        except Exception as e:
            logger.error(f"Realtime callback error: {e}")

    change_filter = {"event": "*", "schema": "public", "table": table}
    if filter_column and filter_value:
        change_filter["filter"] = f"{filter_column}=eq.{filter_value}"

    channel.on_postgres_changes(change_filter, handle_change)
    channel.subscribe()
    return channel


def unsubscribe(channel):
    try:
        channel.unsubscribe()
    except Exception as e:
        logger.error(f"Error unsubscribing: {e}")
