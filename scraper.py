import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_rating_and_rank(player_name, leaderboard):
    url = f"https://gb.hlorenzi.com/reg/{leaderboard}/player/{player_name}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        for _ in range(5):
            try:
                player_div = driver.find_element(By.XPATH, f"//div[contains(text(), '{player_name}')]")
                break 
            except:
                time.sleep(2)

        if not player_div:
            print("Element not found. Debugging page source:")
            print(driver.page_source)
            return None, None

        rank_div = player_div.find_element(By.XPATH, "./div")
        rank = rank_div.text.strip().upper() if rank_div else "INCONNU"

        rating_match = re.search(r"Rating\s*:\s*(-?\d+)", driver.find_element(By.TAG_NAME, "body").text)
        rating = rating_match.group(1) if rating_match else "Inconnu"

        print(f"Joueur: {player_name} | MMR: {rating} | Rang: {rank} | Leaderboard: {leaderboard}")
        return rating, rank

    except Exception as e:
        print(f"Erreur : {str(e)}")
        return None, None

    finally:
        driver.quit()