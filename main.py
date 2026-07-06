import asyncio
import os
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
# لضمان عدم حدوث خطأ Base64، نستخدم os.environ لجلب الجلسة
# اذهب في Railway إلى Variables وأضف متغير باسم SESSION_STRING وضع قيمته هناك
SESSION_STRING = os.environ.get("SESSION_STRING", "ضع_الجلسة_الجديدة_هنا_إذا_لم_تستخدم_المتغيرات")
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# بيانات التنبيه
TARGET_ID = 8965415461 
TARGET_USERNAME = "@hLoshByHere"

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r'\.فحص'))
async def handler(event):
    await event.edit(f"✅ السورس يعمل بكفاءة لصالح: {TARGET_USERNAME}")

# مراقبة الأجهزة
async def watch_new_sessions():
    try:
        auths = await client(GetAuthorizationsRequest())
        known_hashes = [a.hash for a in auths.authorizations]
        while True:
            await asyncio.sleep(60)
            current_auths = await client(GetAuthorizationsRequest())
            for auth in current_auths.authorizations:
                if auth.hash not in known_hashes:
                    msg = (f"🚨 **تنبيه دخول جهاز جديد**\n\n"
                           f"📱 الجهاز: {auth.device_model}\n"
                           f"💻 النظام: {auth.platform}\n"
                           f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    await client.send_message(TARGET_ID, msg)
                    known_hashes.append(auth.hash)
    except Exception as e:
        print(f"Error in monitoring: {e}")

# مراقبة الصلاحيات (Admin Logs)
@client.on(events.ChatAction)
async def monitor_admin_logs(event):
    try:
        if event.admin_rights_changed:
            async for log in client.iter_admin_log(event.chat_id, limit=1):
                msg = (f"⚙️ **تنبيه إداري**\n"
                       f"تغيير صلاحيات في قروب: {event.chat.title}\n"
                       f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                await client.send_message(TARGET_ID, msg)
                break
    except: pass

async def main():
    await client.start()
    print("🚀 السورس يعمل بنجاح...")
    asyncio.create_task(watch_new_sessions())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
