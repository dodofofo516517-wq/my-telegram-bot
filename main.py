import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
SESSION_STRING = os.environ.get("SESSION_STRING", "")
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER = "hLoshByHere"
# ايدي المجموعة (يجب الحصول عليه عبر بوت جلب الايدي)
TARGET_CHAT_ID = -1002245366530 

client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

@client.on(events.ChatAction)
async def monitor_admin_changes(event):
    # مراقبة المجموعة المحددة فقط
    if event.chat_id != TARGET_CHAT_ID:
        return

    # مراقبة تغيير صلاحيات المشرفين
    if getattr(event, 'admin_rights_changed', False):
        try:
            # جلب تفاصيل الجهاز الحالي
            auths = await client(GetAuthorizationsRequest())
            current_device = "غير معروف"
            for auth in auths.authorizations:
                if auth.current:
                    current_device = f"{auth.device_model} ({auth.platform})"
            
            # معلومات الشخص الذي تغيرت صلاحياته
            user = await event.get_user()
            user_name = user.first_name if user else "غير معروف"
            user_id = user.id if user else "غير معروف"
            user_username = f"@{user.username}" if user and user.username else "لا يوجد"

            msg = (
                f"🚨 **تنبيه تغيير صلاحيات مشرف**\n\n"
                f"👤 **الشخص:** {user_name}\n"
                f"🆔 **الأيدي:** `{user_id}`\n"
                f"🔗 **اليوزر:** {user_username}\n\n"
                f"💻 **الجهاز المنفذ للأمر:** {current_device}\n"
                f"💬 **المجموعة:** {event.chat.title}"
            )
            await client.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"خطأ في معالجة التنبيه: {e}")

async def main():
    await client.start()
    print("🚀 سورس المراقبة المتقدم يعمل...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
