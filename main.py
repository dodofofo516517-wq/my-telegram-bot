import os
import sys
import asyncio
import signal
from telethon import TelegramClient, errors
from telethon.sessions import StringSession  # 🔥 السر العبقري لمنع احتراق الجلسات النصية

# ==========================================
# ⚙️ إعدادات الحساب (قم بتغيير الـ API ID والـ API HASH وبيانات المجموعة)
# ==========================================
API_ID = 1234567          # ⚠️ ضع هنا الـ API ID الخاص بك (رقم)
API_HASH = "your_api_hash"  # ⚠️ ضع هنا الـ API HASH الخاص بك (نص)
TARGET_CHAT_ID = -100123456789 # ⚠️ ضع هنا آيدي المجموعة المستهدفة للمراقبة

# 🌟 كود الجلسة الخاص بك مدمج برمجياً بأمان
SESSION_STRING = "1AZWarzsBuzUbfpvJcqZxC3y5a5-B0aPYj9FdDrGE-VXIPG0TeD842cLgRtRBNWBOrnz4L-FrhZTjeKUvtN0lnww_RBZvyVcN4cgosV68rJKv6kznEACCQglGivt5ZX7mab-0HAMsH3Tm3_CC-1yKKj1gLcxALTvdw5QWPKAkp-zS5C12mYhPa_IVxuY75Jzy6hnv8lPaFcN2TQHNZgKrTUvH9e-xX8wsFa9p2N6KCrGOKDOGuTCBVNeGaVF4Mu-vlr0EFaGqKUoYfe9rZv4WCSYPDQ_PKDaw9gTT_w_E_Se3OdVp6dMJBPZ0er9fXc07tXreLd8kByBLTg78CG3WhPKph3wsLFg="

# ✅ إنشاء العميل عبر كائن StringSession لضمان القراءة المباشرة من الذاكرة ومنع الحرق
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ==========================================
# 1️⃣ نظام اعتراض الإشارات: فصل فوري عند التحديث لحماية الجلسة
# ==========================================
def railway_shutdown_handler():
    print("🛑 [نظام الحماية] تم استقبال إشارة الإغلاق والتحديث (SIGTERM) من ريلواي!")
    print("⚡ جاري قطع اتصال الجلسة فوراً لمنع التداخل مع النسخة الجديدة وحمايتها من الحرق...")
    asyncio.create_task(instant_disconnect())

async def instant_disconnect():
    try:
        if client.is_connected():
            await client.disconnect()
        print("✅ تم فصل الجلسة بنجاح مطلق وآمن. إغلاق الحاوية القديمة الآن.")
    except Exception as e:
        print(f"⚠️ خطأ أثناء الفصل السريع: {e}")
    finally:
        sys.exit(0)

# ==========================================
# 2️⃣ سيرفر الاستجابة الفورية لخداع ريلواي وتخطي الفحص
# ==========================================
async def handle_railway_ping(reader, writer):
    try:
        await reader.read(1024)
        response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK"
        writer.write(response.encode('utf-8'))
        await writer.drain()
    except: pass
    finally:
        writer.close()
        await writer.wait_closed()

async def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    try:
        server = await asyncio.start_server(handle_railway_ping, "0.0.0.0", port)
        asyncio.create_task(server.serve_forever())
        print(f"🎯 [السيرفر] تم فتح المنفذ {port} بنجاح.")
    except Exception as e:
        print(f"⚠️ فشل حجز المنفذ: {e}")

# ==========================================
# 3️⃣ دالة الرادار المحصنة (أوامر المراقبة الخاصة بك)
# ==========================================
async def watch_admin_log(group_entity, me_id):
    print("👁️ [الرادار] بدأ العمل والمسح المستمر الآن...")
    while True:
        try:
            # ⬇️ ---- 🛠️ ضع كود أوامر الرادار المخصص لك هنا 🛠️ ---- ⬇️
            
            # مثال مجهز ومحمي لجلب سجلات المشرفين:
            # async for event in client.iter_admin_log(group_entity, limit=5):
            #     print(f"حدث في السجل: {event.action}")
            
            # ⬆️ ---------------------------------------------------- ⬆️
            
            await asyncio.sleep(10) # فحص مستمر كل 10 ثوانٍ
            
        except errors.FloodWaitError as e:
            print(f"⏳ [تنبيه] حظر مؤقت من تيليجرام، يجب الانتظار لـ {e.seconds} ثانية.")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            # تمرير الخطأ لدالة المراقبة الرئيسية لتتخذ إجراء الانهيار الذكي
            raise e

# ==========================================
# 4️⃣ الدالة الرئيسية وتشغيل النظام
# ==========================================
async def main():
    # تفعيل نظام مراقبة إشارات نظام التشغيل لحماية الحاوية في ريلواي
    loop = asyncio.get_running_loop()
    try:
        loop.add_signal_handler(signal.SIGTERM, railway_shutdown_handler)
        loop.add_signal_handler(signal.SIGINT, railway_shutdown_handler)
        print("🛡️ [حصن الإشارات] نظام حماية الجلسة ضد الـ SIGTERM فعال الآن.")
    except NotImplementedError:
        print("⚠️ نظام الإشارات يعمل فقط على بيئة لينكس (Railway)، يتخطى الآن في ويندوز.")

    # تشغيل سيرفر الويب الوهمي لتخطي فحص ريلواي البدائي
    await start_dummy_server()
    await asyncio.sleep(3) # استقرار السيرفر
    
    print("🚀 جاري الاتصال الرسمي والآمن بتيليجرام...")
    try:
        await client.start()
        print("✅ تم الاتصال بنجاح واستقرار تام وثبات أبدي!")
        
        group_entity = await client.get_entity(TARGET_CHAT_ID)
        me = await client.get_me()
        
        # تشغيل الرادار وحفظه في الذاكرة
        radar_task = asyncio.create_task(watch_admin_log(group_entity, me.id))
        
        # 💥 فلسفة الانتحار الذكي (Crash-Early) لحل مشكلة توقف الرادار
        def on_radar_failure(task):
            try:
                task.result() 
            except Exception as error:
                print(f"💥 [خطأ الرادار]: {error}")
                print("☠️ [الانتحار الذكي] إعادة تشغيل الحاوية فوراً لتطهير النظام...")
                sys.exit(1) # انهيار متعمد يجعل ريلواي تعيد تشغيل البوت تلقائياً فوراً

        radar_task.add_done_callback(on_radar_failure)
        
        # إبقاء البوت متصلاً
        await client.run_until_disconnected()
        
    except errors.AuthKeyDuplicatedError:
        print("❌ خطأ: هذه الجلسة محروقة بالفعل من محاولات سابقة خارج هذا الكود.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ تشغيل غير متوقع: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
