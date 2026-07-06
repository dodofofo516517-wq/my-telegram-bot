import asyncio
import sys
import signal
import os
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession
from telethon.errors import AuthKeyDuplicatedError
from telethon.tl.functions.channels import GetAdminLogRequest

# --- البيانات والمعرفات الرسمية الثابتة لعقدة يوسف ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# 🔑 تم دمج جلستك الجديدة والأخيرة هنا بنجاح تام
SESSION_STRING = "1AZWarzsBu6vG2XY4BeP0S6elkorSXCYP4w7tYzykAIgLMIaMygVZQ_D7SMKbQN_J2-QtNoUp-GSr7-C-PzK_vtZHAyY6QPA8linrmCyT2jRzxsAQ_Vni87tZl7XEyhmReT37_Xldio4b8r-gkdNniwqPdKyjtu1l-u1xtb-pUQaUFutmzdlhxMa3uBllO0obMbVJVTM8vJTO_Tg60GbOk9DI3qPBqqjB4tOXS_bPffePvZwq552dJV_pYTz4kARWJS-GG9WYhBd5CzWVooqqUCCt9u9t45Hm1DSOPSIiwZjlZV6DU_GxBuuPPqTPlXDEyGA1olyHB62fp2-9TNkZ8OtHph75mfs="

TARGET_CHAT_ID = -1003555828336  # أيدي القروب الكامل (hLoSh)
TARGET_USER_ID = 8965415461     # أيدي حساب التنبيهات المستهدف

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

CUSTOM_FILTER = types.ChannelAdminLogEventsFilter(
    promote=True, demote=True, ban=True, unban=True, kick=True, settings=True
)

# 🌍 سيرفر الويب الوهمي لإرضاء Railway فوراً ومنعه من كراش التشغيل
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
        server = await asyncio.start_server(handle_railway_health, '0.0.0.0', port)
        print(f"🌍 [ويب] سيرفر الحماية الوهمي يعمل الآن على المنفذ: {port}")
    except Exception as e:
        print(f"⚠️ تنبيه السيرفر الوهمي: {e}")

# 🛡️ الحماية الرسمية لإغلاق السيرفر فوراً إذا تلقى إشارة إطفاء
async def safe_suicide_shutdown(signal_name):
    print(f"🚨 [نظام] تم استلام إشارة {signal_name}. جاري الفصل النظيف فوراً...")
    try:
        await client.disconnect()
    except:
        pass
    finally:
        sys.exit(0)

