import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json
import subprocess
import socket
import threading
# import pyautogui  
from pynput.keyboard import Controller
import glob
import os
import json
import requests
from datetime import datetime
import ssl
import urllib3
from http.client import HTTPSConnection
import http.client
from selenium.webdriver.common.action_chains import ActionChains
import traceback

import threading
DEVICE_IP = "192.168.0.236"
PORT_RANGE = range(30000, 60000)
TAP_X, TAP_Y = 505, 296
SELENIUM_URL = "https://cxp--preprod.sandbox.my.site.com/CXP/s/login/?language=en_US&ec=302&startURL=%2FCXP%2Fs%2Flead%2FLead%2FDefault"
USERNAME = "manharlamba@ariantechsolutions.com"
PASSWORD = "Indian@12345"
found_port = None
lock = threading.Lock()


output_directory = "C:\\SAKET\\RPA\\Salesforce\\alljsonfile"

def fetch_data_with_http_client(api_url, output_directory, prefix, number_of_files, prefixs):
    """Fetch data from API using http.client and save in chunks"""

    try:
        # Bypass SSL verification using http.client and unverified SSL context
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)
        conn.request("GET", "/api/salesforce-dump/leads-data/new",headers={})
        response = conn.getresponse()

        if response.status == 200:
            data = json.loads(response.read().decode())
            # logging.info(f"Fetched {len(data)} items from API using http.client.")

            # Ensure output directory exists
            os.makedirs(output_directory, exist_ok=True)

            # Calculate items per file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
            file_name = f"{prefix}_{timestamp}.json"
            file_path = os.path.join(output_directory, file_name)

            # Save all data to a single JSON file
            try:
                with open(file_path, "w") as output_file:
                    json.dump(data, output_file, indent=4)
                # logging.info(f"All {len(data)} items written to {file_name}")
                
            except Exception as e:
                logging.error(f"Error writing data to file: {e}")
                print(f"Error writing data: {e}")
        else:
            logging.error(f"Failed to fetch data with status code: {response.status}")
            print(f"Failed to fetch data with status code: {response.status}")

    except Exception as e:
        logging.error(f"Error fetching data with http.client: {e}")
        print(f"Error fetching data: {e}")
