import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys

def get_rating_and_rank(player_name):
    url = f"https://gb.hlorenzi.com/reg/D7D6u-/player/{player_name}"

    # Encodage UTF-8 pour éviter les erreurs d'affichage
    sys.stdout.reconfigure(encoding='utf-8')

    # Configurer Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter en arrière-plan
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    # Lancer Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    driver.get(url)

    try:
        # Attendre que la page charge complètement
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Récupérer le texte de la page pour le MMR
        page_text = driver.find_element(By.TAG_NAME, "body").text
        rating_match = re.search(r"Rating\s*:\s*(-?\d+)", page_text)
        rating = rating_match.group(1) if rating_match else "Inconnu"

        # Récupérer le pseudo du joueur (div principal)
        player_div = driver.find_element(By.XPATH, "//div[contains(text(), '{}')]".format(player_name))

        # Récupérer le rang à l'intérieur du même bloc (div suivant)
        rank_div = player_div.find_element(By.XPATH, "./div")
        rank = rank_div.text.strip().upper() if rank_div else "INCONNU"

        print(f"Joueur: {player_name} | MMR: {rating} | Rang: {rank}")
        return rating, rank

    except Exception as e:
        print(f"Erreur : {str(e)}")
        return None, None

    finally:
        driver.quit()

# Test avec un joueur
player = "Eags"
get_rating_and_rank(player)
