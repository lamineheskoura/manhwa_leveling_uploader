# --- Professional Global Commenting Protocol: ROYAL GHOST ENGINE V26.0 (Unified Overlord) سيدي ---
import os
import asyncio
import requests
import time
import re
from DrissionPage import ChromiumPage, ChromiumOptions
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.utils import pack_bot_file_id
from telethon.errors import FloodWaitError

# 🔐 الثوابت الملكية (تُسحب من Secrets)
API_ID = 38020317
API_HASH = '941185ea933fd95a990e881fe50a6882'
CHAT_ID = -1003602777623
SITE_API_KEY = "KING_SECRET_KEY_99x"
SITE_API_URL = "https://manhwa-leveling.onrender.com/shadow-throne-99x/api/bulk-sync"
BRIDGE_URL = os.getenv("NGROK_URL") # رابط النفق الخاص بك سيدي

BOT_TOKENS = [
    '8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA',
    '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8',
    '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE'
]

# إعدادات Supabase سيدي للتحكم بالمهام
SB_URL = (os.getenv("SB_URL") or "").strip()
SB_KEY = (os.getenv("SB_KEY") or "").strip()
HEADERS = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}

# --- 1. محرك الزحف الشبحي (The Ghost Architect) ---
class GhostArchitect:
    def __init__(self):
        self.co = ChromiumOptions()
        # الربط بمتصفح Brave في منزلك سيدي عبر النفق
        addr = BRIDGE_URL.replace("https://", "").replace("http://", "")
        self.co.set_argument(f'--remote-debugging-address={addr}')
        try:
            self.page = ChromiumPage(self.co)
            print("✅ تم اختراق Brave والربط بالجسر بنجاح سيدي!")
        except Exception as e:
            print(f"❌ فشل الجسر: تأكد من تشغيل Ngrok و Brave بوضع التصحيح. {e}")
            self.page = None

    def extract_precise_images(self, url):
        if not self.page: return []
        self.page.get(url)
        print(f"🕵️ زحف سحابي على شاشتك: {url}")
        
        self.page.scroll.to_bottom()
        time.sleep(3) # انتظار تحميل الصور
        
        links = []
        containers = ['.reading-content', '.main-col', '.vung-doc', '.reader-area', '.wp-manga-chapter-img']
        
        target = None
        for s in containers:
            if self.page.ele(s):
                target = self.page.ele(s)
                break
        
        if target:
            imgs = target.eles('tag:img')
            for img in imgs:
                src = img.attr('data-src') or img.attr('data-lazy-src') or img.attr('src')
                if src and 'http' in src and not any(x in src.lower() for x in ['logo', 'banner']):
                    links.append(src)
        
        # إذا فشلت الحاويات، البحث عن الروابط المباشرة سيدي
        if not links:
            links = [l for l in re.findall(r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)', self.page.html) 
                     if not any(x in l.lower() for x in ['logo', 'icon', 'avatar'])]
        
        return list(dict.fromkeys(links))

    def find_next(self):
        selectors = ['.next_page', 'a[rel="next"]', 'a:contains("التالي")']
        for s in selectors:
            btn = self.page.ele(s, timeout=1)
            if btn and btn.link: return btn.link
        return None

# --- 2. محرك الرفع المتوازي (Royal Uploading Squadron) ---
async def safe_upload(client, img_url, semaphore):
    async with semaphore:
        try:
            # التحميل يتم من GitHub مباشرة (سرعة صاروخية)
            content = requests.get(img_url, timeout=20).content
            file_path = f"temp_{time.time()}.jpg"
            with open(file_path, "wb") as f: f.write(content)
            
            sent = await client.send_file(CHAT_ID, file_path, force_document=True)
            os.remove(file_path) # تنظيف المخلفات سيدي
            return str(pack_bot_file_id(sent.media.document))
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 2)
            return await safe_upload(client, img_url, semaphore)
        except: return None

async def process_chapter_task(task, bot_index):
    token = BOT_TOKENS[bot_index]
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    await client.start(bot_token=token)
    
    architect = GhostArchitect()
    semaphore = asyncio.Semaphore(5) # 5 صور في وقت واحد لكل بوت
    
    curr_url = task['source_url']
    m_id = task['target_id']
    last_ch = float(task['last_chapter'])
    
    images = architect.extract_precise_images(curr_url)
    if images:
        print(f"🚀 الفارس {bot_index+1} يرفع الفصل {last_ch+1} ({len(images)} صورة)")
        upload_tasks = [safe_upload(client, img, semaphore) for img in images]
        file_ids = await asyncio.gather(*upload_tasks)
        file_ids = [f for f in file_ids if f]
        
        if file_ids:
            # إرسال البيانات لموقعك سيدي
            payload = {
                "manhwa_id": int(m_id),
                "chapter_number": last_ch + 1,
                "image_ids": file_ids,
                "is_premium": False
            }
            res = requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY})
            
            # تحديث قاعدة البيانات ورابط الفصل التالي
            next_url = architect.find_next()
            update_payload = {
                "last_chapter": last_ch + 1,
                "status": "idle",
                "source_url": next_url if next_url else curr_url
            }
            requests.patch(f"{SB_URL}/rest/v1/manhwa_tasks?id=eq.{task['id']}", 
                           headers=HEADERS, json=update_payload)
            print(f"✅ تم الفصل {last_ch+1} بنجاح سيدي!")

    await client.disconnect()

# --- 3. المهمة الرئيسية (The Grand Orchestration) ---
async def start_operation():
    # جلب المهام من Supabase
    r = requests.get(f"{SB_URL}/rest/v1/manhwa_tasks?status=eq.idle&limit=3", headers=HEADERS)
    tasks = r.json()
    
    if not tasks:
        print("📭 لا مهام حالياً سيدي.")
        return

    # تشغيل كل مهمة ببوت منفصل سيدي لزيادة السرعة
    mission_tasks = []
    for i, task in enumerate(tasks):
        if i < len(BOT_TOKENS):
            mission_tasks.append(process_chapter_task(task, i))
    
    await asyncio.gather(*mission_tasks)

if __name__ == "__main__":
    asyncio.run(start_operation())