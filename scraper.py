import time, pandas as pd, datetime, urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_indeed(roles, location):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    all_jobs = []

    for role in roles:
        url = f"https://in.indeed.com/jobs?q={urllib.parse.quote(role)}&l={urllib.parse.quote(location)}"
        driver.get(url)
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
        print(f"Found {len(cards)} jobs on the page.")

        for job in cards:
            job_data = {
                "Role": role,
                "Scraped On": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Job Title": job.find_element(By.CSS_SELECTOR, "h2 span").text if job.find_elements(By.CSS_SELECTOR, "h2 span") else "",
                "Company": job.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']").text if job.find_elements(By.CSS_SELECTOR, "span[data-testid='company-name']") else "",
                "Location": job.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']").text if job.find_elements(By.CSS_SELECTOR, "div[data-testid='text-location']") else location,
                "Salary": next((job.find_element(By.CSS_SELECTOR, sel).text for sel in ["div.salary-snippet-container", "span.attribute_snippet", "div#salaryInfoAndJobType"] if job.find_elements(By.CSS_SELECTOR, sel)), ""),
                "Link": job.find_element(By.CSS_SELECTOR, "a").get_attribute("href") if job.find_elements(By.CSS_SELECTOR, "a") else ""
            }
            all_jobs.append(job_data)

    driver.quit()
    if all_jobs:
        pd.DataFrame(all_jobs).to_csv("indeed_jobs.csv", index=False, encoding="utf-8-sig")
        print(f"Saved {len(all_jobs)} jobs to indeed_jobs.csv")
    else:
        print("No jobs scraped.")


roles_input = input("Enter job roles: ")
job_roles = [r.strip() for r in roles_input.split(",")]
job_location = input("Enter job location: ")
scrape_indeed(job_roles, job_location)
