import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
# ضع الجلسة الخاصة بك هنا
SESSION_STRING = "1AZWarzsBu701Waif7Hd7gUUt-OFIVhcwRicidHeAUV6J5_1OIrw0FXMLGDC3stUjmEbY1Xj7es-jCk6pG5hyyxSGZXkpGn8ptGDKwBlGQiyb47O4rTHDjTRsXHTQeRSTGDji0ZJJjIJdyQDOEOj_2h1jXkZbtgkRifRwha2CaHWpGNReTnCD7vyUVirxX7ZndNEddGnQrraQhZe7a8jetTrHCDMELhTB6E6kiUxp2eTBTdwFFMjQuuf_6lmXvRCVc89N8jB8btWKhVsp7MhOwdbtZZl0ujTGGwTzT8SIYxkiVW-j-97sCHJp5AoXyxAt9-a8nobTCjr8TiMWLFMvpvKyIAeX8Fg="
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER = "hLoshByHere" 

client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

# 1. أمر الفحص
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_bot(event):
    await event.edit("✅ السورس يعمل ويراقب الصلاحيات والاتصالات!")

# 2. أمر فحص الأجهزة المتصلة
@client.on(events.NewMessage(pattern=r'\.فحص_اتصال'))
async def check_auth(event):
    auths = await client(GetAuthorizationsRequest())
    msg = "📱 **الأجهزة المتصلة بحسابك:**\n"
    for auth in auths.authorizations:
        status = " (الجهاز الحالي)" if auth.current else ""
        msg += f"- {auth.device_model} | {auth.country}{status}\n"
    await client.send_message(TARGET_USER, msg)
    await event.edit("تم إرسال قائمة الأجهزة لحساب التنبيهات.")

# 3. مراقب تغيير الصلاحيات (آمن ضد الأخطاء)
@client.on(events.ChatAction)
async def monitor_admin_logs(event):
    # نتحقق فقط إذا كان الحدث يخص صلاحيات المشرفين
    if getattr(event, 'admin_rights_changed', False):
        try:
            chat = await event.get_chat()
            msg = f"⚠️ **تنبيه: تم تغيير صلاحيات مشرف!**\n\nالدردشة: {chat.title}\nالمشرف: {event.user.first_name}"
            await client.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"خطأ في إرسال التنبيه: {e}")

async def main():
    await client.start()
    print("🚀 سورس المراقبة يعمل بنجاح...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
