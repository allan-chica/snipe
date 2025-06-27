import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote

# Job list:
# https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Developer&start=0

# Job post:
# https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/4245287594

def scrape():

	headers = {
		"User-Agent": "Mozilla/5.0"
	}

	keywords = "Frontend developer" # Keyword for job search
	timespan = "r1800"
	location = "Latin America" # Worldwide, Spain, Argentina, Latin America
	remote = True

	url = (
		"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
		f"?keywords={quote(keywords)}"
		f"&f_TPR={timespan}"
		f"&location={quote(location)}" # Location
		f"{'&f_WT=2' if remote else ''}" # Remote jobs
		"&start=0" # Pagination
	)

	res = requests.get(url, headers = headers)

	if not res.ok:
		print("Failed to fetch jobs: ", res.status_code)
		return

	soup = BeautifulSoup(res.text, "html.parser")
	job_cards = soup.find_all("li")

	job_list = []

	for job in job_cards:
		base_card = job.select_one(".base-card")
		job_id = base_card.get("data-entity-urn").split(":")[3]

		title = job.find('h3').text.strip()
		url = f'https://www.linkedin.com/jobs/view/{job_id}/'
		company = job.find('a', {"class": "hidden-nested-link"})
		location = job.find('span', {"class": "job-search-card__location"})

		date_new = job.find('time', {"class": "job-search-card__listdate--new"})
		date = job.find('time', {"class": "job-search-card__listdate"})

		job = {
			'title': title,
			'url': url,
			'company': company.text.strip() if company else '',
			'location': location.text.strip() if location else '',
			# 'date': date['datetime'] if date else date_new['datetime'] if date_new else '',
			'posted': date.text.strip() if date else date_new.text.strip() if date_new else ''
		}

		job_list.append(job)

	jobs_df = pd.DataFrame(job_list)
	jobs_df.to_csv('results/dev.csv', index=False)

	with open("results/linkedin.json", "w", encoding="utf-8") as f:
		json.dump(job_list, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
	scrape()