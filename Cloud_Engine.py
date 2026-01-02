# --- Professional Global Commenting Protocol: ROYAL GHOST ENGINE V11.5 (Armored) سيدي ---
import os
import asyncio
import re
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from telethon import TelegramClient
from telethon.utils import pack_bot_file_id

# 🔐 الثوابت الملكية المستخرجة سيدي
API_ID = 38020317
API_HASH = '941185ea933fd95a990e881fe50a6882'
CHAT_ID = -1003602777623
SITE_API_KEY = "KING_SECRET_KEY_99x"
SITE_API_URL = "https://manhwa-leveling.onrender.com/shadow-throne-99x/api/bulk-sync"

# 🤖 فيلق البوتات الاحتياطي سيدي
EMBEDDED_TOKENS = [
    '8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA',
    '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8',
    '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE'
]

# 🗄️ إعدادات سوبابيز سيدي
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
        self.co = ChromiumOptions()
        self.co.set_argument('--headless')
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--disable-gpu')
        self.co.set_argument('--incognito') # 🕵️ وضع التخفي سيدي
        self.co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        self.co.set_argument('--disable-blink-features=AutomationControlled')
        self.page = ChromiumPage(self.co)

    def bypass_cloudflare(self, url):
        """بروتوكول الاختراق المتقدم سيدي"""
        print(f"📡 محاولة كسر التشفير للرابط...")
        
        # الخطوة 1: محاولة زيارة الدومين الرئيسي أولاً لزرع الكوكيز
        domain = "/".join(url.split("/")[:3])
        self.page.get(domain)
        time.sleep(3)
        
        # الخطوة 2: الدخول للرابط المستهدف
        self.page.get(url)
        
        for i in range(1, 15): # زيادة المهلة لـ 45 ثانية
            title = self.page.title
            # التحقق من وجود عناصر المانجا فعلياً وليس فقط العنوان
            if self.page.ele('.reading-content') or self.page.ele('tag:img'):
                print(f"✅ تم اختراق الدرع بنجاح سيدي في المحاولة {i}!")
                return True
            
            # محاولة النقر في وسط الشاشة سيدي ربما يوجد زر "إكمال" مخفي
            try: self.page.actions.click()
            except: pass
            
            print(f"⏳ الدرع لا يزال صامداً (المحاولة {i})... العنوان الحالي: {title}")
            time.sleep(3)
        return False



    def extract_images(self):
        """استخراج الصور بدقة المهندس سيدي"""
        links = []
        selectors = ['.reading-content img', '.wp-manga-chapter-img img', '.reader-area img', '.main-col img', '.vung-doc img']
        for s in selectors:
            imgs = self.page.eles(s)
            for img in imgs:
                src = img.attr('data-src') or img.attr('data-lazy-src') or img.attr('src')
                if src and not any(x in src.lower() for x in ['logo', 'banner', 'avatar']):
                    links.append(src)
        return list(dict.fromkeys(links))

async def start_royal_mission():
    tasks = supabase_get_task()
    if not tasks: 
        print("📭 لا توجد مهام جديدة سيدي.")
        return
    
    task = tasks[0]
    task_id = task['id']
    print(f"⚔️ انطلاق المهمة الملكية للهدف: {task['name']} سيدي.")

    # 🤖 نظام جلب التوكنات سيدي (الأولوية لـ Secrets ثم المدمجة)
    raw_tokens = os.getenv("BOT_TOKENS") or ""
    all_tokens = [t.strip() for t in raw_tokens.split(',') if t.strip()]
    if not all_tokens: all_tokens = EMBEDDED_TOKENS
    
    client = None
    # محاولة استخدام البوتات حتى ينجح واحد سيدي
    for i, attempt_token in enumerate(all_tokens, 1):
        try:
            print(f"📡 محاولة تجنيد الفارس {i}...")
            temp_client = TelegramClient(f'sessions/royal_{task_id}', API_ID, API_HASH)
            await temp_client.start(bot_token=attempt_token)
            client = temp_client
            print(f"✅ الفارس {i} في الخدمة الآن سيدي.")
            break
        except Exception as e:
            print(f"⚠️ الفارس {i} سقط في المعركة: {e}")
            continue

    if not client:
        print("🚨 انهيار النظام: لا يوجد فرسان قادرون على القتال سيدي!")
        return

    architect = ManhwaArchitect()
    try:
        curr_url = task['source_url']
        last_ch = float(task['last_chapter'])
        target_id = task['target_id']

        for _ in range(5): 
            print(f"🌐 الهجوم على الرابط: {curr_url}")
            architect.page.get(curr_url)
            
            if not architect.bypass_cloudflare():
                print("⚠️ الحماية قوية جداً سيدي، الصفحة لم تفتح.")
                break

            architect.page.scroll.to_bottom()
            time.sleep(5)
            
            images = architect.extract_images()
            print(f"📸 استخراج {len(images)} هدف (صورة) سيدي.")

            if not images: 
                print("📄 الصفحة فارغة أو لم يتم تحميل الصور.")
                break

            supabase_update_task(task_id, {"status": "uploading"})
            file_ids = []
            for img in images:
                try:
                    sent = await client.send_file(CHAT_ID, img, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                    await asyncio.sleep(0.6)
                except: continue

            if file_ids:
                new_ch = last_ch + 1
                payload = {
                    "manhwa_id": int(target_id),
                    "chapter_number": new_ch,
                    "image_ids": file_ids,
                    "is_premium": False
                }
                
                # 📡 إرسال الغنائم إلى رندر سيدي
                res = requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY}, timeout=60)
                
                if res.status_code == 200:
                    print(f"✅ تم فتح الفصل {new_ch} بنجاح سيدي!")
                    last_ch = new_ch
                    # البحث عن الرابط التالي
                    next_url = architect.page.ele('.next_page').attr('href') if architect.page.ele('.next_page') else None
                    
                    supabase_update_task(task_id, {
                        "last_chapter": new_ch, 
                        "status": "idle",
                        "source_url": next_url if next_url else curr_url
                    })
                    if next_url: curr_url = next_url
                    else: break
                else: 
                    print(f"❌ فشل مزامنة الفصل {new_ch} مع السيرفر الرئيسي.")
                    break
            else: break
                
    except Exception as e:
        print(f"🔥 انفجار غير متوقع: {e} سيدي.")
        supabase_update_task(task_id, {"status": "error"})
    finally:
        if client: await client.disconnect()
        architect.page.quit()

if __name__ == "__main__":
    if not os.path.exists('sessions'): os.makedirs('sessions')
    asyncio.run(start_royal_mission())