"""
Selenium script - Task 2
-------------------------
Opens the Laravel login page (from Task 1), fills the email and
password fields with random values, submits the form, and exits.

Target page fields (from resources/views/caller/auth/login.blade.php):
    <input id="email"    name="email_address" type="text">
    <input id="password" name="password"      type="password">
    <form  id="formAuthentication" action="/login" method="POST">

Requirements (run this on a machine that has a browser installed):
    pip install selenium
    Google Chrome (or Chromium) installed on the machine.

Selenium 4.6+ ships "Selenium Manager", which automatically downloads
the matching chromedriver for you - no manual driver setup needed.

Usage:
    python task2_selenium_login_automation.py
    python task2_selenium_login_automation.py --url http://da.adlynk.in:8000/login
"""

import argparse
import random
import string
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


DEFAULT_LOGIN_URL = "http://da.adlynk.in:8000/login"


def random_email():
    local_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domains = ["example.com", "testmail.com", "demo.io", "mailtest.org"]
    return f"{local_part}@{random.choice(domains)}"


def random_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choices(chars, k=length))


def build_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,768")
    # Selenium Manager (bundled with selenium>=4.6) resolves the driver
    # automatically, so no Service(executable_path=...) is required.
    return webdriver.Chrome(options=options)


def fill_and_submit_login(driver: webdriver.Chrome, url: str, wait_seconds: int = 15):
    email_value = random_email()
    password_value = random_password()

    print(f"Opening login page: {url}")
    driver.get(url)

    wait = WebDriverWait(driver, wait_seconds)

    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    password_field = driver.find_element(By.ID, "password")

    email_field.clear()
    email_field.send_keys(email_value)

    password_field.clear()
    password_field.send_keys(password_value)

    print(f"Filled email:    {email_value}")
    print(f"Filled password: {password_value}")

    submit_button = driver.find_element(
        By.CSS_SELECTOR, "#formAuthentication button[type='submit']"
    )
    submit_button.click()

    # Give the page a moment to respond (success redirect or validation error)
    time.sleep(2)
    print(f"Submitted. Current URL after submit: {driver.current_url}")


def main():
    parser = argparse.ArgumentParser(description="Automate the Laravel login page with random credentials.")
    parser.add_argument("--url", default=DEFAULT_LOGIN_URL, help="Login page URL")
    parser.add_argument("--no-headless", action="store_true", help="Run with a visible browser window")
    args = parser.parse_args()

    driver = build_driver(headless=not args.no_headless)
    try:
        fill_and_submit_login(driver, args.url)
    finally:
        print("Exiting browser.")
        driver.quit()


if __name__ == "__main__":
    main()
