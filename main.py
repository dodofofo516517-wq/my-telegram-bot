import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
SESSION_STRING = "1AZWarzsBu701Waif7Hd7gUUt-OFIVhcwRicidHeAUV6J5_1OIrw0FXMLGDC3stUjmEbY1Xj7es-jCk6pG5hyyxSGZXkpGn8ptGDKwBlGQiyb47O4rTHDjTRsXHTQeRSTGDji0ZJJjIJdyQDOEOj_2h1jXkZbtgkRifRwha2CaHWpGNReTnCD7vyUVirxX7ZndNEddGnQrraQhZe7a8jetTrHCDMELhTB6E6kiUxp2eTBTdwFFMjQuuf_6lmXvRCVc89N8jB8btWKhVsp7MhOwdbtZZl0ujTGGwTzT8SIYxkiVW-j-97sCHJp5AoXyxAt9-a8nobTCjr8TiMWLFMvpvKyIAeX8Fg="
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER = "hLoshByHere" 

client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

# 1. مراقب الاتصالات الجديدة (تنبيه عند دخول جهاز جديد)
@client.on(events.NewMessage(pattern=r'\.فحص_اتصال'))
async def check_auth(event):
    auths = await client(GetAuthorizationsRequest())
    msg = "📱 **الأجهزة المتصلة بحسابك:**\n"
    for auth in auths.authorizations:
        msg += f"- {auth.device_model} ({auth.platform}) - {auth.country}\n"
    await client.send_message(TARGET_USER, msg)

# 2. مراقبة تغيير الصلاحيات في المجموعة
@client.on(events.ChatAction)
async def admin_handler(event):
    # نتحقق إذا كان الحدث تغيير صلاحيات
    if event.user_added or event.user_kicked or event.admin_rights_changed:
        chat = await event.get_chat()
        # نراقب المجموعة المحددة (تأكد من وضع رابط المجموعة أو الـ ID الخاص بها)
        msg = f"⚠️ **تنبيه في المجموعة: {chat.title}**\n\nحدث تغيير: {event.stringify()}"
        await client.send_message(TARGET_USER, msg)

async def main():
    await client.start()
    print("🚀 السورس يعمل ويراقب الاتصالات والمجموعات...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
