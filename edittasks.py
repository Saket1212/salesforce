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
from selenium.webdriver import ActionChains
import http.client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException


logging.basicConfig(filename='event_execution_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

def process_events(api_url, output_directory, selenium_url, driver):
    while True:
        try:
 
            logging.info("Fetching data from API.")
            context = ssl._create_unverified_context()
            conn = http.client.HTTPSConnection(api_url.replace("https://", "").split("/")[0], context=context)
            endpoint = "/" + "/".join(api_url.split("/")[3:])
            print("debug")

            conn.request("GET", endpoint)
            response = conn.getresponse()

            if response.status == 200:
                events_data = json.loads(response.read().decode())
                logging.info(f"Fetched {len(events_data)} entries from API.")
            else:
                logging.error(f"Failed to fetch data with status code: {response.status}")
                continue


            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            json_file_path = os.path.join(output_directory, f"events_data_{int(time.time())}.json")
            with open(json_file_path, 'w') as json_file:
                json.dump(events_data, json_file, indent=4)
            logging.info(f"API data saved to {json_file_path}")
            print(f"API data saved to {json_file_path}")


            noturladata=set()


            for event in events_data:
                logging.info(f"Processing event: {event}")
                lead_email = event.get('lead_email', '').lower()
                subject = event.get('subject', '')  
                due_date_ome = event.get('due_date', '')
                status_ome = event.get('status', '')
                task_id = event.get('task_id', '')
                comments=event.get('comments').lower()
                priority=event.get('priority','')
                print("bhai yeh le url eh chal raha hain yeh dekho yaha pe hain sahi chalega aab bhai ")
                url=event.get('url','')
                print(f"url:{url}")

                if not url :
                    print("missint the url proceeding with the next data")
                    noturladata.add(task_id)
                    continue

                

                logging.info(f"Navigating to URL: {url}")
                driver.get(url)
                time.sleep(10)

                driver.execute_script("window.scrollBy(0, 300);")
                try:

                    pencil_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'inline-edit-trigger') and .//span[text()='Edit Status']]"))
                    )
                    if pencil_btn.is_displayed():
                        print("hogaya bhai")


                        pencil_btn.click()
                    else:
                        print("not clciked")
                    time.sleep(2)
                except Exception as e:
                    print("the error has been found",e)
                    noturladata.add(task_id)
                    
                    continue
                
                textarea_xpath = "//label[normalize-space()='Comments']/following::textarea[1]"

                textarea = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, textarea_xpath))
                )
                textarea.clear()
                textarea.send_keys(comments)

                
               
                dropdown_xpath = "//a[@role='combobox' and contains(@class, 'select')]"

                
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, dropdown_xpath))
                )
                dropdown.click()

                
                status_value =status_ome

                
                options_xpath = "//a[@role='option' and @title]"

                options = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, options_xpath))
                )

             
                option_found = False
                for option in options:
                    if option.get_attribute("title").lower() == status_value.lower():
                        print(f"Found matching option: {option.get_attribute('title')}")
                        option.click()
                        option_found = True
                        break

                if not option_found:
                    print(f"Could not find option with text: {status_value}")
                
                try:


              
                    priority_dropdown_xpath = "//span[text()='Priority']/ancestor::div[contains(@class, 'slds-form-element')]//a[@role='combobox']"
                    priority_dropdown = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, priority_dropdown_xpath))
                    )
                    priority_dropdown.click()

                   
                    time.sleep(0.5)

                    
                    priority_value = priority

                    option_xpath = f"//div[@role='listbox']/descendant::a[@role='option' and @title='{priority_value}']"

                    try:
                       
                        option = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, option_xpath))
                        )
                        
                        
                        print(f"Found priority option: {option.get_attribute('title')}")
                        
                       
                        driver.execute_script("arguments[0].click();", option)
                        print(f"Clicked {priority_value} option with JavaScript")
                        
                      
                        
                    except Exception as e:
                        print(f"Error selecting priority option: {str(e)}")
                except Exception as e:
                    print("error has been found for the priorityy",e)
                        
                       
                    try:
                        
                        all_options_xpath = "//div[@role='listbox']/descendant::a[@role='option']"
                        all_options = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, all_options_xpath))
                        )
                        
                      
                        print(f"Found {len(all_options)} total options")
                        
                        
                        priority_index_map = {
                            "--None--": 0,
                            "High": 1,
                            "Normal": 2,
                            "Low": 3
                        }
                        
                        if priority_value in priority_index_map and priority_index_map[priority_value] < len(all_options):
                            target_option = all_options[priority_index_map[priority_value]]
                            driver.execute_script("arguments[0].click();", target_option)
                            print(f"Clicked {priority_value} option by index")
                        else:
                            print(f"Could not find {priority_value} option by index")
                    except Exception as inner_e:
                        print(f"Fallback approach also failed: {str(inner_e)}")
                                                    
                                                
                                    


               
                
                try: 
                    save_status_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'label') and text()='Save']")) 
                    )
                    save_status_btn.click() 
                    logging.info("Status changes saved successfully.")
                    print("Status saved successfully.") 
                    time.sleep(3) 
                except TimeoutException:
                    logging.error("Failed to find or click the Save button for Status.") 
                    continue
                current_url = driver.current_url
                print(f"Captured URL: {current_url}")
                time.sleep(10)

                file_name = "TASKS.json"
                lead_data = {"task_id": task_id, "url": current_url}

                with open(file_name, 'w') as json_file:
                    json.dump(lead_data, json_file, indent=4)

                with open(file_name, 'r') as json_file:
                    payload = json.load(json_file)

                
                try:
                    context = ssl._create_unverified_context()
                    conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)

                    payload_json = json.dumps(payload)
                    headers = {
                        "Content-Type": "application/json",
                        "Content-Length": str(len(payload_json))
                    }

                    conn.request("PUT", "https://api.smartassistapp.in/api/salesforce-dump/tasks/updated/flag-inactive", body=payload_json, headers=headers)
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


                            
               

        except Exception as e:
            logging.error(f"Error processing events: {e}", exc_info=True)
            print(e)
            time.sleep(60)
            

