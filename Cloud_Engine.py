# --- Professional Global Commenting Protocol: ROYAL CLOUD ENGINE V8.9 سيدي ---
import os
import asyncio
import re
import requests
import time
import random
from DrissionPage import ChromiumPage, ChromiumOptions
from telethon import TelegramClient
from telethon.utils import pack_bot_file_id
from telethon.errors import FloodWaitError

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

# --- المحرك المطور بمنطق المهندس سيدي ---

class RoyalScraper:
    def __init__(self):
        self.co = ChromiumOptions()
        self.co.set_argument('--headless')
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--disable-gpu')
        self.co.set_argument('--disable-blink-features=AutomationControlled')
        self.page = ChromiumPage(self.co)

    def extract_precise_images(self):
        """استخراج الصور بدقة المهندس سيدي"""
        links = []
        # قائمة الحاويات الشهيرة في مواقع المانهوا سيدي
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
        
        # بروتوكول الطوارئ: البحث في كامل الـ HTML سيدي
        if not links:
            all_html_links = re.findall(r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)', self.page.html)
            links = [l for l in all_html_links if not any(x in l.lower() for x in ['logo', 'icon', 'theme', 'avatar'])]

        return list(dict.fromkeys(links))

    def get_data(self, url):
        try:
            self.page.get(url)
            self.page.scroll.to_bottom()
            time.sleep(2)
            
            valid_links = self.extract_precise_images()
            
            # إيجاد الفصل التالي سيدي
            next_url = None
            selectors = ['.next_page', 'a.next_page', 'a[rel="next"]', '.nav-next a', '.next-post', '.ch-next-btn']
            for s in selectors:
                btn = self.page.ele(s, timeout=1)
                if btn and btn.link and btn.link != self.page.url:
                    next_url = btn.link
                    break
            
            if not next_url:
                all_links = self.page.eles('tag:a')
                for link in all_links:
                    text = link.text.lower()
                    if any(x in text for x in ['next', 'التالي', 'الفصل التالي']):
                        if link.link and link.link != self.page.url:
                            next_url = link.link
                            break

            return valid_links, next_url
        except Exception as e:
            print(f"🔥 Error during extraction: {e}")
            return [], None

async def start_royal_mission():
    tasks = supabase_get_task()
    if not tasks:
        print("📭 لا توجد مهام حالياً سيدي.")
        return
    
    task = tasks[0]
    task_id = task['id']
    
    print(f"🚀 تم اختراق الهدف: {task['name']} سيدي.")
    supabase_update_task(task_id, {"status": "downloading"})
    
    scraper = RoyalScraper()
    all_tokens = os.getenv("BOT_TOKENS").split(',')
    bot_index = task_id % len(all_tokens)
    
    client = TelegramClient(f'sess_{task_id}', int(os.getenv("TG_API_ID")), os.getenv("TG_API_HASH"))
    await client.start(bot_token=all_tokens[bot_index].strip())

    curr_url = task['source_url']
    last_ch = float(task['last_chapter'])
    target_id = task['target_id']

    try:
        for _ in range(5): 
            images, next_url = scraper.get_data(curr_url)
            if not images: break

            supabase_update_task(task_id, {"status": "uploading"})
            
            file_ids = []
            for img in images:
                try:
                    sent = await client.send_file(int(os.getenv("TG_CHAT_ID")), img, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                    await asyncio.sleep(0.8) # سرعة المهندس سيدي
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
                    last_ch = new_ch
                    print(f"✅ الفصل {new_ch} تم رفعه بنجاح سيدي!")
                    supabase_update_task(task_id, {
                        "last_chapter": new_ch,
                        "source_url": next_url if next_url else curr_url,
                        "status": "idle"
                    })
                    if next_url: curr_url = next_url
                    else: break
                else: break
            else: break
            
    except Exception as e:
        print(f"❌ تعطلت العملية سيدي: {e}")
        supabase_update_task(task_id, {"status": "error"})
    finally:
        await client.disconnect()
        scraper.page.quit()

if __name__ == "__main__":
    asyncio.run(start_royal_mission())