# import logging
# import os
# import ssl
# import json
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
# import time
# import requests
# import http.client
# from datetime import datetime, timedelta
# from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
# import threading
# import subprocess
# import socket
# import traceback



# logging.basicConfig(
#     filename='Tasks.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )


# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# DEVICE_IP = "192.168.0.108"
# PORT_RANGE = range(30000, 60000)
# USERNAME = "manharlamba@ariantechsolutions.com"
# PASSWORD = "Indian@123456"
# SELENIUM_URL = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
# TAP_X, TAP_Y = 526, 246
# found_port = None
# lock = threading.Lock()

# def login_to_website(driver, selenium_url, username, password):
#     """Log in to the website."""
#     driver.get(selenium_url)
#     WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[3]/c-custom-s-s-o-login/div[3]/lightning-button/button'))
#     ).click()
#     logging.info("Clicked to disable SSO.")

#     WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Email' and @type='text']"))
#     ).send_keys(username)
#     logging.info("Entered username.")

#     WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Password' and @type='password']"))
#     ).send_keys(password)
#     logging.info("Entered password.")

#     WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[2]/div/div[3]/button/span'))
#     ).click()
#     logging.info("Clicked login button.")

#     WebDriverWait(driver, 20).until(EC.url_to_be(selenium_url))
#     time.sleep(5)
#     logging.info("Successfully logged in.")

# def fetch_data_from_api(api_url):
#     """Fetch data from API with SSL verification disabled."""
#     try:
#         response = requests.get(api_url, verify=False)
#         response.raise_for_status()
#         data = response.json()
#         logging.info(f"Fetched {len(data)} entries from API.")
#         return data
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Failed to fetch data from API: {e}")
#         return []
#         driver.refresh()
#         time.sleep(10)
# def convert_due_date(due_date):
    
#     today = datetime.today()
#     tomorrow = today + timedelta(days=1)

    
#     due_date_obj = datetime.strptime(due_date, '%d/%m/%Y') if due_date else None

#     if due_date_obj:
        
#         if due_date_obj.date() == today.date():
#             return "Today"
        
#         elif due_date_obj.date() == tomorrow.date():
#             return "Tomorrow"
#         else:
            
#             return due_date
#     else:
#         return "Invalid date"

# def send_put_request(api_url, payload):
#     """Send a PUT request to the API with SSL verification disabled."""
#     try:
#         response = requests.put(api_url, json=payload, verify=False)
#         response.raise_for_status()
#         logging.info(f"PUT request successful for payload: {payload}. Response: {response.status_code}")
#         return response
#     except requests.exceptions.RequestException as e:
#         logging.error(f"PUT request failed for payload {payload}: {e}")
#         return None
    
# login_done = False

# def process_emails(api_url, output_directory, selenium_url, driver):
#     while True:
#         try:
#             # Retry fetching API until non-empty data is received
#             followups_data = []
#             while not followups_data:
#                 logging.info("Fetching data from API.")
#                 context = ssl._create_unverified_context()
#                 conn = http.client.HTTPSConnection(api_url.replace("https://", "").split("/")[0], context=context)
#                 endpoint = "/" + "/".join(api_url.split("/")[3:])
#                 conn.request("GET", endpoint)
#                 response = conn.getresponse()

#                 if response.status == 200:
#                     followups_data = json.loads(response.read().decode())
#                     if not followups_data:
#                         logging.warning("Empty API response. Retrying in 15 seconds...")
#                         driver.refresh()
#                         time.sleep(15)
#                 else:
#                     logging.error(f"Failed to fetch data. HTTP {response.status}. Retrying in 15 seconds...")
#                     driver.refresh()
                    
#                     time.sleep(15)

#             logging.info(f"Fetched {len(followups_data)} entries from API.")

#             if not os.path.exists(output_directory):
#                 os.makedirs(output_directory)
#             json_file_path = os.path.join(output_directory, "Tasks.json")
#             with open(json_file_path, 'w') as json_file:
#                 json.dump(followups_data, json_file, indent=4)
#             print(f"api data saved{json_file_path}")
#             logging.info(f"API data saved to {json_file_path}")

