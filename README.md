# Delivery Notes

## Contents

* `task1_login_page_screenshot.png` – Task 1 completion screenshot
* `task2_selenium_login_automation.py` – Selenium login automation script
* `task3_calendar_page_screenshot.png` – Task 3 completion screenshot
* `laravel_changes/` – Modified Laravel files
* `README.md` – Documentation

## Task 1 – Laravel Setup

* Added placeholder `app/helpers.php` and `app/helpers2.php` to resolve Composer autoload errors.
* Included `db_fixed.sql` with `utf8mb4_unicode_ci` collation for MariaDB compatibility.
* Verified the application runs successfully and the login page loads (HTTP 200).
* Login screenshot included.

## Task 2 – Selenium Automation

* Script automatically:

  * Opens the login page
  * Enters random credentials
  * Clicks **Login**
  * Closes the browser
* Compatible with Selenium 4.6+ and Chrome.

Run:

```bash
pip install selenium
python task2_selenium_login_automation.py
```

## Task 3 – Calendar Integration

* Added `resources/views/html-page.blade.php`.
* Added `/html-page` route in `routes/web.php`.
* Reused existing project assets; no additional assets required.
* Calendar page loads successfully (HTTP 200).