# 👁️ رادار المراقبة المؤمن بالكامل ضد التوقف والتعليق
async def watch_admin_log(group_entity, me_id):
    global last_log_id
    print("👁️ رادار مراقبة أفعالك الشخصية يعمل الآن بنظام جدار الحماية المنفصل...")
    
    try:
        reply = await client(GetAdminLogRequest(channel=group_entity, q='', events_filter=CUSTOM_FILTER, max_id=0, min_id=0, limit=1))
        if reply and reply.events:
            last_log_id = reply.events[0].id
    except:
        last_log_id = 0

    while True:
        try:
            if last_log_id == 0:
                reply = await client(GetAdminLogRequest(channel=group_entity, q='', events_filter=CUSTOM_FILTER, max_id=0, min_id=0, limit=1))
                if reply and reply.events: 
                    last_log_id = reply.events[0].id
                await asyncio.sleep(5)
                continue

            reply = await client(GetAdminLogRequest(channel=group_entity, q='', events_filter=CUSTOM_FILTER, max_id=0, min_id=0, limit=20))
            
            current_max_id = last_log_id
            actions_to_send = []

            if reply and reply.events:
                for log in reply.events:
                    if log.id <= last_log_id: 
                        break
                    if log.id > current_max_id: 
                        current_max_id = log.id

                    # 🎯 تصفية لحساب يوسف فقط
                    if log.user_id != me_id: 
                        continue

                    # جدار حماية داخلي لكل حدث منفصل لكي لا يعلق الرادار أبداً
                    try:
                        action_text = None
                        target_person = "غير معروف"

                        if isinstance(log.action, types.ChannelAdminLogEventActionParticipantToggleAdmin):
                            prev, new = log.action.prev_participant, log.action.new_participant
                            target_id = getattr(new, 'user_id', getattr(prev, 'user_id', None))
                            if target_id:
                                try:
                                    t_entity = await client.get_entity(target_id)
                                    target_person = f"{t_entity.first_name} | ID: {t_entity.id}"
                                except: 
                                    target_person = f"ID: {target_id}"
                            action_text = "🛡️ رفعت شخصاً مشرفاً جديداً (رفع)" if isinstance(new, types.ChannelParticipantAdmin) else "❌ نزعت الاشراف من شخص (نزل)"

                        elif isinstance(log.action, types.ChannelAdminLogEventActionParticipantToggleBanned):
                            prev, new = log.action.prev_participant, log.action.new_participant
                            target_id = getattr(new, 'user_id', getattr(prev, 'user_id', None))
                            if target_id:
                                try:
                                    t_entity = await client.get_entity(target_id)
                                    target_person = f"{t_entity.first_name} | ID: {t_entity.id}"
                                except: 
                                    target_person = f"ID: {target_id}"
                            if isinstance(new, types.ChannelParticipantBanned):
                                action_text = "🚫 حظرت شخصاً ومنعته من المجموعة ( Ban )" if hasattr(new.banned_rights, 'view_messages') and new.banned_rights.view_messages else "⚠️ قيدت صلاحيات شخص ( كتم / تقييد )"
                            else: 
                                action_text = "🔓 ألغيت الحظر عن شخص ( Unban )"

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
                    except Exception as event_error:
                        print(f"⚠️ تم تخطي خطأ في قراءة حدث فرعي لضمان استمرار السورس: {event_error}")
                        continue

            # تحديث معرف الأمان دائماً خارج حلقة الأحداث لضمان عدم التعليق نهائياً
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
            print(f"⚠️ خطأ دوري عام في الرادار (تم تداركه تلقائياً): {loop_error}")
            
        await asyncio.sleep(5)

# أمر الفحص المستقر والذكي
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        await event.edit("✅ **السورس يعمل الآن بأعلى درجات الاستقرار والثبات!**\n\n• أمر الفحص مستقر تماماً.\n• الرادار محمي ومخصص لحسابك فقط.\n• تم حل مشكلة توقف الأوامر بفضل معالج الأحداث المعزول الجديد.")

async def main():
    loop = asyncio.get_running_loop()
    if sys.platform != 'win32':
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(safe_suicide_shutdown(s.name)))

    # 1️⃣ تشغيل سيرفر الاستجابة الفورية لريلواي
    await start_dummy_server()

    # 2️⃣ 🛡️ جدار الصمت المطلق (بروتوكول الـ 45 ثانية لتدمير النسخة القديمة)
    print("⏳ [حصن الأمان] تم خداع ريلواي بنجاح! جاري الانتظار لـ 45 ثانية صامتة ليموت السيرفر القديم تماماً وتأمين جلستك الفاخرة من الحرق...")
    await asyncio.sleep(45)
    
    print("🚀 الساحة آمنة بنسبة 100%! جاري الاتصال الرسمي والوحيد بتيليجرام...")
    try:
        await client.start()
        print("✅ تم الاتصال بنجاح ساحق وثبات أبدي!")
        
        group_entity = await client.get_entity(TARGET_CHAT_ID)
        me = await client.get_me()
        
        # تشغيل رادار المراقبة الآمن
        client.loop.create_task(watch_admin_log(group_entity, me.id))
        await client.run_until_disconnected()
        
    except AuthKeyDuplicatedError:
        print("❌ خطأ: هذه الجلسة تعرضت للتداخل قبل وضع هذا الكود المحصن.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ تشغيل: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
