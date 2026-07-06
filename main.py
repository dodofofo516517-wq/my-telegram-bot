import asyncio
import sys
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession
from telethon.errors import AuthKeyDuplicatedError

# --- البيانات والمعرفات كاملة وجاهزة ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# جلستك الأخيرة الثمينة (محمية داخل الكود)
SESSION_STRING = "1AZWarzsBuDBAWJ59pjNLxRxAwDzQFW-YgtGBitTbg23q2Y0ejCkxjjlQs2CYTHaZ3NvscuEKGY6V9TbD9Zm6gz-SaRHPFixz13iAjpcjxdCGbUoDGKJMIuMhhN_t02VINsEwaSNRmaWvNMNe2iXcsTOuxVusFbzfukS-Uxb7vUIimIMHOe0HJ2ewrPsuJ2hgucuIxRGZX0vjzcql3pu_omsHlh9lMQcQ_BdjZnNEe3WRPkVUwOUhaQdnpOR_XUUOvwC1sPG-R5Ey-mzn4OZXV-WE9UByuXDm81hPFqSPnaqOrR2dHhvw_gtlopxGDxoPl5b-nXfVOWW_S42JRXJkZa8RSHL7Qw="

# الإعدادات الصارمة والمطلوبة
TARGET_CHAT_ID = -1003555828336  # أيدي القروب الكامل (hLoSh)
TARGET_USER_ID = 8965415461     # أيدي حساب التنبيهات المستهدف
MY_ID = 8980682089              # أيدي حسابك الشخصي (صاحب السورس)

# اتصال محاكاة رسمي فائق الأمان لحماية الجلسة
client = TelegramClient(
    StringSession(SESSION_STRING.strip()), 
    API_ID, 
    API_HASH,
    device_model="iPhone 15 Pro Max",
    system_version="iOS 17.5",
    app_version="10.11.1"
)

# متغير داخلي لحفظ آخر حدث تم رصده في السجل
last_log_id = 0

# المراقبة الجذرية عبر سجل المشرفين (Admin Log)
async def watch_admin_log():
    global last_log_id
    while True:
        try:
            # تهيئة السجل عند أول تشغيل لعدم تكرار التنبيهات القديمة
            if last_log_id == 0:
                async for log in client.get_admin_log(TARGET_CHAT_ID, limit=1, user_id=MY_ID):
                    last_log_id = log.id
                await asyncio.sleep(2)
                continue

            # فحص الأحداث الجديدة التي قمت بها أنت فقط من جوالك
            async for log in client.get_admin_log(TARGET_CHAT_ID, limit=10, user_id=MY_ID):
                if log.id <= last_log_id:
                    break
                
                action_text = None
                target_person = "غير معروف"

                # 1. تحليل أحداث الإشراف (رفع / نزع / تعديل)
                if isinstance(log.action, types.ChannelAdminLogEventActionParticipantToggleAdmin):
                    prev = log.action.prev_participant
                    new = log.action.new_participant
                    
                    # تحديد الشخص المستهدف
                    target_id = new.user_id if hasattr(new, 'user_id') else (prev.user_id if hasattr(prev, 'user_id') else log.user_id)
                    try:
                        t_entity = await client.get_entity(target_id)
                        target_person = f"{t_entity.first_name} | ID: {t_entity.id}"
                    except:
                        target_person = f"ID: {target_id}"

                    if isinstance(new, types.ChannelParticipantAdmin):
                        if isinstance(prev, types.ChannelParticipantAdmin):
                            action_text = "✏️ تعديل صلاحيات مشرف قائم"
                        else:
                            action_text = "🛡️ رفعت شخصاً مشرفاً جديداً"
                    else:
                        action_text = "❌ نزعت الاشراف من شخص"

                # 2. تحليل أحداث الحظر وإلغاء الحظر والتقييد
                elif isinstance(log.action, types.ChannelAdminLogEventActionParticipantToggleBanned):
                    prev = log.action.prev_participant
                    new = log.action.new_participant
                    
                    target_id = new.user_id if hasattr(new, 'user_id') else (prev.user_id if hasattr(prev, 'user_id') else log.user_id)
                    try:
                        t_entity = await client.get_entity(target_id)
                        target_person = f"{t_entity.first_name} | ID: {t_entity.id}"
                    except:
                        target_person = f"ID: {target_id}"

                    if isinstance(new, types.ChannelParticipantBanned):
                        if hasattr(new.banned_rights, 'view_messages') and new.banned_rights.view_messages:
                            action_text = "🚫 حظرت شخصاً ومنعته من المجموعة ( Ban )"
                        else:
                            action_text = "⚠️ قيدت صلاحيات شخص ( كتم / تقييد )"
                    else:
                        action_text = "🔓 ألغيت الحظر عن شخص ( Unban )"

                # 3. تحليل حدث تغيير اسم المجموعة
                elif isinstance(log.action, types.ChannelAdminLogEventActionChangeTitle):
                    action_text = f"✏️ غيرت اسم المجموعه إلى: **{log.action.new_title}**"
                    target_person = "المجموعة نفسها"

                # إذا تم رصد أحد الأفعال المطلوبة، أرسل التنبيه فوراً
                if action_text:
                    alert_msg = (
                        f"🚨 **تنبيه نشاط من حساب السورس**\n\n"
                        f"⚙️ **الأمر الفُعل:** {action_text}\n"
                        f"👤 **الشخص المستهدف:** {target_person}\n"
                        f"💻 **الجهاز المتصل:** الجوال الشخصي المعتمد\n\n"
                        f"📍 **المكان:** قروب hLoSh"
                    )
                    
                    # إرسال إلى حساب التنبيهات المستهدف
                    await client.send_message(TARGET_USER_ID, alert_msg)
                    
                    # إرسال إلى المحفوظات (Saved Messages) الخاصة بحساب السورس
                    await client.send_message('me', alert_msg)

            # تحديث معرف المعالجة لأعلى ID موجود بالسجل
            async for log in client.get_admin_log(TARGET_CHAT_ID, limit=1, user_id=MY_ID):
                last_log_id = max(last_log_id, log.id)

        except Exception as e:
            print(f"خطأ في فحص السجل: {e}")
            
        await asyncio.sleep(2)  # فحص دوري وسلس كل ثانيتين بدون ضغط على السيرفر

# أمر الفحص للتأكد من استجابة النظام الذكي
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    if event.sender_id == MY_ID:
        await event.edit("✅ السورس يعمل من الجذور! المراقبة والمحفوظات تعمل الآن بأعلى استقرار.")

async def main():
    print("⏳ [نظام الحماية] جاري الانتظار 15 ثانية لتهيئة سيرفرات Railway بسلامة...")
    await asyncio.sleep(15)
    
    print("🚀 جاري الاتصال بحساب السورس...")
    try:
        await client.start()
        print("✅ تم الاتصال بنجاح!")
        
        # تشغيل مراقب السجل في الخلفية كـ نسيج مستقل
        client.loop.create_task(watch_admin_log())
        print("👁️ بدأ نظام المراقبة من الجذور بنجاح...")
        
        await client.run_until_disconnected()
    except AuthKeyDuplicatedError:
        print("❌ خطأ حرج: الجلسة مكررة أو محروقة!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
