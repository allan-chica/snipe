from playwright.sync_api import sync_playwright

def run_scraper():
	print("🔍 Starting LinkedIn job scraper...")

	search_url = (
		"https://www.linkedin.com/jobs/search/"
		"?f_TPR=r1800"
		"&keywords=frontend%20developer" # Keyword for job search
		"&f_E=2%2C3%2C4%2C5%2C6%2C7%2C8%2C9" # Full-time, Contract, Internship, etc.
		"&f_WT=2" # Remote jobs
		# "&f_JT=F"  # Full-time jobs
		"&location=Worldwide" # Location
	)

	with sync_playwright() as p:
		browser = p.chromium.launch(headless=True)
		page = browser.new_page()

		print("🌐 Navigating to LinkedIn...")
		# page.goto(search_url, wait_until="networkidle")
		page.goto(search_url, timeout = 60000)

		page.screenshot(path="linkedin.png", full_page=True)
		print("📸 Screenshot taken: linkedin.png")

		# Wait for job cards to load
		# page.wait_for_selector(".jobs-search__results-list")

		# Scrape a few jobs
		jobs = page.query_selector_all(".job-search-card")
		print(f"📦 Found {len(jobs)} job postings.")

		for job in jobs:
			title = job.query_selector(".base-search-card__title").inner_text()
			company = job.query_selector(".base-search-card__subtitle").inner_text()
			location = job.query_selector(".job-search-card__location").inner_text()
			time_posted = job.query_selector(".job-search-card__listdate--new")
			link = job.query_selector("a")

			print("-" * 30)
			print(f"🔹 Title: {title} {'(🕑 ' + time_posted.inner_text() + ')' if time_posted else ''}")
			print(f"🏢 Company: {company} in {location}")
			print(f"🔗 URL: {link.get_attribute("href") if link else ''}")

		browser.close()

if __name__ == "__main__":
	run_scraper()