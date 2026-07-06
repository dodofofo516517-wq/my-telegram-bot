import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
# الجلسة المباشرة التي زودتني بها
SESSION_STRING = "1AZWarzsBu7ZqkyVaeYivrdM-nhqJg9TFUx44GHlgQRrcpd0vchjVvroNHxDWpCBU2K03fyw2kpA3jXwMYDh9k4-EvHKlh4XITdhSfvXpgH66ujafg8tYvYLOcPvK6wMB1-IhIrRrKQZITOAlw1VqZ4syROvRPbjWmTw1GGchZ_WBicPUHox35s_vzr9hKeAOKMj09Pe3gg50tnJ5brKzILSwAT78gdhA54QDIozPWmMhjnhR_HD9BUN5jfBK8nAAJyxoqtZf5pYotpZMDDYbt0ox0oUmZoNXiBt71HPSZM33s0MhGpz-ayQQQEBIFQqLjkY94k84m42c9kOIhIxuyhd9CZ6T_lY="
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER = "hLoshByHere" 
# الأيدي الجديد الذي زودتني به
TARGET_CHAT_ID = -1003712727917 
# رابط المجموعة للمرجع: https://t.me/+8Djv1gteUwpjOGM0

client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

# 1. أمر الفحص
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_bot(event):
    await event.edit("✅ السورس يعمل بكامل طاقته ويراقب أفعالك في القروب!")

# 2. مراقبة كل أفعالك (أنت فقط) في المجموعة المحددة
@client.on(events.ChatAction)
async def monitor_my_actions(event):
    if event.chat_id != TARGET_CHAT_ID:
        return
    
    me = await client.get_me()
    # التأكد أن النشاط صادر منك أنت
    if event.action_message and event.action_message.sender_id == me.id:
        try:
            msg = f"👤 **نشاط جديد قمت به في القروب:**\n\n**الحدث:** {event.stringify()[:150]}"
            await client.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"Error: {e}")

async def main():
    await client.start()
    print("🚀 سورس المراقبة يعمل بنجاح..")
    # تنبيه عند التشغيل بالأجهزة المتصلة
    try:
        auths = await client(GetAuthorizationsRequest())
        current = next((a for a in auths.authorizations if a.current), None)
        if current:
            await client.send_message(TARGET_USER, f"📱 **السورس بدأ العمل الآن!**\nجهازك الحالي المتصل: {current.device_model}")
    except:
        pass
        
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
