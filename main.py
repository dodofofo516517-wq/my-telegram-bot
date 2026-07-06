import asyncio
import os
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_ID = 8965415461 
TARGET_USERNAME = "@hLoshByHere"

# جلب الجلسة من متغيرات البيئة في Railway
SESSION_STRING = os.environ.get("SESSION_STRING")

# التحقق من وجود الجلسة لمنع الأخطاء
if not SESSION_STRING:
    raise ValueError("⚠️ خطأ: SESSION_STRING غير موجود في إعدادات Railway!")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# 1. أمر الفحص
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def handler(event):
    await event.edit(f"✅ السورس يعمل بنجاح للمراقبة لصالح: {TARGET_USERNAME}")

# 2. مراقبة الأجهزة الجديدة (اتصال جديد)
async def watch_new_sessions():
    try:
        auths = await client(GetAuthorizationsRequest())
        known_hashes = {a.hash for a in auths.authorizations}
        
        while True:
            await asyncio.sleep(60)
            current_auths = await client(GetAuthorizationsRequest())
            for auth in current_auths.authorizations:
                if auth.hash not in known_hashes:
                    msg = (f"🚨 **تنبيه: تم اكتشاف اتصال جديد!**\n\n"
                           f"📱 الجهاز: {auth.device_model}\n"
                           f"💻 النظام: {auth.platform}\n"
                           f"📍 الموقع: {auth.country}\n"
                           f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    await client.send_message(TARGET_ID, msg)
                    known_hashes.add(auth.hash)
    except Exception as e:
        print(f"Session Monitor Error: {e}")

# 3. مراقبة تغييرات الصلاحيات
@client.on(events.ChatAction)
async def monitor_admin_logs(event):
    if event.admin_rights_changed:
        try:
            me = await client.get_me()
            async for log in client.iter_admin_log(event.chat_id, limit=1):
                if log.user_id == me.id:
                    await client.send_message(TARGET_ID, f"⚙️ **تنبيه إداري:** تم تغيير صلاحيات بواسطة حسابك في قروب: {event.chat.title}")
                    break
        except: pass

async def main():
    await client.start()
    print("🚀 سورس المراقبة يعمل بنجاح الآن...")
    asyncio.create_task(watch_new_sessions())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
