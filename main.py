import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession

# 1. بيانات الحساب الأساسية
API_ID = 1234567  # استبدله بـ api_id الخاص بك
API_HASH = "your_api_hash_here"  # استبدله بـ api_hash الخاص بك
NEW_SESSION = "1AZWarzsBuzJ7j0cOdaUM4F5JnnF-v6CGikZkHYdjTsO024yj4gW16AJp_i856i4OdGOqP_Yh0AUJYrIkx1sVmG8MnEoQgS6fYELp6nDyifr6XVXR__t-eFNjMwxH6MdxXdA8XjGfLx1y-vEJ-57XqMvGvp2tXBo-phYGQN42qS6Lv3OtUjEyT2X0bkHVJ6_v222LPD3scXcFk6JMCDE9vCKcbE-bfryVb5vpXHFwI3hYDcF7qsQHfCwS7-39DisKbXwSmLFWSYOxAv1mgramcefexTIDI7TyGMEsv6G31FJz3KEtNDdwkJh6UgOK9l9He__osLyX8KHscMi7BuTsnkFRpHYPAFM="

# 2. ضبط التوقيت المعتمد (السعودية)
SAUDI_TZ = pytz.timezone("Asia/Riyadh")

# 3. إعدادات الجهاز الحقيقي لعدم حرق الجلسة نهائياً
client = TelegramClient(
    StringSession(NEW_SESSION),
    api_id=API_ID,
    api_hash=API_HASH,
    device_model="iPhone 15 Pro Max",
    system_version="iOS 17.5",
    app_version="10.11.1"
)

# ==================== [ قسم الأوامر والاستجابة ] ====================
# هذا الأمر مدمج الآن لكي تختبر به استجابة البوت فوراً بمجرد تشغيله
@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تست$|^\.ping$'))
async def test_command(event):
    now_saudi = datetime.now(SAUDI_TZ).strftime('%Y-%m-%d %H:%M:%S')
    await event.edit(f"🚀 **البوت شغال تمام التمام والأوامر تستجيب!**\n⏰ **الوقت الحالي في السعودية:** `{now_saudi}`")

# يمكنك إضافة أي أمر آخر هنا بنفس الطريقة، ومثال ذلك:
# @client.on(events.NewMessage(outgoing=True, pattern=r'^\.تنظيف$'))
# async def clean_command(event):
#     ... كود الأمر هنا ...


# ==================== [ قسم الرادار المستقل ] ====================
async def run_radar():
    print("🛰️ الرادار بدأ العمل في الخلفية بشكل مستقل...")
    while True:
        try:
            # ----------------------------------------------------
            # ضع كود الرادار الخاص بك (الفحص، الصيد، المراقبة) هنا
            # ----------------------------------------------------
            
            # فاصل زمني إجباري (3 ثوانٍ) لحماية الجلسة من الحرق النهائي
            await asyncio.sleep(3)
            
        except errors.FloodWaitError as e:
            print(f"⚠️ تليجرام يطلب التهدئة. انتظار {e.seconds} ثانية لحماية الجلسة.")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"❌ خطأ داخل الرادار: {e}")
            await asyncio.sleep(5)


# ==================== [ محرك التشغيل الرئيسي ] ====================
async def main():
    # بدء تشغيل العميل والتحقق من الحساب
    await client.start()
    me = await client.get_me()
    print(f"✅ تم تسجيل الدخول بنجاح باسم: {me.first_name}")

    # الحل الجذري: إطلاق الرادار كمهمة منفصلة في الخلفية لكي لا يعطل الأوامر
    asyncio.create_task(run_radar())
    
    # الحل الجذري الثاني: جعل السكربت في حالة استماع دائم ولانهائي للأوامر
    print("📥 البوت الآن في حالة استماع كاملة ومطلقة لجميع الأوامر...")
    await client.run_until_disconnected()

# تشغيل السكربت
if __name__ == '__main__':
    client.loop.run_until_complete(main())
