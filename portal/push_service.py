import json
import logging
import threading
from django.conf import settings
from pywebpush import webpush, WebPushException

logger = logging.getLogger(__name__)

def send_web_push(subscription_info, payload_data, ttl=86400):
    """
    Delivers a web push payload directly to a browser push endpoint using VAPID.
    subscription_info: dict with keys 'endpoint', 'keys': {'p256dh': '...', 'auth': '...'}
    payload_data: dict containing title, body, url, icon, badge, tag, etc.
    """
    private_key = getattr(settings, 'WEBPUSH_VAPID_PRIVATE_KEY', None)
    admin_email = getattr(settings, 'WEBPUSH_ADMIN_EMAIL', 'mailto:admin@holifamily.edu.np')
    
    if not private_key:
        logger.warning("WEBPUSH_VAPID_PRIVATE_KEY not configured in settings.")
        return False, "VAPID key not configured"

    payload_json = json.dumps(payload_data)

    vapid_claims = {
        "sub": admin_email
    }

    try:
        response = webpush(
            subscription_info=subscription_info,
            data=payload_json,
            vapid_private_key=private_key,
            vapid_claims=vapid_claims,
            ttl=ttl
        )
        return True, "Delivered"
    except WebPushException as ex:
        # Handle subscription expiration / mismatch (HTTP 400, 403, 404, or 410 Gone)
        if ex.response is not None and ex.response.status_code in (400, 403, 404, 410):
            return False, "Gone"
        logger.error(f"WebPushException sending push: {ex}")
        return False, str(ex)
    except Exception as e:
        logger.error(f"Unexpected error sending push: {e}")
        return False, str(e)


def broadcast_push_notification(title, body, url="/", icon="/static/icons/icon-192x192.png", badge="/static/icons/badge-96x96.png", tag="hf-alert", event_type="general", user=None, is_async=True):
    """
    Broadcasts a notification to all active devices or a specific user's registered devices.
    Executes in a background thread by default so user requests are never delayed.
    """
    def _execute():
        from portal.models import PushSubscription, NotificationLog

        query = PushSubscription.objects.filter(is_active=True)
        if user:
            query = query.filter(user=user)

        subscriptions = list(query)
        if not subscriptions:
            # Log zero-subscription dispatch
            NotificationLog.objects.create(
                title=title,
                body=body,
                url=url,
                icon=icon,
                tag=tag,
                event_type=event_type,
                success_count=0,
                failure_count=0,
                status='sent'
            )
            return

        payload = {
            "title": title,
            "body": body,
            "icon": icon,
            "badge": badge,
            "url": url,
            "tag": tag,
            "sound": "/static/audio/notification.wav",
            "vibrate": [500, 250, 500, 250, 500, 250, 800],
            "silent": False,
            "renotify": True,
            "requireInteraction": True,
            "timestamp": int(threading.get_native_id() if hasattr(threading, 'get_native_id') else 0)
        }

        success_count = 0
        failure_count = 0
        expired_ids = []

        for sub in subscriptions:
            sub_info = {
                "endpoint": sub.endpoint,
                "keys": {
                    "p256dh": sub.p256dh,
                    "auth": sub.auth
                }
            }
            ok, msg = send_web_push(sub_info, payload)
            if ok:
                success_count += 1
            else:
                failure_count += 1
                if msg == "Gone":
                    expired_ids.append(sub.id)

        # Cleanup expired subscriptions (uninstalled PWA, revoked permissions)
        if expired_ids:
            PushSubscription.objects.filter(id__in=expired_ids).delete()

        status = 'sent'
        if failure_count > 0 and success_count == 0:
            status = 'failed'
        elif failure_count > 0:
            status = 'partial'

        NotificationLog.objects.create(
            title=title,
            body=body,
            url=url,
            icon=icon,
            tag=tag,
            event_type=event_type,
            success_count=success_count,
            failure_count=failure_count,
            status=status
        )

    if is_async:
        thread = threading.Thread(target=_execute, daemon=True)
        thread.start()
    else:
        _execute()