#             failed_followups=set()


#             for entry in followups_data:
#                 lead_id_followup = entry.get('task_id', '')
#                 lead_email = entry.get('lead_email', '').lower() if entry.get('lead_email') else ''
#                 subject = entry.get('subject', '') 
#                 due_date = entry.get('due_date', '')
#                 status = entry.get('status', '')
#                 url = entry.get('lead_url', '')
#                 comments=entry.get('comments','')

                
#                 print(f"Processing task for: {lead_email} | URL: {url}")
#                 if not url:
#                     print("skipping the data  as im not  having the url")
#                     driver.refresh()
#                     time.sleep(10)
#                     continue

#                 converted_due_date = convert_due_date(due_date)
#                 total_data = {'subject': subject, 'due_date': converted_due_date}
#                 time.sleep(5)
               
#                 print("yaha se start")
#                 current_url = driver.current_url
#                 if current_url == "https://cxp--preprod.sandbox.my.site.com/CXP/s/login/?language=en_US&ec=302&startURL=%2FCXP%2Fs%2Flead%2FLead%2FDefault":
#                     print("Need to login again...")
#                     DEVICE_IP = "192.168.0.236"
#                     PORT_RANGE = range(30000, 60000)
#                     TAP_X, TAP_Y = 505, 296

#                     found_port = None
#                     lock = threading.Lock()

#                     for port in PORT_RANGE:
#                         if found_port is not None:
#                             break
#                         try:
#                             sock = socket.create_connection((DEVICE_IP, port), timeout=1)
#                             sock.close()
#                             with lock:
#                                 if found_port is None:
#                                     found_port = port
#                         except (socket.timeout, ConnectionRefusedError, OSError):
#                             pass

#                     if found_port is not None:
#                         print(f"✅ Open ADB port found: {found_port}")
#                         print(f"🔗 Connecting to {DEVICE_IP}:{found_port}...")
#                         os.system(f"adb connect {DEVICE_IP}:{found_port}")
#                     else:
#                         print("❌ No open ADB port found.")

                            
#                     WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[3]/c-custom-s-s-o-login/div[3]/lightning-button/button'))
#                     ).click()
#                     logging.info("Clicked to disable SSO.")

#                     WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Email' and @type='text']"))
#                     ).send_keys("manharlamba@ariantechsolutions.com")
#                     logging.info("Entered username.")

#                     WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Password' and @type='password']"))
#                     ).send_keys("Indian@12345")
#                     logging.info("Entered password.")

#                     WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[2]/div/div[3]/button/span'))
#                     ).click()
#                     logging.info("Clicked login button.")
                    
#                     # Wait for mobile approval prompt and use ADB to tap the approve button
#                     time.sleep(5)  # Wait for the mobile prompt to appear
#                     os.system(f"adb shell input tap {TAP_X} {TAP_Y}")
#                     selenium_url="https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
                
                    
#                     WebDriverWait(driver, 30).until(EC.url_to_be(selenium_url))
#                     time.sleep(5)
#                     logging.info("Successfully logged in.")
#                 else:
#                     print("Already logged in, continuing...")
#                     logging.info("Already logged in, continuing with the workflow.")
#                 print("yaha tak end hauin")




              


#                 try:
#                     driver.get(url)
#                     print(f"Opened URL: {url}")
#                     time.sleep(10)
#                 except Exception as e:
#                     print("Error opening URL:", e)

#                 WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[span[text()='New Task']]"))
#                 ).click()
#                 try:

#                     subject_btn = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Subject']/following::input[1]"))
#                     )
#                     subject_btn.clear()
#                     subject_btn.send_keys(subject)
#                     logging.info(f"Entered subject: {subject}")
#                     time.sleep(1)
#                 except Exception as e:
#                     print("the error has been found")
#                     failed_followups.add(lead_id_followup)
#                     driver.refresh()
#                     continue

