import asyncio
import sys
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession
from telethon.errors import AuthKeyDuplicatedError
from telethon.tl.functions.channels import GetAdminLogRequest

# --- البيانات والمعرفات كاملة وجاهزة ومحمية بجلستك الثمينة ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# الجلسة الجديدة التي أرسلتها - قمنا بتثبيتها وحمايتها هنا
SESSION_STRING = "1AZWarzsBu8XcCo82MdU7ydXd5o6n5Wjs_IuersQdGu608iV-oXM8SVWk021ArYj7RICHkj6n8GaAYrGkaQKYs2WQ_bxavmuX9DWFN-mGPAIPLLltdX3PUw2ThtBkyHUfGF9b9c2McxjWEyE7gsYTgImF9v-kSJc5c4g16Y6vQKFvPt0RYAEUkvZ7xkUtnrkUfrakcn_SIWyIm4t_j-7odFS-1rWUe1Qlwqq_-FePpTFjJ85WMFybMaUJ3TGJkjU-N8Ohw7D0mXENNhfiZJJUbXFp0OT-I7s2yaXWqofPo6h-qXHKzYeEfTe6m76czJpKL6l2WPKtjZHfg6vpR1vSJX_MlGSdkOY="

TARGET_CHAT_ID = -1003555828336  # أيدي القروب الكامل (hLoSh)
TARGET_USER_ID = 8965415461     # أيدي حساب التنبيهات المستهدف

# تنظيف تلقائي صارم لمنع أي فراغات أو شوائب في السلسلة النصية
clean_session = SESSION_STRING.strip().replace('"', '').replace("'", "")

# محاكاة ثابتة ومحمية لجهاز آيفون شخصي معتمد من نظام تيليجرام
client = TelegramClient(
    StringSession(clean_session), 
    API_ID, 
    API_HASH,
    device_model="iPhone 15 Pro Max",
    system_version="iOS 17.5",
    app_version="10.11.1"
)

last_log_id = 0

# دالة المراقبة الرسمية والمحمية من الأخطاء والانهيار
async def watch_admin_log(group_entity, me_id):
    global last_log_id
    print("👁️ بدأ نظام الفحص الفولاذي لسجل المشرفين...")
    
    # جلب نقطة البداية للسجل لتفادي الرسائل القديمة
    try:
        reply = await client(GetAdminLogRequest(
            channel=group_entity,
            q='',
            events_filter=types.ChannelAdminLogEventsFilter(),
            max_id=0,
            min_id=0,
            limit=1
        ))
        if reply and reply.events:
            last_log_id = reply.events[0].id
    except Exception as e:
        print(f"⚠️ تنبيه السجل: {e}")
        last_log_id = 0

    while True:
        try:
            if last_log_id == 0:
                reply = await client(GetAdminLogRequest(
                    channel=group_entity,
                    q='',
                    events_filter=types.ChannelAdminLogEventsFilter(),
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
            
            # جلب الأحداث الجديدة مع الفلتر المتوافق
            reply = await client(GetAdminLogRequest(
                channel=group_entity,
                q='',
                events_filter=types.ChannelAdminLogEventsFilter(),
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
                        
                    # التحقق أن الفعل صادر منك حصراً لحماية الخصوصية
                    if log.user_id != me_id:
                        continue

                    action_text = None
                    target_person = "غير معروف"

                    # الفلترة الذكية للأحداث
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

            # إرسال التنبيهات مرتبة
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

# ميثود الفحص السريع لإثبات جهوزية السورس
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    me = await client.get_me()
    if event.sender_id == me.id:
        await event.edit("✅ سورس المراقبة مستقر ومحمي بأعلى درجات الأمان! الجلسة الجديدة تعمل الآن بنجاح تام.")

async def main():
    # [مهم جداً] انتظام الأمان الإجباري لقتل السيرفر القديم في Railway ومنع الاتصال المزدوج تماماً
    print("⏳ [جدار حماية الجلسة] يرجى الانتظار.. يتم الآن خنق وتأخير التشغيل لـ 40 ثانية للتأكد من إغلاق السيرفرات القديمة تماماً ومنع حرق الجلسة...")
    await asyncio.sleep(40)
    
    print("🚀 جاري محاولة الاتصال الآمن بالسيرفرات باستخدام الجلسة الجديدة...")
    try:
        await client.start()
        print("✅ تم الاتصال بنجاح فولاذي وبدون تداخل!")
        
        group_entity = await client.get_entity(TARGET_CHAT_ID)
        me = await client.get_me()
        
        # إطلاق مهمة المراقبة الذكية في الخلفية
        client.loop.create_task(watch_admin_log(group_entity, me.id))
        await client.run_until_disconnected()
        
    except AuthKeyDuplicatedError:
        print("❌ خطأ حرج: تم رصد محاولة اتصال مزدوجة مجدداً! نظام الأمان أوقف التشغيل فوراً لحماية الجلسة.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
