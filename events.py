import logging
import os
import ssl
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import requests
import http.client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
from selenium.common.exceptions import StaleElementReferenceException
import threading
import socket
import subprocess






logging.basicConfig(filename='event_execution_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

DEVICE_IP = "192.168.0.236"
PORT_RANGE = range(30000, 60000)
USERNAME = "manharlamba@ariantechsolutions.com"
PASSWORD = "Indian@123456"
SELENIUM_URL = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
TAP_X, TAP_Y = 505, 296
found_port = None
lock = threading.Lock()





def login_to_website(driver, selenium_url, username, password):
    """
    Log in to the website. This function is only called once.
    """
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

        WebDriverWait(driver, 20).until(EC.url_to_be(selenium_url))
        time.sleep(5)
        logging.info("Reached target URL after login.")
    except Exception as e:
        logging.error(f"Error during login: {e}", exc_info=True)
    
        raise

def convert_due_date(lead_start_time, lead_start_date):
    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    try:
        # pehle full date se day-month extract kar le
        date_obj = datetime.strptime(lead_start_date, '%d-%b-%Y')
        short_date = date_obj.strftime('%d-%b')  # "29-Feb" format

        lead_datetime = datetime.strptime(f"{lead_start_time} | {short_date}", '%H:%M | %d-%b')
        lead_datetime = lead_datetime.replace(year=today.year)  # same year mein rakh

        time_part = lead_datetime.strftime('%H:%M')

        if lead_datetime.date() == today.date():
            return f"{time_part} | Today"
        elif lead_datetime.date() == tomorrow.date():
            return f"{time_part} | Tomorrow"
        else:
            return f"{time_part} | {lead_datetime.strftime('%d-%b')}"
    except ValueError:
        return "Invalid date"
def process_events(api_url, output_directory, selenium_url, driver):
    # wait = WebDriverWait(driver, 10)  # Define wait object once

    while True:
        try:
            # Step 1: Fetch data from API
            logging.info("Fetching data from API.")
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection(api_url.replace("https://", "").split("/")[0], context=context)
            endpoint = "/" + "/".join(api_url.split("/")[3:])
            conn.request("GET", endpoint)
            response = conn.getresponse()

            if response.status == 200:
                events_data = json.loads(response.read().decode())
                logging.info(f"Fetched {len(events_data)} entries from API.")
            else:
                logging.error(f"Failed to fetch data with status code: {response.status}")
                continue

            # Save API data to file
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            json_file_path = os.path.join(output_directory, f"events_data_{int(time.time())}.json")
            with open(json_file_path, 'w') as json_file:
                json.dump(events_data, json_file, indent=4)
            logging.info(f"API data saved to {json_file_path}")
            print(f"API data saved to {json_file_path}")

            # def process_events(api_url,output_directory, selenium_url, driver):
            #     """Process event data from JSON file and fill in the event form."""
                
            #     events_data = load_event_data()
            #     if not events_data:
            #         print("No event data found. Exiting process.")
            #         return
            # Process each event
            print("hi bhai")
            
           
            for event in events_data:
                print("data aayahoga")
                print(f"Processing event: {event}")
               
                subject = event.get('subject', '')
                lead_start_date = event.get('start_date', '')
                
                lead_start_time = event.get('start_time', '')
                #print(lead_start_date)
                lead_end_date = event.get('end_date', '')
                lead_end_time = event.get('end_time', '')
                lead_id = event.get('event_id', '')
                lead_url=event.get('lead_url','')
                print("yaha hao raha hain")
                if not lead_url or not lead_id or not subject or not lead_start_date:
                    print("Skipping event due to missing critical data (lead_email, event_id, subject, or start_date).")
                    continue

                # url1="https://cxp--preprod.sandbox.my.site.com/CXP/s/login/?language=en_US&ec=302&startURL=%2FCXP%2Fs%2Flead%2FLead%2FDefault"
                # driver.get(url1)

                
                

                # converted_due_date = convert_due_date(due_date)
                # total_data = {'subject': subject, 'due_date': converted_due_date}
                # time.sleep(5)
               
                print("yaha se start")
                current_url = driver.current_url

                
                if current_url == "https://cxp--preprod.sandbox.my.site.com/CXP/s/login/?language=en_US&ec=302&startURL=%2FCXP%2Fs%2Flead%2FLead%2FDefault":
                    print("🔐 Need to login again...")

                    DEVICE_IP = "192.168.0.108"
                    PORT_RANGE = range(30000, 60000)
                    TAP_X, TAP_Y = 526, 246

                    found_port = None
                    lock = threading.Lock()

                    def is_adb_port_open(ip, port):
                        try:
                            sock = socket.create_connection((ip, port), timeout=1)
                            sock.close()
                            return True
                        except:
                            return False

                    def scan_port(port):
                        global found_port
                        if found_port is not None:
                            return
                        if is_adb_port_open(DEVICE_IP, port):
                            with lock:
                                if found_port is None:
                                    found_port = port

                    
                    adb_devices_output = subprocess.run(["adb", "devices"], capture_output=True, text=True).stdout

                    if DEVICE_IP in adb_devices_output and "device" in adb_devices_output:
                        print(f"✅ Device {DEVICE_IP} already connected, skipping ADB scan.")
                    else:
                        print(f"🔍 Scanning ports on {DEVICE_IP}...")
                        threads = []
                        for port in PORT_RANGE:
                            t = threading.Thread(target=scan_port, args=(port,))
                            t.start()
                            threads.append(t)

                        for t in threads:
                            t.join()

                        if not found_port:
                            print("❌ No ADB port found. Is your device paired?")
                            exit()

                        print(f"✅ Found ADB port: {found_port}")
                        result = subprocess.run(["adb", "connect", f"{DEVICE_IP}:{found_port}"], capture_output=True, text=True)
                        print(result.stdout.strip())

                        if "connected" in result.stdout or "already connected" in result.stdout:
                            devices_result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
                            devices_output = devices_result.stdout.strip()
                            print(devices_output)

                            device_serial = None
                            for line in devices_output.splitlines():
                                if DEVICE_IP in line:
                                    device_serial = line.split()[0]
                                    break

                            if not device_serial:
                                print("❌ Device serial not found.")
                                exit()

                    # Perform login
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[3]/c-custom-s-s-o-login/div[3]/lightning-button/button'))
                    ).click()
                    logging.info("🟢 Clicked to disable SSO.")

                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Email' and @type='text']"))
                    ).send_keys("manharlamba@ariantechsolutions.com")
                    logging.info("✍️ Entered username.")

                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Password' and @type='password']"))
                    ).send_keys("Indian@123456")
                    logging.info("🔑 Entered password.")

                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[2]/div/div[3]/button/span'))
                    ).click()
                    logging.info("➡️ Clicked login button.")

                    # Wait for approval screen on mobile and approve using ADB
                    print("📲 Waiting for mobile approval...")
                    time.sleep(5)
                    os.system(f"adb shell input tap {TAP_X} {TAP_Y}")

                    selenium_url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"

                    WebDriverWait(driver, 30).until(EC.url_to_be(selenium_url))
                    time.sleep(15)
                    logging.info("✅ Successfully logged in.")

                else:
                    print("✅ Already logged in, continuing...")
                    logging.info("Already logged in, continuing with the workflow.")
                    

                print("📌 yaha tak end hauin")

          
                # WebDriverWait(driver, 20).until(
                #     EC.presence_of_element_located((By.TAG_NAME, "body"))
                # )
                # logging.info(f"Successfully navigated to {url}")
                # time.sleep(5)
                if not lead_url:
                    print("skipping the data  as im not  having the url")
                    continue

                driver.get(lead_url)
                time.sleep(10)

     
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[span[text()='New Event']]"))
                ).click()
                print("clicked on new event")
                logging.info("Clicked 'New Event' button.")
                time.sleep(2)
               

                try:
                    sub_btn=WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Subject']/following::input[1]"))
                    )
                    print("subject is clicked")
                    # if sub_btn.is_displayed():
                    sub_btn.click()
                    
                    time.sleep(3)
                    # else:
                    #     print("elemnt not found")

                except Exception as e:
                    print("yeh dekh error milgaye ",e)
                    
                try:
                        # Step 1: Click the dropdown field to open the list
                    dropdown_field = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Subject']/following::input[1]"))
                    )
                    dropdown_field.click()
                    logging.info("Clicked on the Subject dropdown.")
                    print("Clicked on Subject dropdown.")

                    time.sleep(2)  # Small wait to ensure the listbox loads

    # Step 2: Wait for the dropdown list to appear
                    dropdown_list = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@role='listbox' and @data-dropdown-element and contains(@class, 'slds-listbox')]"))
                    )

                    # Step 3: Find and Click the Correct Subject Option
                    subject_option_xpath = f"//lightning-base-combobox-item[@data-value='{subject}']"
                    subject_option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, subject_option_xpath))
                    )
                    subject_option.click()
                    logging.info(f"Selected subject from dropdown: {subject}")
                    print(f"Selected Subject: {subject}")

                    time.sleep(3)  # Ensure selection registers before proceeding

                except TimeoutException:
                    logging.error(f"Subject selection failed: {subject} not found in dropdown.")
                    print(f"ERROR: Subject '{subject}' not found or not clickable.")
                   
                    
                
      
                try:
                   
                    renukaaa_start_date = "06-Mar-2025"
                    start_date_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@class='slds-input' and @type='text' and @required]"))
                    )
                   
                    if start_date_btn.is_displayed():
                        start_date_btn.click()
                        start_date_btn.clear()
                        start_date_btn.send_keys(lead_start_date)
                        # print("the elemnt has found")
                        print("start date has been clicked")
                    else:
                        print("teh elemnt has not been found")
                    
                    time.sleep(5)
                except Exception as e:
                    print(f"start date not clicked {e}")
                try:

                    
                    start_time_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//label[normalize-space(text())='Time']/following-sibling::div//input"))
                    )
                    start_time_btn.click()                                 
                    if start_time_btn.is_displayed():
                        # print("the elemnt has found")
                        print("start time has been clicked")
                        renuka_start_time = "16:00" 
                        try: 
                            # WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-container")))

                        
                            element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, f"//lightning-base-combobox-item//span[@title='{lead_start_time}']"))
                            )
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            element.click()
                            print("Clicked the start timev  clciked ho raha hai bhai")
                        except Exception as e:
                            print(f"start time not clicked {e}")

                   
                    
                   
                    print("The start time input field has been found and is clickable.")
                    
                  
                 
                    time.sleep(10)
                except Exception as e:
                    print(f"start time not clicked {e}")
                    
            

                    

                  
                         
                       

                
                 
                    time.sleep(10)
                except Exception as e:
                    print(f"end time not clicked {e}")
                   
                try:
                    save_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'slds-button--brand') and .//span[text()='Save']]"))
                    )
                    if save_btn.is_displayed():
                        print("clicked on saved event created successfully")
                    else:
                        print("elemnt nahi mila")
                    
                    driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
                    driver.execute_script("window.scrollBy(0, 200);")
                    save_btn.click()
                    time.sleep(3)
                    try:
                        print("hi bhaiya")
                    
                       
                        time.sleep(5)
                        try:
                        
                            wait = WebDriverWait(driver, 10)
                            toast_link = wait.until(EC.element_to_be_clickable((
                                By.XPATH,
                                "//div[@data-key='success']//a[contains(@class, 'forceActionLink')]"
                            )))

                            # Click the toast message
                            toast_link.click()
                            print("Clicked on the toast message successfully!")
                        except Exception as e:
                            print("the error has been found",e)


                        
                    except Exception as e:
                        print("the error has been found",e)
                  
                         
                    current_url = driver.current_url
                    print(f"Captured URL: {current_url}")
                    time.sleep(10)
                    print("yaha toh aaagate yrr")
                    try:

                        file_name = "events.json"
                        lead_data = {"event_id": lead_id, "url": current_url}

                        with open(file_name, 'w') as json_file:
                            json.dump(lead_data, json_file, indent=4)

                        with open(file_name, 'r') as json_file:
                            payload = json.load(json_file)
                        print("yaha pahuch gaya ")
                    except Exception as e:
                        print("the error has been found",e)
                
                    
                    try:
                        context = ssl._create_unverified_context()
                        conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)

                        payload_json = json.dumps(payload)
                        headers = {
                            "Content-Type": "application/json",
                            "Content-Length": str(len(payload_json))
                        }

                        conn.request("PUT", "/api/salesforce-dump/events/new/flag-inactive", body=payload_json, headers=headers)
                        response = conn.getresponse()

                        if response.status == 200:
                            print("Successfully updated the lead data!")
                            data = response.read().decode()
                            logging.info(f"PUT Response: {data}")
                        else:
                            print(f"Failed to update lead data. HTTP {response.status}")
                            logging.error(f"PUT Error Response: {response.read().decode()}")
                    except Exception as e:
                        logging.error(f"PUT request error: {e}")
                        print(f"PUT request error: {e}")

                    driver.back()
                    time.sleep(10)

                    logging.info("Event saved successfully.")
                except Exception as e:
                    logging.error(f"Error processing task ID {event.get('task_id')}: {e}")
                    print(f"Error processing task ID {event.get('task_id')}: {e}")
                    continue 
                               
                    

                # # Save the lead data to a JSON file
                # outputs_folder = r"C:\SAKET\RPA\Salesforce\Renuka"
                # os.makedirs(outputs_folder, exist_ok=True)
                # file_name = os.path.join(outputs_folder, f"lead_{lead_id}.json")

                # lead_data = {"lead_id": lead_id}
                # with open(file_name, 'w') as json_file:
                #     json.dump(lead_data, json_file, indent=4)
           

                
            
        except Exception as e:
            logging.error(f"Error processing events: {e}", exc_info=True)
            



if __name__ == "__main__":
    api_url = "https://api.smartassistapp.in/api/salesforce-dump/events-data/new"
    output_directory = "C:\\SAKET\\RPA\\Salesforce\\Eventjsonallfiles"
    selenium_url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
    username = "manharlamba@ariantechsolutions.com"
    password = "Indian@123456"

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
    try:
        login_to_website(driver, selenium_url, username, password)
        process_events(api_url, output_directory, selenium_url, driver)
    except Exception as e:
        print("the error was found",e)