#                 if due_date:
#                     due_date_input = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Due Date']/following::input[1]"))
#                     )
#                     due_date_input.clear()
#                     due_date_input.send_keys(due_date)
#                     logging.info(f"Entered due date: {due_date}")
#                 textarea = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'uiInputTextArea') and @role='textbox']"))
#                 )
#                 textarea.clear()  
#                 textarea.send_keys(comments)
#                 print("✅ Text entered successfully in the textarea.")
#                 time.sleep(2)

#                 try:
#                     status_dropdown = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, "//a[@role='combobox' and contains(@class, 'select')]"))
#                     )
#                     driver.execute_script("arguments[0].click();", status_dropdown)  # JS click avoids interception
#                     time.sleep(1)

#                     if status:
#                         option_xpath = f"//a[normalize-space(text())='{status}']"
#                         status_option = WebDriverWait(driver, 10).until(
#                             EC.element_to_be_clickable((By.XPATH, option_xpath))
#                         )
#                         driver.execute_script("arguments[0].click();", status_option)
#                         logging.info(f"Selected status: {status}")
#                 except Exception as e:
#                     logging.error(f"Error selecting status '{status}': {e}")
#                     failed_followups.add(lead_id_followup)
#                     driver.refresh()
#                     continue


#                 try:

#                     save_btn = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'slds-button--brand') and .//span[text()='Save']]"))
#                     )
#                     driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
#                     save_btn.click()
                   
                    
#                     time.sleep(2)
#                     print("hiiii")
#                 except Exception as e:
#                     print("the errpor has been found",e)
#                     driver.refresh()
#                     continue

#                 try:
                    
#                     try:
#                         element=WebDriverWait(driver,10).until(
#                             EC.element_to_be_clickable((By.XPATH,"//div[contains(@class,'forceToastMessage')]//a[contains(@class, 'forceActionLink')]"))
#                         )
#                         if element.is_displayed():
#                             print("elemnt is  dispalyed")
#                             element.click()
#                         else:
#                             print("elemnt not found")

#                     except Exception as e:
#                         print("Error with 'View More' toast click:", e)
                     
#                     # time.sleep(5)
#                     # vechiles = WebDriverWait(driver, 10).until(
#                     #     EC.any_of(
#                     #         EC.element_to_be_clickable((By.XPATH, f"//a[@title='{subject}']")),
#                     #         EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'dueDate') and contains(text(), '{converted_due_date}')]"))
#                     #     )
#                     # )

#                     # if vechiles.is_displayed():
#                     #     print(f"converdate milgaya bhai with subject{subject},{converted_due_date}")
#                     #     vechiles.click()
#                     # else:
#                     #     driver.execute_script("window.scrollBy(0, 800);")
#                     #     vechiles.click()
#                     # # time.sleep(5)
#                     # wait = WebDriverWait(driver, 10)
#                     # toast_link = wait.until(EC.element_to_be_clickable((
#                     #     By.XPATH,
#                     #     "//div[@data-key='success']//a[contains(@cviewlass, 'forceActionLink')]"
#                     # )))
#                     # toast_link.click()
#                     # time.sleep(2)
                        

                    
                   
#                 except Exception as e:
#                     print("Error with 'View More' button:", e)

               
#                 current_url = driver.current_url
#                 print(f"Captured URL: {current_url}")
#                 time.sleep(10)

#                 file_name = "TASKS.json"
#                 lead_data = {"task_id": lead_id_followup, "url": current_url}

#                 with open(file_name, 'w') as json_file:
#                     json.dump(lead_data, json_file, indent=4)

#                 with open(file_name, 'r') as json_file:
#                     payload = json.load(json_file)

                
#                 try:
#                     context = ssl._create_unverified_context()
#                     conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)

#                     payload_json = json.dumps(payload)
#                     headers = {
#                         "Content-Type": "application/json",
#                         "Content-Length": str(len(payload_json))
#                     }

#                     conn.request("PUT", "/api/RPA/tasks/new/flag-inactive", body=payload_json, headers=headers)
#                     response = conn.getresponse()

#                     if response.status == 200:
#                         print("Successfully updated the lead data!")
#                         data = response.read().decode()
#                         logging.info(f"PUT Response: {data}")
#                     else:
#                         print(f"Failed to update lead data. HTTP {response.status}")
#                         logging.error(f"PUT Error Response: {response.read().decode()}")
#                 except Exception as e:
#                     logging.error(f"PUT request error: {e}")
#                     print(f"PUT request error: {e}")

