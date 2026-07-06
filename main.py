import asyncio
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession

# --- الإعدادات الأساسية ---
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
SESSION_STRING = "1AZWarzsBu4k3MBIAdWLJyf9TIaaAtTpPJtpXMW2hoMG0DKTxRt4_5T4qrZdsdyst7yWaqj-0CW-lCUorSPLC8MgZVbjoAHTatD_fQmi2R89Bvq69zprOCCkcanFjZGhme9ahTK83eyqmpezk6Ufvm7Kym-5dtR5WUOKfqKys3dk6n5HMeq67OJIw3w8i-D9pVOrLjyaFHhJoiifBE450rwl5L-hBKdFD3flPaGydpw7WR5WVh6XSqgscmqQv7EB1dG0J3wPU32F9kDKdNKvjhfSLg0ARbzxcP6W7O28VQ7HySzXNdD54hGrqyLW2I3ujzmt8bvqFQ_LdIsPBupJpkvgAX8m89U0="

# المعرفات الدقيقة
TARGET_CHAT_ID = -1003555828336  # أيدي القروب الكامل
PURE_CHAT_ID = 3555828336        # أيدي القروب بدون (-100) للتنصت العميق
TARGET_USER_ID = 8965415461     # أيدي حساب التنبيهات المنشود
MY_ID = 8980682089              # أيدي حساب السورس الخاص بك

# تشغيل الكلينت بمحاكاة آمنة لحماية الجلسة
client = TelegramClient(
    StringSession(SESSION_STRING.strip()), 
    API_ID, 
    API_HASH,
    device_model="iPhone 15 Pro Max",
    system_version="iOS 17.5",
    app_version="10.11.1"
)

# 1. المراقبة العميقة (الحظر، إلغاء الحظر، رفع ونزع الإشراف)
@client.on(events.Raw(types.UpdateChannelParticipant))
async def on_channel_participant_update(event):
    if event.channel_id != PURE_CHAT_ID:
        return
    
    # التحقق الصارم: هل أنت من قمت بالفعل من جوالك؟
    if event.actor_id != MY_ID:
        return
        
    try:
        action_text = "إجراء غير محدد"
        
        # جلب معلومات الشخص المستهدف برمجياً
        try:
            user_entity = await client.get_entity(event.user_id)
            target_person = f"{user_entity.first_name} | ID: {user_entity.id}"
        except:
            target_person = f"ID: {event.user_id}"

        prev = event.prev_participant
        new = event.new_participant

        # الفلترة الدقيقة للأفعال الإدارية
        if isinstance(new, types.ChannelParticipantAdmin):
            if isinstance(prev, types.ChannelParticipantAdmin):
                action_text = "✏️ تعديل صلاحيات مشرف"
            else:
                action_text = "🛡️ رفعت شخصاً مشرفاً"
        elif isinstance(prev, types.ChannelParticipantAdmin) and not isinstance(new, types.ChannelParticipantAdmin):
            action_text = "❌ نزعت الاشراف من شخص"
        elif isinstance(new, types.ChannelParticipantBanned):
            if hasattr(new.banned_rights, 'view_messages') and new.banned_rights.view_messages:
                action_text = "🚫 حظرت شخصاً ( Ban )"
            else:
                action_text = "⚠️ قيدت صلاحيات شخص ( كتم / Restrict )"
        elif isinstance(prev, types.ChannelParticipantBanned) and not isinstance(new, types.ChannelParticipantBanned):
            action_text = "🔓 ألغيت الحظر عن شخص ( Unban )"
        else:
            return  # تخطي الأحداث العادية كالمغادرة والانضمام

        # صياغة الرسالة الموحدة
        alert_msg = (
            f"🚨 **تنبيه نشاط من حساب السورس:**\n\n"
            f"⚙️ **الأمر الفُعل:** {action_text}\n"
            f"👤 **الشخص المستهدف:** {target_person}\n"
            f"💻 **الجهاز المتصل:** الجوال الشخصي المعتمد\n\n"
            f"📍 **المكان:** قروب hLoSh"
        )
        await client.send_message(TARGET_USER_ID, alert_msg)
        
    except Exception as e:
        print(f"Error: {e}")

# 2. مراقبة تغيير اسم المجموعة (تأتي عبر الرسائل الخدمية المباشرة)
@client.on(events.NewMessage(chats=TARGET_CHAT_ID))
async def on_service_message(event):
    if event.sender_id != MY_ID:
        return
        
    if event.message.action and isinstance(event.message.action, types.MessageActionChatEditTitle):
        try:
            new_title = event.message.action.title
            alert_msg = (
                f"🚨 **تنبيه نشاط من حساب السورس:**\n\n"
                f"⚙️ **الأمر الفُعل:** ✏️ غيرت اسم المجموعه\n"
                f"👤 **الاسم الجديد:** {new_title}\n"
                f"💻 **الجهاز المتصل:** الجوال الشخصي المعتمد\n\n"
                f"📍 **المكان:** قروب hLoSh"
            )
            await client.send_message(TARGET_USER_ID, alert_msg)
        except Exception as e:
            print(f"Error: {e}")

# أمر الفحص للتأكد من الحالة
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def check_status(event):
    if event.sender_id == MY_ID:
        await event.edit("✅ السورس مستقر تماماً ويراقب الحظر والإشراف والأسماء الآن في الخلفية!")

async def main():
    print("🚀 بدء تشغيل السورس المطور بنظام التنصت العميق...")
    await client.start()
    print("✅ السورس يعمل ويراقب الآن بدقة متناهية.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
