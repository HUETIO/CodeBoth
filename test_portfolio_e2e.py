import os
import time
import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException
)
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://localhost:5173/"

# ------------------------
# UTILIDADES
# ------------------------

def human_pause(min_s=0.2, max_s=0.8):
    time.sleep(random.uniform(min_s, max_s))

def human_type(element, text, delay=0.07):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

# ------------------------
# FIXTURE DRIVER
# ------------------------

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")

    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    try:
        drv.maximize_window()
    except Exception:
        pass
    drv.implicitly_wait(2)
    yield drv
    drv.quit()

# ------------------------
# TEST 1: STRESS LOGIN TOGGLE
# ------------------------

def test_stress_login_toggle(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 5)

    CYCLES = 2
    print(f"\n[Stress] Login toggle x{CYCLES}")

    for _ in range(CYCLES):
        try:
            login_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".auth-btn"))
            )
            login_btn.click()

            dropdown = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".register-dropdown"))
            )

            human_pause(0.1, 0.3)

            close_btn = dropdown.find_element(By.CSS_SELECTOR, ".btn-close")
            close_btn.click()

            wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".register-dropdown"))
            )

        except (StaleElementReferenceException, ElementClickInterceptedException):
            human_pause(0.4, 0.7)

    print("✅ Stress login toggle OK")

# ------------------------
# TEST 2: LOGIN REALISTA + NAVEGACIÓN
# ------------------------

def test_realistic_login_navigation(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    print("\n[UserFlow] Login realista")

    fb_email = os.getenv("FIREBASE_EMAIL")
    fb_password = os.getenv("FIREBASE_PASSWORD")
    if not fb_email or not fb_password:
        pytest.skip("FIREBASE_EMAIL/FIREBASE_PASSWORD no configuradas")

    # Abrir login
    login_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".auth-btn"))
    )
    login_btn.click()

    dropdown = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".register-dropdown"))
    )

    # Inputs del formulario de login (segundo form)
    login_form = dropdown.find_elements(By.CSS_SELECTOR, "form")[-1]
    email_input = login_form.find_element(By.CSS_SELECTOR, "input[type='email']")
    pass_input = login_form.find_element(By.CSS_SELECTOR, "input[type='password']")

    human_type(email_input, fb_email)
    human_pause()
    human_type(pass_input, fb_password)

    human_pause()

    submit_btn = login_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    # Sesión iniciada: aparece el botón con el email en navbar
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".auth-dropdown .auth-btn"))
    )

    print("✅ Login exitoso")

    # Scroll humano
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    human_pause(0.5, 1.2)
    driver.execute_script("window.scrollTo(0, 0);")
    human_pause()

    # Navegación
    driver.back()
    human_pause()
    driver.forward()
    human_pause()

    driver.refresh()
    human_pause(0.8, 1.5)

    # Verificar sesión persistente
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".auth-dropdown .auth-btn"))
    )

    print("✅ Sesión persistente tras refresh")

    # Logout
    auth_btn = driver.find_element(By.CSS_SELECTOR, ".auth-dropdown .auth-btn")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", auth_btn)
    driver.execute_script("arguments[0].click();", auth_btn)

    logout_btn = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".dropdown-menu .dropdown-item"))
    )
    driver.execute_script("arguments[0].click();", logout_btn)
    logout_btn.click()

    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".auth-btn"))
    )

    print("✅ Logout correcto")

    # Reingreso
    driver.get(BASE_URL)
    human_pause(1, 2)

    login_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".auth-btn"))
    )
    login_btn.click()

    print("🔁 Reingreso completado")

# ------------------------
# TEST 3: STRESS MODALES DE PELÍCULAS
# ------------------------

def test_stress_movie_modals(driver):
    wait = WebDriverWait(driver, 10)

    cinema_section = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#cinema-container"))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        cinema_section
    )

    CYCLES = 5
    print(f"\n[Stress] Modales de películas x{CYCLES}")

    for i in range(CYCLES):
        cards = driver.find_elements(By.CSS_SELECTOR, ".movie-card")
        if not cards:
            pytest.fail("No se cargaron películas")

        card = cards[i % len(cards)]

        ActionChains(driver).move_to_element(card).perform()
        human_pause(0.2, 0.5)

        play_btn = card.find_element(By.CSS_SELECTOR, ".btn-play")
        driver.execute_script("arguments[0].click();", play_btn)

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-window"))
        )

        human_pause(0.3, 0.8)

        close_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-actions button"))
        )
        close_btn.click()

        wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-window"))
        )

    print("✅ Stress modales OK")

# ------------------------
# TEST 4: STRESS TABS RÁPIDOS
# ------------------------

def test_stress_rapid_tabs(driver):
    wait = WebDriverWait(driver, 5)

    tabs_section = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".color-buttons"))
    )
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        tabs_section
    )

    buttons = driver.find_elements(By.CSS_SELECTOR, ".color-buttons button")
    assert buttons, "No hay botones de tabs"

    CYCLES = 5
    print(f"\n[Stress] Tabs rápidos x{CYCLES}")

    for i in range(CYCLES):
        btn = buttons[i % len(buttons)]
        btn.click()

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".tabs-container"))
        )

        human_pause(0.1, 0.4)

        if i % 5 == 0:
            try:
                close_tab = driver.find_element(By.CSS_SELECTOR, ".close-tab")
                if close_tab.is_displayed():
                    close_tab.click()
            except Exception:
                pass

    print("✅ Stress tabs OK")
