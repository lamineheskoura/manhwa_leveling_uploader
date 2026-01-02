# --- Professional Global Commenting Protocol: ROYAL CLOUD ENGINE V8.6 سيدي ---
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

# 🔐 إعدادات الاتصال المباشر سيدي - تجاوزنا المكتبة العقيمة
SB_URL = (os.getenv("SB_URL") or "").strip().rstrip('/')
SB_KEY = (os.getenv("SB_KEY") or "").strip()
HEADERS = {
    "apikey": SB_KEY,
    "Authorization": f"Bearer {SB_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- دالات المناورة المباشرة سيدي (Supabase Direct Helpers) ---

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

# --- محرك السحب الملكي سيدي ---

class RoyalScraper:
    def __init__(self):
        self.co = ChromiumOptions()
        self.co.set_argument('--headless')
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--disable-gpu')
        self.page = ChromiumPage(self.co)

    def get_data(self, url):
        try:
            self.page.get(url)
            time.sleep(3) # انتظار التحميل سيدي
            
            links = []
            imgs = self.page.eles('tag:img')
            for img in imgs:
                src = img.attr('data-src') or img.attr('data-lazy-src') or img.attr('src')
                if src and "http" in src:
                    links.append(src)

            unique_links = list(dict.fromkeys(links))
            
            next_url = None
            for s in ['a.next_page', 'a[rel="next"]', '.nav-next a', '.ch-next-btn']:
                btn = self.page.ele(s, timeout=2)
                if btn and btn.link: 
                    next_url = btn.link
                    break

            return unique_links, next_url
        except: return [], None

async def start_royal_mission():
    # 🎯 سحب المهمة سيدي
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
    await client.start(bot_token=all_tokens[bot_index])

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
                    await asyncio.sleep(1)
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
        print(f"❌ تعطلت العملية: {e} سيدي.")
        supabase_update_task(task_id, {"status": "error"})
    finally:
        await client.disconnect()
        scraper.page.quit()

if __name__ == "__main__":
    asyncio.run(start_royal_mission())