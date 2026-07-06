import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelAdminLogEventActionParticipantToggleAdmin

# --- الإعدادات ---
SESSION = "1AZWarzsBu8...ضع_جلستك_الجديدة_هنا..."
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_ID = 8965415461 # أيدي الحساب المستقبل

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# --- 1. مراقبة تغييرات الصلاحيات (Admin Logs) ---
# هذه الدالة تراقب أي تغيير في إشراف القروب
@client.on(events.ChatAction)
async def monitor_admin_logs(event):
    if event.user_added or event.user_kicked or event.admin_rights_changed:
        try:
            # البحث في سجلات المشرفين
            async for log in client.iter_admin_log(event.chat_id, limit=1):
                # إذا كان الحدث تغيير صلاحيات
                if isinstance(log.action, ChannelAdminLogEventActionParticipantToggleAdmin):
                    msg = (f"⚠️ **تنبيه إداري!**\n"
                           f"تغيير صلاحيات تم رصده في القروب.\n"
                           f"المتأثر: {log.action.user_id}\n"
                           f"تم الإرسال لـ {TARGET_ID}")
                    await client.send_message(TARGET_ID, msg)
                    break
        except Exception as e:
            print(f"خطأ في المراقبة: {e}")

# --- 2. مراقبة الاتصال (Device/Connection) ---
# ملاحظة: تيليجرام لا يرسل "إشعار اتصال" فوري إلا عبر الجلسات (Authorizations)
# هذا الجزء يراقب أي تحديث في حالة الجلسات النشطة
@client.on(events.Raw)
async def monitor_connection(event):
    # نراقب تحديثات الحالة الخاصة بالحساب
    if hasattr(event, 'status'):
        await client.send_message(TARGET_ID, "📱 تم اكتشاف نشاط/اتصال جديد على حساب السورس.")

async def main():
    await client.start()
    print("السورس يعمل ويراقب...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
