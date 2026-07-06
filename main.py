import asyncio
import sys
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession
from telethon.errors import AuthKeyDuplicatedError

# --- البيانات والمعرفات كاملة وجاهزة ومحمية ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# جلستك الأخيرة الثمينة (تنظيف آلي لأي مسافات أو رموز زائدة لعدم حرقها)
SESSION_STRING = "1AZWarzsBu6DBAWJ59pjNLxRxAwDzQFW-YgtGBitTbg23q2Y0ejCkxjjlQs2CYTHaZ3NvscuEKGY6V9TbD9Zm6gz-SaRHPFixz13iAjpcjxdCGbUoDGKJMIuMhhN_t02VINsEwaSNRmaWvNMNe2iXcsTOuxVusFbzfukS-Uxb7vUIimIMHOe0HJ2ewrPsuJ2hgucuIxRGZX0vjzcql3pu_omsHlh9lMQcQ_BdjZnNEe3WRPkVUwOUhaQdnpOR_XUUOvwC1sPG-R5Ey-mzn4OZXV-WE9UByuXDm81hPFqSPnaqOrR2dHhvw_gtlopxGDxoPl5b-nXfVOWW_S42JRXJkZa8RSHL7Qw="

TARGET_CHAT_ID = -1003555828336  # أيدي القروب الكامل (hLoSh)
TARGET_USER_ID = 8965415461     # أيدي حساب التنبيهات المستهدف

# تهيئة الجلسة مع تنظيفها تماماً لمنع أخطاء الـ Padding
clean_session = SESSION_STRING.strip().replace('"', '').replace("'", "")

client = TelegramClient(
    StringSession(clean_session), 
    API_ID, 
    API_HASH,
    device_model="iPhone 15 Pro Max",
    system_version="iOS 17.5",
    app_version="10.11.1"
)

last_log_id = 0

# الدالة الفولاذية للمراقبة الذكية من الجذور
async def watch_admin_log(group_entity, me_id):
    global last_log_id
    print("👁️ بدأ نظام الفحص الجذري لسجل المشرفين بنجاح...")
    
    # جلب المعرف الأولي لتجنب تكرار الأفعال القديمة عند التشغيل
    try:
        async for log in client.get_admin_log(group_entity, limit=1):
            last_log_id = log.id
    except Exception as e:
        print(f"⚠️ تنبيه أولي: سجل المشرفين فارغ حالياً أو تعذر جلب المعرف الأول: {e}")
        last_log_id = 0

    while True:
        try:
            if last_log_id == 0:
                async for log in client.get_admin_log(group_entity, limit=1):
                    last_log_id = log.id
                await asyncio.sleep(2)
                continue

            actions_to_send = []
            current_max_id = last_log_id
            
            # جلب آخر 20 حدث من السجل بدون فلاتر بارامترية مسببة للأخطاء
            async for log in client.get_admin_log(group_entity, limit=20):
                if log.id <= last_log_id:
                    break
                
                if log.id > current_max_id:
                    current_max_id = log.id
                    
                # [الحل الجذري] الفلترة البرمجية الداخلية: التحقق أن الفاعل هو أنت فقط من جوالك
                if log.user_id != me_id:
                    continue

                action_text = None
                target_person = "غير معروف"

                # 1. تحليل أحداث الإشراف (رفع، نزع، صلاحيات)
                if isinstance(log.action, types.ChannelAdminLogEventActionParticipantToggleAdmin):
                    prev = log.action.prev_participant
                    new = log.action.new_participant
                    target_id = getattr(new, 'user_id', getattr(prev, 'user_id', None))
                    
                    if target_id:
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

                # 2. تحليل أحداث الحظر، الكتم، وإلغاء الحظر
                elif isinstance(log.action, types.ChannelAdminLogEventActionParticipantToggleBanned):
                    prev = log.action.prev_participant
                    new = log.action.new_participant
                    target_id = getattr(new, 'user_id', getattr(prev, 'user_id', None))
                    
                    if target_id:
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

                if action_text:
                    alert_msg = (
                        f"🚨 **تنبيه نشاط من حساب السورس**\n\n"
                        f"⚙️ **الأمر الفُعل:** {action_text}\n"
                        f"👤 **الشخص المستهدف:** {target_person}\n"
                        f"💻 **الجهاز المتصل:** الجوال الشخصي المعتمد\n\n"
                        f"📍 **المكان:** قروب hLoSh"
                    )
                    actions_to_send.append(alert_msg)

            # حفظ آخر معرف تم الوصول إليه لتفادي التكرار
            last_log_id = current_max_id

            # إرسال الأحداث المرصودة بترتيبها الزمني الصحيح (من الأقدم للأحدث)
            for alert_msg in reversed(actions_to_send):
                # أولاً: إرسال لحساب التنبيهات المستهدف
                try:
                    await client.send_message(TARGET_USER_ID, alert_msg)
                except Exception as e:
                    print(f"❌ فشل الإرسال لحساب التنبيهات: {e}")
                
                # ثانياً: إرسال إلى المحفوظات (Saved Messages) الخاصة بك فوراً
                try:
                    await client.send_message('me', alert_msg)
                except Exception as e:
                    print(f"❌ فشل الإرسال للمحفوظات: {e}")

        except Exception as e:
            print(f"خطأ دوري في فحص سجل المشرفين: {e}")
            
        await asyncio.sleep(2)

# أمر الفحص السريع للتأكد من استقرارية الربط
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        await event.edit("✅ السورس مستقر ويعمل من الجذور! المراقبة والمحفوظات تعمل الآن بأعلى كفاءة.")

async def main():
    print("⏳ [نظام الحماية] جاري الانتظار 15 ثانية لتهيئة سيرفرات Railway بسلامة ومنع تداخل الجلسات...")
    await asyncio.sleep(15)
    
    print("🚀 جاري الاتصال بحساب السورس...")
    try:
        await client.start()
        print("✅ تم الاتصال بنجاح!")
        
        print("🔄 جاري ربط وتثبيت كيان المجموعة وحسابك الشخصي لضمان عمل المراقبة...")
        group_entity = await client.get_entity(TARGET_CHAT_ID)
        me = await client.get_me()
        
        # تشغيل نظام المراقبة المعزز وتمرير الكيانات الجاهزة له
        client.loop.create_task(watch_admin_log(group_entity, me.id))
        
        await client.run_until_disconnected()
    except AuthKeyDuplicatedError:
        print("❌ خطأ حرج: الجلسة مكررة أو تم استخدامها في مكان آخر في نفس الوقت!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع أثناء التشغيل: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
