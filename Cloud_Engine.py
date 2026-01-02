# --- Professional Global Commenting Protocol: ROYAL OLYMPUS ENGINE V24.0 (Final Armored) سيدي ---
import os
import asyncio
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.utils import pack_bot_file_id
from pyvirtualdisplay import Display

# 🔐 الثوابت الملكية (تُسحب من Secrets في GitHub)
API_ID = 38020317
API_HASH = '941185ea933fd95a990e881fe50a6882'
CHAT_ID = -1003602777623
SITE_API_KEY = "KING_SECRET_KEY_99x"
SITE_API_URL = "https://manhwa-leveling.onrender.com/shadow-throne-99x/api/bulk-sync"

# 💉 مفاتيح العبور (مدمجة مباشرة كما طلبت سيدي)
ROYAL_COOKIES = "XSRF-TOKEN=eyJpdiI6ImVaOWNneTVaZTJPMlVQRGtBT3poakE9PSIsInZhbHVlIjoiRk9xK3hTUmhkV1QrWUFOY0Ntak1RSW91Vng1Q1E4d1VIZjJGam84OGsvMHMwK1Z1RDJjYnZka3ZhaUk0NXA0VytrYzJsWEdtOHRFTDlIVzRWamU2MnRDZDRWSTNESDlxV1QyM3ExTFRlYXJmb3g4V1c0c0tGdUpYYkNDNlNNL2YiLCJtYWMiOiI1NWYwNGQ5YmY5NjA2ZjJiMzUyZjIzOWIyYmQ2MDg5ZmY5YzIxNzcwYTNhNmI3ZDhhMmI5ZWYyZjBjMGI1ZGU1IiwidGFnIjoiIn0%3D; team_x_session=eyJpdiI6IjdkTEdzRWxjaVJkRWxaVWRoZ01KZEE9PSIsInZhbHVlIjoiS2taV3hXZHh0RDJOTkZURjhqNGJ5clNnZ25yNnRDYXZGeWRjU2hWMmFxeS8rN3krQlQ3K1F4bFQvWTFQbWVBbytZaXdrazlDQ25sTXg1R2pSdk44aXRvTTQvdGRtR1B4elB0Z2FocnErZ3huYW45Szl2czdVaVpEc2U4UHBmek4iLCJtYWMiOiI0NDBlMjU1Yjc1NDYxZTE3Mzk0ZTdhMjQ4NTkxZmRlMGRjNzI3Mjg0Y2M3NTNmYzU4ODZlNTZkYjUxZjUyN2M2IiwidGFnIjoiIn0%3D"

# جلب بيانات Supabase من البيئة سيدي كما فعلنا سابقاً
SB_URL = (os.getenv("SB_URL") or "").strip().rstrip('/')
SB_KEY = (os.getenv("SB_KEY") or "").strip()
HEADERS = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}

EMBEDDED_TOKENS = [
    '8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA',
    '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8',
    '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE'
]

# --- دوال التحكم في قاعدة البيانات ---

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

# --- المهندس المعماري المصفح سيدي ---

class ManhwaArchitect:
    def __init__(self):
        self.page = None
        self.co = ChromiumOptions()
        self.co.set_argument('--no-sandbox') 
        self.co.set_argument('--disable-gpu')
        self.co.set_argument('--disable-dev-shm-usage')
        self.co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        self.co.auto_port()

        try:
            self.page = ChromiumPage(self.co)
            print("✅ محرك التصفح جاهز.")
        except: self.page = None

    def inject_identity(self):
        """حقن مفتاح العبور لتجاوز الكلود فاير سيدي"""
        if not self.page: return
        domain = "olympustaff.com"
        self.page.get(f"https://{domain}")
        time.sleep(3)
        
        # تفكيك الكوكيز وحقنها سيدي
        pairs = ROYAL_COOKIES.split('; ')
        for pair in pairs:
            if '=' in pair:
                name, value = pair.split('=', 1)
                self.page.set.cookies({'name': name.strip(), 'value': value.strip(), 'domain': domain})
        
        self.page.refresh()
        print("💉 تم حقن الهوية الملكية.")
        time.sleep(5)

    def extract_images(self, url):
        if not self.page: return []
        self.inject_identity()
        
        print(f"🕵️ الهجوم على الرابط: {url}")
        self.page.get(url)
        
        # الانتظار والتمرير سيدي
        self.page.scroll.to_bottom()
        time.sleep(4)
        
        links = []
        for img in self.page.eles('tag:img'):
            src = img.attr('src') or img.attr('data-src') or img.attr('data-lazy-src')
            if src and 'http' in src and not any(x in src.lower() for x in ['logo', 'banner', 'avatar', 'loader']):
                links.append(src)
        
        return list(dict.fromkeys(links))

    def quit(self):
        if self.page: self.page.quit()

# --- محرك المهمة والرفع سيدي ---

async def start_royal_mission():
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    
    tasks = supabase_get_task()
    if not tasks:
        print("📭 لا يوجد مهام حالياً سيدي.")
        display.stop()
        return
    
    task = tasks[0]
    task_id, target_id = task['id'], task['target_id']
    curr_url, last_ch = task['source_url'], float(task['last_chapter'])
    
    print(f"⚔️ الهدف المكتشف: {task['name']}")

    # الاتصال بتلجرام سيدي
    client = None
    raw_tokens = os.getenv("BOT_TOKENS") or ""
    all_tokens = [t.strip() for t in raw_tokens.split(',') if t.strip()]
    if not all_tokens: all_tokens = EMBEDDED_TOKENS
    
    for token in all_tokens:
        try:
            c = TelegramClient(MemorySession(), API_ID, API_HASH)
            await c.start(bot_token=token)
            client = c
            print(f"✅ متصل بالبوت: {token[:10]}...")
            break
        except: continue

    if not client:
        display.stop()
        return

    architect = ManhwaArchitect()
    try:
        images = architect.extract_images(curr_url)
        
        if images:
            print(f"📸 تم سحب {len(images)} صورة. جاري الرفع لتلجرام سيدي...")
            supabase_update_task(task_id, {"status": "uploading"})
            
            file_ids = []
            for img in images:
                try:
                    sent = await client.send_file(CHAT_ID, img, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                    await asyncio.sleep(0.3)
                except: continue

            if file_ids:
                new_ch = last_ch + 1
                # إرسال البيانات لموقعك سيدي
                payload = {"manhwa_id": int(target_id), "chapter_number": new_ch, "image_ids": file_ids, "is_premium": False}
                requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY}, timeout=60)
                
                # تحديث قاعدة البيانات
                next_url = None
                try:
                    next_btn = architect.page.ele('text:Next') or architect.page.ele('.next_page')
                    if next_btn: next_url = next_btn.attr('href')
                except: pass

                supabase_update_task(task_id, {
                    "last_chapter": new_ch,
                    "status": "idle",
                    "source_url": next_url if next_url else curr_url
                })
                print(f"🏆 تمت المهمة بنجاح! الفصل {new_ch}")
            else:
                supabase_update_task(task_id, {"status": "error"})
        else:
            print("⚠️ الصور لم تظهر. تأكد من تجديد الكوكيز سيدي.")
            supabase_update_task(task_id, {"status": "error"})

    except Exception as e:
        print(f"🔥 خطأ: {e}")
        supabase_update_task(task_id, {"status": "error"})
    finally:
        await client.disconnect()
        architect.quit()
        display.stop()

if __name__ == "__main__":
    asyncio.run(start_royal_mission())