from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class EventScraper:
    def __init__(self):
        self.driver = None
        self.meetup_logged_in = False
        self.luma_logged_in = False

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def login_meetup(self, email, password):
        try:
            self.driver.get('https://www.meetup.com/login/')
            
            # Wait for email input and enter credentials
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_input.send_keys(email)
            
            password_input = self.driver.find_element(By.ID, "current-password")
            password_input.send_keys(password)
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            self.meetup_logged_in = True
            return True
        except Exception as e:
            print(f"Failed to login to Meetup: {str(e)}")
            return False

    def login_luma(self, email, password):
        try:
            self.driver.get('https://lu.ma/login')
            
            # Wait for email input and enter credentials
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(email)
            
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            self.luma_logged_in = True
            return True
        except Exception as e:
            print(f"Failed to login to Lu.ma: {str(e)}")
            return False

    def get_meetup_events(self):
        if not self.meetup_logged_in:
            return []
            
        self.driver.get('https://www.meetup.com/find/?source=EVENTS')
        time.sleep(5)
        
        events = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        event_cards = soup.find_all('div', {'class': 'group-content'})
        
        for card in event_cards[:10]:  # Limit to first 10 events
            try:
                title = card.find('h3').text.strip()
                date = card.find('time').text.strip()
                link = card.find('a')['href']
                events.append({
                    'platform': 'meetup',
                    'title': title,
                    'date': date,
                    'link': link
                })
            except:
                continue
                
        return events

    def get_luma_events(self):
        if not self.luma_logged_in:
            return []
            
        self.driver.get('https://lu.ma/explore')
        time.sleep(5)
        
        events = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        event_cards = soup.find_all('div', {'class': 'event-card'})
        
        for card in event_cards[:10]:  # Limit to first 10 events
            try:
                title = card.find('h2').text.strip()
                date = card.find('time').text.strip()
                link = 'https://lu.ma' + card.find('a')['href']
                events.append({
                    'platform': 'luma',
                    'title': title,
                    'date': date,
                    'link': link
                })
            except:
                continue
                
        return events

    def rsvp_event(self, event):
        try:
            self.driver.get(event['link'])
            time.sleep(3)
            
            if event['platform'] == 'meetup':
                rsvp_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='attend-button']")
            else:  # luma
                rsvp_button = self.driver.find_element(By.CSS_SELECTOR, "button.rsvp-button")
                
            rsvp_button.click()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Failed to RSVP: {str(e)}")
            return False

    def cleanup(self):
        if self.driver:
            self.driver.quit()