# --- Professional Global Commenting Protocol: SOVEREIGN EXECUTIONER V1.0 سيدي ---
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

# توكينات الفرسان الثلاثة سيدي
BOT_TOKENS = [
    '8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA',
    '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8',
    '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE'
]

class SovereignScout:
    """المتسلل السيادي الذي يكسر حصون الكلود فاير سيدي"""
    async def get_links(self, url):
        try:
            # بدء المتصفح في وضع مخفي تماماً داخل GitHub سيدي
            # سيدي، أضفنا --no-sandbox و --disable-dev-shm-usage لتجاوز قيود السيرفر
            browser = await uc.start(
                headless=True, 
                browser_args=[
                    '--no-sandbox', 
                    '--disable-setuid-sandbox', 
                    '--disable-dev-shm-usage', # لمنع انهيار الذاكرة في GitHub
                    '--disable-gpu'
                ]
            )
            page = await browser.get(url)
            
            # سحر الانتظار: يتخطى الكلود فاير تلقائياً سيدي
            await page.wait(8) 
            
            content = await page.get_content()
            
            # استخراج الروابط بالنمط العبقري الذي اكتشفناه
            image_pattern = r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)'
            links = re.findall(image_pattern, content)
            
            # تصفية الروابط سيدي لضمان الجودة
            clean_links = [l for l in dict.fromkeys(links) if 'manga' in l.lower() and not any(x in l.lower() for x in ['logo', 'icon'])]
            
            await browser.stop()
            return clean_links
        except Exception as e:
            print(f"❌ خطأ في التسلل: {e}")
            return []

async def execute_mission(task, bot_index):
    """الفارس الذي ينفذ المهمة ويرفع الغنائم سيدي"""
    token = BOT_TOKENS[bot_index]
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    
    try:
        await client.start(bot_token=token)
        scout = SovereignScout()
        
        links = await scout.get_links(task['source_url'])
        if not links: return

        print(f"🚀 الفارس {bot_index+1} يبدأ رفع {len(links)} صورة سيدي...")
        file_ids = []
        
        for link in links:
            try:
                # رفع الرابط مباشرة سيدي لتوفير الوقت والمساحة
                sent = await client.send_file(CHAT_ID, link, force_document=True)
                file_ids.append(str(pack_bot_file_id(sent.media.document)))
            except: continue

        if file_ids:
            # إرسال البيانات لموقعك سيدي
            payload = {
                "manhwa_id": task['target_id'],
                "chapter_number": task['last_chapter'] + 1,
                "image_ids": file_ids,
                "is_premium": False
            }
            requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY})
            
            # تحديث حالة المهمة سيدي
            requests.patch(f"{SB_URL}/rest/v1/manhwa_tasks?id=eq.{task['id']}", 
                           headers=HEADERS, json={"status": "idle", "last_chapter": task['last_chapter'] + 1})
            
        await client.disconnect()
    except Exception as e:
        print(f"❌ خطأ الفارس {bot_index}: {e}")

async def main():
    r = requests.get(f"{SB_URL}/rest/v1/manhwa_tasks?status=eq.idle&limit=3", headers=HEADERS)
    tasks = r.json()
    if not tasks: return
    
    mission_pool = [execute_mission(task, i) for i, task in enumerate(tasks)]
    await asyncio.gather(*mission_pool)

if __name__ == "__main__":
    asyncio.run(main())