import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# الإعدادات
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
SESSION_STRING = "1AZWarzsBuwl8jFH-dOoO5RYGSH33HlLqKCDK8Dbrhg_PQc7o05vJlpE2d0hTBUNLz20bDnYdH9ithnoxtQ8vTUsoLdXWjpLkGx3Y_AXlAQex1eJI2GXOWZK54KaTrFS3hBSuYrtutFk1-TZUAnVhF7PLJLC_TUxI3eK-bkwcjBTBfGRYAkyBbPn1CnyQ1j1LxKHXyYQFIVkCC4X9WyHqZqfsyDCxKGfIvFbj_mfhZVI395oIKtx6D3hp8ptq16kx5Px0TPAJLzMmxmmlxQU4waLvIBpKEs0tEkQM5Hax60Qd1YIsWOtzfHLK-x1ubZAxZDzHAwqzkGhsReojrmYi2_cNtl5tsJs="
TARGET_USER = "hLoshByHere"
TARGET_CHAT_ID = -1003555828336
MY_ID = 8980682089

# تعريف الكلينت مع تعطيل التحقق من الأجهزة (لتقليل فرص الحظر)
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, device_model="Railway-Monitor")

@client.on(events.ChatAction)
async def monitor_my_actions(event):
    if event.chat_id != TARGET_CHAT_ID:
        return
    
    # مراقبة أفعالك فقط
    if event.action_message and event.action_message.sender_id == MY_ID:
        try:
            msg = f"👤 **نشاط قمت به:**\n\n{event.stringify()[:200]}"
            await client.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"Error: {e}")

async def main():
    print("🚀 محاولة الاتصال...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