#                 driver.back()
#                 time.sleep(5)

#                 driver.refresh()
#                 time.sleep(5)
                
#         except Exception as e:
            
#             logging.error(f"Error processing task ID {entry.get('task_id')}: {e}")
#             print(f"the error has been found{lead_id_followup}")
#             print(f"Error processing task ID {entry.get('task_id')}: {e}")
#             continue 
        


# if __name__ == "__main__":
#     api_url = "https://api.smartassistapp.in/api/RPA/tasks-data/new"
#     output_directory = "C:\\SAKET\\RPA\\Salesforce\\Tasksjsonfiles"
#     selenium_url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
#     username = "manharlamba@ariantechsolutions.com"
#     password = "Indian@12345678"


#     options = webdriver.ChromeOptions()
#     options.add_argument('--disable-gpu')
#     options.add_argument('--start-maximized')

#     driver = webdriver.Chrome(options=options)
 
#     login_to_website(driver, selenium_url, username, password)
#     process_emails(api_url, output_directory, selenium_url, driver)

        
import logging
import os
import ssl
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import requests
import http.client
from datetime import datetime, timedelta
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import threading
import subprocess
import socket
import traceback

# Logging setup
logging.basicConfig(
    filename='Tasks.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
DEVICE_IP = "192.168.0.108"
PORT_RANGE = range(30000, 60000)
USERNAME = "manharlamba@ariantechsolutions.com"
PASSWORD = "Indian@123456"
SELENIUM_URL = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
TAP_X, TAP_Y = 526, 246
found_port = None
lock = threading.Lock()

def check_flask_api_status():
    """Check if Flask API is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Flask API is running and healthy")
            return True
        else:
            print("❌ Flask API is not responding properly")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask API is not reachable: {e}")
        print("🔧 Please start the Flask API first by running: python flask_api.py")
        return False

def login_to_website(driver, selenium_url, username, password):
    """Log in to the website."""
    try:
        driver.get(selenium_url)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[3]/c-custom-s-s-o-login/div[3]/lightning-button/button'))
        ).click()
        logging.info("Clicked to disable SSO.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Email' and @type='text']"))
        ).send_keys(username)
        logging.info("Entered username.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Password' and @type='password']"))
        ).send_keys(password)
        logging.info("Entered password.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[2]/div/div[3]/button/span'))
        ).click()
        logging.info("Clicked login button.")

        WebDriverWait(driver, 30).until(EC.url_to_be(selenium_url))
        time.sleep(5)
        logging.info("Successfully logged in.")
        print("✅ Successfully logged in to Salesforce")
    except Exception as e:
        logging.error(f"Login failed: {e}")
        print(f"❌ Login failed: {e}")
        raise

def convert_due_date(due_date):
    """Convert due date to readable format"""
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    
    due_date_obj = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

    if due_date_obj:
        if due_date_obj.date() == today.date():
            return "Today"
        elif due_date_obj.date() == tomorrow.date():
            return "Tomorrow"
        else:
            return due_date
    else:
        return "Invalid date"

def check_for_new_data():
    """Check for new JSON files from POST API"""
    rpa_logs_dir = "rpa_logs"
    if not os.path.exists(rpa_logs_dir):
        print(f"📁 Directory {rpa_logs_dir} does not exist")
        return None
    
    # Get all JSON files in the directory
    json_files = [f for f in os.listdir(rpa_logs_dir) if f.endswith('.json')]
    
    if not json_files:
        return None
    
    # Get the most recent file
    latest_file = max(json_files, key=lambda f: os.path.getctime(os.path.join(rpa_logs_dir, f)))
    file_path = os.path.join(rpa_logs_dir, latest_file)
    
    print(f"📂 Processing file: {latest_file}")
    
    # Read and return the data
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Debug: Print the actual data structure
    print(f"🔍 Data structure received: {list(data.keys()) if isinstance(data, dict) else type(data)}")
    print(f"🔍 Full data: {json.dumps(data, indent=2)}")
    
    # Delete the file after reading to avoid reprocessing
    os.remove(file_path)
    logging.info(f"Processed and removed file: {latest_file}")
    
    # ✅ CHANGED LINES START HERE
    # Replaced original key-checking logic with this robust version
    if isinstance(data, list):
        followups_data = data
    elif isinstance(data, dict):
        for key in ['followups_data', 'data', 'tasks']:
            if key in data and isinstance(data[key], list):
                followups_data = data[key]
                break
        else:
            followups_data = [data]  
    else:
        followups_data = []
   
    
    print(f"📊 Found {len(followups_data) if followups_data else 0} entries to process")
    
    return followups_data

def send_put_request(api_url, payload):
    """Send a PUT request to the API with SSL verification disabled."""
    try:
        response = requests.put(api_url, json=payload, verify=False)
        response.raise_for_status()
        logging.info(f"PUT request successful for payload: {payload}. Response: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"PUT request failed for payload {payload}: {e}")
        return None

def process_emails(output_directory, selenium_url, driver):
    """Main processing loop"""
    print("🔄 Starting email processing loop...")
    print("⏳ Waiting for new data from Flask API...")
    
    while True:
        try:
            # Check for new data from POST API
            followups_data = check_for_new_data()
            
            if not followups_data:
                print("📡 No new data found, refreshing driver and waiting...")
                driver.refresh()
                time.sleep(15)
                continue

            print(f"📨 Found new data with {len(followups_data)} entries.")
            logging.info(f"Found new data with {len(followups_data)} entries.")

            # Save data to output directory
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            json_file_path = os.path.join(output_directory, "Tasks.json")
            with open(json_file_path, 'w') as json_file:
                json.dump(followups_data, json_file, indent=4)
            print(f"💾 API data saved to {json_file_path}")
            logging.info(f"API data saved to {json_file_path}")

            failed_followups = set()

            for entry in followups_data:
                lead_id_followup = entry.get('task_id', '')
                lead_email = entry.get('lead_email', '').lower() if entry.get('lead_email') else ''
                subject = entry.get('subject', '') 
                due_date = entry.get('due_date', '')
                status = entry.get('status', '')
                url = entry.get('lead_url', '')
                comments = entry.get('comments','')

                print(f"🔄 Processing task for: {lead_email} | URL: {url}")
                if not url:
                    print("⚠️ Skipping the data as URL is missing")
                    driver.refresh()
                    time.sleep(10)
                    continue

                converted_due_date = convert_due_date(due_date)
                total_data = {'subject': subject, 'due_date': converted_due_date}
                time.sleep(5)
               
                print("⚡ Starting processing...")
                current_url = driver.current_url
                
                # Check if need to login again
                if current_url == "https://cxp--preprod.sandbox.my.site.com/CXP/s/login/?language=en_US&ec=302&startURL=%2FCXP%2Fs%2Flead%2FLead%2FDefault":
                    print("🔐 Need to login again...")
                    # Re-login logic here...
                    # [Your existing login code]
                else:
                    print("✅ Already logged in, continuing...")
                    logging.info("Already logged in, continuing with the workflow.")

                try:
                    driver.get(url)
                    print(f"🌐 Opened URL: {url}")
                    time.sleep(10)
                except Exception as e:
                    print(f"❌ Error opening URL: {e}")

                # Click New Task button
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='New Task']]"))
                ).click()

                # Fill task details
                try:
                    subject_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Subject']/following::input[1]"))
                    )
                    subject_btn.clear()
                    subject_btn.send_keys(subject)
                    logging.info(f"Entered subject: {subject}")
                    time.sleep(1)
                except Exception as e:
                    print(f"❌ Error entering subject: {e}")
                    failed_followups.add(lead_id_followup)
                    driver.refresh()
                    continue

                # Fill due date
                if due_date:
                    due_date_input = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Due Date']/following::input[1]"))
                    )
                    due_date_input.clear()
                    due_date_input.send_keys(due_date)
                    logging.info(f"Entered due date: {due_date}")

                # Fill comments
                textarea = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'uiInputTextArea') and @role='textbox']"))
                )
                textarea.clear()  
                textarea.send_keys(comments)
                print("✅ Text entered successfully in the textarea.")
                time.sleep(2)

                # Select status
                try:
                    status_dropdown = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[@role='combobox' and contains(@class, 'select')]"))
                    )
                    driver.execute_script("arguments[0].click();", status_dropdown)
                    time.sleep(1)

                    if status:
                        option_xpath = f"//a[normalize-space(text())='{status}']"
                        status_option = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, option_xpath))
                        )
                        driver.execute_script("arguments[0].click();", status_option)
                        logging.info(f"Selected status: {status}")
                except Exception as e:
                    logging.error(f"Error selecting status '{status}': {e}")
                    failed_followups.add(lead_id_followup)
                    driver.refresh()
                    continue

                # Save task
                try:
                    save_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'slds-button--brand') and .//span[text()='Save']]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
                    save_btn.click()
                    time.sleep(2)
                    print("✅ Task saved successfully")
                except Exception as e:
                    print(f"❌ Error saving task: {e}")
                    driver.refresh()
                    continue

                # Handle toast message
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'forceToastMessage')]//a[contains(@class, 'forceActionLink')]"))
                    )
                    if element.is_displayed():
                        print("📋 Toast message found, clicking...")
                        element.click()
                    else:
                        print("ℹ️ Toast element not displayed")
                except Exception as e:
                    print(f"⚠️ Error with toast message: {e}")

                # Capture current URL and send PUT request
                current_url = driver.current_url
                print(f"🔗 Captured URL: {current_url}")
                time.sleep(10)

                # Prepare payload for PUT request
                file_name = "TASKS.json"
                lead_data = {"task_id": lead_id_followup, "url": current_url}

                with open(file_name, 'w') as json_file:
                    json.dump(lead_data, json_file, indent=4)

                # Send PUT request
                try:
                    context = ssl._create_unverified_context()
                    conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)

                    payload_json = json.dumps(lead_data)
                    headers = {
                        "Content-Type": "application/json",
                        "Content-Length": str(len(payload_json))
                    }

                    conn.request("PUT", "/api/RPA/tasks/new/flag-inactive", body=payload_json, headers=headers)
                    response = conn.getresponse()

                    if response.status == 200:
                        print("✅ Successfully updated the lead data!")
                        data = response.read().decode()
                        logging.info(f"PUT Response: {data}")
                    else:
                        print(f"❌ Failed to update lead data. HTTP {response.status}")
                        logging.error(f"PUT Error Response: {response.read().decode()}")
                except Exception as e:
                    logging.error(f"PUT request error: {e}")
                    print(f"❌ PUT request error: {e}")

                # Navigate back and refresh
                driver.back()
                time.sleep(5)
                driver.refresh()
                time.sleep(5)
                
        except Exception as e:
            logging.error(f"Error processing task: {e}")
            print(f"❌ Error processing task: {e}")
            continue 

if __name__ == "__main__":
    print("🚀 Starting Selenium RPA Script...")
    
    # Check if Flask API is running
    if not check_flask_api_status():
        print("\n❌ Flask API is not running!")
        print("📝 Please run the Flask API first:")
        print("   python flask_api.py")
        print("\n🔄 Then run this script again:")
        print("   python main_rpa.py")
        exit(1)
    
    # Configuration
    output_directory = "C:\\SAKET\\RPA\\Salesforce\\Tasksjsonfiles"
    selenium_url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
    username = "manharlamba@ariantechsolutions.com"
    password = "Indian@12345678"

    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')

    print("🌐 Initializing Chrome WebDriver...")
    driver = webdriver.Chrome(options=options)
    
    try:
        # Login to website
        print("🔐 Logging in to Salesforce...")
        login_to_website(driver, selenium_url, username, password)
        
        # Start processing
        print("🚀 Starting main processing loop...")
        process_emails(output_directory, selenium_url, driver)
        
    except KeyboardInterrupt:
        print("\n⏹️ Process interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error: {e}")
    finally:
        print("🔚 Closing browser...")
        driver.quit()
        print("✅ Script completed")
