# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pytz
from selenium.common.exceptions import NoSuchElementException
import time
from tabulate import tabulate
import csv
import os
import re
import openpyxl
import pandas as pd
import datetime
from twilio.rest import Client
import sys
import math

# Set timezone for Houston
houston_tz = pytz.timezone('America/Chicago') 

# Define a class for creating tables
class Table:
    def __init__(self, headers):
        self.headers = headers
        self.rows = []
        
    def add_row(self, row):
        self.rows.append(row)
        
    def print_table(self):
        print(tabulate(self.rows, headers=self.headers))

# Initialize table
table = Table(["TOD", "Name", "Phone_Num", "Num_Of_Persons", "Employee", "EmployeePhone"])
tableTOD = []

# Set up the web driver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.binary_location = "/usr/bin/google-chrome"

chrome_driver_path = "/home/ubuntu/.cache/selenium/chromedriver/linux64/112.0.5615.49/chromedriver"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Get today's date and format it
today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d')

# Define the URL to scrape
url = f'https://fareharbor.com/lonestarkayaktours/dashboard/manifest/date/2023-04-26/availabilities/'
driver.get(url)

# Wait for the page to load
time.sleep(3)

print(driver.title)

# Find the username and password fields
username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")

# Input the username and password
username_field.send_keys("--------")
password_field.send_keys("--------")

# Find and click the login button
login_button = driver.find_element(By.CSS_SELECTOR, ".test-login-button")
login_button.click()

time.sleep(2)

button = driver.find_element(By.CLASS_NAME, "overlay-close")

# Click on the button
button.click()

time.sleep(2)

print(driver.title)

# Save the page source to a file
with open("page_source.html", "w") as f:
    f.write(driver.page_source)
    
print("Page source saved as 'page_source.html'")

# Wait for the elements to load
wait = WebDriverWait(driver, 20)  # Change the 20 to the number of seconds you want to wait

# Add an explicit wait for the elements to load
try:
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".spreadsheet--no-bottom-border td")))
except TimeoutException:
    print("Timeout Exception occurred. Saving page source to a file.")
    
    with open("page_source.html", "w") as f:
        f.write(driver.page_source)
    
    print("Page source saved as 'page_source.html'")

# Get crew names
crew = []
elements = driver.find_elements(By.CSS_SELECTOR, ".spreadsheet--no-bottom-border td")

for element in elements:
    text = element.text
    crew.append([text])

crew_names = [crew[i+3][0] for i in range(0, len(crew), 3) if crew[i][0] == 'Crew name']

print(crew_names)

# Get table time of day
elements = driver.find_elements(By.CSS_SELECTOR, ".manifest-block-title span")

for element in elements:
    text = element.text
    tableTOD.append([text])

# Get customer details
elements = driver.find_elements(By.CSS_SELECTOR, ".ng-hide+ div")

texts = []
for element in elements:
    text = element.text
    texts.append(text)

all_lines = []
for i in texts:
    lines = i.splitlines()
    all_lines.append(lines)

lines = all_lines

# Initialize indexes
toggle_details_indexes = []
toggle_customers_indexes = []

# Get indexes for details and customers
Rtoggle_details_indexes = []
Rtoggle_customers_indexes = []

for i in range(len(all_lines)):
    for j, item in enumerate(all_lines[i]):
        if item == "Toggle details":
            toggle_details_indexes.append(j)
            Rtoggle_details_indexes.append(j)
        if item == "Toggle customers":
            toggle_details_indexes.append(j)
            Rtoggle_customers_indexes.append(j)

print("Details and Customers Combined and in Order")
print(toggle_details_indexes)
print("Real only details")
print(Rtoggle_details_indexes)
print("Real only customers")
print(Rtoggle_customers_indexes)
print("tableTOD")
print(tableTOD)

# Initialize table data and counters
table_data = []
TODChangeCounter = 0
TDICounter = 1

# Employee Database
employee_numbers = {"john": "2545419312", "mary": "2545419313", "jane": "2545419314"}

