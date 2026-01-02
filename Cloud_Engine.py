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

# --- Professional Global Commenting Protocol: UC-SOVEREIGN V5.7 (PRECISION STRIKE) سيدي ---

async def execute_mission(task, bot_index, architect):
    token = BOT_TOKENS[bot_index]
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    driver = None
    
    try:
        await client.start(bot_token=token)
        driver = uc.Chrome(options=architect.options)
        driver.set_window_size(1920, 1080) # توحيد الشاشة لتحديد الإحداثيات سيدي
        
        print(f"🌐 الفارس {bot_index+1}: يقف أمام البوابة الحصينة...")
        driver.get(task['source_url'])
        await asyncio.sleep(10)

        # --- ⚡ عملية التسلل لمركز البوابة سيدي ---
        try:
            # البحث عن إطار Cloudflare Turnstile
            # غالباً ما يكون له اسم يبدأ بـ cf-chl-widget سيدي
            gate_iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for frame in gate_iframes:
                if "cloudflare" in frame.get_attribute("src") or "turnstile" in frame.get_attribute("src"):
                    print(f"🎯 تم رصد ثغرة البوابة (Iframe)، جاري محاكاة النقر البشري...")
                    
                    # الحصول على موقع الإطار على الشاشة سيدي
                    location = frame.location
                    size = frame.size
                    
                    # حساب نقطة النقر في منتصف الإطار تماماً
                    center_x = location['x'] + (size['width'] / 2)
                    center_y = location['y'] + (size['height'] / 2)
                    
                    # تنفيذ النقر الدقيق سيدي
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(driver)
                    actions.move_by_offset(center_x, center_y).click().perform()
                    
                    print(f"⚡ تم توجيه ضربة دقيقة للإحداثيات ({center_x}, {center_y})")
                    break
            
            # انتظار المعالجة بعد النقر سيدي
            await asyncio.sleep(15) 
        except Exception as e:
            print(f"⚠️ فشل نظام التسلل الدقيق: {e}")

        # --- 📜 محاولة سحب الغنائم بعد الاختراق ---
        # سنقوم بتحديث الصفحة داخلياً (Scroll) لتنشيط المحتوى سيدي
        driver.execute_script("window.scrollBy(0, 500);")
        await asyncio.sleep(2)
        
        links = architect.extract_precise_images(driver)
        
        if links:
            print(f"🔥 نصر مؤزر! اخترقنا البوابة ووجدنا {len(links)} صورة سيدي.")
            # (نفس كود الرفع كما هو سيدي)
            # ...
        else:
            print(f"❌ الفارس {bot_index+1}: الحصن لا يزال صامداً. جاري سحب تقرير الـ HTML...")
            with open(f"failed_capture_{bot_index}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

    except Exception as e:
        print(f"❌ سيدي، واجهنا عطل فني: {e}")
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