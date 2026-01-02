# --- Professional Global Commenting Protocol: ROYAL CLOUD ENGINE V9.0 سيدي ---
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
    "Content-Type": "application/json",
    "Prefer": "return=representation"
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

# --- منطق المهندس V15.0 الموحد سيدي ---

class ManhwaArchitect:
    def __init__(self):
        self.co = ChromiumOptions()
        self.co.set_argument('--headless')
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--disable-gpu')
        self.co.set_argument('--disable-blink-features=AutomationControlled')
        self.page = ChromiumPage(self.co)

    def extract_precise_images(self):
        """استخراج الصور بدقة المهندس V15.0 سيدي"""
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

    def find_next(self):
        """نظام البحث عن الفصل التالي (Architect Logic) سيدي"""
        selectors = ['.next_page', 'a.next_page', 'a[rel="next"]', '.nav-next a', '.next-post']
        for s in selectors:
            btn = self.page.ele(s, timeout=1)
            if btn and btn.link and btn.link != self.page.url:
                return btn.link

        all_links = self.page.eles('tag:a')
        for link in all_links:
            text = link.text.lower()
            if ('next' in text) or ('التالي' in text) or ('الفصل التالي' in text):
                if link.link and link.link != self.page.url:
                    return link.link
        return None

# --- محرك التنفيذ السحابي سيدي ---

async def start_royal_mission():
    tasks = supabase_get_task()
    if not tasks:
        print("📭 لا توجد مهام حالياً سيدي.")
        return
    
    task = tasks[0]
    task_id = task['id']
    print(f"⚔️ بروتوكول المهندس V15.0 مفعل للهدف: {task['name']} سيدي.")
    
    architect = ManhwaArchitect()
    # زيادة وقت الانتظار الافتراضي للمتصفح سيدي لضمان استقرار السحاب
    architect.page.set.timeouts(20) 
    
    all_tokens = os.getenv("BOT_TOKENS").split(',')
    bot_index = task_id % len(all_tokens)
    
    client = TelegramClient(f'sess_{task_id}', int(os.getenv("TG_API_ID")), os.getenv("TG_API_HASH"))
    
    try:
        await client.start(bot_token=all_tokens[bot_index].strip())
        print("📡 تم تسجيل دخول البوت بنجاح سيدي.")

        curr_url = task['source_url']
        last_ch = float(task['last_chapter'])
        target_id = task['target_id']

        for _ in range(5): 
            print(f"🌐 جاري الدخول إلى الرابط: {curr_url}")
            architect.page.get(curr_url)
            
            # محاكاة حركة بشرية سيدي لضمان تحميل الصور
            architect.page.scroll.down(2000)
            time.sleep(5) # وقت إضافي للسحاب
            architect.page.scroll.to_bottom()
            time.sleep(2)

            images = architect.extract_precise_images()
            print(f"📸 نتيجة البحث عن الصور: تم العثور على ({len(images)}) صورة سيدي.")

            if not images:
                print(f"⚠️ تحذير: لم يتم العثور على أي صور! قد يكون الموقع حجب السحاب أو الصفحة لم تكتمل.")
                # طباعة عنوان الصفحة للتأكد مما يراه المتصفح سيدي
                print(f"📄 عنوان الصفحة الحالي: {architect.page.title}")
                break

            print(f"📦 بدء رفع الفصل {last_ch + 1} إلى تلجرام...")
            file_ids = []
            for i, img in enumerate(images, 1):
                try:
                    sent = await client.send_file(int(os.getenv("TG_CHAT_ID")), img, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                    if i % 10 == 0: print(f"🚀 تم رفع {i} صورة...")
                except Exception as upload_err:
                    print(f"❌ خطأ في رفع الصورة {i}: {upload_err}")
                    continue

            if file_ids:
                # منطق الـ POST والـ PATCH (كما هو)
                print(f"✅ تم إنهاء رفع الفصل {last_ch + 1} بنجاح سيدي!")
                # ... (بقية الكود الخاص بالتحديث) ...
            else:
                print("❌ لم يتم رفع أي ملفات بنجاح، توقف العملية.")
                break
                
    except Exception as e:
        print(f"🔥 خطأ فادح غير متوقع: {e} سيدي.")
    finally:
        await client.disconnect()
        architect.page.quit()
if __name__ == "__main__":
    asyncio.run(start_royal_mission())