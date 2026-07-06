import asyncio
from telethon import TelegramClient, events

# --- الإعدادات ---
SESSION_STRING = "1AZWarzsBuwl8jFH-dOoO5RYGSH33HlLqKCDK8Dbrhg_PQc7o05vJlpE2d0hTBUNLz20bDnYdH9ithnoxtQ8vTUsoLdXWjpLkGx3Y_AXlAQex1eJI2GXOWZK54KaTrFS3hBSuYrtutFk1-TZUAnVhF7PLJLC_TUxI3eK-bkwcjBTBfGRYAkyBbPn1CnyQ1j1LxKHXyYQFIVkCC4X9WyHqZqfsyDCxKGfIvFbj_mfhZVI395oIKtx6D3hp8ptq16kx5Px0TPAJLzMmxmmlxQU4waLvIBpKEs0tEkQM5Hax60Qd1YIsWOtzfHLK-x1ubZAxZDzHAwqzkGhsReojrmYi2_cNtl5tsJs="
BOT_TOKEN = "8804475722:AAG-6RKc7W1tTJELdxKsKhFJ3KJwQxAxawM"
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

TARGET_USER = "hLoshByHere" 
TARGET_CHAT_ID = -1003555828336 

# السورس (للمراقبة) والبوت (للإرسال)
client = TelegramClient('user_session', API_ID, API_HASH)
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.ChatAction)
async def monitor_actions(event):
    if event.chat_id != TARGET_CHAT_ID:
        return
    
    me = await client.get_me()
    # مراقبة الأفعال التي تقوم بها أنت فقط
    if event.action_message and event.action_message.sender_id == me.id:
        try:
            # رسالة التنبيه المرسلة عبر البوت
            msg = (
                f"🚨 **نشاط جديد قمت به في القروب:**\n\n"
                f"📝 **التفاصيل:** {event.stringify()[:200]}\n"
                f"🔗 **القروب:** https://t.me/c/1003555828336/{event.action_message.id}"
            )
            await bot.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"Error: {e}")

@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check(event):
    await event.edit("✅ السورس والبوت يعملان بكفاءة!")

async def main():
    print("🚀 بدء تشغيل السورس والبوت...")
    await client.start(session=SESSION_STRING)
    await asyncio.gather(client.run_until_disconnected(), bot.run_until_disconnected())

if __name__ == '__main__':
    asyncio.run(main())
