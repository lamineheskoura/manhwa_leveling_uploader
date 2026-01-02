# --- Professional Global Commenting Protocol: UC-SOVEREIGN V5.4 (Strategic Wait) سيدي ---
import os, asyncio, re, requests, time
import undetected_chromedriver as uc
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.utils import pack_bot_file_id
from selenium.webdriver.common.by import By

# --- (الثوابت تبقى كما هي سيدي دون تغيير) ---
API_ID = 38020317
API_HASH = '941185ea933fd95a990e881fe50a6882'
CHAT_ID = -1003602777623
SITE_API_KEY = "KING_SECRET_KEY_99x"
SITE_API_URL = "https://manhwa-leveling.onrender.com/shadow-throne-99x/api/bulk-sync"
SB_URL = os.getenv("SB_URL")
SB_KEY = os.getenv("SB_KEY")
HEADERS = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}
BOT_TOKENS = ['8561369211:AAGAN-YVY03WgbBDfeQmbh4EvxBD_SWKlzA', '8287317424:AAGwuglZT6fK8aDUjgYN4cRMfO6a0INlgK8', '8321405841:AAGbRHcmjMm9i2l0obI0k3skMmO9zbpzVOE']

class CloudArchitect:
    def __init__(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    def extract_precise_images(self, driver):
        links = []
        selectors = ['.reading-content', '.main-col', '.vung-doc', '.reader-area', '.wp-manga-chapter-img', '#chapter-video-frame']
        
        target = None
        for s in selectors:
            try:
                target = driver.find_element(By.CSS_SELECTOR, s)
                if target: 
                    print(f"🎯 تم العثور على الحاوية المستهدفة: {s}")
                    break
            except: continue

        if target:
            imgs = target.find_elements(By.TAG_NAME, 'img')
            for img in imgs:
                src = img.get_attribute('data-src') or img.get_attribute('data-lazy-src') or img.get_attribute('src')
                if src and 'http' in src and not any(x in src.lower() for x in ['logo', 'banner', 'avatar']):
                    links.append(src)
        
        if not links:
            print("⚠️ لم يتم العثور على صور داخل الحاويات، ننتقل للبحث العام (Regex)...")
            links = re.findall(r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)', driver.page_source)
            links = [l for l in links if not any(x in l.lower() for x in ['logo', 'icon', 'theme'])]
            
        return list(dict.fromkeys(links))

# --- Professional Global Commenting Protocol: UC-SOVEREIGN V5.6 (GATE-CRACKER) سيدي ---

async def execute_mission(task, bot_index, architect):
    token = BOT_TOKENS[bot_index]
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    driver = None
    
    try:
        await client.start(bot_token=token)
        driver = uc.Chrome(options=architect.options)
        
        print(f"🌐 الفارس {bot_index+1}: يقف أمام بوابة التحقق... {task['source_url']}")
        driver.get(task['source_url'])
        
        # 1. نظام كسر بوابة الروبوت سيدي
        await asyncio.sleep(8) # انتظار ظهور البوابة
        try:
            # البحث عن iframe الخاص بـ Cloudflare أو الزر مباشرة
            # نستخدم نظام النقر الإحداثي سيدي لتجنب كشف البوت
            print(f"⚡ الفارس {bot_index+1}: يحاول اختراق بوابة 'أنا لست روبوت'...")
            
            # محاولة النقر في منتصف الشاشة تقريباً حيث يظهر التحدي عادةً
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(driver)
            actions.move_by_offset(200, 300).click().perform() # نقرة عمياء ذكية
            
            # ننتظر 10 ثوانٍ إضافية ليرى الموقع أننا "بشر" ويفتح الصور
            await asyncio.sleep(12) 
        except:
            print("⚠️ البوابة قد لا تكون موجودة أو مخفية، نتابع الهجوم...")

        # 2. التمرير لتنشيط الصور سيدي
        driver.execute_script("window.scrollTo(0, 1000);")
        await asyncio.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(5)

        # 3. سحب الصور الآن (بعد أن فتح الموقع الحماية سيدي)
        links = architect.extract_precise_images(driver)
        
        if links:
            print(f"🔥 تم الاختراق! وجدنا {len(links)} صورة خلف البوابة سيدي.")
            # ... (بقية كود الرفع كما هو سيدي)
        else:
            # إذا فشلنا، سنحفظ صفحة الـ HTML لنعرف نوع البوابة الجديد سيدي
            with open(f"failed_gate_{bot_index}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"❌ الفارس {bot_index+1}: البوابة لا تزال مغلقة. تم حفظ الكود للتحليل.")

    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        if driver: driver.quit()
        await client.disconnect()

async def main():
    architect = CloudArchitect()
    r = requests.get(f"{SB_URL}/rest/v1/manhwa_tasks?status=eq.idle&limit=3", headers=HEADERS)
    tasks = r.json()
    if tasks:
        await asyncio.gather(*[execute_mission(task, i, architect) for i, task in enumerate(tasks)])

if __name__ == "__main__":
    asyncio.run(main())