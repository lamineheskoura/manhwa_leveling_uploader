# --- Professional Global Commenting Protocol: UC-SOVEREIGN V5.2 (Cloud Edition) سيدي ---
import os, asyncio, re, requests, time
import undetected_chromedriver as uc
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.utils import pack_bot_file_id
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔐 الثوابت الملكية سيدي
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
        # سيدي، نجهز خيارات المتصفح لتناسب بيئة GitHub القاسية
        self.options = uc.ChromeOptions()
        self.options.add_argument('--headless') # ضروري في السحاب سيدي
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')

    def extract_precise_images(self, driver):
        """نفس منطق حاسوبك سيدي: البحث العميق عن الصور"""
        links = []
        # الحاويات المشهورة التي أضفتها أنت سيدي
        selectors = ['.reading-content', '.main-col', '.vung-doc', '.reader-area', '.wp-manga-chapter-img']
        
        target = None
        for s in selectors:
            try:
                target = driver.find_element(By.CSS_SELECTOR, s)
                if target: break
            except: continue

        if target:
            imgs = target.find_elements(By.TAG_NAME, 'img')
            for img in imgs:
                src = img.get_attribute('data-src') or img.get_attribute('data-lazy-src') or img.get_attribute('src')
                if src and 'http' in src and not any(x in src.lower() for x in ['logo', 'banner', 'avatar']):
                    links.append(src)
        
        # خطة بديلة سيدي: Regex إذا فشلت الحاويات
        if not links:
            links = re.findall(r'https?://[^\s"\'<>]+?\.(?:webp|jpg|png|jpeg)', driver.page_source)
            links = [l for l in links if not any(x in l.lower() for x in ['logo', 'icon', 'theme'])]
            
        return list(dict.fromkeys(links))

    def find_next_link(self, driver):
        """مطاردة الفصل التالي كما في كودك سيدي"""
        selectors = ['.next_page', 'a[rel="next"]', 'a:contains("التالي")']
        for s in selectors:
            try:
                btn = driver.find_element(By.CSS_SELECTOR, s)
                if btn: return btn.get_attribute('href')
            except: continue
        return None

async def execute_mission(task, bot_index, architect):
    token = BOT_TOKENS[bot_index]
    client = TelegramClient(MemorySession(), API_ID, API_HASH)
    driver = None
    
    try:
        await client.start(bot_token=token)
        # بدء المتصفح الخفي سيدي
        driver = uc.Chrome(options=architect.options)
        
        print(f"🕵️ الفارس {bot_index+1} يقتحم: {task['source_url']}")
        driver.get(task['source_url'])
        
        # محاكاة التمرير كما في حاسوبك لضمان تحميل الصور سيدي
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        await asyncio.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(5) # انتظار التحميل

        links = architect.extract_precise_images(driver)
        
        if links:
            print(f"🚀 تم العثور على {len(links)} صورة. جاري الرفع سيدي...")
            file_ids = []
            for link in links:
                try:
                    sent = await client.send_file(CHAT_ID, link, force_document=True)
                    file_ids.append(str(pack_bot_file_id(sent.media.document)))
                except: continue

            if file_ids:
                # إرسال البيانات لموقعك سيدي
                payload = {
                    "manhwa_id": int(task['target_id']),
                    "chapter_number": float(task['last_chapter']) + 1,
                    "image_ids": file_ids,
                    "is_premium": False
                }
                requests.post(SITE_API_URL, json=payload, headers={"X-API-KEY": SITE_API_KEY})
                
                # البحث عن الرابط التالي سيدي
                next_url = architect.find_next_link(driver)
                
                # تحديث قاعدة البيانات
                update_payload = {
                    "last_chapter": float(task['last_chapter']) + 1,
                    "status": "idle",
                    "source_url": next_url if next_url else task['source_url']
                }
                requests.patch(f"{SB_URL}/rest/v1/manhwa_tasks?id=eq.{task['id']}", 
                               headers=HEADERS, json=update_payload)
                print(f"✅ تم إنهاء الفصل بنجاح سيدي!")

    except Exception as e:
        print(f"❌ خطأ الفارس {bot_index+1}: {e}")
    finally:
        if driver: driver.quit()
        await client.disconnect()

async def main():
    architect = CloudArchitect()
    r = requests.get(f"{SB_URL}/rest/v1/manhwa_tasks?status=eq.idle&limit=3", headers=HEADERS)
    tasks = r.json()
    if not tasks: return
    
    # تشغيل الفرسان بالتوازي سيدي
    await asyncio.gather(*[execute_mission(task, i, architect) for i, task in enumerate(tasks)])

if __name__ == "__main__":
    asyncio.run(main())