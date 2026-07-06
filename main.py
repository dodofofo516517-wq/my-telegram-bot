import asyncio
import sys
import signal
import os
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession
from telethon.errors import AuthKeyDuplicatedError
from telethon.tl.functions.channels import GetAdminLogRequest

# --- البيانات والمعرفات الرقمية الثابتة ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

SESSION_STRING = "1AZWarzsBu6vG2XY4BeP0S6elkorSXCYP4w7tYzykAIgLMIaMygVZQ_D7SMKbQN_J2-QtNoUp-GSr7-C-PzK_vtZHAyY6QPA8linrmCyT2jRzxsAQ_Vni87tZl7XEyhmReT37_Xldio4b8r-gkdNniwqPdKyjtu1l-u1xtb-pUQaUFutmzdlhxMa3uBllO0obMbVJVTM8vJTO_Tg60GbOk9DI3qPBqqjB4tOXS_bPffePvZwq552dJV_pYTz4kARWJS-GG9WYhBd5CzWVooqqUCCt9u9t45Hm1DSOPSIiwZjlZV6DU_GxBuuPPqTPlXDEyGA1olyHB62fp2-9TNkZ8OtHph75mfs="
DEVICE_NAME = "iPhone 15 Pro Max"

TARGET_CHAT_ID = -1003555828336  # ايدي القروب (hLoSh)
TARGET_USER_ID = 8965415461     # ايدي حساب التنبيهات المستهدف

clean_session = SESSION_STRING.strip().replace('"', '').replace("'", "")

client = TelegramClient(
    StringSession(clean_session), 
    API_ID, 
    API_HASH,
    device_model=DEVICE_NAME,
    system_version="iOS 17.5",
    app_version="10.11.1"
)

last_log_id = 0

# سيرفر الويب الوهمي لتأمين استجابة ريلواي السريعة
async def handle_railway_health(reader, writer):
    try:
        await reader.read(1024)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 2\r\n\r\nOK"
        writer.write(response.encode())
        await writer.drain()
    except:
        pass
    finally:
        writer.close()

async def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    try:
        await asyncio.start_server(handle_railway_health, '0.0.0.0', port)
        print(f"سيرفر الحماية الوهمي يعمل على المنفذ: {port}")
    except Exception as e:
        print(f"تنبيه السيرفر الوهمي: {e}")

# فصل الجلسة النظيف عند الإطفاء المفاجئ
async def safe_suicide_shutdown(signal_name):
    print(f"تم استلام إشارة {signal_name}. جاري الفصل الفوري النظيف...")
    try:
        await client.disconnect()
    except:
        pass
    finally:
        sys.exit(0)

