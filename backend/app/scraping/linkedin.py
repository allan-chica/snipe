from playwright.sync_api import sync_playwright
import json

def run_scraper():
	print("🔍 Starting LinkedIn job scraper...")

	search_url = (
		"https://www.linkedin.com/jobs/search/"
		"?f_TPR=r1800"
		"&keywords=frontend" # Keyword for job search
		# "&f_E=2%2C3%2C4%2C5%2C6%2C7%2C8%2C9" # Full-time, Contract, Internship, etc.
		"&f_WT=2" # Remote jobs
		# "&f_JT=F"  # Full-time jobs
		# "&location=Worldwide" # Location
		# "&location=Argentina" # Location
		"&geoId=91000011" # Location latin america
	)

	with sync_playwright() as p:
		browser = p.chromium.launch(headless=True)
		page = browser.new_page()

		print("🌐 Navigating to LinkedIn...")

		try:
			page.goto(search_url, timeout = 60000)
		except Exception as e:
			print(f"❌ Error navigating to LinkedIn: {e}")
			browser.close()
			return

		page.screenshot(path="linkedin.png", full_page=True)
		print("📸 Screenshot taken: linkedin.png")

		# Wait for job cards to load
		# page.wait_for_selector(".jobs-search__results-list")

		# Scrape a few jobs
		jobs = page.query_selector_all(".job-search-card")
		print(f"📦 Found {len(jobs)} job postings.")

		job_data = []

		for job in jobs:
			title = job.query_selector(".base-search-card__title")
			company = job.query_selector(".base-search-card__subtitle")
			location = job.query_selector(".job-search-card__location")
			time_posted = job.query_selector(".job-search-card__listdate--new")
			link = job.query_selector("a")

			time_info = time_posted.inner_text() if time_posted else None
			url = link.get_attribute("href") if link else None

			job_data.append({
				"title": title.inner_text().strip(),
				"company": company.inner_text().strip(),
				"location": location.inner_text().strip(),
				"time_posted": time_info.strip() if time_info else None,
				"url": url.strip() if url else None
			})

			# Log to console
			# print("-" * 30)
			# print(f"🔹 Title: {title} {'(🕑 ' + time_posted.inner_text() + ')' if time_posted else ''}")
			# print(f"🏢 Company: {company} in {location}")
			# print(f"🔗 URL: {link.get_attribute("href") if link else ''}")

		# Save job data to JSON file
		with open("linkedin.json", "w", encoding="utf-8") as f:
			json.dump(job_data, f, indent=4, ensure_ascii=False)

		browser.close()

if __name__ == "__main__":
	run_scraper()