# --- Professional Global Commenting Protocol: SOVEREIGN EXECUTIONER V1.1 (RESTORATION) سيدي ---
import os
import asyncio
import requests
import re
import nodriver as uc
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.utils import pack_bot_file_id

# 🔐 الثوابت الملكية سيدي (تُسحب من بيئة GitHub)
API_ID = 38020317
API_HASH = '941185ea933fd95a990e881fe50a6882'
CHAT_ID = -1003602777623
SITE_API_KEY = "KING_SECRET_KEY_99x"
SITE_API_URL = "https://manhwa-leveling.onrender.com/shadow-throne-99x/api/bulk-sync"

SB_URL = os.getenv("SB_URL")
SB_KEY = os.getenv("SB_KEY")
HEADERS = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}

BOT_TOKENS = [
    '8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA',
    '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8',
    '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE'
]

class SovereignScout:
    async def get_links(self, url):
        browser = None
        try:
            print(f"🌐 جاري محاولة اقتحام الرابط سيدي: {url}")
            # الترميم الملكي لبيئة GitHub سيدي
            browser = await uc.start(
                headless=True,
                browser_args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage', # حل مشكلة الذاكرة في GitHub
                    '--disable-gpu',
                    '--no-first-run',
                    '--no-zygote'
                ]
            )
            page = await browser.get(url)
            
            # انتظار استراتيجي لتجاوز الكلود فاير سيدي
            print("⏳ انتظار فك التشفير...")
            await page.wait(10) 
            
            content = await page.get_content()
            image_pattern = r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)'
            links = re.findall(image_pattern, content)
            
            clean_links = [l for l in dict.fromkeys(links) if 'manga' in l.lower() and not any(x in l.lower() for x in ['logo', 'icon'])]
            
            print(f"🎯 تم استخراج {len(clean_links)} صورة بنجاح سيدي.")
            return clean_links
        except Exception as e:
            print(f"❌ خطأ في التسلل سيدي: {e}")
            return []
        finally:
            if browser:
                await browser.stop()

async def execute_mission(task, bot_index):
    token = BOT_TOKENS[bot_index]
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    try:
        await client.start(bot_token=token)
        scout = SovereignScout()
        links = await scout.get_links(task['source_url'])
        
        if not links:
            print(f"⚠️ الفارس {bot_index+1}: لم يجد غنائم، قد تكون الحماية أقوى سيدي.")
            return

        print(f"🚀 الفارس {bot_index+1} يرفع الفصل {task['last_chapter']+1}")
        file_ids = []
        for link in links:
            try:
                sent = await client.send_file(CHAT_ID, link, force_document=True)
                file_ids.append(str(pack_bot_file_id(sent.media.document)))
            except Exception as up_err:
                continue

        if file_ids:
            payload = {
                "manhwa_id": int(task['target_id']),
                "chapter_number": float(task['last_chapter']) + 1,
                "image_ids": file_ids,
                "is_premium": False
            }
            requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY})
            
            requests.patch(f"{SB_URL}/rest/v1/manhwa_tasks?id=eq.{task['id']}", 
                           headers=HEADERS, json={"status": "idle", "last_chapter": float(task['last_chapter']) + 1})
            print(f"✅ تم بنجاح رفع الفصل لـ ID: {task['target_id']}")
            
    except Exception as e:
        print(f"❌ خطأ الفارس {bot_index}: {e}")
    finally:
        await client.disconnect()

async def main():
    if not SB_URL or not SB_KEY:
        print("❌ نقص في مفاتيح Supabase سيدي!")
        return
    r = requests.get(f"{SB_URL}/rest/v1/manhwa_tasks?status=eq.idle&limit=3", headers=HEADERS)
    try:
        tasks = r.json()
        if not tasks:
            print("📭 لا مهام في الانتظار سيدي.")
            return
        mission_pool = [execute_mission(task, i) for i, task in enumerate(tasks)]
        await asyncio.gather(*mission_pool)
    except Exception as e:
        print(f"🔥 خطأ في قراءة المهام: {e}")

if __name__ == "__main__":
    asyncio.run(main())