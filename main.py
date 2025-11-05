from flask import Flask
from telethon import TelegramClient
import asyncio, os, json, time

app = Flask(__name__)

API_ID = 123456  # <--- اینجا api_id رو بذار
API_HASH = "your_api_hash_here"  # <--- اینجا api_hash رو بذار
SESSION_NAME = "asanpresta_session"
SENT_LOG = "sent_contacts.json"

MESSAGE = """
💐 بنام آفریننده و خالق یکتای مهربان

✍️ با سلام و عرض ادب خدمت تمامی دوستان و همکاران و مشتریان عزیز محترم
📢 به اطلاع می‌رساند کانال رسمی آسان پرستا راه‌اندازی شده است.
🌐 لطفاً برای اطلاع از آخرین خدمات و تخفیف‌ها عضو شوید:
📌 https://t.me/asanpresta_ir
🙏 از توجه و همراهی شما بی‌نهایت سپاسگزاریم.
"""

@app.route('/')
def index():
    asyncio.run(send_messages())
    return '✅ ارسال پیام‌ها کامل شد؛ فایل sent_contacts.json ذخیره شد.'

async def send_messages():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    sent = []
    if os.path.exists(SENT_LOG):
        with open(SENT_LOG, 'r', encoding='utf-8') as f:
            sent = json.load(f)

    contacts = await client.get_contacts()
    updated = sent

    for c in contacts:
        name = f"{c.first_name or ''} {c.last_name or ''}".strip()
        if 'آسان پرستا' in name and c.id not in sent:
            try:
                await client.send_message(c.id, MESSAGE)
                print(f'✅ پیام ارسال شد به {name}')
                updated.append(c.id)
                time.sleep(15)  # فاصله ضد اسپم
            except Exception as e:
                print(f'⚠️ خطا در ارسال برای {name}: {e}')

    with open(SENT_LOG, 'w', encoding='utf-8') as f:
        json.dump(updated, f, ensure_ascii=False)

    print('✅ پایان ارسال')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
