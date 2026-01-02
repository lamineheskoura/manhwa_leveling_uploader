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
    
    supabase_update_task(task_id, {"status": "downloading"})
    
    architect = ManhwaArchitect()
    all_tokens = os.getenv("BOT_TOKENS").split(',')
    bot_index = task_id % len(all_tokens)
    
    client = TelegramClient(f'sess_{task_id}', int(os.getenv("TG_API_ID")), os.getenv("TG_API_HASH"))
    await client.start(bot_token=all_tokens[bot_index].strip())

    curr_url = task['source_url']
    last_ch = float(task['last_chapter'])
    target_id = task['target_id']

    try:
        # معالجة الفصول سيدي (بحد أقصى 5 فصول في الدورة الواحدة)
        for _ in range(5): 
            architect.page.get(curr_url)
            architect.page.scroll.to_bottom()
            time.sleep(2)
            
            images = architect.extract_precise_images()
            next_url = architect.find_next()

            if not images:
                print(f"⚠️ لم يتم العثور على صور في: {curr_url}")
                break

            supabase_update_task(task_id, {"status": "uploading"})
            
            file_ids = []
            for img in images:
                try:
                    sent = await client.send_file(int(os.getenv("TG_CHAT_ID")), img, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                    await asyncio.sleep(1) # تأخير لضمان استقرار التليجرام سيدي
                except: continue

            if file_ids:
                new_ch = last_ch + 1
                payload = {
                    "manhwa_id": int(target_id),
                    "chapter_number": new_ch,
                    "image_ids": file_ids,
                    "bot_index": bot_index
                }
                
                r = requests.post(os.getenv("SITE_API_URL"), json=payload, 
                                 headers={"X-API-KEY": os.getenv("SITE_API_KEY")}, timeout=60)
                
                if r.status_code == 200:
                    print(f"✅ تم غزو الفصل {new_ch} بنجاح سيدي!")
                    last_ch = new_ch
                    supabase_update_task(task_id, {
                        "last_chapter": new_ch,
                        "source_url": next_url if next_url else curr_url,
                        "status": "idle"
                    })
                    if next_url: curr_url = next_url
                    else: break
                else: 
                    print(f"❌ فشل إرسال الفصل لـ Render: {r.status_code}")
                    break
            else: break
            
    except Exception as e:
        print(f"🔥 خطأ فادح: {e} سيدي.")
        supabase_update_task(task_id, {"status": "error"})
    finally:
        await client.disconnect()
        architect.page.quit()

if __name__ == "__main__":
    asyncio.run(start_royal_mission())