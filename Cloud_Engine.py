# --- Professional Global Commenting Protocol: ROYAL GHOST ENGINE V16.5 (Linux Armored) سيدي ---
import os
import asyncio
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.utils import pack_bot_file_id
# استدعاء الشاشة الوهمية سيدي
from pyvirtualdisplay import Display

# 🔐 الثوابت الملكية
API_ID = 38020317
API_HASH = '941185ea933fd95a990e881fe50a6882'
CHAT_ID = -1003602777623
SITE_API_KEY = "KING_SECRET_KEY_99x"
SITE_API_URL = "https://manhwa-leveling.onrender.com/shadow-throne-99x/api/bulk-sync"

# قائمة البوتات المدمجة للطوارئ
EMBEDDED_TOKENS = [
    '8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA',
    '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8',
    '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE'
]

SB_URL = (os.getenv("SB_URL") or "").strip().rstrip('/')
SB_KEY = (os.getenv("SB_KEY") or "").strip()
HEADERS = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}

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
        self.page = None
        self.co = ChromiumOptions()
        
        # 🛡️ إعدادات "الدرع المصفح" لبيئة Linux سيدي
        # هذه الأوامر ضرورية جداً لمنع انهيار كروم في السحاب
        self.co.set_argument('--no-sandbox') 
        self.co.set_argument('--disable-gpu')
        self.co.set_argument('--disable-dev-shm-usage') # حل مشكلة الذاكرة المشتركة
        self.co.set_argument('--disable-setuid-sandbox')
        self.co.set_argument('--window-size=1920,1080')
        self.co.set_argument('--start-maximized')
        
        # تضليل الحماية
        self.co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        
        # تعيين منفذ تلقائي لتجنب تعارض 9222
        self.co.auto_port()

        try:
            print("🔧 جاري تشغيل المتصفح مع إعدادات Linux المصفحة...")
            self.page = ChromiumPage(self.co)
            print("✅ تم إقلاع المتصفح بنجاح!")
        except Exception as e:
            print(f"⚠️ فشل أولي، جاري المحاولة بوضع Headless الجديد... الخطأ: {e}")
            # خطة بديلة: العودة لوضع headless=new إذا فشلت الشاشة الوهمية
            try:
                self.co.set_argument('--headless=new')
                self.page = ChromiumPage(self.co)
                print("✅ تم الإقلاع بوضع Headless New.")
            except Exception as e2:
                print(f"🔥 فشل نهائي في تشغيل المتصفح: {e2}")
                self.page = None

    def bypass_and_extract(self, url):
        if not self.page:
            print("❌ لا يوجد متصفح يعمل سيدي!")
            return []

        print(f"🕵️ الهجوم على: {url}")
        self.page.get(url)
        
        # انتظار ذكي
        for i in range(15):
            if "Just a moment" not in self.page.title and "Cloudflare" not in self.page.title:
                print("✅ تم خداع الحماية! نحن في الداخل.")
                break
            time.sleep(2)
        
        # التمرير لإظهار الصور
        self.page.scroll.to_bottom()
        time.sleep(3)
        self.page.scroll.up(500)
        time.sleep(2)

        links = []
        selectors = ['img[src*="http"]', '.reading-content img', '.main-col img', 'div img']
        
        for s in selectors:
            imgs = self.page.eles(s)
            for img in imgs:
                src = img.attr('src') or img.attr('data-src') or img.attr('data-lazy-src')
                if src and src.startswith('http') and not any(x in src.lower() for x in ['logo', 'banner', 'avatar', 'icon', 'facebook', 'twitter']):
                    links.append(src)
        
        return list(dict.fromkeys(links))

    def quit(self):
        if self.page:
            self.page.quit()

async def start_royal_mission():
    # 📺 تشغيل الشاشة الوهمية (Virtual Display)
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    print("🖥️ تم تفعيل الشاشة الشبحية بنجاح.")

    tasks = supabase_get_task()
    if not tasks: 
        print("📭 لا مهام.")
        display.stop()
        return
    
    task = tasks[0]
    task_id = task['id']
    print(f"⚔️ الهدف: {task['name']}")

    raw_tokens = os.getenv("BOT_TOKENS") or ""
    all_tokens = [t.strip() for t in raw_tokens.split(',') if t.strip()]
    if not all_tokens: all_tokens = EMBEDDED_TOKENS
    
    client = None
    for token in all_tokens:
        try:
            temp_client = TelegramClient(MemorySession(), API_ID, API_HASH)
            await temp_client.start(bot_token=token)
            client = temp_client
            print(f"✅ تم الاتصال بالبوت: {token[:5]}...")
            break
        except: continue

    if not client: 
        print("🚨 فشل الاتصال بجميع البوتات.")
        display.stop()
        return

    architect = ManhwaArchitect()
    try:
        curr_url = task['source_url']
        last_ch = float(task['last_chapter'])
        target_id = task['target_id']

        # جلب الصور
        images = architect.bypass_and_extract(curr_url)
        print(f"📸 تم سحب {len(images)} صورة.")

        if images:
            supabase_update_task(task_id, {"status": "uploading"})
            file_ids = []
            for img in images:
                try:
                    sent = await client.send_file(CHAT_ID, img, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                    await asyncio.sleep(0.5)
                except: continue

            if file_ids:
                new_ch = last_ch + 1
                payload = {"manhwa_id": int(target_id), "chapter_number": new_ch, "image_ids": file_ids, "is_premium": False}
                requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY}, timeout=60)
                
                # الحصول على الرابط التالي
                next_url = None
                try:
                    if architect.page:
                        next_ele = architect.page.ele('text:Next') or architect.page.ele('.next_page')
                        if next_ele: next_url = next_ele.attr('href')
                except: pass

                supabase_update_task(task_id, {
                    "last_chapter": new_ch, 
                    "status": "idle",
                    "source_url": next_url if next_url else curr_url
                })
                print(f"✅ تمت المهمة! الفصل {new_ch}")
            else:
                supabase_update_task(task_id, {"status": "error"})
        else:
            print("⚠️ لم يتم العثور على صور.")
            supabase_update_task(task_id, {"status": "error"})

    except Exception as e:
        print(f"🔥 خطأ: {e}")
        supabase_update_task(task_id, {"status": "error"})
    finally:
        if client: await client.disconnect()
        if architect: architect.quit()
        display.stop() # إغلاق الشاشة الشبحية

if __name__ == "__main__":
    asyncio.run(start_royal_mission())