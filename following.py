from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

#Set the path to the ChromeDriver executable
chrome_driver_path = 'C:/Program Files/chromedriver_win64/chromedriver.exe'
os.environ["PATH"] += os.pathsep + chrome_driver_path

#Function to read followers from a text file
def read_followers_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

#Login to Instagram
USERNAME = 'Your Username'
PASSWORD = 'Your Password'

#Initialize Chrome WebDriver
driver = webdriver.Chrome()

#Navigate to Instagram login page
driver.get("https://www.instagram.com/accounts/login/")

#Wait for page to load
time.sleep(5)

#Fill in username and password and submit
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)

password_input.send_keys(Keys.RETURN)

#Wait for login to complete
time.sleep(5)

#Path to the text file containing follower usernames
file_path = 'unfollow.txt'

#Read the list of followers from the file
followers_to_remove = read_followers_from_file(file_path)

#Function to remove a follower by username
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def remove_follower(username):
    try:
    # Navigate to the follower's profile
        driver.get(f"https://www.instagram.com/{username}/")
            # Wait for the 'Following' button to become clickable
        following_button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Following']"))
            )
        following_button.click()
        time.sleep(2)  # Adjust the sleep time as needed

        # Find and click on the 'Unfollow' option in the dropdown menu
        unfollow_option = driver.find_element(By.XPATH, "//button[text()='Unfollow']")
        unfollow_option.click()
        time.sleep(2)  # Adjust the sleep time as needed

        print(f"Successfully removed {username}")
    except Exception as e:
        print(f"Failed to remove {username}: {e}")
            
#Set the number of followers to remove (maximum 48)
num_to_remove = min(48, len(followers_to_remove))

#Remove followers
for i in range(num_to_remove):
    remove_follower(followers_to_remove[i])
    
# To avoid being flagged by Instagram, add a delay between each request
time.sleep(5) # adjust the sleep time as needed

print("Follower removal process completed.")

#Close the WebDriver
driver.quit()