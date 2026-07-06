import asyncio
import os
import sys
import time
from telethon import TelegramClient, events

# --- إعدادات الحساب (ضع بياناتك هنا) ---
API_ID = 123456        # استبدله بـ API ID الخاص بك
API_HASH = 'your_api_hash_here'

# متغير عالمي لتتبع آخر وقت استجاب فيه الرادار
last_radar_activity = time.time()

# إعداد العميل مع ميزات إعادة الاتصال التلقائي اللانهائي وتوسيع سعة البيانات
client = TelegramClient(
    'radar_session', 
    API_ID, 
    API_HASH,
    connection_retries=None,  # محاولات إعادة اتصال غير محدودة عند انقطاع الإنترنت
    auto_reconnect=True,      # إعادة اتصال تلقائي فوري
    flood_sleep_threshold=86400 # التعامل الذكي مع حظر الفلود المؤقت
)

# --- 1. المعالج الخلفي (العامل الذكي) ---
async def async_worker_processor(event):
    """
    هنا تضع منطق الرادار الخاص بك (فحص الكلمات، التنظيف، إلخ).
    هذه الدالة تعمل في الخلفية تماماً دون تأخير الرادار الأساسي.
    """
    try:
        # مثال: طباعة نص الرسالة القادمة
        text = event.raw_text
        print(f"[{time.strftime('%X')}] الرادار رصد رسالة: {text[:30]}...")
        
        # تنبيه: إذا كنت تحتاج لتأخير، استخدم دائماً asyncio.sleep وليس time.sleep
        await asyncio.sleep(0.1) 
        
    except Exception as e:
        print(f"خطأ أثناء معالجة البيانات في الخلفية: {e}")

# --- 2. الرادار الأساسي (المستقبل الفوري) ---
@client.on(events.NewMessage(incoming=True))
async def radar_main_handler(event):
    global last_radar_activity
    # تحديث العداد فوراً لإثبات أن الرادار حيّ ويعمل
    last_radar_activity = time.time()
    
    # الحل الجذري: الرادار لا ينفذ الكود بنفسه، بل يوكّل المهمة للخلفية وينصرف فوراً
    asyncio.create_task(async_worker_processor(event))

# --- 3. نظام الحارس الذاتي (Watchdog) ---
async def radar_watchdog():
    """
    وظيفة هذا الحارس هي مراقبة الرادار، إذا تجمد الاتصال مع التليجرام 
    ولم تصل أي تحديثات لفترة طويلة (مثلاً 10 دقائق) والجروبات نشطة، 
    سيقوم بإعادة تشغيل البرنامج كاملاً كلياً وجذرياً.
    """
    global last_radar_activity
    print("الحارس الذاتي (Watchdog) يعمل الآن في الخلفية...")
    
    while True:
        await asyncio.sleep(60) # يفحص حالة الرادار كل دقيقة
        
        # حساب الوقت المنقضي منذ آخر رسالة
        time_since_last_message = time.time() - last_radar_activity
        
        # إذا مرت 10 دقائق (600 ثانية) بدون استجابة (يمكنك تعديل الوقت حسب حاجتك)
        if time_since_last_message > 600:
            print("🚨 تحذير: تم كشف تجمد أو خمول غير طبيعي في الرادار!")
            print("جاري إعادة تشغيل السكريبت كاملاً من الجذور تلقائياً...")
            
            # إنهاء العميل بأمان قبل إعادة التشغيل
            try:
                await client.disconnect()
            except:
                pass
                
            # الأمر السحري لإعادة تشغيل الملف برمجياً وكأنه فتح لأول مرة
            os.execv(sys.executable, ['python'] + sys.argv)

# --- 4. نقطة الانطلاق الأساسية ---
async def main():
    print("جاري تشغيل الرادار...")
    await client.start()
    print("⚡ الرادار متصل الآن ويعمل بأقصى سرعة استجابة!")
    
    # تشغيل نظام الحارس الذاتي بالتوازي مع البوت
    asyncio.create_task(radar_watchdog())
    
    # الحفاظ على تشغيل البوت مستمراً
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nتم إيقاف الرادار يدوياً.")
