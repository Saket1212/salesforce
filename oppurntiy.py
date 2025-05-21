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


def login_to_website(driver, selenium_url, username, password):
    """Log in to the website."""
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
    logging.info("Successfully logged in.")

def process_opportunities(api_url, output_directory, selenium_url, driver):
    """
    Fetch data from API and process follow-up opportunities in Salesforce.
    """
    while True:
    
    
        logging.info("Fetching data from API.")
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection(api_url.replace("https://", "").split("/")[0], context=context)
        endpoint = "/" + "/".join(api_url.split("/")[3:])
        conn.request("GET", endpoint)
        response = conn.getresponse()


        opportunities_data = []  # Initialize the variable

        if response.status == 200:
            opportunities_data = json.loads(response.read().decode())
            logging.info(f"Fetched {len(opportunities_data)} entries from API.")
        else:
            logging.error(f"Failed to fetch data with status code: {response.status}")

        # Check if opportunities_data is populated before proceeding
        if not opportunities_data:
            logging.warning("No opportunities data to process.")
            continue

        # Save API data
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        json_file_path = os.path.join(output_directory, "Opportunities.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(opportunities_data, json_file, indent=4)
        logging.info(f"API data saved to {json_file_path}")
        print(f"API data saved to {json_file_path}")

        # Step 2: Process opportunities
        for entry in opportunities_data:
            lead_url = entry.get('lead_url', '')
            accountserach = entry.get('Abh', '')
            oppurnties_id=entry.get('opportunity_id','')

            # if not lead_url or accountserach or oppurnties_id:
            #     print(f"this datas are presnt{lead_url},{accountserach},{oppurnties_id}")
            #     continue
            

            print(f"Raw accountserach: '{accountserach}'")


            words = accountserach.split()


            print(f"Words after splitting: {words}")


            first_four_words = ' '.join(words[:4])


            print(f"First four words: '{first_four_words}'")

            # Log the value of accountserach
            logging.info(f"Searching for account: {accountserach}")

            driver.get(lead_url)
            time.sleep(20)

            # Convert Opportunity
            convert_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@data-target-selection-name='sfdc:StandardButton.Lead.Convert']//button[text()='Convert']"))
            )
            convert_button.click()
            time.sleep(5)





        
            
            # Convert button click
            try:
                save_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(@class, 'slds-button_brand') and text()='Convert']"))
                )
                save_btn.click()
                logging.info("Clicked Convert button.")
                time.sleep(25)
            except TimeoutException:
                logging.error("Convert button not found or not clickable.")

            # Click on the link for the next step
            try:
                king_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'outputLookupLink')]"))
                )
                king_btn.click()
                logging.info("King button clicked.")
            except TimeoutException:
                logging.error("King button not found or not clickable.")
            time.sleep(5)
            
        
            current_url = driver.current_url
            print(f"Captured URL: {current_url}")
            time.sleep(10)

            file_name = "opp.json"
            lead_data = {"opportunity_id": oppurnties_id, "url": current_url}


            

            # Save the payload to a JSON file
            with open(file_name, 'w') as json_file:
                json.dump(lead_data, json_file, indent=4)

            print(f"Successfully stored lead_id: {oppurnties_id} in file: {file_name}")

            # Load payload from the JSON file
            with open(file_name, 'r') as json_file:
                payload = json.load(json_file)

            # API endpoint
            api_url = "https://api.smartassistapp.in/api/salesforce-dump/opps/new/flag-inactive"


            # SSL and connection setup
            try:
                context = ssl._create_unverified_context()
                conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)

                
                payload_json = json.dumps(payload)

                # Headers
                headers = {
                    "Content-Type": "application/json",
                    "Content-Length": str(len(payload_json))
                }

                # PUT request
                conn.request("PUT", api_url, body=payload_json, headers=headers)

                # Process response
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


if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    api_url = "https://api.smartassistapp.in/api/salesforce-dump/opportunities-data/new"
    output_directory = "C:\\SAKET\\RPA\\Salesforce\\oppurnityalljsonfile"
    selenium_url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default"
    username = "manharlamba@ariantechsolutions.com"
    password = "Indian@123456"

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
    login_to_website(driver, selenium_url, username, password)
    process_opportunities(api_url, output_directory, selenium_url, driver)
