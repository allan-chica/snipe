import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Job list:
# https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Developer&start=0

# Job post:
# https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/4245287594

# Location options: worldwide, spain, argentina, latin america
# Timespan is in minutes

def scrape(keywords="Frontend developer", location="latin america", timespan=30, remote=True):

	headers = {
		"User-Agent": "Mozilla/5.0"
	}

	url = (
		"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
		f"?keywords={quote(keywords)}"
		f"&location={quote(location)}"
		f"&f_TPR=r{timespan * 60}"
		f"{'&f_WT=2' if remote else ''}"
		"&start=0" # Pagination
	)

	print(url)

	res = requests.get(url, headers = headers)

	if not res.ok:
		return []

	soup = BeautifulSoup(res.text, "html.parser")
	job_cards = soup.find_all("li")

	jobs = []

	for job in job_cards:
		try:
			base_card = job.select_one(".base-card")
			job_id = base_card.get("data-entity-urn").split(":")[3]

			title = job.find('h3').text.strip()
			url = f'https://www.linkedin.com/jobs/view/{job_id}/'
			company = job.find('a', {"class": "hidden-nested-link"})
			location = job.find('span', {"class": "job-search-card__location"})

			date_new = job.find('time', {"class": "job-search-card__listdate--new"})
			date = job.find('time', {"class": "job-search-card__listdate"})

			jobs.append({
				'title': title,
				'url': url,
				'company': company.text.strip() if company else '',
				'location': location.text.strip() if location else '',
				# 'date': date['datetime'] if date else date_new['datetime'] if date_new else '',
				'posted': date.text.strip() if date else date_new.text.strip() if date_new else ''
			})

		except Exception:
			continue

	with open("results/linkedin.json", "w", encoding="utf-8") as f:
		json.dump(jobs, f, indent=4, ensure_ascii=False)

	return jobs

if __name__ == "__main__":
	scrape()