from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.scraping.linkedin import scrape

app = FastAPI()

# Frontend access for later
app.add_middleware(
	CORSMiddleware,
	allow_credentials=True,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"]
)

@app.get("/jobs")
def read_jobs(
	keywords: str = Query("Frontend developer"),
	location: str = Query("latin america"),
	timespan: int = 30,
	remote: bool = Query(True)
):
	job_list = []
	max_pages = 10

	for page in range(max_pages):
		jobs = scrape(keywords, location, timespan, remote, start=len(job_list))
		job_list.extend(jobs)

		if (len(jobs) < 10):
			break

	job_list.sort(key=lambda job: job['minutes_ago'])

	return {"results": job_list, "number_of_jobs": len(job_list)}