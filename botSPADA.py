import time
import os
import sys
import pyautogui
import pywhatkit as kit
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plyer import notification

# --- DYNAMIC PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
DB_FILE = os.path.join(BASE_DIR, "seen_assignments.txt")
ENV_PATH = os.path.join(BASE_DIR, ".env")

# --- LOAD SECRETS ---
load_dotenv(ENV_PATH)
USERNAME = os.getenv("SPADA_USER")
PASSWORD = os.getenv("SPADA_PASS")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# --- SETTINGS ---
CHECK_INTERVAL = 3600 # 1 Hour

def get_seen_assignments():
    if not os.path.exists(DB_FILE):
        return set()
    with open(DB_FILE, "r", encoding='utf-8') as f:
        return set(line.strip() for line in f)

def save_assignment(assignment_name):
    with open(DB_FILE, "a", encoding='utf-8') as f:
        f.write(assignment_name + "\n")

def send_whatsapp_alert(task_name):
    try:
        print(f"Opening WhatsApp for: {task_name}")
        # 1. Type message (tab_close=False so we can force enter)
        kit.sendwhatmsg_instantly(
            phone_no=PHONE_NUMBER, 
            message=f"🚨 *NEW SPADA TASK*\n\n📝 {task_name}",
            wait_time=20,
            tab_close=False 
        )
        # 2. Force Send & Close
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'w')
        print("✅ WhatsApp Alert Sent.")
    except Exception as e:
        print(f"❌ WhatsApp Error: {e}")

def check_spada():
    print("\n" + "="*40)
    print(f"SCAN START: {time.strftime('%H:%M:%S')}")
    print("="*40)
    
    options = Options()
    # Note: Headless is OFF so WhatsApp can open its window
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0")

    driver = webdriver.Edge(options=options)
    wait = WebDriverWait(driver, 45)
    
    try:
        print("Step 1: Logging into SPADA...")
        driver.get("https://spada.upnyk.ac.id/login/index.php")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "loginbtn").click()
        
        print("Step 2: Loading Dashboard...")
        wait.until(EC.presence_of_element_located((By.ID, "region-main")))
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(15) 

        print("Step 3: Scraping Assignments...")
        items = driver.find_elements(By.CSS_SELECTOR, "a[href*='mod/assign']")
        
        found_tasks = []
        for el in items:
            try:
                text = el.get_attribute("aria-label") or el.text.strip()
                if text and len(text) > 4:
                    text = text.replace(" is due", "").replace(" due date", "").replace("Assignment is due", "")
                    junk = ["Add submission", "View", "Go to", "Submission", "Upcoming", "Course name"]
                    if not any(word in text for word in junk):
                        found_tasks.append(text)
            except: continue
        
        unique_tasks = list(set(found_tasks))
        seen = get_seen_assignments()
        new_count = 0

        for task in unique_tasks:
            if task not in seen:
                print(f"🚨 NEW TASK: {task}")
                save_assignment(task)
                
                # Desktop Alert
                notification.notify(title='SPADA ALERT!', message=task, timeout=10)
                
                # WhatsApp Alert
                send_whatsapp_alert(task)
                new_count += 1
            else:
                print(f"⚪ Old: {task}")

        if new_count == 0:
            print("Status: No new tasks found.")

    except Exception as e:
        print(f"❌ Scan Error: {type(e).__name__}")
    finally:
        print("Step 4: Cleaning up.")
        driver.quit()

if __name__ == "__main__":
    while True:
        check_spada()
        print(f"\nSleeping for {CHECK_INTERVAL/60} minutes...")
        time.sleep(CHECK_INTERVAL)