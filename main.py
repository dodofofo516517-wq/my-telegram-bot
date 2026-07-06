import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest
import os

# --- الإعدادات ---
# الأفضل قراءة المتغير من Railway مباشرة
SESSION_STRING = os.environ.get("SESSION_STRING", "")
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER = "hLoshByHere" 

# 1. تعريف الـ client أولاً (هذا هو الخطأ الذي كان يظهر)
client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

# 2. الآن نضع أسطر المراقبة (لأن client أصبح معروفاً)

@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_bot(event):
    await event.edit("✅ السورس يعمل ويراقب الصلاحيات والاتصالات!")

@client.on(events.NewMessage(pattern=r'\.فحص_اتصال'))
async def check_auth(event):
    auths = await client(GetAuthorizationsRequest())
    msg = "📱 **الأجهزة المتصلة بحسابك:**\n"
    for auth in auths.authorizations:
        status = " (الجهاز الحالي)" if auth.current else ""
        msg += f"- {auth.device_model} | {auth.country}{status}\n"
    await client.send_message(TARGET_USER, msg)
    await event.edit("تم إرسال قائمة الأجهزة لحساب التنبيهات.")

@client.on(events.ChatAction)
async def monitor_admin_logs(event):
    # نتحقق من الخاصية بأمان لتجنب أي خطأ
    if getattr(event, 'admin_rights_changed', False):
        try:
            chat = await event.get_chat()
            msg = f"⚠️ **تنبيه: تم تغيير صلاحيات مشرف!**\n\nالدردشة: {chat.title}\nالمشرف: {event.user.first_name}"
            await client.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"خطأ في إرسال التنبيه: {e}")

# 3. تشغيل البوت
async def main():
    await client.start()
    print("🚀 سورس المراقبة يعمل بنجاح...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
