# --- Professional Global Commenting Protocol: ROYAL CLOUD ENGINE V10.0 (GHOST) سيدي ---
import os
import asyncio
import re
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from telethon import TelegramClient
from telethon.utils import pack_bot_file_id

# 🔐 إعدادات الاتصال المباشر سيدي
SB_URL = (os.getenv("SB_URL") or "").strip().rstrip('/')
SB_KEY = (os.getenv("SB_KEY") or "").strip()
HEADERS = {
    "apikey": SB_KEY,
    "Authorization": f"Bearer {SB_KEY}",
    "Content-Type": "application/json"
}

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

# --- منطق المهندس V15.0 المطور للتسلل سيدي ---

class ManhwaArchitect:
    def __init__(self):
        self.co = ChromiumOptions()
        self.co.set_argument('--headless')
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--disable-gpu')
        self.co.set_argument('--disable-dev-shm-usage')
        # 🕵️ تقنيات التخفي سيدي
        self.co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        self.co.set_argument('--disable-blink-features=AutomationControlled')
        
        self.page = ChromiumPage(self.co)

    def bypass_cloudflare(self):
        """بروتوكول اختراق درع Cloudflare سيدي"""
        print("🛡️ جاري فحص وجود درع حماية...")
        for i in range(1, 16):  # محاولات لمدة 30 ثانية
            title = self.page.title
            if "Just a moment" not in title and "Cloudflare" not in title:
                print(f"✅ تم تجاوز الدرع بنجاح في المحاولة {i} سيدي!")
                return True
            print(f"⏳ الدرع لا يزال نشطاً (المحاولة {i})...")
            # محاكاة حركة الماوس أو التمرير الطفيف سيدي لفك الحظر
            self.page.scroll.down(100)
            time.sleep(2)
        return False

    def extract_precise_images(self):
        links = []
        containers = ['.reading-content', '.main-col', '#chapter-video-frame', '.vung-doc', '.reader-area', '.wp-manga-chapter-img']
        
        target_container = None
        for selector in containers:
            if self.page.ele(selector):
                target_container = self.page.ele(selector)
                break

        if target_container:
            imgs = target_container.eles('tag:img')
            for img in imgs:
                src = img.attr('data-src') or img.attr('data-lazy-src') or img.attr('src')
                if src and not any(x in src.lower() for x in ['logo', 'banner', 'avatar', 'icon']):
                    links.append(src)
        
        if not links:
            all_html_links = re.findall(r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)', self.page.html)
            links = [l for l in all_html_links if not any(x in l.lower() for x in ['logo', 'icon', 'theme', 'avatar'])]

        return list(dict.fromkeys(links))

# --- محرك التنفيذ السحابي المطور سيدي ---

async def start_royal_mission():
    tasks = supabase_get_task()
    if not tasks: return

    task = tasks[0]
    task_id = task['id']
    print(f"⚔️ بروتوكول GHOST V10.0 مفعل للهدف: {task['name']} سيدي.")
    
    architect = ManhwaArchitect()
    architect.page.set.timeouts(30)
    
    all_tokens = os.getenv("BOT_TOKENS").split(',')
    token = all_tokens[task_id % len(all_tokens)].strip()
    
    client = TelegramClient(f'sess_{task_id}', int(os.getenv("TG_API_ID")), os.getenv("TG_API_HASH"))
    
    try:
        await client.start(bot_token=token)
        curr_url = task['source_url']
        last_ch = float(task['last_chapter'])

        for _ in range(5): 
            print(f"🌐 الهجوم على: {curr_url}")
            architect.page.get(curr_url)
            
            if not architect.bypass_cloudflare():
                print("❌ فشل اختراق الدرع هذه المرة سيدي. الصفحة عالقة.")
                break

            # 📄 النزول التدريجي لتحفيز التحميل سيدي
            architect.page.scroll.down(2500)
            time.sleep(4)
            
            images = architect.extract_precise_images()
            print(f"📸 الصور المكتشفة: ({len(images)}) صورة سيدي.")

            if not images: break

            supabase_update_task(task_id, {"status": "uploading"})
            file_ids = []
            for img in images:
                try:
                    sent = await client.send_file(int(os.getenv("TG_CHAT_ID")), img, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                    await asyncio.sleep(0.8)
                except: continue

            if file_ids:
                new_ch = last_ch + 1
                # (هنا يوضع كود إرسال البيانات لموقعك سيدي كما في النسخة السابقة)
                print(f"✅ الفصل {new_ch} في قبضتنا سيدي!")
                last_ch = new_ch
                # الانتقال للفصل التالي
                next_btn = architect.page.ele('.next_page') # مثال
                if next_btn and next_btn.link: curr_url = next_btn.link
                else: break
            else: break
                
    except Exception as e:
        print(f"🔥 انفجار في النظام: {e} سيدي.")
    finally:
        await client.disconnect()
        architect.page.quit()

if __name__ == "__main__":
    asyncio.run(start_royal_mission())