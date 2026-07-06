import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- البيانات ---
# 1. حساب السورس (المراقب)
SESSION = "1AZWarzsBu8NBA9nrnT_E3iBZkHeYV36FTtQa0dsHHwYbRQr-aPJ9yG3cfKQGB9GD0FizqskxSqUWe2uMF9eHKZ7bxkf96n67036JV7NE2jJKE2DoyyhOplSDWN11NyCeDeCHuSw2BJKz8XLlGbtsaZNyIMsoGIfuqVfJLHrK6nMYLouMrgHqA6WYnPJZnOR5p9ZWqkqqyNtEtNsmRjlSN56JJhnHlwPXmBg42urpH5q_Cv17J_9oNuhXiKgDDMvQHIEjk8JVheiQToGdzWSXleBZ4sYY-Sx6yaT4aMq5PjflhhYKdmlxCeCkQyzcvxVz3aDkW8gpTeOZByIjcRdOwK-e38OO0ck="
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# 2. بيانات الحساب الذي يستقبل التنبيهات (الهدف)
TARGET_ID = 8965415461 
TARGET_USERNAME = "@hLoshByHere" # اليوزر الذي سيتم إرسال التنبيهات إليه

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- أمر الفحص ---
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def handler(event):
    await event.edit(f"✅ السورس يعمل بنجاح للمراقبة لصالح الحساب: {TARGET_USERNAME}")

# --- مراقبة الأجهزة (إرسال للهدف) ---
async def watch_new_sessions():
    auths = await client(GetAuthorizationsRequest())
    known_count = len(auths.authorizations)
    while True:
        await asyncio.sleep(60)
        try:
            current_auths = await client(GetAuthorizationsRequest())
            if len(current_auths.authorizations) > known_count:
                new_dev = current_auths.authorizations[0]
                msg = (f"🚨 **تنبيه دخول جهاز جديد**\n\n"
                       f"📱 الجهاز: {new_dev.device_model}\n"
                       f"🌐 IP: {new_dev.ip}\n"
                       f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                # إرسال التنبيه للهدف بالأيدي واليوزر
                await client.send_message(TARGET_ID, f"إلى {TARGET_USERNAME}:\n{msg}")
                known_count = len(current_auths.authorizations)
        except: pass

# --- مراقبة القروبات ---
@client.on(events.ChatAction)
async def group_monitor(event):
    me = await client.get_me()
    try:
        async for log in client.iter_admin_log(event.chat_id, limit=1):
            if log.user_id == me.id: 
                msg = (f"⚙️ **تنبيه إدارة القروب**\n"
                       f"📝 الحدث: تم تغيير صلاحيات أو معلومات بواسطة حساب السورس\n"
                       f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                # إرسال التنبيه للهدف
                await client.send_message(TARGET_ID, f"إلى {TARGET_USERNAME}:\n{msg}")
                break
    except: pass

async def main():
    await client.start()
    print(f"🚀 السورس جاهز ويرسل التنبيهات إلى {TARGET_USERNAME}")
    asyncio.create_task(watch_new_sessions())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
