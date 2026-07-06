import asyncio
import os
from datetime import datetime
import aiohttp
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest
from telethon.tl.types import ChannelAdminLogEventActionParticipantToggleAdmin
from aiohttp import web

# --- خادم ويب مدمج وآلية لمنع النوم التلقائي نهائياً ---
async def handle(request):
    return web.Response(text="السورس يعمل بأقصى كفاءة وبدون انقطاع!")

async def self_ping(url):
    """آلية مدمجة تقوم بعمل فحص ذاتي (Ping) كل 5 دقائق لمنع الاستضافة من النوم نهائياً"""
    await asyncio.sleep(30)  # الانتظار حتى يكتمل إقلاع السيرفر
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    print(f"🔄 تم عمل فحص ذاتي مستمر للحفاظ على النشاط: {response.status}")
        except Exception as e:
            print(f"تنبيه الفحص الذاتي: {e}")
        await asyncio.sleep(300)  # فحص كل 5 دقائق (300 ثانية)

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"📢 خادم الاستجابة الوهمي يعمل الآن على منفذ: {port}")

# --- البيانات الأساسية للحساب ---
SESSION = "1AZWarzsBu8NBA9nrnT_E3iBZkHeYV36FTtQa0dsHHwYbRQr-aPJ9yG3cfKQGB9GD0FizqskxSqUWe2uMF9eHKZ7bxkf96n67036JV7NE2jJKE2DoyyhOplSDWN11NyCeDeCHuSw2BJKz8XLlGbtsaZNyIMsoGIfuqVfJLHrK6nMYLouMrgHqA6WYnPJZnOR5p9ZWqkqqyNtEtNsmRjlSN56JJhnHlwPXmBg42urpH5q_Cv17J_9oNuhXiKgDDMvQHIEjk8JVheiQToGdzWSXleBZ4sYY-Sx6yaT4aMq5PjflhhYKdmlxCeCkQyzcvxVz3aDkW8gpTeOZByIjcRdOwK-e38OO0ck="
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"
TARGET_USER_ID = 8965415461

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def get_latest_device():
    try:
        authorizations = await client(GetAuthorizationsRequest())
        if authorizations and authorizations.authorizations:
            sorted_auths = sorted(authorizations.authorizations, key=lambda x: x.date_active, reverse=True)
            latest = sorted_auths[0]
            return f"📱 الجهاز: {latest.device_model}\n💻 النظام: {latest.platform}\n📍 الموقع: {latest.country}\n🌐 IP: {latest.ip}"
    except Exception as e:
        return f"تعذر جلب تفاصيل الجهاز: {str(e)}"
    return "جهاز غير معروف"

async def watch_new_sessions():
    known_sessions_count = 0
    try:
        auths = await client(GetAuthorizationsRequest())
        known_sessions_count = len(auths.authorizations)
    except:
        pass

    while True:
        await asyncio.sleep(15)
        try:
            auths = await client(GetAuthorizationsRequest())
            current_count = len(auths.authorizations)
            
            if current_count > known_sessions_count:
                sorted_auths = sorted(auths.authorizations, key=lambda x: x.date_created, reverse=True)
                new_device = sorted_auths[0]
                
                msg = (
                    "🚨 **تنبيه: دخول جهاز جديد إلى الحساب!**\n\n"
                    f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"📱 الجهاز: {new_device.device_model}\n"
                    f"💻 النظام: {new_device.platform}\n"
                    f"🌐 IP: {new_device.ip}\n"
                    f"📍 الدولة: {new_device.country}"
                )
                await client.send_message(TARGET_USER_ID, msg)
                known_sessions_count = current_count
            elif current_count < known_sessions_count:
                known_sessions_count = current_count
        except Exception:
            continue

@client.on(events.ChatAction)
async def group_monitor(event):
    try:
        if event.is_group or event.is_channel:
            me = await client.get_me()
            async for log in client.iter_admin_log(event.chat_id, limit=1):
                if log.user_id == me.id:
                    device_info = await get_latest_device()
                    action_title = "تعديل في الصلاحيات / الإشراف"
                    target_user = "غير محدد"
                    
                    if isinstance(log.action, ChannelAdminLogEventActionParticipantToggleAdmin):
                        target_user = f"👤 الأيدي للمتأثر: {log.action.new_participant.user_id}"
                        action_title = "تغيير رتبة مشرف (رفع / تنزيل)"

                    msg = (
                        f"⚙️ **تنبيه: تعديل صلاحيات في القروب**\n\n"
                        f"📝 الإجراء: {action_title}\n"
                        f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"{target_user}\n"
                        f"--- تفاصيل الجهاز المنفذ ---\n"
                        f"{device_info}"
                    )
                    await client.send_message(TARGET_USER_ID, msg)
                    break
    except Exception:
        pass

async def main():
    await start_web_server()
    await client.start()
    print("🚀 سورس المراقبة يعمل بنجاح الآن...")
    
    # سنقوم بتحديث هذا الرابط لاحقاً برابط الخدمة من Render للحفاظ على النشاط
    my_render_url = "https://تغيير_هذا_الرابط_لاحقا.onrender.com"
    asyncio.create_task(self_ping(my_render_url))
    
    asyncio.create_task(watch_new_sessions())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
