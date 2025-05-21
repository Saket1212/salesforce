import logging
import os
import ssl
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

import time
import http.client

# Set up logging
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

def safe_interaction(driver, xpath, value):
    """
    Safely interact with elements on the page to handle potential stale element references.

    Parameters:
    - driver: WebDriver instance
    - xpath: XPath of the element to interact with
    - value: The value to set in the element (input or similar)
    """
    for attempt in range(3):  # Retry up to 3 times
        try:
            # Wait for the element to be clickable
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            # Clear the field and input the value
            element.clear()
            element.send_keys(value)
            logging.info(f"Successfully interacted with element: {xpath}")
            return True  # Exit after successful interaction
        except StaleElementReferenceException:
            logging.warning(f"Stale element reference on attempt {attempt + 1} for XPath: {xpath}. Retrying...")
        except TimeoutException:
            logging.error(f"Timeout waiting for element at XPath: {xpath}. Retrying...")
    logging.error(f"Failed to interact with element after multiple attempts: {xpath}")
    return False  # Return False if all attempts fail

def process_events(api_url, output_directory, selenium_url, driver):
    wait = WebDriverWait(driver, 10)  # Define wait object once

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
                raise Exception(f"Failed to fetch data: {response.status}")
           
            # Save API data to file
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            json_file_path = os.path.join(output_directory, f"events_data_{int(time.time())}.json")
            with open(json_file_path, 'w') as json_file:
                json.dump(events_data, json_file, indent=4)
            logging.info(f"API data saved to {json_file_path}")
            print(f"API data saved to {json_file_path}")
            
            if not events_data:  # If no events data
                logging.info("No new events to process. Exiting loop.")
                break
            

            updatedevent=set()

            for event in events_data:
                    logging.info(f"Processing event: {event}")
                    lead_email = event.get('lead_email', '').lower()
                    subject = event.get('subject', '')
                    lead_start_date = event.get('start_date', '')
                    lead_start_time = event.get('start_time', '')
                    lead_end_date = event.get('end_date', '')
                    lead_end_time = event.get('end_time', '')
                    event_id = event.get('event_id', '')
                    lead_status=event.get('status','')
                    url=event.get('url','')

                    if not url:
                        print(f"there is no url for this data we are skipping{event_id}")
                        continue

                  
                    
                    # Navigate to URL
                    logging.info(f"Navigating to URL: {url}")
                    driver.get(url)
                    time.sleep(10)
                    
                    # WebDriverWait(driver, 20).until(
                    #     EC.presence_of_element_located((By.TAG_NAME, "body"))
                    # )
                    # logging.info(f"Successfully navigated to {url}")
                    # time.sleep(5)

                    # # Wait for the element to be clickable
                    # new_button = WebDriverWait(driver, 30).until(
                    #     EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "subjectLink") and contains(@title, "[No subject]")]'))
                    # )
                    # print("Test Drive button is located.")
                    # logging.info("Test Drive button is located.")
                    
                    # # Scroll to the element
                    # actions = ActionChains(driver)
                    # actions.move_to_element(new_button).perform()
                    
                    # # Check visibility and click
                    # if new_button.is_displayed():
                    #     print("element found")
                    #     new_button.click()
                    #     time.sleep(20)
                    #     logging.info("Clicked the Test Drive button successfully.")
                    #     print("Test Drive button is clicked")
                    # else:
                    #     print("not found")
                    #     time.sleep(20)
                    #     logging.warning("Test Drive button is not visible.")
                        # print("Test Drive button is not visible")
                    

                    try:
                        # Try to find and click the pencil icon (Edit Subject)
                        edit_subject_btn = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'test-id__inline-edit-trigger') and @title='Edit Subject']"))
                        )
                        print("It's working, clicking the pencil icon.")
                        edit_subject_btn.click()

                        logging.info("Clicked on the Assigned to button.")
                        print("Pencil icon clicked, waiting to proceed...")
                        time.sleep(3)
                        driver.execute_script("window.scrollBy(0, 300);")
                       
                        pencil_clicked = True
                    except TimeoutException:
                        logging.warning("Assigned button for Subject not found or not clickable.")
                        updatedevent.add(event_id)
                        continue
                        pencil_clicked = False
                    try:
                                   
                        VALID_STATUSES = {"Planned", "Approved", "Not Required", "Finished", "No Show"}


                        try:
                        
                            status_dropdown = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//a[@role='combobox' and contains(@class,'select')]"))
                            )
                            driver.execute_script("arguments[0].click();", status_dropdown)


                            options = WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'uiMenuList')]//a[@role='option']"))
                            )


                            option_map = {}
                            for opt in options:
                                text = opt.text.strip()
                                if text in VALID_STATUSES:
                                    option_map[text] = opt

                        
                            if lead_status in option_map:
                                chosen = option_map[lead_status]
                                driver.execute_script("arguments[0].click();", chosen)
                                logging.info(f"✅ Selected status: {lead_status}")
                            else:
                                logging.warning(f"⚠️ Desired status '{lead_status}' not available. Available: {list(option_map)}")

                        except Exception as e:
                            logging.error(f"Error while selecting status '{lead_status}': {e}")
                    except Exception as e:
                        logging.error(f"Error selecting status dropdown: {e}")
                        print("Error selecting status dropdown:", e)

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
                    try:
                
                               
                        save_btn = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'uiButton') and .//span[text()='Save']]"))
                        )
                        save_btn.click()
                        logging.info("Event saved successfully.")
                        print("Event saved successfully.")
                    except Exception as e:
                        print("the error has been fpund",e)


                    current_url = driver.current_url
                    print(f"Captured URL: {current_url}")
                    time.sleep(10)

                    file_name = "eventsupdated.json"
                    lead_data = {"event_id": event_id, "url": current_url}

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

                        conn.request("PUT", "https://api.smartassistapp.in/api/salesforce-dump/events/updated/flag-inactive", body=payload_json, headers=headers)
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


                            

                    # Now, proceed to the search button only if the pencil icon was successfully clicked
                 
                                #     EC.presence_of_all_elements_located((By.XPATH, "//lightning-base-combobox-item"))
                                # )

                                # # Iterate through the options and select the matching one
                                # for option in dropdown_options:
                                #     if desired_option.lower() in option.text.lower():
                                #         print(f"Selecting option: {option.text}")
                                #         option.click()
                                #         time.sleep(2)  # Allow time for selection
                                #         logging.info(f"Successfully selected: {option.text}")
                                #         break
                                # else:
                                #     print(f"Option '{desired_option}' not found.")
                                #     logging.warning(f"Option '{desired_option}' not found in dropdown.")
                               

                                
                                



                            
                    # dropdown_list = WebDriverWait(driver, 10).until(
                    #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'slds-listbox_vertical') and @role='listbox']"))
                    # )

                    # subject_option_xpath = f"//lightning-base-combobox-item[@data-value='{subject}']"
                    # subject_option = WebDriverWait(driver, 10).until(
                    #     EC.element_to_be_clickable((By.XPATH, subject_option_xpath))
                    # )
                    # subject_option.click()
                    # logging.info(f"Selected subject from dropdown: {subject}")
                    # print(f"Selected Subject: {subject}")

                    time.sleep(3)  # Ensure selection registers before proceeding



        except Exception as e:
            logging.error(f"Error processing events: {e}", exc_info=True)
            continue 
            


        
                # sub_btn = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Subject']/following::input[1]"))
                # )
                # sub_btn.click()
                # time.sleep(2)

                
                # print(subject)

                # try:
                   
                #     if subject == 'Meeting':
                #         btn = WebDriverWait(driver, 10).until(
                #             EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Meeting']"))
                #         )
                        
                       
                #         driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                        
                       
                #         time.sleep(2)
                        
                     
                #         btn.click()
                #         time.sleep(10)
        
                        




        #             elif subject == 'Test Drive':
        #                 btn = WebDriverWait(driver, 10).until(
        #                     EC.element_to_be_clickable(By.XPATH, "//lightning-base-combobox-item[@data-value='Test Drive']")
        #                 )
        #                 btn.click()

        #             elif subject == 'Showroom appointment':
        #                 btn = WebDriverWait(driver, 10).until(
        #                     EC.element_to_be_clickable(By.XPATH, "//lightning-base-combobox-item[@data-value='Showroom appointment']")
        #                 )
        #                 btn.click()

        #             elif subject == 'Service Appointment':
        #                 btn = WebDriverWait(driver, 10).until(
        #                     EC.element_to_be_clickable(By.XPATH, "//lightning-base-combobox-item[@data-value='Service Appointment']")
        #                 )
        #                 btn.click()

        #             elif subject == 'Quotation':
        #                 btn = WebDriverWait(driver, 10).until(
        #                     EC.element_to_be_clickable(By.XPATH, "//lightning-base-combobox-item[@data-value='Quotation']")
        #                 )
        #                 btn.click()

        #             elif subject == 'Trade in evaluation':
        #                 btn = WebDriverWait(driver, 10).until(
        #                     EC.element_to_be_clickable(By.XPATH, "//lightning-base-combobox-item[@data-value='Trade in evaluation']")
        #                 )
        #                 btn.click()

        #             else:
        #                 print("No matching subject found.")
                        
        #         except Exception as e:
        #             print("An error has occurred:", e)


                


                   
        #             dropdown_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Test Drive']")))
        #             dropdown_option.click() 
        #         except Exception as e:
        #             print("tehe erro has been found",e)

    
                
        #         option_xpath = f'//*[@id="dropdown-element-522"]'
        #         print(option_xpath)
        #         if option_xpath.is_displayed():
        #             print("The element has been found")
        #         else:
        #             print("the elemnt has not found")

        #         Step 4: Wait for the option and click it
        #         option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        #         option.click()
        #         print(f"Selected option: {subject}")
        #         start_date_btn = WebDriverWait(driver, 20).until(
        #             EC.element_to_be_clickable((By.XPATH, "//lightning-input[@class='slds-form-element uiInput sfaEventDateTime uiInput--default']//label[contains(text(), 'Start')]/ancestor::div[@class='slds-form-element__control']//lightning-datepicker"))
        #         )
        #         start_date_btn.click()
        #         start_date_btn.send_keys(lead_start_date)

        #         logging.info(f"Entered start date: {lead_start_date}")
        #         if start_date_btn.is_displayed():
        #             print("elemnt has found")
        #         else:
        #             print("elemn ha s bot been found")

        #         start_time_btn = WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, "//lightning-input[@class='slds-form-element uiInput sfaEventDateTime uiInput--default']//label[contains(text(), 'Start')]/ancestor::div[@class='slds-form-element__control']//lightning-timepicker"))
        #         )
        #         start_time_btn.send_keys(lead_start_time)
        #         logging.info(f"Entered start time: {lead_start_time}")
        #         time.sleep(10)

        #         # Optionally, handle end date and end time if needed
        #         # end_date_btn = WebDriverWait(driver, 10).until(
        #         #     EC.element_to_be_clickable((By.XPATH, "//lightning-datepicker//label[@for='input-532']/following-sibling::div//input[@type='text']"))
        #         # )
        #         # end_date_btn.send_keys(lead_end_date)
        #         # end_time_btn = WebDriverWait(driver, 10).until(
        #         #     EC.element_to_be_clickable((By.XPATH, "//lightning-timepicker//label[@for='combobox-input-536']/following-sibling::div//input[@role='combobox']"))
        #         # )
        #         # end_time_btn.send_keys(lead_end_time)

        #         # Save the event
        #         save_btn = WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'slds-button--brand') and .//span[text()='Save']]"))
        #         )
        #         save_btn.click()
        #         logging.info("Event saved successfully.")

        #         # Save the lead data to a JSON file
        #         outputs_folder = r"C:\SAKET\RPA\Salesforce\Eventjsonallfiles"
        #         os.makedirs(outputs_folder, exist_ok=True)
        #         file_name = os.path.join(outputs_folder, f"lead_{lead_id}.json")

        #         lead_data = {"lead_id": lead_id}
        #         with open(file_name, 'w') as json_file:
        #             json.dump(lead_data, json_file, indent=4)

        #         print(f"Successfully stored lead_id: {lead_id} in file: {file_name}")

        #         # Send the data to API
        #         api_url = "https://api.smartassistapp.in/api/salesforce/externalPostLeadToSmartAssists"
        #         headers = {
        #             "Content-Type": "application/json",
        #             "Authorization": "Bearer your-token-here"
        #         }
        #         lead_data = {
        #             "lead_id": lead_id,
        #             "lead_email": lead_email,
        #             "subject": subject,
        #             "start_date": lead_start_date,
        #             "start_time": lead_start_time,
        #             "end_date": lead_end_date,
        #             "end_time": lead_end_time
        #         }

        #         response = requests.post(api_url, headers=headers, json=lead_data)
        #         if response.status_code == 200:
        #             print(f"Lead {lead_id} sent successfully to API.")
        #         else:
        #             logging.error(f"Failed to send lead {lead_id} to API: {response.status_code}")
        #             print(f"Error sending data for lead {lead_id}")
            
        # except Exception as e:
        #     logging.error(f"Error processing events: {e}", exc_info=True)
        
        



if __name__ == '__main__':
    api_url = "https://api.smartassistapp.in/api/salesforce-dump/events-data/updated"
    output_directory = "C:\\SAKET\\RPA\\Salesforce\\Eventjsonallfiles"
    selenium_url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
    username = "manharlamba@ariantechsolutions.com"
    password = "Indian@123456"

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
 
    login_to_website(driver, selenium_url, username, password)
    process_events(api_url, output_directory, selenium_url, driver)
