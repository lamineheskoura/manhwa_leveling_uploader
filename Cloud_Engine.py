# --- Professional Global Commenting Protocol: SOVEREIGN GHOST V6.0 (DRISSION-TECH) سيدي ---
import os, asyncio, requests, re, time
from DrissionPage import ChromiumPage, ChromiumOptions
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.utils import pack_bot_file_id

# --- ⚙️ الإعدادات الاستراتيجية سيدي ---
API_ID = 38020317
API_HASH = '941185ea933fd95a990e881fe50a6882'
CHAT_ID = -1003602777623
SITE_API_KEY = "KING_SECRET_KEY_99x"
SITE_API_URL = "https://manhwa-leveling.onrender.com/shadow-throne-99x/api/bulk-sync"

SB_URL = os.getenv("SB_URL")
SB_KEY = os.getenv("SB_KEY")
HEADERS = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}

BOT_TOKENS = [
    '8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA', 
    '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8', 
    '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE'
]

class SovereignGhost:
    def __init__(self):
        # إعداد المتصفح ليعمل كأنه متصفح شخصي سيدي
        self.co = ChromiumOptions()
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--disable-gpu')
        self.co.set_argument('--disable-dev-shm-usage')
        self.co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        self.co.headless(True) # وضع الشبح سيدي

    def extract_images(self, page):
        """استخراج دقيق للصور حتى المخفي منها سيدي"""
        links = []
        # البحث في الحاويات المشهورة
        selectors = '.reading-content img, .main-col img, .vung-doc img, .wp-manga-chapter-img img'
        imgs = page.eles(selectors)
        
        for img in imgs:
            src = img.attr('data-src') or img.attr('data-lazy-src') or img.attr('src')
            if src and 'http' in src and not any(x in src.lower() for x in ['logo', 'banner', 'staff', 'icon']):
                links.append(src)
        
        # إذا فشل، نستخدم البحث النصي العميق سيدي
        if not links:
            raw_html = page.html
            pattern = r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)'
            links = re.findall(pattern, raw_html)
            links = [l for l in links if not any(x in l.lower() for x in ['logo', 'icon', 'theme'])]
            
        return list(dict.fromkeys(links))

async def execute_mission(task, bot_index, ghost):
    token = BOT_TOKENS[bot_index]
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    # تشغيل صفحة مستقلة لكل بوت سيدي
    page = ChromiumPage(ghost.co)
    
    try:
        await client.start(bot_token=token)
        print(f"📡 الفارس {bot_index+1}: يتسلل إلى {task['source_url']}")
        
        page.get(task['source_url'])
        
        # 🛡️ التعامل مع بوابة التحقق (Wait & Click) سيدي
        page.wait(10) # انتظار ظهور البوابة
        
        # إذا وجدنا زر التحقق، ننقر عليه بمحاكاة بشرية سيدي
        human_btn = page.ele('@value=Verify you are human', timeout=5)
        if human_btn:
            print(f"🎯 تم رصد بوابة التحقق، جاري الاختراق...")
            human_btn.click()
            page.wait(10)

        # التمرير لتنشيط الصور سيدي
        page.scroll.to_bottom()
        page.wait(5)

        img_links = ghost.extract_images(page)
        
        if img_links:
            print(f"🔥 نصر مؤزر! وجدنا {len(img_links)} صورة سيدي.")
            file_ids = []
            for link in img_links:
                try:
                    sent = await client.send_file(CHAT_ID, link, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                except: continue

            if file_ids:
                # إبلاغ موقعك بالنتائج سيدي
                payload = {
                    "manhwa_id": int(task['target_id']),
                    "chapter_number": float(task['last_chapter']) + 1,
                    "image_ids": file_ids,
                    "is_premium": False
                }
                requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY})
                
                # تحديث المهمة في Supabase سيدي
                requests.patch(
                    f"{SB_URL}/rest/v1/manhwa_tasks?id=eq.{task['id']}", 
                    headers=HEADERS, 
                    json={"status": "idle", "last_chapter": float(task['last_chapter']) + 1}
                )
                print(f"✅ تم الانتهاء من الفصل بنجاح!")
        else:
            print(f"❌ الفارس {bot_index+1}: لم يجد صوراً. قد تكون البوابة صامدة.")
            
    except Exception as e:
        print(f"❌ خطأ فادح: {e}")
    finally:
        page.quit()
        await client.disconnect()

async def main():
    ghost = SovereignGhost()
    # جلب المهام سيدي
    try:
        r = requests.get(f"{SB_URL}/rest/v1/manhwa_tasks?status=eq.idle&limit=3", headers=HEADERS)
        tasks = r.json()
        if tasks:
            await asyncio.gather(*[execute_mission(task, i, ghost) for i, task in enumerate(tasks)])
        else:
            print("📭 لا توجد مهام حالياً سيدي.")
    except Exception as e:
        print(f"🚨 خطأ في الاتصال بـ Supabase: {e}")

if __name__ == "__main__":
    asyncio.run(main())
# --- نهاية بروتوكول التعليق العالمي المهني: SOVEREIGN GHOST V6.0 (DRISSION-TECH) سيدي ---