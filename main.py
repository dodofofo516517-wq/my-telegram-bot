import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest

# --- البيانات المحدثة ---
SESSION = "1AZWarzsBuwRlA4e4vbYOqXXFtJDnQKRn_lnGga1vIKkAeC0FM_BzYLlBnUZmpuadvLx8s-nq4jWUlW4_QJhmyw3ox5-O19mKA20OpbTG7oAHr35xQinqtSdoiAerXtRW98iCqWUYrNwKc2Vev0jT0pdI45yGnjYZ6B1ZQF7ib776ztOs5jlzBGE2giLAQUWgFj26O6UE616M-mWOMTBMPoHa3wkht1Pwgo85xKW060DBYMmmlRCvjVhV-Z6XY9386olPNAb-6EcLAotVgKzTcpJvsUVufCd0ivzP0lG08yP7VWSKHWzkU2d-_vTvqhxHTZxxN_lPZa5lNw8LRXDlBlRExMDxdd4="
API_ID = 39123507
API_HASH = "7d18adec71b1e5ce85938c97244b8a7b"

# بيانات الحساب المستقبل للتنبيهات
TARGET_ID = 8965415461 
TARGET_USERNAME = "@hLoshByHere"

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 1. أمر الفحص (للتحقق من عمل السورس)
@client.on(events.NewMessage(pattern=r'\.فحص'))
async def handler(event):
    await event.edit(f"✅ السورس يعمل بنجاح للمراقبة لصالح: {TARGET_USERNAME}")

# 2. مراقبة الأجهزة الجديدة (إرسال تفاصيل الجهاز فوراً)
async def watch_new_sessions():
    # جلب قائمة الجلسات الحالية عند التشغيل
    try:
        auths = await client(GetAuthorizationsRequest())
        known_devices = [a.hash for a in auths.authorizations]
    except:
        known_devices = []

    while True:
        await asyncio.sleep(30) # فحص كل 30 ثانية
        try:
            current_auths = await client(GetAuthorizationsRequest())
            for auth in current_auths.authorizations:
                if auth.hash not in known_devices:
                    # تم اكتشاف جهاز جديد
                    msg = (f"🚨 **تنبيه: دخول جهاز جديد للحساب!**\n\n"
                           f"📱 الجهاز: {auth.device_model}\n"
                           f"💻 النظام: {auth.platform}\n"
                           f"🌐 IP: {auth.ip}\n"
                           f"📍 الدولة: {auth.country}\n"
                           f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    await client.send_message(TARGET_ID, f"إلى {TARGET_USERNAME}:\n{msg}")
                    known_devices.append(auth.hash)
        except: continue

# 3. مراقبة تغييرات الصلاحيات في القروبات
@client.on(events.ChatAction)
async def group_monitor(event):
    me = await client.get_me()
    try:
        # التحقق من أن الشخص الذي قام بالفعل هو صاحب هذا الحساب (السورس)
        async for log in client.iter_admin_log(event.chat_id, limit=1):
            if log.user_id == me.id: 
                msg = (f"⚙️ **تنبيه إدارة القروب**\n"
                       f"👤 الحساب المنفذ: {me.username or me.id}\n"
                       f"📝 الحدث: تم تغيير صلاحيات / إشراف\n"
                       f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                await client.send_message(TARGET_ID, f"إلى {TARGET_USERNAME}:\n{msg}")
                break
    except: pass

async def main():
    await client.start()
    print(f"🚀 السورس يعمل ويرسل التنبيهات إلى {TARGET_USERNAME}")
    asyncio.create_task(watch_new_sessions())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
