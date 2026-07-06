import asyncio
import sys
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession
from telethon.errors import AuthKeyDuplicatedError

# --- البيانات والمعرفات كاملة ومدمجة داخلياً ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# الجلسة الأخيرة والجديدة الخاصة بك
SESSION_STRING = "1AZWarzsBu6DBAWJ59pjNLxRxAwDzQFW-YgtGBitTbg23q2Y0ejCkxjjlQs2CYTHaZ3NvscuEKGY6V9TbD9Zm6gz-SaRHPFixz13iAjpcjxdCGbUoDGKJMIuMhhN_t02VINsEwaSNRmaWvNMNe2iXcsTOuxVusFbzfukS-Uxb7vUIimIMHOe0HJ2ewrPsuJ2hgucuIxRGZX0vjzcql3pu_omsHlh9lMQcQ_BdjZnNEe3WRPkVUwOUhaQdnpOR_XUUOvwC1sPG-R5Ey-mzn4OZXV-WE9UByuXDm81hPFqSPnaqOrR2dHhvw_gtlopxGDxoPl5b-nXfVOWW_S42JRXJkZa8RSHL7Qw="

# الإعدادات الصارمة للقنوات والمستخدمين
TARGET_CHAT_ID = -1003555828336  # أيدي القروب الكامل (hLoSh)
PURE_CHAT_ID = 3555828336        # أيدي القروب للتنصت العالي بدون (-100)
TARGET_USER_ID = 8965415461     # أيدي حساب التنبيهات المستهدف
MY_ID = 8980682089              # أيدي حسابك الشخصي (صاحب السورس)

# محاكاة رسمية فائقة الأمان لمنع أنظمة كشف البوتات
client = TelegramClient(
    StringSession(SESSION_STRING.strip()), 
    API_ID, 
    API_HASH,
    device_model="iPhone 15 Pro Max",
    system_version="iOS 17.5",
    app_version="10.11.1"
)

# 1. مراقبة الحظر، إلغاء الحظر، رفع ونزع الإشراف (التنصت العميق)
@client.on(events.Raw(types.UpdateChannelParticipant))
async def on_channel_participant_update(event):
    if event.channel_id != PURE_CHAT_ID:
        return
    
    # الفلترة الصارمة: التحقق أن الفاعل هو أنت فقط من جوالك
    if event.actor_id != MY_ID:
        return
        
    try:
        action_text = ""
        
        # جلب اسم الشخص المتأثر بالإجراء بشكل آمن
        try:
            user_entity = await client.get_entity(event.user_id)
            target_person = f"{user_entity.first_name} | ID: {user_entity.id}"
        except:
            target_person = f"ID: {event.user_id}"

        prev = event.prev_participant
        new = event.new_participant

        # تحليل الحدث الإداري بدقة
        if isinstance(new, types.ChannelParticipantAdmin):
            if isinstance(prev, types.ChannelParticipantAdmin):
                action_text = "✏️ تعديل صلاحيات مشرف قائم"
            else:
                action_text = "🛡️ رفعت شخصاً مشرفاً جديداً"
        elif isinstance(prev, types.ChannelParticipantAdmin) and not isinstance(new, types.ChannelParticipantAdmin):
            action_text = "❌ نزعت الاشراف من شخص"
        elif isinstance(new, types.ChannelParticipantBanned):
            if hasattr(new.banned_rights, 'view_messages') and new.banned_rights.view_messages:
                action_text = "🚫 حظرت شخصاً ( Ban )"
            else:
                action_text = "⚠️ قيدت صلاحيات شخص ( كتم / تقييد )"
        elif isinstance(prev, types.ChannelParticipantBanned) and not isinstance(new, types.ChannelParticipantBanned):
            action_text = "🔓 ألغيت الحظر عن شخص ( Unban )"
        else:
            return  # تخطي الأحداث غير الإدارية

        # إعداد الرسالة الموحدة
        alert_msg = (
            f"🚨 **تنبيه نشاط من حساب السورس**\n\n"
            f"⚙️ **الأمر الفُعل:** {action_text}\n"
            f"👤 **الشخص المستهدف:** {target_person}\n"
            f"💻 **الجهاز المتصل:** الجوال الشخصي المعتمد (اتصال آمن)\n\n"
            f"📍 **المكان:** قروب hLoSh"
        )
        await client.send_message(TARGET_USER_ID, alert_msg)
        
    except Exception as e:
        print(f"خطأ في معالجة الحدث الإداري: {e}")

# 2. مراقبة تغيير اسم المجموعة
@client.on(events.NewMessage(chats=TARGET_CHAT_ID))
async def on_service_message(event):
    if event.sender_id != MY_ID:
        return
        
    if event.message.action and isinstance(event.message.action, types.MessageActionChatEditTitle):
        try:
            new_title = event.message.action.title
            alert_msg = (
                f"🚨 **تنبيه نشاط من حساب السورس**\n\n"
                f"⚙️ **الأمر الفُعل:** ✏️ غيرت اسم المجموعه\n"
                f"👤 **الاسم الجديد:** {new_title}\n"
                f"💻 **الجهاز المتصل:** الجوال الشخصي المعتمد\n\n"
                f"📍 **المكان:** قروب hLoSh"
            )
            await client.send_message(TARGET_USER_ID, alert_msg)
        except Exception as e:
            print(f"خطأ في معالجة تغيير الاسم: {e}")

# أمر فحص الحالة السريع
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    if event.sender_id == MY_ID:
        await event.edit("✅ السورس مستقر وحاضر، ويراقب كامل الصلاحيات والأسماء بنجاح!")

async def main():
    print("⏳ [نظام الحماية] جاري الانتظار 15 ثانية لتهيئة سيرفرات Railway بسلامة...")
    await asyncio.sleep(15)  # الأمان المطلق لمنع تداخل السيرفرات وحرق الجلسة
    
    print("🚀 جاري الاتصال بحساب السورس...")
    try:
        await client.start()
        print("✅ تم الاتصال بنجاح! السورس يعمل الآن في الخلفية دون أي مشاكل.")
        await client.run_until_disconnected()
    except AuthKeyDuplicatedError:
        print("❌ خطأ حرج: تم رصد اتصال متزامن من مكان آخر على هذه الجلسة!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
