# --- Professional Global Commenting Protocol: ROYAL TITAN ENGINE V14.0 (Full Restoration) سيدي ---
import os
import asyncio
import re
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.utils import pack_bot_file_id

# 🔐 الثوابت الملكية الاستراتيجية سيدي
API_ID = 38020317
API_HASH = '941185ea933fd95a990e881fe50a6882'
CHAT_ID = -1003602777623
SITE_API_KEY = "KING_SECRET_KEY_99x"
SITE_API_URL = "https://manhwa-leveling.onrender.com/shadow-throne-99x/api/bulk-sync"

EMBEDDED_TOKENS = [
    '8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA',
    '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8',
    '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE'
]

SB_URL = (os.getenv("SB_URL") or "").strip().rstrip('/')
SB_KEY = (os.getenv("SB_KEY") or "").strip()
HEADERS = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}

# --- أدوات الاستخبارات والمزامنة سيدي ---

def supabase_get_task():
    try:
        url = f"{SB_URL}/rest/v1/manhwa_tasks?status=eq.idle&order=priority.desc&limit=1"
        r = requests.get(url, headers=HEADERS, timeout=20)
        return r.json() if r.status_code == 200 else []
    except: return []

def supabase_update_task(task_id, payload):
    try:
        url = f"{SB_URL}/rest/v1/manhwa_tasks?id=eq.{task_id}"
        requests.patch(url, headers=HEADERS, json=payload, timeout=20)
    except: pass

class ManhwaArchitect:
    def __init__(self):
        self.co = ChromiumOptions()
        self.co.set_argument('--headless')
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--disable-gpu')
        self.co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        self.co.set_argument('--disable-blink-features=AutomationControlled')
        self.page = ChromiumPage(self.co)

    def bypass_cloudflare(self, url):
        """اختراق الدروع مع محاكاة النشاط سيدي"""
        print(f"🌐 محاولة الدخول: {url}")
        self.page.get(url)
        for i in range(1, 15):
            title = self.page.title
            if "Just a moment" not in title and "Cloudflare" not in title:
                print(f"✅ تم الاختراق. جاري تحفيز الصور...")
                # تمرير ذكي سيدي لفك القفل عن الصور الكسولة (Lazy Load)
                for _ in range(4):
                    self.page.scroll.down(1200)
                    time.sleep(1)
                return True
            print(f"⏳ الدرع نشط ({i})...")
            time.sleep(3)
        return False

    def extract_precise_images(self):
        """نظام البحث العميق عن الأهداف سيدي"""
        links = []
        # مصفوفة المحددات القوية من النسخ السابقة سيدي
        selectors = [
            '.reading-content img', '.main-col img', '.wp-manga-chapter-img img',
            '.reader-area img', '.vung-doc img', '#chapter-video-frame img'
        ]
        
        for s in selectors:
            imgs = self.page.eles(s)
            for img in imgs:
                src = img.attr('data-src') or img.attr('data-lazy-src') or img.attr('src') or img.attr('data-original')
                if src and 'http' in src and not any(x in src.lower() for x in ['logo', 'banner', 'avatar', 'icon']):
                    links.append(src)
        
        # إذا فشلت المحددات، نستخدم المسح الشامل للـ HTML سيدي
        if not links:
            links = re.findall(r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)', self.page.html)
            links = [l for l in links if not any(x in l.lower() for x in ['logo', 'icon', 'theme'])]
            
        return list(dict.fromkeys(links))

    def find_next_chapter(self):
        """البحث عن بوابة الفصل التالي سيدي"""
        btn = self.page.ele('.next_page') or self.page.ele('text:التالي') or self.page.ele('text:Next')
        return btn.attr('href') if btn and btn.attr('href') else None

# --- المحرك الرئيسي للهجوم سيدي ---

async def start_royal_mission():
    tasks = supabase_get_task()
    if not tasks: 
        print("📭 الساحة خالية من المهام سيدي.")
        return
    
    task = tasks[0]
    task_id = task['id']
    print(f"⚔️ استعادة العمليات لـ: {task['name']}...")

    # نظام اختيار الفرسان الموثوق سيدي
    raw_tokens = os.getenv("BOT_TOKENS") or ""
    all_tokens = [t.strip() for t in raw_tokens.split(',') if t.strip()]
    if not all_tokens: all_tokens = EMBEDDED_TOKENS
    
    client = None
    for token in all_tokens:
        try:
            # استخدام الذاكرة لمنع Database Locked سيدي
            temp_client = TelegramClient(MemorySession(), API_ID, API_HASH)
            await temp_client.start(bot_token=token)
            client = temp_client
            print("✅ الفارس جاهز.")
            break
        except: continue

    if not client: return

    architect = ManhwaArchitect()
    try:
        curr_url = task['source_url']
        last_ch = float(task['last_chapter'])
        target_id = task['target_id']

        # حلقة الغزو المستمر (رفع 5 فصول متتالية سيدي)
        for mission_count in range(5):
            if not architect.bypass_cloudflare(curr_url): break

            images = architect.extract_precise_images()
            print(f"📸 فصل {last_ch + 1}: تم رصد {len(images)} هدف.")

            if not images: break

            supabase_update_task(task_id, {"status": "uploading"})
            file_ids = []
            
            # رفع الصور سيدي
            for i, img in enumerate(images, 1):
                try:
                    sent = await client.send_file(CHAT_ID, img, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                    if i % 10 == 0: print(f"🚀 تم رفع {i} صور...")
                except: continue

            if file_ids:
                new_ch = last_ch + 1
                payload = {"manhwa_id": int(target_id), "chapter_number": new_ch, "image_ids": file_ids, "is_premium": False}
                res = requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY}, timeout=60)
                
                if res.status_code == 200:
                    print(f"🏆 نصر ملكي! تم إنهاء الفصل {new_ch}")
                    last_ch = new_ch
                    next_url = architect.find_next_chapter()
                    
                    # تحديث سوبابيز سيدي للانتقال للفصل التالي
                    supabase_update_task(task_id, {
                        "last_chapter": new_ch,
                        "status": "idle",
                        "source_url": next_url if next_url else curr_url
                    })
                    
                    if next_url: curr_url = next_url
                    else: 
                        print("🏁 لا يوجد فصول تالية حالياً.")
                        break
                else: break
            else: break
            
    except Exception as e:
        print(f"🚨 خطأ ميداني: {e}")
    finally:
        if client: await client.disconnect()
        architect.page.quit()

if __name__ == "__main__":
    asyncio.run(start_royal_mission())