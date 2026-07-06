import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, errors
from telethon.sessions import StringSession

# 1. بيانات الحساب الأساسية (ضع الـ api_id والـ api_hash الخاصين بك هنا)
API_ID = 1234567  # استبدله برقمك
API_HASH = "your_api_hash_here"  # استبدله بالهاش الخاص بك

# الجلسة الجديدة التي أرسلتها
NEW_SESSION = "1AZWarzsBuzJ7j0cOdaUM4F5JnnF-v6CGikZkHYdjTsO024yj4gW16AJp_i856i4OdGOqP_Yh0AUJYrIkx1sVmG8MnEoQgS6fYELp6nDyifr6XVXR__t-eFNjMwxH6MdxXdA8XjGfLx1y-vEJ-57XqMvGvp2tXBo-phYGQN42qS6Lv3OtUjEyT2X0bkHVJ6_v222LPD3scXcFk6JMCDE9vCKcbE-bfryVb5vpXHFwI3hYDcF7qsQHfCwS7-39DisKbXwSmLFWSYOxAv1mgramcefexTIDI7TyGMEsv6G31FJz3KEtNDdwkJh6UgOK9l9He__osLyX8KHscMi7BuTsnkFRpHYPAFM="

# 2. ضبط التوقيت على توقيت السعودية (AST - UTC+3)
SAUDI_TZ = pytz.timezone("Asia/Riyadh")

# 3. الحل الجذري لظهور نفس الجهاز وحماية الجلسة:
# نقوم بتمرير مواصفات دقيقة لتليجرام لتبدو الجلسة كأنها من هاتف حقيقي تماماً
client = TelegramClient(
    StringSession(NEW_SESSION),
    api_id=API_ID,
    api_hash=API_HASH,
    device_model="iPhone 15 Pro",  # نوع الجهاز الذي سيظهر في الأجهزة المتصلة
    system_version="iOS 17.5",  # إصدار النظام لتبدو الجلسة طبيعية
    app_version="10.11.1",  # إصدار تطبيق تليجرام حديث
)


async def main():
    await client.start()
    me = await client.get_me()
    print(f"🔗 تم تسجيل الدخول بنجاح باسم: {me.first_name}")

    # اختبار الوقت بتوقيت السعودية
    now_saudi = datetime.now(SAUDI_TZ)
    print(
        f"⏰ الوقت الحالي المعتمد (توقيت السعودية): {now_saudi.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # 4. حل مشكلة الرادار وحمايته من حرق الجلسة
    print("🛰️ تشغيل الرادار الآمن...")
    await run_radar()


async def run_radar():
    while True:
        try:
            # --- ضع كود الرادار الخاص بك هنا ---
            # مثال على جلب الوقت بالتوقيت السعودي داخل الرادار عند رصد أي حدث:
            current_time = datetime.now(SAUDI_TZ).strftime("%H:%M:%S")

            # (هنا يوضع أمر الفحص أو الرادار الخاص بك)
            # print(f"[{current_time}] الرادار يعمل ويبحث...")

            # حل جذري للحرق: وضع فاصل زمني (تأخير) بين كل طلب وآخر لحماية الجلسة
            await asyncio.sleep(3)  # انتظر 3 ثوانٍ قبل الفحص التالي لتجنب الحظر

        except errors.FloodWaitError as e:
            # إذا أرسل الرادار طلبات كثيرة، هذا الأمر يمنع حرق الجلسة ويجعلها تنتظر تلقائياً
            print(
                f"⚠️ تحذير من تليجرام (Flood)! الرادار أرسل طلبات مكثفة. سيتم التوقف مؤقتاً لمدة {e.seconds} ثانية لحماية الجلسة."
            )
            await asyncio.sleep(e.seconds)

        except Exception as e:
            # التعامل مع أي خطأ آخر في الرادار دون إغلاق السكربت أو تدمير الجلسة
            print(f"❌ خطأ في الرادار: {e}")
            await asyncio.sleep(5)


# تشغيل السكربت
with client:
    client.loop.run_until_complete(main())
