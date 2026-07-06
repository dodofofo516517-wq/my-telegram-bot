# 2. مراقبة تغيير الصلاحيات في المجموعة بشكل آمن
@client.on(events.ChatAction)
async def admin_handler(event):
    # التحقق أولاً إذا كان الحدث يخص المشرفين
    if event.user_added or event.user_kicked:
        return # تجاهل أحداث دخول وخروج الأعضاء العاديين

    # استخدام try-except لتجنب الانهيار إذا لم تكن الخاصية موجودة
    try:
        if getattr(event, 'admin_rights_changed', False):
            chat = await event.get_chat()
            msg = f"⚠️ **تنبيه: تم تغيير صلاحيات مشرف!**\n\nالدردشة: {chat.title}"
            await client.send_message(TARGET_USER, msg)
            print(f"تم إرسال تنبيه إلى {TARGET_USER}")
    except Exception as e:
        # إذا حدث خطأ، سنقوم بتجاهله وطباعته في الـ Logs فقط
        print(f"خطأ غير متوقع في معالجة الحدث: {e}")
