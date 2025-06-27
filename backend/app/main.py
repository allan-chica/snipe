from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.scraping.linkedin import scrape

app = FastAPI()

# Frontend access for later
# app.add_middleware(
# 	CORSMiddleware,
# 	allow_credentials=True,
# 	allow_origins=["*"],
# 	allow_methods=["*"],
# 	allow_headers=["*"]
# )

@app.get("/jobs")
def read_jobs(
	keywords: str = Query("Frontend developer"),
	location: str = Query("latin america"),
	remote: bool = Query(True)
):
	jobs = scrape(keywords, location, remote)
	return {"results": jobs}