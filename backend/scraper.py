def get_rating(player_name):
    url = f"https://gb.hlorenzi.com/reg/D7D6u-/player/{player_name}"
    sys.stdout.reconfigure(encoding='utf-8')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page_text = driver.find_element(By.TAG_NAME, "body").text

        match = re.search(r"Rating\s*:\s*(-?\d+)", page_text)
        if match:
            return match.group(1)
        else:
            return "Rating non trouvé"

    except Exception as e:
        return f"Erreur : {str(e)}"
    finally:
        driver.quit()
