import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- الإعدادات ---
SESSION_STRING = "1AZWarzsBu7ZqkyVaeYivrdM-nhqJg9TFUx44GHlgQRrcpd0vchjVvroNHxDWpCBU2K03fyw2kpA3jXwMYDh9k4-EvHKlh4XITdhSfvXpgH66ujafg8tYvYLOcPvK6wMB1-IhIrRrKQZITOAlw1VqZ4syROvRPbjWmTw1GGchZ_WBicPUHox35s_vzr9hKeAOKMj09Pe3gg50tnJ5brKzILSwAT78gdhA54QDIozPWmMhjnhR_HD9BUN5jfBK8nAAJyxoqtZf5pYotpZMDDYbt0ox0oUmZoNXiBt71HPSZM33s0MhGpz-ayQQQEBIFQqLjkY94k84m42c9kOIhIxuyhd9CZ6T_lY="
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER = "hLoshByHere" 
TARGET_CHAT_ID = -1003712727917 

client = TelegramClient(StringSession(SESSION_STRING.strip()), API_ID, API_HASH)

# 1. أمر الفحص
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_bot(event):
    await event.edit("✅ السورس يعمل ويراقب الأفعال في القروب!")

# 2. مراقبة الأفعال (طرد، إضافة، صلاحيات)
@client.on(events.ChatAction)
async def monitor_actions(event):
    if event.chat_id != TARGET_CHAT_ID:
        return
    
    # التحقق من أن النشاط تم من قبلك
    me = await client.get_me()
    if event.action_message and event.action_message.sender_id == me.id:
        try:
            # جلب معلومات الجهاز
            auths = await client(GetAuthorizationsRequest())
            device = next((a.device_model for a in auths.authorizations if a.current), "جهاز غير معروف")
            
            msg = (
                f"👤 **نشاط جديد قمت به في القروب:**\n\n"
                f"📝 **الحدث:** {event.stringify()[:150]}\n"
                f"💻 **الجهاز المستخدم:** {device}"
            )
            await client.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"Error in monitor_actions: {e}")

# 3. تنبيه عند تسجيل دخول جهاز جديد (يعمل تلقائياً)
@client.on(events.NewMessage)
async def check_new_device(event):
    # نتحقق إذا كان التحديث يخص قائمة الأجهزة
    try:
        # يمكن استدعاؤه يدوياً بـ .تحديث
        if event.raw_text == ".تحديث":
            auths = await client(GetAuthorizationsRequest())
            msg = "📱 **الأجهزة المتصلة بحسابك:**\n" + "\n".join([a.device_model for a in auths.authorizations])
            await client.send_message(TARGET_USER, msg)
    except:
        pass

async def main():
    await client.start()
    print("🚀 السورس يعمل..")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
