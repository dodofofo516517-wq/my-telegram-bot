import asyncio
from telethon import TelegramClient, events
from telethon.بsessions import StringSession

# ضع الجلسة الجديدة هنا بعد استخراجها
SESSION_STRING = "ضع_هنا_الجلسة_الجديدة_التي_استخرجتها" 
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# 1. التعريف أولاً
client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

# 2. الأوامر تأتي بعد تعريف الكلينت
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
