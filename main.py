import asyncio
from telethon import TelegramClient, events

# --- الإعدادات ---
SESSION_STRING = "1AZWarzsBu6aYCss8UCHaJb4Yjos6BXvSyP2n-PKtkpVJuIv-ba0TLNn6YxLGZi44uZztJ4xq6WCVelgl_HTOFSfWzADaDo7GsMzesRZNMcl0fHyIn7psNmxI6um3JEoyOMbPFt8L-pulMDR1l6EVkfTL5XmmbxGQwWyUgziBYLL2dBbqP3oTuf_eszazo3s0jpSadAA89rVf6GZ83A3E69rWnq_rktDiqRMq31w-V3-FK5rvpIZ7hMOeFJj343FSXrd58TxT9bC20uIRonAM_zEy8bg3YRyryNSdhCu0m7-V49d0J3x4r5eTGkxZpo-NRkGmN49n0HNYxhSxVmuMakaoSzttnUo"
BOT_TOKEN = "8804475722:AAG-6RKc7W1tTJELdxKsKhFJ3KJwQxAxawM"
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER = "hLoshByHere" # يوزر حسابك للتنبيه
TARGET_CHAT_ID = -1003555828336 # أيدي القروب الجديد

# السورس يراقب
client = TelegramClient('userbot_session', API_ID, API_HASH)
# البوت يرسل
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.ChatAction)
async def monitor_everything(event):
    if event.chat_id != TARGET_CHAT_ID:
        return
    
    me = await client.get_me()
    # مراقبة أفعالك أنت فقط
    if event.action_message and event.action_message.sender_id == me.id:
        try:
            # تفاصيل الجهاز الحالي
            auths = await client.get_messages('me', limit=1) # خدعة بسيطة لجلب معلومات الاتصال
            
            # بناء رسالة التنبيه التفصيلية
            msg = (
                f"🚨 **نشاط جديد من السورس:**\n\n"
                f"📝 **الحدث:** {event.stringify()[:200]}\n"
                f"🔗 **رابط القروب:** https://t.me/c/1003555828336/{event.action_message.id}\n"
                f"💻 **تم الإرسال بواسطة البوت.**"
            )
            # البوت يرسل التنبيه لحساب التنبيهات
            await bot.send_message(TARGET_USER, msg)
        except Exception as e:
            print(f"Error: {e}")

# أمر الفحص
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check(event):
    await event.edit("✅ نظام المراقبة يعمل بكامل قوته!")

async def main():
    await client.start(session=StringSession(SESSION_STRING))
    print("🚀 سورس المراقبة والبوت يعملان الآن...")
    await asyncio.gather(client.run_until_disconnected(), bot.run_until_disconnected())

if __name__ == '__main__':
    asyncio.run(main())
