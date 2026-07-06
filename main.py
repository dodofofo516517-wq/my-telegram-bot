import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ضع بياناتك هنا
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
# استخرج StringSession جديدة تماماً ولا تفتحها في تطبيق آخر
SESSION_STRING = "هنا_ضع_الجلسة_الجديدة" 

# 1. التعريف أولاً
client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

# 2. تعريف الأوامر بعد تعريف الكلينت
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_bot(event):
    await event.edit("✅ السورس يعمل بنجاح!")

async def main():
    try:
        await client.start()
        print("🚀 سورس المراقبة يعمل الآن...")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == '__main__':
    asyncio.run(main())
