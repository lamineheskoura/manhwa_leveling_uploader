# --- Professional Global Commenting Protocol: ROYAL CLOUD ENGINE V8.5 سيدي ---
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
from supabase import create_client

# 🔐 الاتصال بالقوى العظمى عبر الأسرار سيدي
supabase = create_client(os.getenv("SB_URL"), os.getenv("SB_KEY"))

class RoyalScraper:
    def __init__(self):
        # إعدادات الشبح لتجاوز حماية المواقع سيدي
        self.co = ChromiumOptions()
        self.co.set_argument('--headless')
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--disable-gpu')
        self.co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        self.page = ChromiumPage(self.co)

    def js_infiltration(self, html):
        """استخراج الروابط المخفية في حال فشل الـ HTML سيدي"""
        found = re.findall(r'(https?://[^\s"\'<>]+(?:\.jpg|\.png|\.jpeg|\.webp))', html, re.IGNORECASE)
        return list(dict.fromkeys(found))

    def get_data(self, url):
        """المناورة وسحب البيانات سيدي"""
        try:
            self.page.get(url)
            # محاكاة التصفح البشري لتجاوز كلودفلار
            for _ in range(2):
                self.page.scroll.down(800)
                time.sleep(random.uniform(1, 2))
            
            links = []
            imgs = self.page.eles('tag:img')
            for img in imgs:
                src = img.attr('data-src') or img.attr('data-lazy-src') or img.attr('src')
                if src and not any(x in src.lower() for x in ['logo', 'banner', 'avatar']):
                    links.append(src)

            # 🛡️ تطبيق بروتوكول كاشف الفخاخ سيدي
            unique_links = list(dict.fromkeys(links))
            if len(links) > 5 and len(unique_links) < 3:
                unique_links = self.js_infiltration(self.page.html)
            
            if not unique_links:
                unique_links = self.js_infiltration(self.page.html)

            # 🧭 إيجاد الفصل التالي
            next_url = None
            for s in ['a.next_page', 'a[rel="next"]', '.nav-next a', '.ch-next-btn']:
                btn = self.page.ele(s, timeout=2)
                if btn and btn.link: 
                    next_url = btn.link
                    break

            return unique_links, next_url
        except: return [], None

async def safe_telegram_upload(client, chat_id, img_url):
    """الرفع مع بروتوكول مقاومة الحظر سيدي"""
    try:
        sent = await client.send_file(chat_id, img_url, force_document=True)
        await asyncio.sleep(random.uniform(0.7, 1.5)) # تأخير وقائي
        return str(pack_bot_file_id(sent.media.document))
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds + 5)
        return await safe_telegram_upload(client, chat_id, img_url)
    except: return None

async def start_royal_mission():
    # 🎯 سحب المهمة بناءً على الأعلى أولوية (Priority DESC) سيدي
    res = supabase.table("manhwa_tasks").select("*")\
        .eq("status", "idle")\
        .order("priority", desc=True)\
        .limit(1).execute()
    
    if not res.data: return
    task = res.data[0]
    
    # تحديث الحالة فوراً لمنع التكرار سيدي
    supabase.table("manhwa_tasks").update({"status": "downloading"}).eq("id", task['id']).execute()
    
    scraper = RoyalScraper()
    all_tokens = os.getenv("BOT_TOKENS").split(',')
    bot_index = task['id'] % len(all_tokens)
    
    client = TelegramClient(f'sess_{task["id"]}', int(os.getenv("TG_API_ID")), os.getenv("TG_API_HASH"))
    await client.start(bot_token=all_tokens[bot_index])

    curr_url = task['source_url']
    last_ch = float(task['last_chapter'])
    target_id = task['target_id']

    try:
        for _ in range(5): # معالجة 5 فصول
            images, next_url = scraper.get_data(curr_url)
            if not images: break

            supabase.table("manhwa_tasks").update({"status": "uploading"}).eq("id", task['id']).execute()
            
            file_ids = []
            for img in images:
                f_id = await safe_telegram_upload(client, int(os.getenv("TG_CHAT_ID")), img)
                if f_id: file_ids.append(f_id)

            if file_ids:
                new_ch = last_ch + 1
                # 📤 المزامنة مع رندر سيدي
                payload = {
                    "manhwa_id": int(target_id),
                    "chapter_number": new_ch,
                    "image_ids": file_ids,
                    "bot_index": bot_index,
                    "is_premium": False
                }
                
                r = requests.post(os.getenv("SITE_API_URL"), json=payload, 
                                 headers={"X-API-KEY": os.getenv("SITE_API_KEY")}, timeout=60)
                
                if r.status_code == 200:
                    last_ch = new_ch
                    # التزام كامل بالأعمدة المتوفرة سيدي
                    supabase.table("manhwa_tasks").update({
                        "last_chapter": new_ch,
                        "source_url": next_url if next_url else curr_url,
                        "status": "idle"
                    }).eq("id", task['id']).execute()
                    
                    if next_url: curr_url = next_url
                    else: break
                else: break
            else: break
    except Exception as e:
        supabase.table("manhwa_tasks").update({"status": "error"}).eq("id", task['id']).execute()
    finally:
        await client.disconnect()
        scraper.page.quit()

if __name__ == "__main__":
    asyncio.run(start_royal_mission())