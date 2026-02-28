#!/usr/bin/env python3
"""
Simple screenshot script for Django app using selenium
"""

import time
import subprocess
import sys
from pathlib import Path

# Try to use selenium, fallback to manual instructions
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Selenium not installed. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "selenium", "-q"])
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        SELENIUM_AVAILABLE = True
    except:
        print("Could not install selenium. Please install manually.")
        sys.exit(1)

OUTPUT_DIR = Path("/home/node/.openclaw/workspace/projects/musiclist-for-soundiiz/output/gui-screenshots")
BASE_URL = "http://localhost:8000"

def take_screenshots():
    """Take screenshots of all main pages"""
    
    # Setup Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Could not start Chrome: {e}")
        print("Make sure Chrome/Chromium is installed")
        return False
    
    screenshots = [
        ("00-landing-page.png", "/", "Landing Page"),
        ("01-login.png", "/accounts/login/", "Login Page"),
        ("02-dashboard.png", "/dashboard/", "Dashboard"),
        ("03-upload.png", "/scanner/upload/", "Upload Page"),
        ("04-scan-list.png", "/scanner/", "Scan List"),
        ("05-playlists.png", "/playlists/", "Playlists"),
        ("06-exports.png", "/exports/", "Exports"),
    ]
    
    taken = []
    for filename, path, description in screenshots:
        try:
            url = f"{BASE_URL}{path}"
            print(f"Taking screenshot of {description}...")
            driver.get(url)
            time.sleep(2)  # Wait for page to load
            
            filepath = OUTPUT_DIR / filename
            driver.save_screenshot(str(filepath))
            taken.append(filename)
            print(f"  ✓ Saved: {filepath}")
        except Exception as e:
            print(f"  ✗ Error taking {description}: {e}")
    
    # Mobile view
    try:
        print("Taking mobile view screenshot...")
        driver.set_window_size(375, 812)  # iPhone X size
        driver.get(f"{BASE_URL}/")
        time.sleep(2)
        filepath = OUTPUT_DIR / "99-mobile-view.png"
        driver.save_screenshot(str(filepath))
        taken.append("99-mobile-view.png")
        print(f"  ✓ Saved: {filepath}")
    except Exception as e:
        print(f"  ✗ Error taking mobile view: {e}")
    
    driver.quit()
    return taken

if __name__ == "__main__":
    print("=" * 60)
    print("Django App Screenshot Generator")
    print("=" * 60)
    print()
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if server is running
    import urllib.request
    try:
        urllib.request.urlopen(BASE_URL, timeout=5)
        print(f"✓ Server detected at {BASE_URL}")
    except:
        print(f"✗ Server not running at {BASE_URL}")
        print("Please start the server first with: just web-dev")
        sys.exit(1)
    
    print()
    print("Taking screenshots...")
    taken = take_screenshots()
    
    print()
    print("=" * 60)
    if taken:
        print(f"✓ Successfully took {len(taken)} screenshots")
        print(f"Location: {OUTPUT_DIR}")
        for s in taken:
            print(f"  - {s}")
    else:
        print("✗ No screenshots were taken")
    print("=" * 60)