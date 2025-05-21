import logging
import os
import json
import ssl
import http.client
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime 

def fetch_data_from_api(api_url):
    """Fetch data from API with SSL verification disabled."""
    try:
        response = requests.get(api_url, verify=False)
        response.raise_for_status()
        logging.info(f"Raw response: {response.text}")
        data = response.json()
        logging.info(f"Fetched {len(data)} entries from API.")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from API: {e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON response: {e}")
        return []


def process_emails(api_url, output_directory):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=options)
    driver.get("https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default")
    logging.info("Navigated to login page.")


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
    time.sleep(20)
    while True:


        logging.info("Fetching data from API.")
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection(api_url.replace("https://", "").split("/")[0], context=context)
        endpoint = "/" + "/".join(api_url.split("/")[3:])
        conn.request("GET", endpoint)
        response = conn.getresponse()

        if response.status == 200:
            lead_update = json.loads(response.read().decode())
            logging.info(f"Fetched {len(lead_update)} entries from API.")
        else:
            logging.error(f"Failed to fetch data with status code: {response.status}")
            return


        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        json_file_path = os.path.join(output_directory, "leads_update.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(lead_update, json_file, indent=4)
        logging.info(f"API data saved to {json_file_path}")


        for entry in lead_update:
            url = entry.get('url', '')
            fname = entry.get('fname', '')
            lname = entry.get('lname', '')
            lead_status = entry.get('status')
            lead_source = entry.get('lead_source', '')
            enquiry_type = entry.get('enquiry_type', '')
            mobile = entry.get('mobile', '')
            brand = entry.get('brand', '')
            purchase_type = entry.get('purchase_type', '')
            sub_type = entry.get('sub_type', '')
            PMI = entry.get('PMI', '')
            lead_id = entry.get('lead_id', '')
            email = entry.get('email', '')
            # if lead_status=='Follow Up':
            #     print(f"this is {lead_id} is already Follow up")
            #     continue

            if url and fname and lname and lead_status and lead_source and enquiry_type and mobile and brand and purchase_type and sub_type and lead_id:
                logging.info(f"Opening URL: {url}")
                driver.get(url)

                time.sleep(5)
            
                time.sleep(5)
                
                

                try:

                    # edit_btn = WebDriverWait(driver, 10).until(
                    #     EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'slds-sectiontitle-action') and .//span[text()='Lead Information']]"))
                    # )
                    # edit_btn.click()
                    # time.sleep(5)

                    edit_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@title="Edit Name" and contains(@class, "inline-edit-trigger")]'))
                    )
                    edit_btn.click()
                    time.sleep(5)
                    driver.execute_script("window.scrollBy(0, 300);")
                    try:

                        name_btn=WebDriverWait(driver,10).until(
                            EC.element_to_be_clickable((By.XPATH,"//label[contains(text(), 'First Name')]/following::input[@name='firstName'][1]"))
                        )
                        if name_btn.is_displayed():
                            print(" the elemnt found")
                            name_btn.click()
                            name_btn.clear()
                            name_btn.send_keys(fname)
                        else:
                            print("elemnt not found")

                        print("fname button is updated")
                    except Exception as e:
                        print("the lemnt for nae is not found",e)

                    

                    try:
                        mobile_btn=WebDriverWait(driver,10).until(
                            EC.element_to_be_clickable((By.XPATH,"//input[contains(@class, 'slds-input') and @type='text' and @name='MobilePhone']"))
                        )
                        if mobile_btn.is_displayed():
                            print("mboile button is found")
                            mobile_btn.click()
                            mobile_btn.clear()
                            mobile_btn.send_keys(mobile)
                        else:
                            print("elemnt not found")
                    except Exception as e:
                        print("the elemnt not found for mobile",e)
                    try:

                        mobile_xpath = "//input[@name='Email' and @type='text']"
                                
                        # Explicit wait for the element to be visible and clickable
                        mobile_element = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, mobile_xpath))
                        )
                        if mobile_element.is_displayed:
                            mobile_element.clear()
                        
                            # Send the email to the input field
                            mobile_element.send_keys(email)
                            print("email has enter succesfully")
                        else:
                            print("email is not visible")
                                
                    except Exception as e:
                            print("the emailupdate ntn is not updating error is found",e)
                    
                    
                    

                    
                    try:
                        lead_status_button = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and @aria-label='Lead Status']"))
                        )
                        lead_status_button.click()
                    except Exception as e:
                        logging.error(f"Lead Status element not found: {e}")
                        driver.save_screenshot("error_screenshot.png")
                        with open("page_dump.html", "w", encoding="utf-8") as f:
                            f.write(driver.page_source)
                        continue

                    
         
                    if lead_status == "Follow Up":
                        follow_up_xpath = "//lightning-base-combobox-item[@data-value='Follow Up']"
                        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, follow_up_xpath))).click()
                        logging.info("Pressed down once for 'Follow Up'.")
                    elif lead_status == "New":
                        new_up_xpath = "//span[@class='slds-truncate' and text()='New']"
                        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, new_up_xpath))).click()
                        logging.info("Pressed down for 'New'.")
                    elif lead_status == "Qualified":
                        qual_xpath = "//lightning-base-combobox-item[@data-value='Qualified']"
                        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, qual_xpath))).click()
                        logging.info("Pressed down for 'Qualified'.")
                    elif lead_status == "Lost":
                        last_xpath = "//lightning-base-combobox-item[@data-value='Lost']"
                        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, last_xpath))).click()
                        logging.info("Pressed down for 'Lost'.")
                    
                   

                   
                    
                    time.sleep(3)

                    fifth_dropdown = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enquiry Type' and contains(@class, 'slds-combobox__input')]"))
                    )

                    # Click the Lead Source dropdown
                    fifth_dropdown.click()
                    print("Lead Source dropdown clicked successfully.")

                    if enquiry_type == "(Generic) Purchase intent within 90 days":
                                genric = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Generic']"))
                                )
                                genric.click()
                                time.sleep(1)
                    elif enquiry_type == "KMI":
                                    KMI_TYPE = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='KMI']"))
                                    )
                                    KMI_TYPE.click()
                                    time.sleep(1)
                    else:
                        print(" enquiry button has not been found")

                    
                    
                   
                    #         EC.element_to_be_clickable((By.XPATH,'//lightning-base-combobox//input[@placeholder="Search Vehicle Specifications..."]'))
                    #     )
                    #     if pmidata.is_displayed():
                    #         print("bhail milgfaa ")
                    #         pmidata.click()
                    #         pmidata.send_keys(PMI[:4])
                    #         time.sleep(1)
                    #     else:
                    #         print("nahi mila yrr")
                    # except Exception as e:
                    #     print("the errro hgas been found",e)
                   
                    # try:
                    #     option_data = WebDriverWait(driver, 10).until(
                    #         EC.element_to_be_clickable((By.XPATH, f"//lightning-base-combobox-item[normalize-space(.//span[contains(@class,'slds-listbox__option-text')])='{PMI}']"))
                    #     )
                    #     if option_data.is_displayed():
                    #         print("elemnt milgaya bhai")
                    #         option_data.click()
                    #     else:
                    #         print("elemnt nahi mila bhai ")
                    #     print("pmi data has been inserted succesfully")
                        
                        
                    # except Exception as e:
                    #     print("the elemnt has not been found",e)
                    #     logging.error(f"Error in processing PMI: {e}", exc_info=True)
                    # time.sleep(2)

                   
                    
                    # time.sleep(10)
                    

                    # purchase_button = "//button[contains(@class, 'slds-combobox__input') and contains(@aria-label, 'Purchase Type') and @data-value='--None--']"
                    # purchase_button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, purchase_button)))
                    # driver.execute_script("arguments[0].scrollIntoView(true);", purchase_button)


                    # purchase_button.send_keys(purchase_type)
                    # logging.info("Entered First Name successfully.")
                    

                    # print(f"the  purchase type is", {purchase_type})



                    # if purchase_type=='New Vehicle':
                    #     purchase_btn = "//lightning-base-combobox-item[@data-value='New Vehicle']"
                    #     purchase_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, purchase_btn)))
                    #     purchase_btn.click()
                        
                    # elif purchase_type=='Used Vehicle':
                    #     used_btn = "//lightning-base-combobox-item[@data-value='Used Vehicle']"
                    #     used_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, used_btn)))
                    #     used_btn.click()
                        
                        
                    # else:
                    #     print("Purchase type not found")
                    # print("purchase button cliked succesfully")


            

                    
                    save_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//li[@role='presentation']//button[@class='slds-button slds-button_brand' and @name='SaveEdit']"))
                    )
                    save_btn.click()
                    logging.info("Save button clicked successfully.")
                    time.sleep(5)
                    

                except Exception as e:
                    logging.error(f"Unexpected error for entry {entry.get('lead_id', 'UNKNOWN')}: {e}", exc_info=True)
                    continue  

            

def main():
    api_url = "https://api.smartassistapp.in/api/salesforce-dump/leads-data/updated"
    output_directory = "C:\\SAKET\\RPA\\Salesforce\\lead_update"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    process_emails(api_url, output_directory)
    

if __name__ == '__main__':
    main()
