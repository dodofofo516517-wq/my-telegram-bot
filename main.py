import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- البيانات الأساسية ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# الجلسة الجديدة التي زودتني بها
SESSION_STRING = "1AZWarzsBu4k3MBIAdWLJyf9TIaaAtTpPJtpXMW2hoMG0DKTxRt4_5T4qrZdsdyst7yWaqj-0CW-lCUorSPLC8MgZVbjoAHTatD_fQmi2R89Bvq69zprOCCkcanFjZGhme9ahTK83eyqmpezk6Ufvm7Kym-5dtR5WUOKfqKys3dk6n5HMeq67OJIw3w8i-D9pVOrLjyaFHhJoiifBE450rwl5L-hBKdFD3flPaGydpw7WR5WVh6XSqgscmqQv7EB1dG0J3wPU32F9kDKdNKvjhfSLg0ARbzxcP6W7O28VQ7HySzXNdD54hGrqyLW2I3ujzmt8bvqFQ_LdIsPBupJpkvgAX8m89U0="

# إعدادات المراقبة والإرسال
TARGET_CHAT_ID = -1003555828336  # أيدي قروب hLoSh , fls3h
TARGET_USER_ID = 8965415461     # أيدي حساب التنبيهات المنشود
MY_ID = 8980682089              # أيدي حساب السورس الخاص بك

# الخدعة البرمجية: محاكاة تطبيق رسمي مستقر لعدم لفت انتباه فلاتر الحظر
client = TelegramClient(
    StringSession(SESSION_STRING.strip()), 
    API_ID, 
    API_HASH,
    device_model="iPhone 15 Pro Max",
    system_version="iOS 17.5",
    app_version="10.11.1"
)

@client.on(events.ChatAction)
async def monitor_my_actions(event):
    # التأكد من مراقبة المجموعة المستهدفة فقط
    if event.chat_id != TARGET_CHAT_ID:
        return
    
    # فلترة صارمة: التحقق أن الفاعل هو حساب السورس الخاص بك فقط
    if event.action_message and event.action_message.sender_id == MY_ID:
        try:
            action_text = "إجراء غير محدد"
            target_person = "غير معروف أو المجموعة نفسها"
            
            # جلب معلومات الشخص المستهدف إن وجد
            if event.user:
                target_person = f"{event.user.first_name} | ID: {event.user.id}"
            elif event.user_id:
                target_person = f"ID: {event.user_id}"

            # 1. رصد الحظر أو الطرد
            if event.user_kicked:
                action_text = "❌ حظر شخص أو طرده من المجموعة"
                
            # 2. رصد إلغاء الحظر
            elif event.unbanned:
                action_text = "🔓 إلغاء الحظر عن شخص"
                
            # 3. رصد رفع مشرف / نزع صلاحيات / تعديل رتبة
            elif event.admin_rights_changed:
                action_text = "🛡️ تعديل صلاحيات مشرف (رفع مشرف / نزع الإشراف / تغيير صلاحيات)"
                
            # 4. رصد تغيير اسم المجموعة
            elif event.chat_title_changed:
                action_text = f"✏️ تغيير اسم المجموعة إلى: **{event.new_title}**"
                target_person = "اسم المجموعة"
            else:
                # إذا لم يتطابق مع المعايير، نتخطى الإجراء لتوفير استهلاك الجلسة
                return

            # جلب تفاصيل الجهاز المتصل بالسورس بشكل آمن لمنع تداخل الـ IP
            try:
                auths = await client(GetAuthorizationsRequest())
                device_name = next((a.device_model for a in auths.authorizations if a.current), "جهاز الجوال")
            except:
                device_name = "جهاز متصل (تعذر الفحص المباشر لحماية أمان الجلسة)"

            # صياغة رسالة التنبيه الموحدة (رسالة واحدة كاملة التفاصيل)
            alert_message = (
                f"🚨 **تنبيه: نشاط جديد من حساب السورس**\n\n"
                f"⚙️ **الأمر الفُعل:** {action_text}\n"
                f"👤 **الشخص المستهدف:** {target_person}\n"
                f"💻 **الجهاز المتصل عند الفعل:** {device_name}\n\n"
                f"📍 **مكان الحدث:** قروب hLoSh"
            )

            # إرسال التنبيه إلى حسابك المخصص للتنبيهات
            await client.send_message(TARGET_USER_ID, alert_message)

        except Exception as e:
            print(f"خطأ أثناء معالجة الحدث: {e}")

# أمر فحص للتأكد من الحالة دون إحداث تغيير في الجروب
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    if event.sender_id == MY_ID:
        await event.edit("✅ السورس مستقر، متصل، ويراقب الأفعال المطلوبة بدقة!")

async def main():
    print("🚀 جاري تشغيل السورس بنظام محاكاة أمان الأجهزة المتقدمة...")
    await client.start()
    print("✅ السورس يعمل الآن في الخلفية دون انقطاع.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
