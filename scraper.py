import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_rating_and_rank(player_name):
    url = f"https://gb.hlorenzi.com/reg/D7D6u-/player/{player_name}"

    sys.stdout.reconfigure(encoding='utf-8')

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure Chrome runs in headless mode
    chrome_options.add_argument("--no-sandbox")  # Added for sandboxing issues
    chrome_options.add_argument("--disable-dev-shm-usage")  # For certain environments like Heroku
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page_text = driver.find_element(By.TAG_NAME, "body").text
        rating_match = re.search(r"Rating\s*:\s*(-?\d+)", page_text)
        rating = rating_match.group(1) if rating_match else "Inconnu"

        player_div = driver.find_element(By.XPATH, "//div[contains(text(), '{}')]".format(player_name))

        rank_div = player_div.find_element(By.XPATH, "./div")
        rank = rank_div.text.strip().upper() if rank_div else "INCONNU"

        print(f"Joueur: {player_name} | MMR: {rating} | Rang: {rank}")
        return rating, rank

    except Exception as e:
        print(f"Erreur : {str(e)}")
        return None, None

    finally:
        driver.quit()