if __name__ == "__main__":
    api_url = "https://api.smartassistapp.in/api/salesforce-dump/tasks-data/updated"
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
        print("Error found:", e)
# import pandas as pd
# from datetime import datetime

# def csv_modified(csv_file):
#     try:
#         # Load CSV file
        
#         df = pd.read_csv(csv_file)
#         df.to_excel('latest_file.xlsx', index=False)

#         # Load Dealer Payment file
#         df_raw = pd.read_excel('Dealer Payment.xlsx', header=None)
#         new_header = df_raw.iloc[0].fillna('') + ' ' + df_raw.iloc[1].fillna('')
#         new_header = new_header.str.strip()
#         df1 = df_raw[2:]
#         df1.columns = new_header
#         df1.reset_index(drop=True, inplace=True)

#         # Automatically detect relevant columns
#         rs_columns = [col for col in df1.columns if 'Rs.' in col and 'As on' in col]
#         code_columns = [col for col in df1.columns if any(x in col for x in ['ACC CODE', 'SBI CODE', 'HDFC CODE', 'New AXIS CODE'])]

#         # Validate required columns
#         if 'Account' not in df.columns or 'Amount in doc. curr.' not in df.columns:
#             print("Required columns not found in CSV.")
#             return

#         # Map account to amount
#         amount_dict = dict(zip(df['Account'].astype(str), df['Amount in doc. curr.']))

#         # Match codes with amounts
#         for idx, row in df1.iterrows():
#             for code_col, rs_col in zip(code_columns, rs_columns):
#                 acc_code = str(row[code_col]).strip()
#                 if acc_code in amount_dict:
#                     df1.at[idx, rs_col] = -amount_dict[acc_code]
#                 else:
#                     df1.at[idx, rs_col] = 0.00

#         # Save output with timestamp
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         final_csv = f"new_updated_{timestamp}.csv"
#         df1.to_csv(final_csv, index=False)
#         print(f"Modified file saved as: {final_csv}")
#         print(df1[rs_columns].head())

#     except Exception as e:
#         print("The error has been found:", str(e))

# def csv_modified(csv_file):
#     try:
#         df = pd.read_csv(csv_file)
#         df.to_excel('latest_file.xlsx', index=False)

#         df_raw = pd.read_excel('Dealer Payment.xlsx', header=None)
#         new_header = df_raw.iloc[0].fillna('') + ' ' + df_raw.iloc[1].fillna('')
#         new_header = new_header.str.strip()
#         df1 = df_raw[2:]
#         df1.columns = new_header
#         df1.reset_index(drop=True, inplace=True)

        
#         rs_columns = [col for col in df1.columns if 'Rs.' in col and 'As on' in col]
#         code_columns = [col for col in df1.columns if 'ACC CODE' in col or 'SBI CODE' in col or 'HDFC CODE']

#         if 'Account' not in df.columns or 'Amount in doc. curr.' not in df.columns:
#             print(" Required columns not found in CSV.")
#             return

#         amount_dict = dict(zip(df['Account'].astype(str), df['Amount in doc. curr.']))

#         for idx, row in df1.iterrows():
#             matched = False
#             for code_col, rs_col in zip(code_columns, rs_columns):
#                 acc_code = str(row[code_col]).strip()
#                 if acc_code in amount_dict:
#                     amt = amount_dict[acc_code]
#                     new_amt = -amt 
#                     df1.at[idx, rs_col] = new_amt
#                     # matched = True
#                 else:
#                     df1.at[idx, rs_col] = 0.00  
                    
#         # Generate timestamp for the final CSV filename
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         final_csv = f"new_updated_{timestamp}.csv"  # Include timestamp
#         df1.to_csv(final_csv, index=False)
#         print(f"Modified file saved as: {final_csv}")
#         print(df1[rs_columns].head())
#         return final_csv

#     except Exception as e:
#         print(" Error in csv_modified:", str(e))



# # Call the function here
# csv_modified("Downloads\\yellow_rows_20250505_160526.csv")
