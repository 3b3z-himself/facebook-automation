import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configuration
EMAIL = ''
PASSWORD = ''
PROFILE_URL = 'https://www.facebook.com/ahmed.abdelzaher.1217'

# Initialize Chrome WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

def login():
    driver.get('https://www.facebook.com')
    
    # Enter email
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    email_field.send_keys(EMAIL)
    
    # Enter password
    password_field = driver.find_element(By.ID, 'pass')
    password_field.send_keys(PASSWORD)
    
    # Click login button
    login_button = driver.find_element(By.NAME, 'login')
    login_button.click()
    
    # Wait for login to complete
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Account controls and settings']")))
    except TimeoutException:
        print("Login failed. Check credentials or handle 2FA.")
        driver.quit()
        exit()

def navigate_to_profile():
    driver.get(PROFILE_URL)
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Timeline')]")))

def scroll_to_load_posts():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def change_post_audience():
    # Find all post elements
    posts = driver.find_elements(By.XPATH, "//div[@role='article']")
    print(f"Found {len(posts)} posts.")

    for post in posts:
        try:
            # Find audience button
            audience_button = post.find_element(By.XPATH, ".//div[@aria-label='Edit privacy']")
            driver.execute_script("arguments[0].click();", audience_button)
            
            # Select 'Only Me' option
            only_me_option = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Only me')]/ancestor::div[@role='menuitem']")
            ))
            driver.execute_script("arguments[0].click();", only_me_option)
            time.sleep(1)  # Allow time for the change to apply
            
        except (NoSuchElementException, TimeoutException):
            continue  # Skip if audience button not found or already set

def main():
    try:
        login()
        navigate_to_profile()
        scroll_to_load_posts()
        change_post_audience()
        print("Audience settings updated successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()