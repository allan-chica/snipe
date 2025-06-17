from playwright.sync_api import sync_playwright
import json
import os
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("LINKEDIN_EMAIL")
password = os.getenv("LINKEDIN_PASSWORD")

COOKIE_PATH = "linkedin_cookies.json"

def save_cookies(context):
	cookies = context.cookies()
	with open(COOKIE_PATH, "w", encoding="utf-8") as f:
		json.dump(cookies, f, indent=4, ensure_ascii=False)
	print("💾 Saved cookies.")

def load_cookies(context):
	if os.path.exists(COOKIE_PATH):
		with open(COOKIE_PATH, "r", encoding="utf-8") as f:
			cookies = json.load(f)
			context.add_cookies(cookies)
			print("🍪 Loaded cookies.")
	else:
		print("⚠️ No cookies found.")

def is_logged_in(page):
	try:
		page.goto("https://www.linkedin.com/feed/", timeout=60000)
		page.wait_for_selector("img.global-nav__me-photo", timeout=5000)
		# return "feed" in page.url
		return True
	except:
		return False

def login(page):
	print("🔐 Logging in to LinkedIn...")
	page.goto("https://www.linkedin.com/login")

	page.fill("input[name='session_key']", email)
	page.fill("input[name='session_password']", password)
	page.click("button[type='submit']")

	page.wait_for_url("https://www.linkedin.com/feed/", timeout=10000)
	print("✅ Logged in.")

def run():
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=True)
		context = browser.new_context()
		page = context.new_page()

		load_cookies(context)

		if not is_logged_in(page):
			login(page)
			save_cookies(context)
		else:
			print("✅ Already logged in.")

		print("🌐 Navigating to LinkedIn feed...")
		page.goto("https://www.linkedin.com/feed/", timeout=60000)

		page.screenshot(path="linkedin_feed.png", full_page=True)
		print("📸 Screenshot taken: linkedin_feed.png")

		browser.close()

if __name__ == "__main__":
	run()