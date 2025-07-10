import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

# Job list:
# https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Developer&start=0

# Job post:
# https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/4245287594

# Location options: worldwide, spain, argentina, latin america
# Timespan is in minutes

def scrape(keywords="Frontend developer", location="latin america", timespan=30, remote=True, start=0):

	headers = {
		"User-Agent": "Mozilla/5.0"
	}

	url = (
		"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
		f"?keywords={quote(keywords)}"
		f"&location={quote(location)}"
		f"&f_TPR=r{timespan * 60}"
		f"{'&f_WT=2' if remote else ''}"
		f"&start={start}" # Pagination
	)

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

			posted_str = date.text.strip() if date else date_new.text.strip() if date_new else ''

			jobs.append({
				'job_id': job_id,
				'title': title,
				'url': url,
				'company': company.text.strip() if company else '',
				'location': location.text.strip() if location else '',
				'posted': posted_str,
				'minutes_ago': parse_posted_time(posted_str)
			})

		except Exception:
			continue

	return jobs

def parse_posted_time(posted_str):
	"""
	Convert 'Just now', '1 minute ago', '2 hours ago', etc. to minutes.
	"""
	posted_str = posted_str.lower().strip()

	if "just now" in posted_str:
		return 0

	match = re.search(r"(\d+)\s+(minute|hour|day|week|month|year)", posted_str)
	if not match:
		return float('inf') # Push unknown times to end

	number = int(match.group(1))
	unit = match.group(2)

	if unit == "minute":
		return number
	elif unit == "hour":
		return number * 60
	elif unit == "day":
		return number * 60 * 24
	elif unit == "week":
		return number * 60 * 24 * 7
	elif unit == "month":
		return number * 60 * 24 * 30
	elif unit == "year":
		return number * 60 * 24 * 365

	return float('inf')