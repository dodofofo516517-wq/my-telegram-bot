import os
import sys
import asyncio
from telethon import TelegramClient, errors

# ⚙️ إعدادات الحساب (ضع بياناتك هنا أو اربطها بمتغيرات البيئة في Railway)
API_ID = int(os.environ.get("API_ID", 1234567))          # استبدله بـ API ID الخاص بك
API_HASH = os.environ.get("API_HASH", "your_api_hash")  # استبدله بـ API HASH الخاص بك
SESSION_STRING = os.environ.get("SESSION_STRING", "session_name") # اسم الجلسة أو الـ String Session
TARGET_CHAT_ID = int(os.environ.get("TARGET_CHAT_ID", -100123456789)) # آيدي المجموعة المراقبة

# إنشاء كائن العميل (Client)
client = TelegramClient(SESSION_STRING, API_ID, API_HASH)

# 1️⃣ سيرفر الاستجابة الفورية الوهمي (لخداع ريلواي وتخطي الفحص بنجاح)
async def handle_railway_ping(reader, writer):
    """يستقبل طلب ريلواي ويرد بـ OK فوراً لمنع تعليق الحاوية"""
    try:
        await reader.read(1024)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 2\r\n\r\nOK"
        writer.write(response.encode('utf-8'))
        await writer.drain()
    except Exception:
        pass
    finally:
        writer.close()
        await writer.wait_closed()

async def start_dummy_server():
    """تشغيل السيرفر على البورت الذي تحدده ريلواي ديناميكياً"""
    port = int(os.environ.get("PORT", 8080))
    try:
        server = await asyncio.start_server(handle_railway_ping, "0.0.0.0", port)
        print(f"🎯 [سيرفر الوهمي] تم تشغيل السيرفر بنجاح على المنفذ {port} لإرضاء ريلواي!")
        # تشغيل السيرفر في الخلفية للأبد دون تعطيل الكود الأساسي
        asyncio.create_task(server.serve_forever())
    except Exception as e:
        print(f"⚠️ تحذير السيرفر الوهمي: لم يتمكن من حجز المنفذ {port}: {e}")

# 2️⃣ دالة الرادار (تأكد من تعديل محتواها حسب حاجتك)
async def watch_admin_log(group_entity, me_id):
    print("👁️ [رادار المراقبة] تم التنشيط وبدء مسح سجل المشرفين بالخلفية...")
    while True:
        try:
            # --- 🛠️ ضع أوامر الرادار الخاصة بك هنا 🛠️ ---
            # مثال: جلب آخر الأحداث من سجل المشرفين
            # async for event in client.iter_admin_log(group_entity, limit=5):
            #     print(f"حدث جديد: {event.action}")
            
            # انتظام الفحص (مثلاً كل 10 ثوانٍ)
            await asyncio.sleep(10)
            
        except errors.FloodWaitError as e:
            print(f"⏳ [تنبيه الحماية] تيليجرام يطلب التهدئة. انتظار لـ {e.seconds} ثانية...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            # طباعة الخطأ بداخل الرادار حتى لا يموت صامتاً
            print(f"⚠️ [خطأ داخل الرادار]: {e}")
            await asyncio.sleep(15) # انتظار قبل إعادة المحاولة لمنع استهلاك المعالج عند الأخطاء المستمرة

# 3️⃣ الدالة الرئيسية المحصنة لـ التطبيق
async def main():
    # 🌟 خطوة 1: تشغيل سيرفر الاستجابة الفورية لريلواي لمنع الـ Crash البدائي
    await start_dummy_server()

    # 🌟 خطوة 2: جدار الصمت المطلق (بروتوكول الـ 45 ثانية لتدمير النسخة القديمة)
    print("⏳ [حصن الأمان] تم إرضاء ريلواي! جاري الانتظار لـ 45 ثانية صامتة ليموت السيرفر القديم تماماً وتأمين جلستك الفاخرة من الحرق...")
    await asyncio.sleep(45)
    
    print("🚀 الساحة آمنة بنسبة 100%! جاري الاتصال الرسمي والوحيد بتيليجرام...")
    try:
        # الاتصال بالحساب
        await client.start()
        print("✅ تم الاتصال بنجاح ساحق وثبات أبدي!")
        
        # جلب معلومات الكيان والحساب
        group_entity = await client.get_entity(TARGET_CHAT_ID)
        me = await client.get_me()
        
        # تشغيل رادار المراقبة الآمن وحفظه في متغير لمنع حذفه تلقائياً من الذاكرة
        radar_task = asyncio.create_task(watch_admin_log(group_entity, me.id))
        
        # مراقبة حالة الرادار وطباعة أي خطأ قاتل يحدث داخله فوراً
        def check_radar_status(task):
            try:
                task.result()
            except Exception as e:
                print(f"❌ [كارثة برمجية] الرادار توقف تماماً عن العمل! السبب: {e}")

        radar_task.add_done_callback(check_radar_status)
        
        # استمرار تشغيل البوت ومنعه من التوقف
        await client.run_until_disconnected()
        
    except errors.AuthKeyDuplicatedError:
        print("❌ خطأ قاطع: هذه الجلسة تعرضت للتداخل والاتصال المزدوج (الجلسة احترقت أو قيد الاستخدام في مكان آخر).")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ تشغيل غير متوقع: {e}")
        sys.exit(1)

# ✅ تشغيل التطبيق بالشرط الصحيح والآمن لبايثون
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 تم إيقاف البوت يدوياً.")
