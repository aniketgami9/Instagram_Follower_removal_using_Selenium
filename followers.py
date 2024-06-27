from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Set the path to the ChromeDriver executable
chrome_driver_path = 'C:/Program Files/chromedriver_win64/chromedriver.exe'
os.environ["PATH"] += os.pathsep + chrome_driver_path

# Function to read followers from a text file
def read_followers_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Login to Instagram
USERNAME = 'YOUR Username'
PASSWORD = 'Your Password'

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Navigate to Instagram login page
driver.get("https://www.instagram.com/accounts/login/")

# Wait for page to load
time.sleep(5)

# Fill in username and password and submit
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)

password_input.send_keys(Keys.RETURN)

# Wait for login to complete
time.sleep(5)

# Navigate to your profile
driver.get("https://www.instagram.com/{}/".format(USERNAME))

# Wait for profile page to load
time.sleep(2)

# Navigate to followers
followers_link = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]")))
followers_link.click()

# Wait for followers list to load
time.sleep(2)

# Path to the text file containing follower usernames
file_path = 'unfollow.txt'

# Read the list of followers from the file
followers_to_remove = read_followers_from_file(file_path)

# Function to remove a follower by username
def remove_follower(username):
    try:
        # Search for the follower in the followers list
        search_box = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
        search_box.clear()
        search_box.send_keys(username)
        
        # Wait for the user to appear in the list
        time.sleep(2)
        
        
        # Find the follower and click on the 'Following' button
        following_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Following']")))
        following_button.click()
        
        # Wait for the 'Unfollow' option to appear
        unfollow_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Unfollow']")))
        unfollow_button.click()
        
        # Click on 'Remove' to confirm
        remove_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Remove']")))
        driver.execute_script("arguments[0].click();", remove_button)  # Click using JavaScript executor
        
        print(f"Successfully removed {username}")
        
    except Exception as e:
        print(f"Failed to remove {username}: {e}")
        



# Set the number of followers to remove (maximum 48)
num_to_remove = min(48, len(followers_to_remove))



# Remove followers
for i in range(num_to_remove):
    remove_follower(followers_to_remove[i])
    
    # To avoid being flagged by Instagram, add a delay between each request
    time.sleep(2) # Adjust the sleep time as needed


print("Follower removal process completed.")

# Close the WebDriver
driver.quit()
