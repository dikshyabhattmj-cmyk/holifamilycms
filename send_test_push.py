"""
Test Script: Send Push Notification to all subscribed devices
Usage:
    .\venv\Scripts\python send_test_push.py
"""
import os
import sys
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holifamily_core.settings')
django.setup()

from portal.models import PushSubscription, NotificationLog
from portal.push_service import broadcast_push_notification

def main():
    print("=" * 60)
    print("  Holy Family Secondary School - Push Notification Test")
    print("=" * 60)

    # 1. Check Subscribed Devices
    subscriptions = PushSubscription.objects.filter(is_active=True)
    count = subscriptions.count()
    print(f"\n[1] Subscribed Devices in Database: {count}")
    
    if count == 0:
        print("\n⚠️  No active device subscriptions found.")
        print("👉  Please open the website in your phone or browser:")
        print("    https://overbid-removal-clerk.ngrok-free.dev/")
        print("    Click 'Allow' or tap '🔔 Alerts' at the top to register your device.")
        return

    for idx, sub in enumerate(subscriptions, 1):
        device_ua = sub.user_agent[:45] if sub.user_agent else "Unknown Device"
        print(f"    {idx}. ID #{sub.id} | Endpoint: {sub.endpoint[:45]}... | {device_ua}")

    # 2. Trigger Real-Time Push Notification
    title = "📢 Test Alert: Holy Family School"
    body = "Real-time push delivery & notification sound alert is working perfectly!"
    url = "/notices/"

    print(f"\n[2] Broadcasting notification...")
    print(f"    Title: {title}")
    print(f"    Body:  {body}")
    print(f"    URL:   {url}")

    # Execute synchronously so we can read the immediate result
    broadcast_push_notification(
        title=title,
        body=body,
        url=url,
        tag="hf-test-alert",
        event_type="test",
        is_async=False
    )

    # 3. Check Latest Log
    latest_log = NotificationLog.objects.order_by('-created_at').first()
    if latest_log:
        print("\n[3] Broadcast Results:")
        print(f"    Status:         {latest_log.status.upper()}")
        print(f"    Delivered:      {latest_log.success_count} device(s)")
        print(f"    Failed/Expired: {latest_log.failure_count} device(s)")
        if latest_log.success_count > 0:
            print("\n🎉 SUCCESS! Push notification with sound sent to your device(s).")
        else:
            print("\n⚠️  Notification was not received. Please re-enable alerts on your device.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
