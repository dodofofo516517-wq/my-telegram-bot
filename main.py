import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
SESSION_STRING = os.environ.get("SESSION_STRING", "")
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER = "hLoshByHere" # يوزر حساب التنبيهات
TARGET_CHAT_ID = -1002245366530 # تأكد من الأيدي الصحيح للمجموعة

client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

# مراقبة كل الأفعال (طرد، إضافة، تغيير صلاحيات، إلخ)
@client.on(events.ChatAction)
async def monitor_all_actions(event):
    # 1. مراقبة المجموعة المحددة فقط
    if event.chat_id != TARGET_CHAT_ID:
        return

    # 2. مراقبة أفعالك أنت فقط (Sender)
    # ملاحظة: إذا كان الحدث صادر عنك، فإن event.action_message.from_id سيساوي الأيدي الخاص بك
    me = await client.get_me()
    if event.action_message and event.action_message.sender_id != me.id:
        return

    try:
        # جلب تفاصيل الجهاز الحالي
        auths = await client(GetAuthorizationsRequest())
        current_device = "غير معروف"
        for auth in auths.authorizations:
            if auth.current:
                current_device = f"{auth.device_model} ({auth.platform})"

        # تجهيز تفاصيل الحدث
        action_desc = "حدث غير معروف"
        if event.user_added: action_desc = "إضافة عضو"
        elif event.user_kicked: action_desc = "طرد عضو"
        elif event.admin_rights_changed: action_desc = "تغيير صلاحيات مشرف"

        msg = (
            f"👤 **نشاط جديد من حسابك (السورس):**\n"
            f"📝 **الحدث:** {action_desc}\n"
            f"💬 **المجموعة:** {event.chat.title}\n"
            f"💻 **الجهاز المنفذ:** {current_device}\n\n"
            f"ℹ️ التفاصيل: {event.stringify()[:100]}"
        )
        await client.send_message(TARGET_USER, msg)
    except Exception as e:
        print(f"خطأ في المراقبة: {e}")

async def main():
    try:
        await client.start()
        print("🚀 السورس يعمل ويراقب أفعالك أنت فقط...")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"فشل الاتصال: {e}")

if __name__ == '__main__':
    asyncio.run(main())
