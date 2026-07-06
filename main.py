import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
SESSION_STRING = os.environ.get("SESSION_STRING")
TARGET_USER = "hLoshByHere"
TARGET_CHAT_ID = -1003555828336

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.ChatAction)
async def monitor_my_actions(event):
    # التأكد من مراقبة المجموعة المطلوبة فقط
    if event.chat_id != TARGET_CHAT_ID:
        return
    
    # التأكد أن الفعل صادر عنك أنت (السورس)
    me = await client.get_me()
    if event.action_message and event.action_message.sender_id == me.id:
        try:
            # جلب معلومات الجهاز الحالي
            auths = await client(GetAuthorizationsRequest())
            device = next((a.device_model for a in auths.authorizations if a.current), "جهاز غير معروف")
            
            # تحديد نوع الفعل
            action_text = "حدث غير معروف"
            if event.user_added: action_text = "إضافة عضو"
            elif event.user_kicked: action_text = "طرد عضو"
            elif event.admin_rights_changed: action_text = "تعديل صلاحيات مشرف"
            elif event.chat_title_changed: action_text = "تغيير اسم المجموعة"

            # صياغة رسالة التنبيه
            msg = (
                f"🚨 **تنبيه نشاط من حسابك (السورس):**\n\n"
                f"📝 **الحدث:** {action_text}\n"
                f"👤 **المستهدف:** {event.user.first_name if event.user else 'غير محدد'}\n"
                f"💻 **الجهاز المستخدم:** {device}\n"
                f"🔗 **رابط القروب:** https://t.me/c/1003555828336/{event.action_message.id}"
            )
            
            await client.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"Error: {e}")

async def main():
    print("🚀 سورس المراقبة يعمل الآن...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
