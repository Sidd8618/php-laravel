# Delivery Notes - All 3 Tasks

## What's in this package
```
task1_login_page_screenshot.png      -> Task 1 closure screenshot
task2_selenium_login_automation.py   -> Task 2 selenium script
task3_calendar_page_screenshot.png   -> Task 3 closure screenshot
laravel_changes/                     -> Only the files added/changed in your Laravel project (see below)
README.md                            -> This file
```

I ran everything end-to-end in my own sandbox (PHP 8.3 + MariaDB + `php artisan serve`),
confirmed both pages return HTTP 200, and captured screenshots as proof. Below is exactly
what was done and how to reproduce it on your own machine.

---

## Task 1 - Laravel project live + DB import

**Two issues in the uploaded zip that had to be fixed to get it running at all:**

1. `composer.json` declares two autoload files that were missing from the zip:
   `app/helpers.php` and `app/helpers2.php`. Without them, Composer's autoloader fatal-errors
   immediately on every `php artisan` call. I added them back as empty placeholder files
   (`laravel_changes/app/helpers.php`, `helpers2.php`) so the app boots. **If your original
   project had real code in these files, you must restore your real versions** - these
   placeholders are empty stubs, added purely to unblock booting.

2. `db/db.sql` was exported from **MySQL 8** and uses the `utf8mb4_0900_ai_ci` collation,
   which **MariaDB** doesn't recognize (`ERROR 1273: Unknown collation`). I've included a
   fixed copy, `laravel_changes/db/db_fixed.sql`, with that collation swapped to
   `utf8mb4_unicode_ci`. Use this file if you're importing into MariaDB; if you have real
   MySQL 8 available, the original `db.sql` will work as-is.

   Also worth flagging: the `users` table in the dump has **no seed rows** - schema only,
   0 users. That's fine for viewing the login page, but there's no account to actually log
   in with until you insert one.

**Steps to reproduce locally:**
```bash
# 1. Extract your project, then apply the fixes above (or drop in laravel_changes/ files)

# 2. Install PHP 8.1+ with common extensions, and MySQL/MariaDB
sudo apt install php8.3 php8.3-cli php8.3-mysql php8.3-mbstring php8.3-xml php8.3-curl \
                  php8.3-bcmath php8.3-zip php8.3-gd mariadb-server composer

# 3. Create the DB and import
mysql -u root -e "CREATE DATABASE myad CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root myad < db_fixed.sql

# 4. .env already has DB_DATABASE=myad, DB_USERNAME=root, DB_PASSWORD= (blank) - adjust if needed

# 5. Point a local domain at 127.0.0.1 (the app's routes are locked to Route::domain('da.adlynk.in'))
echo "127.0.0.1 da.adlynk.in" | sudo tee -a /etc/hosts

# 6. Composer + permissions
composer install
chmod -R 775 storage bootstrap/cache

# 7. Serve it
php artisan serve --host=0.0.0.0 --port=8000

# 8. Visit:
http://da.adlynk.in:8000/login
```

The login screenshot (`task1_login_page_screenshot.png`) was taken from exactly this URL/setup.

---

## Task 2 - Selenium automation script

`task2_selenium_login_automation.py` opens the login page, fills the two real form fields
found in `resources/views/caller/auth/login.blade.php`:
- `#email` (posted as `email_address`)
- `#password`

...with randomly generated values, clicks Login, waits briefly, and exits/quits the driver.

**To run it (on a machine with Chrome installed):**
```bash
pip install selenium
python task2_selenium_login_automation.py
# or point it at a different URL:
python task2_selenium_login_automation.py --url http://da.adlynk.in:8000/login --no-headless
```
Selenium 4.6+ auto-manages the chromedriver binary for you (Selenium Manager) - no manual
driver download needed, as long as Chrome itself is installed.

Note: my sandbox environment has no browser binary available (network is restricted to
package registries, not general internet, so Chrome/Chromium can't be installed here) - so
the script is written and syntax-verified but not executed against a live browser on my end.
It's straightforward Selenium and will run as-is anywhere Chrome + selenium are available.

---

## Task 3 - Calendar template wired in as `/html-page`

From the template zip, `html/vertical-menu-template/app-calendar.html` uses the exact same
theme/asset structure (`assets/vendor/...`) as your Laravel project's `public/assets` folder
already does - so no new assets needed copying in; everything it needs (FullCalendar, Select2,
Flatpickr, moment.js, etc.) was already present in `public/assets`.

Changes made:
1. Copied the HTML into `resources/views/html-page.blade.php`, rewriting all
   `../../assets/...` relative paths to `{{ config('app.url') }}assets/...` (same pattern
   your `login.blade.php` already uses).
2. Added a route in `routes/web.php`:
   ```php
   Route::get('/html-page', function () {
       return view('html-page');
   });
   ```
   This is a plain top-level route (not inside the `Route::domain('da.adlynk.in')` group), so
   it's reachable on any host/port your app is served on.

Visit: `http://da.adlynk.in:8000/html-page` (or just `http://<your-host>/html-page`)

Note: the page's own sidebar still has nav links to other demo pages (dashboards, ecommerce,
etc.) that weren't part of this task and aren't wired up - those will 404 if clicked, which
is expected since only the calendar page itself was requested.