# رادار المراقبة الشامل والجذري الشامل لكل العمليات
async def watch_admin_log(group_entity, me_id):
    global last_log_id
    print("رادار المراقبة الشامل والذكي يعمل الآن بنظام جدار الحماية النصي...")
    
    try:
        # نرسل events_filter=None لجلب كافة أحداث السجل دون استثناء أو حجب من سيرفر تيليجرام
        reply = await client(GetAdminLogRequest(channel=group_entity, q='', events_filter=None, max_id=0, min_id=0, limit=1))
        if reply and reply.events:
            last_log_id = reply.events[0].id
    except:
        last_log_id = 0

    while True:
        try:
            if last_log_id == 0:
                reply = await client(GetAdminLogRequest(channel=group_entity, q='', events_filter=None, max_id=0, min_id=0, limit=1))
                if reply and reply.events: 
                    last_log_id = reply.events[0].id
                await asyncio.sleep(5)
                continue

            reply = await client(GetAdminLogRequest(channel=group_entity, q='', events_filter=None, max_id=0, min_id=0, limit=20))
            
            current_max_id = last_log_id
            actions_to_send = []

            if reply and reply.events:
                for log in reply.events:
                    if log.id <= last_log_id: 
                        break
                    if log.id > current_max_id: 
                        current_max_id = log.id

                    # تصفية أفعال حسابك أنت فقط
                    if log.user_id != me_id: 
                        continue

                    try:
                        action_class = log.action.__class__.__name__
                        action_text = None
                        event_time = log.date.strftime('%Y-%m-%d %H:%M:%S')

                        # 1. تحليل الرفع والتنزيل وتعديل الصلاحيات للمشرفين
                        if action_class == "ChannelAdminLogEventActionParticipantToggleAdmin":
                            prev = log.action.prev_participant
                            new = log.action.new_participant
                            
                            if hasattr(new, 'admin_rights') and new.admin_rights:
                                if hasattr(prev, 'admin_rights') and prev.admin_rights:
                                    action_text = "تعديل صلاحيات مشرف قائم"
                                else:
                                    action_text = "رفع مشرف جديد"
                            else:
                                action_text = "تنزيل من الاشراف"

                        # 2. تحليل الحظر الكلي والتقييد (الكتم) وإلغائهما
                        elif action_class == "ChannelAdminLogEventActionParticipantToggleBanned":
                            new = log.action.new_participant
                            if hasattr(new, 'banned_rights') and new.banned_rights:
                                if getattr(new.banned_rights, 'view_messages', False):
                                    action_text = "حظر من المجموعة"
                                else:
                                    action_text = "تقييد صلاحيات العضو كتم او منع"
                            else:
                                action_text = "الغاء الحظر او التقييد عن العضو"

                        # 3. تحليل الطرد المباشر (Kick)
                        elif action_class == "ChannelAdminLogEventActionParticipantKick":
                            action_text = "طرد عضو من المجموعة"

                        # 4. تعديل اسم المجموعة
                        elif action_class == "ChannelAdminLogEventActionChangeTitle":
                            action_text = f"تعديل اسم المجموعة الى: {log.action.new_title}"

                        # 5. تعديل وصف المجموعة
                        elif action_class == "ChannelAdminLogEventActionChangeAbout":
                            action_text = f"تعديل وصف المجموعة الى: {log.action.new_about}"

                        # 6. تثبيت الرسائل أو إلغائها
                        elif action_class == "ChannelAdminLogEventActionUpdatePinned":
                            if log.action.message:
                                action_text = "تثبيت رسالة جديدة"
                            else:
                                action_text = "الغاء تثبيت رسالة"

                        # 7. حذف الرسائل
                        elif action_class == "ChannelAdminLogEventActionDeleteMessage":
                            action_text = "حذف رسالة من المجموعة"

                        # 8. نظام الرصد الاحتياطي الذكي لأي تفاعل آخر غير مدرج
                        else:
                            clean_name = action_class.replace("ChannelAdminLogEventAction", "")
                            action_text = f"اجراء فني غير مصنف: {clean_name}"

                        # استخراج الشخص المستهدف بشكل ديناميكي آمن تماماً مهما كان نوع الحدث
                        target_id = None
                        if hasattr(log.action, 'new_participant') and log.action.new_participant:
                            target_id = getattr(log.action.new_participant, 'user_id', None)
                        if not target_id and hasattr(log.action, 'prev_participant') and log.action.prev_participant:
                            target_id = getattr(log.action.prev_participant, 'user_id', None)
                        if not target_id and hasattr(log.action, 'participant_id'):
                            target_id = log.action.participant_id
                        if not target_id and hasattr(log.action, 'user_id'):
                            target_id = log.action.user_id

                        target_person = "المجموعة نفسها او حدث عام"
                        if target_id:
                            try:
                                t_entity = await client.get_entity(target_id)
                                target_person = f"{t_entity.first_name} | ID: {t_entity.id}"
                            except: 
                                target_person = f"ID: {target_id}"

                        if action_text:
                            alert_msg = (
                                f"تنبيه نشاط من حساب السورس\n\n"
                                f"الفعل: {action_text}\n"
                                f"المستهدف: {target_person}\n"
                                f"الجهاز: {DEVICE_NAME}\n"
                                f"الوقت: {event_time}\n"
                                f"المكان: قروب hLoSh"
                            )
                            actions_to_send.append(alert_msg)
                    except Exception as event_error:
                        print(f"تم تخطي خطأ قراءة حدث فرعي: {event_error}")
                        continue

            last_log_id = current_max_id

            for alert_msg in reversed(actions_to_send):
                try: 
                    await client.send_message(TARGET_USER_ID, alert_msg)
                except: 
                    pass
                try: 
                    await client.send_message('me', alert_msg)
                except: 
                    pass

        except Exception as loop_error:
            print(f"تنبيه عام في الرادار: {loop_error}")
            
        await asyncio.sleep(5)

# أمر الفحص الرسمي والمختصر والخالي تماماً من الإيموجيات والزخارف
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        await event.edit(
            "السورس يعمل باعلى درجات الاستقرار والثبات\n\n"
            "- امر الفحص مستقر تماما\n"
            "- الرادار محمي ومخصص لحسابك فقط\n"
            "- معالج الاحداث شامل لجميع العمليات بدون استثناء"
        )

async def main():
    loop = asyncio.get_running_loop()
    if sys.platform != 'win32':
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(safe_suicide_shutdown(s.name)))

    # تشغيل سيرفر الويب الوهمي الخاص بـ Railway
    await start_dummy_server()

    # بروتوكول الـ 45 ثانية الحامي للاتصال الأحادي لمنع حرق الجلسة
    print("جاري الانتظار لـ 45 ثانية لتأمين الساحة بالكامل وفصل السيرفر القديم...")
    await asyncio.sleep(45)
    
    print("بدء الاتصال الرسمي والآمن بتيليجرام...")
    try:
        await client.start()
        print("تم الاتصال بنجاح وثبات كامل.")
        
        group_entity = await client.get_entity(TARGET_CHAT_ID)
        me = await client.get_me()
        
        client.loop.create_task(watch_admin_log(group_entity, me.id))
        await client.run_until_disconnected()
        
    except AuthKeyDuplicatedError:
        print("خطأ: الجلسة تعرضت للتداخل والنسخ قبل تثبيت هذا الكود الحامي.")
        sys.exit(1)
    except Exception as e:
        print(f"خطأ تشغيل: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