# Iterate through all lines and toggle details indexes
for j in range(len(all_lines)):
    for i in toggle_details_indexes:
        print("I and J")
        print( i, j)

        # Check if the element is "Toggle details"
        if all_lines[j][i] == "Toggle details":
            # Extract necessary details
            time = tableTOD[TODChangeCounter]
            name = all_lines[j][i+1]
            phonenumber = all_lines[j][i+2]
            NumOfPeople = all_lines[j][i+3]
            Employee = crew_names[j]
            EmployeePhone = 2545419312

            # Create a new row and append it to table data
            new_row = [time, name, phonenumber, NumOfPeople, Employee, EmployeePhone]
            print(new_row)
            table_data.append(new_row)

            # Increment counters
            TDICounter = TDICounter + 1
            if all_lines[j][i] == "Toggle details" and i == 1:
                TODChangeCounter = TODChangeCounter +1
                j = j +1
            if TDICounter >= len(toggle_details_indexes) :
                # Prepare table headers and generate the table using the tabulate library
                table_headers = ['TOD', 'Name', 'Phone_Num', 'Num_Of_Persons', 'Employee', 'EmployeePhone']
                table = tabulate(table_data, headers=table_headers)

                # Split the table string into lines and write it to a CSV file
                table_lines = table.splitlines()
                table_data = [re.split('\s{2,}', line) for line in table_lines]

                # Write the list of values as a single row using writerow()
                file_path = os.path.join(os.path.expanduser("~"), "Desktop", "scraped.csv")
                print("File path:", file_path) # print file path
                with open(file_path, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(table_headers)  # write the header row first
                    writer.writerows(table_data)
                    print("CSV printed successfully!")
                    break
            elif (i > toggle_details_indexes[TDICounter]):
                j = j+1
                TODChangeCounter = TODChangeCounter +1
                TDICounter = TDICounter + 1
                print("wtfffffffffffffffffffffffffff")
    if TDICounter >= len(toggle_details_indexes):            
        break

print("table data")
print(table_data)
# Define a function to format phone numbers
def addformat_phone_number(number):
    digits_only = re.sub(r'\D', '', number)  # Remove all non-digit characters
    formatted_number = f'+1{digits_only}'
    return formatted_number

# Quit the webdriver to save RAM
driver.quit()

# Define Twilio account SID and auth token
account_sid = 'AC51d3ce6da2feae4c06e4074ff872ced0'
auth_token = '441e2e22fad07b5dae726c754386a588'

# Create a Twilio client
client = Client(account_sid, auth_token)

# Define a function to send a "Play music" message
def send_play_music():
    message = client.messages.create(
        body="Play music",
        from_='+18336940987',
        to='+12545419312'
    )

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("/home/ubuntu/Desktop/scraped_FAKE.csv")
print(df)

# Iterate through the rows of the DataFrame and send a message to each recipient
for index, row in df.iloc[2:].iterrows(): 
    # Extract recipient's name and phone number from the row
    name = row['Name']
    Num_of_Peop = row['Num_Of_Persons']
    employee = row['Employee']
    recipient_number = row["Phone_Num"]
    Num_of_Peop = row['Num_Of_Persons']
    employee = row['Employee']
    TOD = row['TOD']

    # Split the message into three parts
    message = (
        f"Hi {name}, this is {employee} youre tour guide for the {TOD} tour!.() = MONKEY'"
    )
    #recipient_number = '+12545419312'
    # Create a Twilio client object
    client = Client(account_sid, auth_token)
    # Send an SMS message
    print(recipient_number)
    recipient_number = addformat_phone_number(recipient_number)
    print(recipient_number)
    try:
        message = client.messages.create(
            to=recipient_number,
            from_='+18336940987',
            body=message
        )
        print(f"Message segment sent to {name} ({recipient_number}): {message.sid}")
    except AttributeError as error:
        if " 'list' object has no attribute 'body'" in str(error):
            pass
        else:
            raise
# Define a function to format phone numbers
def format_phone_number(number):
    return re.sub(r'\D', '', number)[-10:] 

# Define a function to check the sender's role
def check_sender_role(sender_number, df):
    for index, row in df.iterrows():
        if format_phone_number(str(row['EmployeePhone'])) == sender_number:
            return 'employee'
        elif format_phone_number(str(row['Phone_Num'])) == sender_number:
            return 'customer'
    return None

# Define a function to process the response
def process_response(message):
    return f"Processed: {message.body}"

# Define the file to store processed messages
processed_messages_file = "processed_messages.txt"

# Define a function to check for new responses
def check_new_responses():
    new_responses = []

    # Read the processed_messages.txt file and store message IDs in a set
    processed_message_ids = set()
    if os.path.exists(processed_messages_file):
        with open(processed_messages_file, "r") as f:
            for line in f:
                processed_message_ids.add(line.strip())

    for res in client.messages.list(to='+18336940987'):
        if res.sid not in processed_message_ids:
            print(f"Message: {res.body}, Date sent: {res.date_sent}, Sender: {res._from}")
            new_responses.append(res)

            # Save the message ID to processed_messages.txt
            with open(processed_messages_file, "a") as f:
                f.write(f"{res.sid}\n")

    return new_responses
# Initialize variables
processed_responses = []
message_sent = False

# Set the time at which the script should restart
restart_time = datetime.time(10, 10)

# Assign a default value to prev_time
prev_time = datetime.datetime.now(houston_tz).time()
prev_date = 0
# Start a loop that will run indefinitely
while True:
    # Get the current date
    current_date = datetime.date.today()
    print(current_date)

    # Check if the current date is different from the previous date
    if current_date != prev_date:
        # If it is, update the previous date and reset the message_sent flag
        prev_date = current_date
        message_sent = False

    # Get the current time
    current_time = datetime.datetime.now(houston_tz).time()
    print(current_time)

    # Check if it's time to send the "Play Music" message
    if current_time.hour == 8 and current_time.minute == 0 and not message_sent:
        # If it is, send the message and set the message_sent flag to True
        send_play_music()
        message_sent = True
        processed_responses = []

    # Check for a response from the recipient
    while True:
        # Update the current time
        current_time = datetime.datetime.now(houston_tz).time()
        print(current_time)

        # Check if it's time to send the "Play Music" message again
        if current_time.hour == 4 and current_time.minute == 0 and not message_sent:
            # If it is, send the message and set the message_sent flag to True
            send_play_music()
            message_sent = True

        # Check for new responses
        response = check_new_responses()

        # If there are new responses, process them
        if len(response) > 0:
            result = process_response(response[0])
            processed_responses.append(result)

            # Delete the first message in the response list
            del response[0]

        # Check if it's time to restart the script
        if prev_time < restart_time <= current_time:
            print("Restarting script...")
            os.system("sleep 2")  # Optional: sleep for 2 seconds before restarting
            os.execv("/usr/bin/python3",['python3', '/home/ubuntu/T.py'])  # Restart the script

        # Update prev_time
        prev_time = current_time

        # Sleep for 30 seconds
        os.system("sleep 30")