def click_element(output_directory):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920x1080")  
    #options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=options)
    
    # Navigate to the login page
    driver.get("https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default")
    print("yaha pahucha")
    logging.info("Navigated to login page.")



    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[3]/c-custom-s-s-o-login/div[3]/lightning-button/button'))
        ).click()
        logging.info("Clicked to disable SSO.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Email' and @type='text']"))
        ).send_keys("manharlamba@ariantechsolutions.com")
        logging.info("Entered username.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Password' and @type='password']"))
        ).send_keys("Indian@123456")
        logging.info("Entered password.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="centerPanel"]/div/div[2]/div/div[2]/div/div[3]/button/span'))
        ).click()
        logging.info("Clicked login button.")
        WebDriverWait(driver, 30).until(
            EC.url_to_be("https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default")
        )
        logging.info("Desired URL reached successfully.")
            

       

      

        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Set up logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")




        
        while True:  
            api_url = "https://api.smartassistapp.in/api/salesforce-dump/leads-data/new"
            output_directory = "C:\\SAKET\\RPA\\Salesforce\\alljsonfile"
            prefix = "default_tab1"
            
            number_of_files = 5
            prefixs='default_tab'
            fetch_data_with_http_client(api_url, output_directory, prefix, number_of_files,prefixs)
            
            
        

            # Find the latest file in the directory (based on timestamp)
            json_files = glob.glob(os.path.join(output_directory, f'{prefix}_*.json'))
      

            if not json_files:
                print("file name is milgaya")
                print(f"No JSON files found with prefix '{prefix}' in the directory.")
            else:
                # Get the latest file based on modification time
                latest_file = max(json_files, key=os.path.getmtime)
                # print(f"The latest JSON file with prefix '{prefix}' is: {latest_file}")

                # Load the latest file and count the items
                try:
                   with open(latest_file, 'r') as file:
                        print("yaha hai data")
                        # print(latest_file)
                        latest_data = json.load(file)
                        # print("Latest Data in File:", json.dumps(latest_data, indent=4))
                        #logging.info(f"Loaded {len(latest_data)} items from the latest file.")
                except Exception as e:
                    logging.error(f"Error reading the latest file: {e}")
                if isinstance(latest_data,list):

                    lead_data_list = [item for item in latest_data if 'lead_id' in item]
                    if not lead_data_list:
                        print("No lead data found in the latest file.")
                        continue
                    print("kya ch al raha hai yrrr")
                else:
                    lead_data_list=[]
                    continue
                
                            
                                

                            
                            
                            
                            
                print("hi skagtejndkdmk")
                print("aab hoga ")
                currenturl = driver.current_url

              

                



                if lead_data_list:
                    failed_leads = set()
                   
                    
                    
                    for index, lead_data in enumerate(lead_data_list):
                        
                        logging.info(json.dumps(lead_data, indent=4))
                        time.sleep(2)
                        
                        # if currenturl.rstrip('/') == "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default":
                        #     print("URL is fine")
                        # else:
                        #     print("URL is wrong. Going back.")
                        #     driver.back()
                        #     time.sleep(5)

                        
                        
                                
                    
                        fname = lead_data.get('fname', '')
                        lname = lead_data.get('lname', '')
                        lead_status = lead_data.get('status', '')
                        lead_source = lead_data.get('lead_source', '')
                        print(lead_source)
                        print(lead_source)
                        enquiry_type = lead_data.get('enquiry_type', '')
                        print(enquiry_type)
                        mobile = lead_data.get('mobile', '')
                        brand = lead_data.get('brand', '')
                        purchase_type = lead_data.get('purchase_type', '')
                        print(purchase_type)
                        sub_type = lead_data.get('sub_type', '')
                        PMI = lead_data.get('PMI', '')
                        print(PMI)
                        lead_id = lead_data.get('lead_id', '')
                        email=lead_data.get('email','')

                        if brand=='Jaguar':
                            continue

                        # required_fields = {
                        #         "fname": fname,
                        #         "lname": lname,
                        #         "lead_status": lead_status,
                        #         "lead_source": lead_source,
                        #         "enquiry_type": enquiry_type,
                        #         "mobile": mobile,
                        #         "brand": brand,
                        #         "purchase_type": purchase_type,
                        #         "sub_type": sub_type,
                        #         "lead_id": lead_id
                        #     }

                        # missing_fields = [field for field, value in required_fields.items() if not value]

                        # if missing_fields:
                        #     print(f"❌ Missing data in fields: {', '.join(missing_fields)}")
                        #     continue


                    

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

                        time.sleep(10)
                        try:
                            print("new button ke passed pahucha ")
                    
                            new_button = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.XPATH, '//a[@title="New" and contains(@class, "forceActionLink")]/div[@title="New"]'))
                            )
                            logging.info("New button is located.")
                            
                            # Scroll to the element
                            actions = ActionChains(driver)
                            actions.move_to_element(new_button).perform()
                            logging.info("Scrolled to the New button.")

                            # Check visibility and click
                            if new_button.is_displayed():
                                new_button.click()
                                logging.info("Clicked the New button successfully.")
                                print("new button has been clcikded")
                            else:
                                logging.warning("New button is not visible.")
                        except Exception as e:
                            logging.error(f"Failed to locate or click the New button: {e}")
                            traceback.print_exc()
                            driver.refresh()
                            time.sleep(5)
                            continue
                        time.sleep(10)
                            



                       
                       
                       

                                

                                
                    

                        if lname and lead_status and lead_source and enquiry_type and mobile and brand and purchase_type  and lead_id:
                           
                            

                            # salution_btn='//*[@id="sectionContent-91"]/dl/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/span/slot/records-record-layout-input-name/lightning-input-name/fieldset/div/div/div[1]/lightning-picklist/lightning-combobox/div/div[1]/lightning-base-combobox'
                            # salution_btn=driver.find_element(By.XPATH, salution_btn)
                            # salution_btn.click()
                            # pyautogui.press('down')
                            # pyautogui.press('enter')
                            

                            


                            try:
                            #     # Wait for the First Name field to be visible
                                first_name_xpath = "//label[text()='First Name']/following-sibling::div//input"
                                first_name_input = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, first_name_xpath))
                                )
                                time.sleep(2)
                                first_name_input.send_keys(fname)
                                logging.info("Entered First Name successfully.")
                            except TimeoutException:
                                logging.error("First Name input field was not found.")
                            except Exception as e:
                                logging.error(f"Unexpected error when entering First Name: {e}")

                            try:
                                # Wait for the Last Name field to be visible
                                last_name_xpath = "//label[text()='Last Name']/following-sibling::div//input"
                                last_name_input = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, last_name_xpath))
                                )
                                if last_name_input.is_displayed():
                                    print("elemnt found last name")
                                else:
                                    print("elemnt not found")
                                print(lname)
                                last_name_input.send_keys(lname)
                                logging.info("Entered Last Name successfully.")
                                driver.execute_script("arguments[0].scrollIntoView();", last_name_input)
                            except TimeoutException:
                                logging.error("Last Name input field was not found.")
                            except Exception as e:
                                print("yeh error dekho sdjvnsdjknnn: {e}")
                                traceback.print_exc()

                                print(f"yeh error dekho sdjvnsdjknnn: {e}")

                            
                            logging.info("Entered Last Name successfully.")
                            

                            # Wait for and click the cancel button
                            
                            
                            
                                
                            
                            try:
    # Wait for the button to be clickable
                                button = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Lead Status' and contains(@class, 'slds-combobox__input')]"))
                                )
                                                                
                                # Click the button
                                button.click()
                                print("Button clicked successfully.")

                            except Exception as e:
                                print(f"Error occurred: {e}")
                                traceback.print_exc()
                                continue



                            # # Wait for dropdown options to be visible
                            try:
                        
                                print(f" the lead status are {lead_status}")
                                

                                # Use pyautogui to navigate if the specific status is known
                                if lead_status == "Follow Up":
                                    follow_up_xpath="//lightning-base-combobox-item[@data-value='Follow Up']"
                                    follow_up_xpath = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, follow_up_xpath)))
                                    follow_up_xpath.click()
                                    

                                    
                                    logging.info("Pressed down once for 'Follow Up'.")
                                elif lead_status == "New":
                                    new_up_xpath="//lightning-base-combobox-item[@data-value='New']"
                                    new_up_xpath = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,new_up_xpath)))
                                    new_up_xpath.click()
                                    
                                    

                                elif lead_status == "Qualified":
                                    qual_xpath="//lightning-base-combobox-item[@data-value='Qualified']"
                                    qual_xpath = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,qual_xpath)))
                                    qual_xpath.click()
                                
                                    logging.info("Pressed down twice for 'Qualified'.")
                                elif lead_status == "Lost":
                                    last_xpath="//lightning-base-combobox-item[@data-value='Lost']"
                                    last_xpath = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,last_xpath)))
                                    last_xpath.click()
                                    
                                
                                else:
                                    logging.info(f"No specific action for status '{lead_status}'.")

                                
                            except Exception as e:
                                print(f"Error occurred: {e}")
                                traceback.format_exc()
                            
                            
                                
                            try:

                                
                                fourth_dropdown = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Lead Source' and contains(@class, 'slds-combobox__input')]"))
                                )
                                
                            # Click the dropdown
                                fourth_dropdown.click()
                                print("Fourth dropdown clicked successfully.")
                                                                    
                                

                                
                                
                                # After you handle lead_status and enquiry_type, add the following for lead_source
                                if lead_source == "Email":
                                    email_dropdown = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Email']"))
                                    )
                                    email_dropdown.click()
                                
                                    
                                    

                                elif lead_source == "Existing Customer":
                                    exist_drop = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Existing Customer']"))
                                    )
                                    exist_drop.click()
                                elif lead_source == "Field Visit":
                                    feild_drop = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Field Visit']"))
                                    )
                                    feild_drop.click()

                                elif lead_source == "Google SEM Ads":
                                    Google_dropdown = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Google SEM Ads']"))
                                    )
                                    Google_dropdown.click()

                                elif lead_source == "Line":
                                    line_dropdown = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Line']"))
                                    )
                                    line_dropdown.click()
                                    
                                

                                elif lead_source == "OEM Experience":
                                    OEM = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='OEM Experience']"))
                                    )
                                    OEM.click()
                                elif lead_source == "OEM Web & Digital":
                                    OEM_web = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='OEM Web & Digital']"))
                                    )
                                    OEM_web.click()
                                    

                                elif lead_source == "Online Booking":
                                    online_booking = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Online Booking']"))
                                    )
                                    online_booking.click()

                                elif lead_source == "Online Chat":
                                    online_chat = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Online Chat']"))
                                    )
                                    online_chat.click()

                                elif lead_source == "Phone-in":
                                    xpath = "//lightning-base-combobox-item[@data-value='Phone-in']"

    # Wait for presence
                                    Phone_in = WebDriverWait(driver, 5).until(
                                        EC.presence_of_element_located((By.XPATH, xpath))
                                    )

                                    # Scroll into view
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Phone_in)

                                    # Ensure clickable
                                    Phone_in = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, xpath))
                                    )

                                    try:
                                        # Try ActionChains click
                                        ActionChains(driver).move_to_element(Phone_in).click().perform()
                                    except:
                                        # JS fallback click
                                        driver.execute_script("arguments[0].click();", Phone_in)

                                                                    

                                elif lead_source == "Phone-out":
                                    Phone_out = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Phone-out']"))
                                    )
                                    Phone_out.click()
                                    
                                    

                                elif lead_source == "Purchased List":
                                    purchase_list = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Purchased List']"))
                                    )
                                    purchase_list.click()
                                    
                                    

                                elif lead_source == "Referral":
                                    Referral_drop = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Referral']"))
                                    )
                                    Referral_drop.click()
                                    
                                    

                                elif lead_source == "Retailer Experience":
                                    retailer_experinece = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Retailer Experience']"))
                                    )
                                    retailer_experinece.click()
                                    
                                elif lead_source == "Retailer Website":
                                    Retailer_website = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Retailer Website']"))
                                    )
                                    Retailer_website.click()
                                    
                                elif lead_source == "SMS":
                                    SMS = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='SMS']"))
                                    )
                                    SMS.click()
                                    
                                    

                                elif lead_source == "Social":
                                    
                                    Social_dropdown = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Social']"))
                                    )
                                    Social_dropdown.click()

                                elif lead_source == "Social (Retailer)":
                                    Social_dropdown_retailer = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Social (Retailer)']"))
                                    )
                                    Social_dropdown_retailer.click()

                                    
                                elif lead_source == "Walk-in":
                                    walk_in = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Walk-in']"))
                                    )
                                    walk_in.click()
                                    

                                elif lead_source == "Whatsapp":
                                    Whatsapp = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Whatsapp']"))
                                    )
                                    Whatsapp.click()
                                    

                                else:
                                    logging.info(f"No specific action for lead source '{lead_source}'.")
                            except Exception as e:
                                print("no third is not working")
                                traceback.print_exc()
                                failed_leads.add(lead_id)
                                continue
                           


                            
                            


                            fifth_dropdown = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enquiry Type' and contains(@class, 'slds-combobox__input')]"))
                            )

                            # Click the Lead Source dropdown
                            fifth_dropdown.click()
                            print("Lead Source dropdown clicked successfully.")
                            


                            
                                                                    
                                



                            
                            try:
                                print(f"the  lead status are {enquiry_type}")
                                

                                if enquiry_type == "(Generic) Purchase intent within 90 days":
                                    genric = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Generic']"))
                                    )
                                    genric.click()
                                    
                                #             logging.info("Pressed down for '(Generic) Purchase intent within 90 days'.")
                                elif enquiry_type == "Accessory Offers":
                                    Accessories_type = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Accessory Offers']"))
                                    )
                                    Accessories_type.click()

                                elif enquiry_type == "Approved Pre-owned":
                                    Accessories_type = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Accessory Offers']"))
                                    )
                                    Accessories_type.click()

                                
                                # elif enquiry_type == "Approved Used Vehicle":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Approved Used Vehicle'.")
                                # elif enquiry_type == "Brochure Request":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Brochure Request'.")
                                # elif enquiry_type == "e-Brochure":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')

                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'e-Brochure'.")
                                # elif enquiry_type == "Extended Warranty":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')

                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Extended Warranty'.")
                                # elif enquiry_type == "Find & Price - Deposit":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Find & Price - Deposit'.")
                                # elif enquiry_type == "Find & Price Enquiry":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                    
                                # #         logging.info("Pressed down for 'Find & Price Enquiry'.")
                                # elif enquiry_type == "Fleet and Business Enquiry":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                    
                               
                                # elif enquiry_type == "JLR Event":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                #         logging.info("Pressed down for 'JLR Event'.")
                                elif enquiry_type == "KMI":
                                    KMI_TYPE = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='KMI']"))
                                    )
                                    KMI_TYPE.click()
                                    
                                    
                                # elif enquiry_type == "KMI+":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                
                                # elif enquiry_type == "Mobile Lead":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                
                                # elif enquiry_type == "New Vehicle Offers":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                
                                # elif enquiry_type == "Online Reservation":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')

                            
                                # elif enquiry_type == "Owner Offers":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Owner Offers'.")
                                # elif enquiry_type == "Personalised Brochure Request":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Personalised Brochure Request'.")
                                # elif enquiry_type == "Request a Call Back":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')

                                
                                # elif enquiry_type == "Resurrected Lead":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                            
                                # elif enquiry_type == "Retention":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')

                                
                                # elif enquiry_type == "Service Interception":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')

                                
                                # elif enquiry_type == "Test Drive Request":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')

                                
                                # elif enquiry_type == "Used Vehicle Offers":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')

                                
                                # elif enquiry_type == "Vehicle Configuration":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                
                                # elif enquiry_type == "Financial Services":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                
                                # elif enquiry_type == "FS Intelligent Lead":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                
                                # elif enquiry_type == "Intelligent Lead":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                
                                # elif enquiry_type == "Request A Quote (RAQ)":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Request A Quote (RAQ)'.")
                                # elif enquiry_type == "Email My Finished Build (EMF)":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Email My Finished Build (EMF)'.")
                                # elif enquiry_type == "Waiting list":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Waiting list'.")
                                # elif enquiry_type == "Pre-order intent":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                
                                # elif enquiry_type == "Finance Calculator":
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('down')
                                #     pyautogui.press('enter')
                                # #         logging.info("Pressed down for 'Finance Calculator'.")
                                else:
                                    logging.info(f"No specific action for enquiry type '{enquiry_type}'.")
                            except Exception as e:
                                print("no  exception",e)
                                traceback.print_exc()
                                failed_leads.add(lead_id)
                                continue
                            
                            print(f"the brand is {brand}")

                            input_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//input[@class='slds-combobox__input slds-input' and @placeholder='Search Vehicle Specifications...']"))
                            )
                            input_element.click()
                            if  brand == "Land Rover":
                                input_element.send_keys("Land")
                                icon_element = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.XPATH, "//lightning-icon[@icon-name='custom:custom67']"))
                                )


                            # Click the icon
                                icon_element.click()

                            
                            elif brand=="Jaguar":
                                input_element.send_keys("Jag")
                                time.sleep(2)
                                icon_element = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.XPATH, "//lightning-icon[@icon-name='custom:custom67']"))
                                )
                                icon_element.click()
                                
                               
                            else:
                                print(" not found brand ")
                            # elemnt=WebDriverWait(driver,10).until(
                            #     EC.element_to_be_clickable(By.XPATH,"//input[@placeholder='Search Vehicle Specifications...']")
                            # )
                            # element.click()

                            # if PMI=='Range Rover Velar':
                            #     input_element.send_keys("Range Rover Velar")
                            #     time.sleep(2)
                            #     icon_element=WebDriverWait(driver,10).until(
                            #         ec.visibility_of_element_located((By.XPATH,"//input[@data-value='Range Rover Velar']"))
                            #     )
                            #     icon_element.click()
                            # else:
                            #     print("no pmi found")


                            
                            

                            print(PMI)

                            # try:
                            #     # Locate and click the PMI input element
                            #     input_element = WebDriverWait(driver, 10).until(
                            #         EC.element_to_be_clickable((By.XPATH, "//input[@data-value='Range Rover Velar']"))
                            #     )
                            #     input_element.click()
                            #     input_element.clear()
                            #     input_element.send_keys(PMI)
                            #     logging.info(f"Entered PMI: {PMI}")
                            #     print(f"Entered PMI: {PMI}")
                            # except Exception as e:
                            #     print("the error is ",e)
                            try:
                                pmidata=WebDriverWait(driver,10).until(
                                    EC.element_to_be_clickable((By.XPATH,'//lightning-base-combobox//input[@placeholder="Search Vehicle Specifications..."]'))
                                )
                                if pmidata.is_displayed():
                                    print("bhail milgfaa ")
                                    pmidata.click()
                                    pmidata.send_keys(PMI[:4])
                                    time.sleep(1)
                                else:
                                    print("nahi mila yrr")
                            except Exception as e:
                                print("the errro hgas been found",e)
                            try:
                                option_data = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, f"//lightning-base-combobox-item[normalize-space(.//span[contains(@class,'slds-listbox__option-text')])='{PMI}']"))
                                )
                                if option_data.is_displayed():
                                    print("elemnt milgaya bhai")
                                    option_data.click()
                                else:
                                    print("elemnt nahi mila bhai ")
                                
                               
                            except Exception as e:
                                print("the elemnt has not been found",e)
                                logging.error(f"Error in processing PMI: {e}", exc_info=True)
                                failed_leads.add(lead_id)
                                traceback.print_exc()
                                continue
                            
                            

                                                                
                            try:
                               
                                mobile_xpath = "//input[@name='Email' and @type='text']"
                                
                                # Explicit wait for the element to be visible and clickable
                                mobile_element = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, mobile_xpath))
                                )
                                if mobile_element.is_displayed:
                                
                                    # Send the email to the input field
                                    mobile_element.send_keys(email)
                                    print("email has enter succesfully")
                                else:
                                    print("email is not visible")
                                
                                
                                logging.info("Entered email successfully.")
                            except Exception as e:
                                logging.error(f"The email input field was not found or there was an issue: {e}")
                                print("The email input field has not been found:", e)
                           


                            # type_button = "//button[contains(@class, 'slds-combobox__input') and contains(@aria-label, 'Type') and @data-value='Product']"
                            # type_button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, type_button)))
                            # type_button.send_keys(type)
                            # logging.info("Entered First Name successfully.")
                            


                            # if type=='Product':
                            #     product_button = "//lightning-base-combobox-item[@data-value='Product']"
                            #     product_button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, product_button)))
                            #     product_button.click()
                                
                            # elif type=='Service':
                            #     Service_button = "//lightning-base-combobox-item[@data-value='Services']"
                            #     Service_button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, Service_button)))
                            #     Service_button.click()
                                
                            # elif type=='Experience':
                            #     EXPERIENCE_button = "//lightning-base-combobox-item[@data-value='Experience']"
                            #     EXPERIENCE_button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, EXPERIENCE_button)))
                            #     EXPERIENCE_button.click()
                            # elif type=='offer':
                            #     offer_btn = "//lightning-base-combobox-item[@data-value='offer']"
                            #     offer_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, offer_btn)))
                            #     offer_btn.click()
                            # else:
                            #     print("Product not found")
                            try:
                            


                                purchase_button = "//button[contains(@class, 'slds-combobox__input') and contains(@aria-label, 'Purchase Type') and @data-value='--None--']"
                                purchase_button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, purchase_button)))
                                driver.execute_script("arguments[0].scrollIntoView(true);", purchase_button)


                                purchase_button.send_keys(purchase_type)
                                logging.info("Entered First Name successfully.")
                                

                                print(f"the  purchase type is {purchase_type}")
                                


                                if purchase_type=='New Vehicle':
                                    purchase_btn = "//lightning-base-combobox-item[@data-value='New Vehicle']"
                                    purchase_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, purchase_btn)))
                                    purchase_btn.click()
                                    
                                elif purchase_type=='Used Vehicle':
                                    used_btn = "//lightning-base-combobox-item[@data-value='Used Vehicle']"
                                    used_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, used_btn)))
                                    used_btn.click()
                                    
                                    
                                else:
                                    print("Purchase type not found")
                            except Exception as e:
                                print("the error has been found",e)
                            # try:


                            #     subtype="//button[contains(@class, 'slds-combobox__input') and contains(@aria-label, 'Sub Type') and @data-value='--None--']"
                            #     subtype= WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.XPATH,subtype)))
                            #     driver.execute_script("arguments[0].scrollIntoView(true);", subtype)

                            #     # subtype.send_keys(sub_type)
                            #     # logging.info("Entered subtype successfully.")
                                


                            #     if sub_type=='Retail':
                            #         Retail_btn = "//lightning-base-combobox-item[@data-value='Retail']"
                            #         Retail_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, Retail_btn)))
                            #         Retail_btn.click()
                                    
                            #     elif sub_type=='Fleet':
                            #         fleet_btn = "//lightning-base-combobox-item[@data-value='Fleet']"
                            #         fleet_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, fleet_btn)))
                            #         fleet_btn.click()
                            #     elif sub_type=='Approved Pre-Owned':
                            #         Approve_btn = "//lightning-base-combobox-item[@data-value='AUV']"
                            #         Approve_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, Approve_btn)))
                            #         Approve_btn.click()
                                    
                            #     elif sub_type=='Service/Repair':
                            #         service_btn = "//lightning-base-combobox-item[@data-value='Service/Repair']"
                            #         service_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, service_btn)))
                            #         service_btn.click()
                                    
                            #     elif sub_type=='Branded Goods':
                            #         Branded_btn = "//lightning-base-combobox-item[@data-value='Branded Goods']"
                            #         Branded_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, Branded_btn)))
                            #         Branded_btn.click()
                                    
                            #     elif  sub_type=='Parts':
                            #         parts_btn = "//lightning-base-combobox-item[@data-value='Parts']"
                            #         parts_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, parts_btn)))
                            #         parts_btn.click()
                            #         # pyautogui.press('enter')
                            #     elif sub_type=='Special Vechile Ops':
                            #         Special_btn = "//lightning-base-combobox-item[@data-value='SV']"
                            #         Special_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, Special_btn)))
                            #         Special_btn.click()
                            #     elif sub_type=='Accessories':
                            #         # pyautogui.press('down')
                            #         Accesiories_btn = "//lightning-base-combobox-item[@data-value='Accessories']"
                            #         Accesiories_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, Accesiories_btn)))
                            #         Accesiories_btn.click()
                            #     elif  sub_type=='EVHC':
                            #         # pyautogui.press('down')
                            #         EVCH_btn= "//lightning-base-combobox-item[@data-value='EVHC']"
                            #         EVCH_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, EVCH_btn)))
                            #         EVCH_btn.click()
                            # except Exception as e:
                            #     print("the error has been found",e)
                            #     continue

                            try:
                            
                            
                                save_btn_xpath = "//li[@data-target-selection-name='sfdc:StandardButton.Lead.SaveEdit']//button[@name='SaveEdit']"
                                save_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, save_btn_xpath)))
                                
                                if save_btn.is_displayed() and save_btn.is_enabled():
                                    logging.info("Save button is visible and enabled.")
                                    save_btn.click()  
                                    print("save button has been clciked succesfully")
                                    time.sleep(3)
                                    logging.info("Save button clicked successfully.")
                                else:
                                    logging.error("Save button is either not displayed or disabled.")
                                WebDriverWait(driver, 20).until(EC.url_changes(driver.current_url))
                                logging.info("URL has changed, page is reloading or redirecting.")
                                time.sleep(2)
                            except Exception as e:
                                failed_leads.add(lead_id)
                                driver.refresh()
                                time.sleep(5)
                                continue
                                
                            
                            # WebDriverWait(driver, 10).until(
                            #     EC.element_to_be_clickable((By.XPATH, "//button[span[text()='New Task']]"))
                            # ).click()
                            # json_file_path = r"C:\SAKET\RPA\Salesforce\alljsonfile\tasksdata.json"


                            

                                # Process each follow-up entry
                            # for entry in followups_data:
                            #     lead_id_followup = entry.get('task_id','')
                            #     lead_email = entry.get('lead_email', '').lower()
                            #     print(lead_email)
                            #     subject = entry.get('subject', '')
                            #     due_date = entry.get('due_date', '')
                            #     status = entry.get('status', '')
                            # subject_btn = WebDriverWait(driver, 10).until(
                            #         EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Subject']/following::input[1]"))
                            #     )
                            # subject_btn.clear()
                            # subject_btn.send_keys(subject)
                            # logging.info(f"Entered subject: {subject}")
                            

                                
                            # if due_date:
                            #     due_date_input = WebDriverWait(driver, 10).until(
                            #         EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Due Date']/following::input[1]"))
                            #     )
                            #     due_date_input.clear()
                            #     due_date_input.send_keys(due_date)
                                
                            
                            

                           
                            # try:
                            #     status_dropdown = WebDriverWait(driver, 10).until(
                            #         EC.element_to_be_clickable((By.XPATH, "//a[@role='combobox' and contains(@class, 'select')]"))
                            #     )
                            #     status_dropdown.click()
                            #     logging.info("Status dropdown opened successfully.")

                            #     if status:
                            #         option_xpath = f"//a[normalize-space(text())='{status}']"
                            #         WebDriverWait(driver, 10).until(
                            #             EC.element_to_be_clickable((By.XPATH, option_xpath))
                            #         ).click()
                            #         logging.info(f"Selected status: {status}")
                                
                            # except Exception as e:
                            #     logging.error(f"Error selecting status '{status}': {e}")

                            
                            # save_btn = WebDriverWait(driver, 10).until(
                            #     EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'slds-button--brand') and .//span[text()='Save']]"))
                            # )
                            # driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
                            # save_btn.click()
                            # time.sleep(5)
                            # logging.info("Save button clicked successfully.")
                            # print("Save button clicked successfully.")
                            
                        

                            

                            

                            

                            try:
                                current_url = driver.current_url

                                
                                print(f"the lead_id: {lead_id}")

                            
                                urlname = current_url
                                print(f"the url hain yeh bhai{urlname}")
                            
                                file_name = f"lead_{lead_id}.json"
                                lead_data = {"lead_id": lead_id, "url": urlname}

                            
                                with open(file_name, 'w') as json_file:
                                    json.dump(lead_data, json_file, indent=4)

                                print(f"Successfully stored lead_id: {lead_id} in file: {file_name}")

                                
                                with open(file_name, 'r') as json_file:
                                    payload = json.load(json_file)

                                
                                api_url = "https://api.smartassistapp.in/api/salesforce-dump/leads/new/flag-inactive"


                                
                                try:
                                    context = ssl._create_unverified_context()
                                    conn = http.client.HTTPSConnection("dev.smartassistapp.in", context=context)

                                    
                                    payload_json = json.dumps(payload)

                                
                                    headers = {
                                        "Content-Type": "application/json",
                                        "Content-Length": str(len(payload_json))
                                    }

                                    
                                    conn.request("PUT", api_url, body=payload_json, headers=headers)

                                    
                                    response = conn.getresponse()
                                    if response.status == 200:
                                        print("Successfully updated the lead data!")
                                        data = response.read().decode()
                                        logging.info(f"Response: {data}")
                                    else:
                                        print(f"Failed to update lead data. HTTP {response.status}")
                                        logging.error(f"Response: {response.read().decode()}")

                                except Exception as e:
                                    logging.error(f"Error during PUT request: {e}")
                                    print(f"Error during PUT request: {e}")
                                    
                                    continue
                            except Exception as e:
                                print("the error has been found",e)
                                traceback.print_exc()
                                
                                continue
                            driver.back()
                            time.sleep(5)
                            driver.refresh()
                            time.sleep(5)
                           



                                                                    





                            
                        

                            
                           
                              

                            

                            




                            
                        



                            # if index == len(lead_data_list) - 1:
                            #     logging.info("Processing last item, will not click 'New' button.")
                            #     # You can perform any additional logic here if needed
                            # else:
                            #     # Click the 'New' button if it's not the last item
                            #     new_buttons = driver.find_element(By.XPATH, "//a[@title='New' and contains(@class, 'forceActionLink') and descendant::div[@title='New']]")
                            #     new_buttons.click()
                            #     logging.info("New button clicked.")
                            #     failed_leads.add(lead_id)
                            #     driver.refresh()
                            #     time.sleep(5)
                            #     continue
                           





                            
                            
                            
                        
                    
                        else:
                            logging.error("First name, last name, or lead status not found in lead data.")
                            failed_leads.add(lead_id)
                            traceback.print_exc()
                            driver.refresh()
                            time.sleep(10)
                            continue
                    
                        

                else:
                    error_msg = f"Missing required data for {fname} {lname} with lead_id {lead_id}. Required fields: fname, lname, lead_status, lead_source, enquiry_type, mobile, brand, type, purchase_type, sub_type, PMI."
                    logging.error(error_msg)
                    traceback.print_exc()
                    failed_leads.add(lead_id)
                    driver.refresh()
                    time.sleep(5)
                    continue
                    
        



        


          
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        traceback.print_exc()
        
       
        
        

def main():
    output_directory = "C:\\SAKET\\RPA\\Salesforce\\alljsonfile"
    
   
        
    click_element(output_directory)
    logging.info("Waiting for 1 hour before next execution...")
        

       
         

if __name__ == "__main__":
    main()