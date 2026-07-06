import asyncio
import sys
import signal
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession
from telethon.errors import AuthKeyDuplicatedError
from telethon.tl.functions.channels import GetAdminLogRequest

# --- البيانات والمعرفات كاملة ومحمية ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# ⚠️ الجلسة القديمة احترقت؛ استخرج جلسة جديدة كلياً وضَعها بين القوسين هنا ⚠️
SESSION_STRING = "ضَع_كود_الجلسة_الجديد_هنا"

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

# الفلتر المصحح والمفعل بالكامل لجلب الأحداث دون حجب
CUSTOM_FILTER = types.ChannelAdminLogEventsFilter(
    promote=True,  
    demote=True,   
    ban=True,      
    unban=True,    
    kick=True,     
    settings=True  
)

# 🛡️ نظام الانتحار البرمجي لقطع الاتصال فوراً عند التحديث
async def safe_suicide_shutdown(signal_name):
    print(f"🚨 [درع الأمان] تم استلام إشارة {signal_name} من Railway!")
    print("⚡ جاري قطع الاتصال فوراً ونظيفاً لحماية الجلسة من الحرق...")
    try:
        await client.disconnect()
        print("✅ تم فصل الجلسة بأمان واختفى السيرفر القديم.")
    except Exception as e:
        print(f"خطأ أثناء الفصل المفاجئ: {e}")
    finally:
        sys.exit(0)

# دالة مراقبة حساب يوسف الشخصي فقط في القروب
async def watch_admin_log(group_entity, me_id):
    global last_log_id
    print("👁️ رادار المراقبة الخاص بحسابك فقط يعمل الآن بثبات...")
    
    try:
        reply = await client(GetAdminLogRequest(
            channel=group_entity,
            q='',
            events_filter=CUSTOM_FILTER,
            max_id=0,
            min_id=0,
            limit=1
        ))
        if reply and reply.events:
            last_log_id = reply.events[0].id
    except Exception as e:
        print(f"⚠️ تنبيه السجل الأولي: {e}")
        last_log_id = 0

    while True:
        try:
            if last_log_id == 0:
                reply = await client(GetAdminLogRequest(
                    channel=group_entity,
                    q='',
                    events_filter=CUSTOM_FILTER,
                    max_id=0,
                    min_id=0,
                    limit=1
                ))
                if reply and reply.events:
                    last_log_id = reply.events[0].id
                await asyncio.sleep(3)
                continue

            actions_to_send = []
            current_max_id = last_log_id
            
            reply = await client(GetAdminLogRequest(
                channel=group_entity,
                q='',
                events_filter=CUSTOM_FILTER,
                max_id=0,
                min_id=0,
                limit=20
            ))
            
            if reply and reply.events:
                for log in reply.events:
                    if log.id <= last_log_id:
                        break
                    
                    if log.id > current_max_id:
                        current_max_id = log.id

                    # 🎯 الفلتر الحاسم: مراقبة أفعال حساب يوسف فقط وتجاهل باقي المشرفين
                    if log.user_id != me_id:
                        continue

                    action_text = None
                    target_person = "غير معروف"

                    # 1️⃣ تحليل الرفع والنزل
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
                                action_text = "🛡️ رفعت شخصاً مشرفاً جديداً (رفع)"
                        else:
                            action_text = "❌ نزعت الاشراف من شخص (نزل)"

                    # 2️⃣ تحليل الحظر والكتم
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

            last_log_id = current_max_id

            for alert_msg in reversed(actions_to_send):
                try:
                    await client.send_message(TARGET_USER_ID, alert_msg)
                except Exception as e:
                    print(f"❌ فشل إرسال لحساب التنبيهات: {e}")
                
                try:
                    await client.send_message('me', alert_msg)
                except Exception as e:
                    print(f"❌ فشل إرسال للمحفوظات: {e}")

        except Exception as e:
            print(f"خطأ دوري في فحص السجل: {e}")
            
        await asyncio.sleep(3)

# أمر الفحص المستقر
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        await event.edit("✅ **السورس مستقر ويعمل بأعلى كفاءة وجاهزية!**\n\n• أمر الفحص مستقر.\n• رادار المراقبة يعمل لحسابك الشخصي فقط.\n• الجلسة محمية ببروتوكول الـ 55 ثانية الأمني ضد تداخل ريلواي.")

async def main():
    # تسجيل مستشعرات الأمان لحماية الجلسة من الاتصال المزدوج
    loop = asyncio.get_running_loop()
    if sys.platform != 'win32':
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(safe_suicide_shutdown(s.name)))

    # 🛡️ الحصن الفولاذي: الانتظار 55 ثانية لضمان موت السيرفر القديم تماماً قبل بدء الاتصال
    print("⏳ [بروتوكول الأمان الفولاذي] جاري الانتظار لـ 55 ثانية للتأكد من تدمير السيرفر القديم وحماية جلستك الجديدة من الحرق...")
    await asyncio.sleep(55)
    
    print("🚀 جاري الاتصال الآمن بالسيرفرات الرسمية لتيليجرام...")
    try:
        await client.start()
        print("✅ تم الاتصال بنجاح وثبات مطلق!")
        
        group_entity = await client.get_entity(TARGET_CHAT_ID)
        me = await client.get_me()
        
        # تشغيل رادار المراقبة لحسابك الشخصي
        client.loop.create_task(watch_admin_log(group_entity, me.id))
        await client.run_until_disconnected()
        
    except AuthKeyDuplicatedError:
        print("❌ خطأ حرج: الجلسة محروقة! تأكد من استخراج واحدة جديدة تماماً وضعها في الكود.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
