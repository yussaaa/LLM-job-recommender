def filter_skills_and_job(job_parsed):
    """Filter the skills and first four keys of job key-value pairs from job_parsed

    Args:
        job_parsed (dict): job_parsed

    Returns:
        str: Serialized string of non-empty key-value pairs
    """
    unnested_dict = {}

    skills = job_parsed.get("skills", {})
    job = job_parsed.get("job", {})
    unnested_dict.update(skills)
    unnested_dict.update(
        {
            k: v
            for k, v in job.items()
            if k in ["title", "location", "years_of_experience_required"]
        }  # "industry",
    )

    serialized_string = ", ".join(f"{k}: {v}" for k, v in unnested_dict.items() if v)
    return serialized_string


if __name__ == "__main__":
    job_parsed = {
        "job": {
            "title": "Principal Engineer - AI & Machine Learning",
            "company": "Royal Bank of Canada",
            "industry": "Wealth Management",
            "location": "Toronto, ON, Canada",
            "years_of_experience_required": "",
            "employment_type": "Full time",
            "source": "RBC Careers",
            "application_link": "https://jobs.rbc.com/ca/en/job/R-0000075808/Principal-Engineer-AI-Machine-Learning?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic",
        },
        "skills": {
            "programming_languages": ["Python", "Java"],
            "data_visualization_tools": [],
            "databases": [],
            "devops_tools": ["Docker", "Kubernetes", "OpenShift"],
            "statistical_analysis_methods": [],
            "machine_learning_frameworks": [],
            "machine_learning_operations": ["MLOps"],
            "cloud_platforms": [],
            "big_data_technologies": ["Apache Spark", "Hadoop"],
            "natural_language_processing": [],
            "deep_learning_concepts": [],
            "data_engineering_tools": [],
            "large_models": [],
        },
        "company_culture": [
            "Flexible work/life balance options",
            "Leaders who support your development through coaching and managing opportunities",
        ],
        "job_benefits": {
            "salary_range": "",
            "salary_currency": "",
            "paid_time_off": "",
            "retirement_plan_matching": False,
            "professional_development_budget": "",
            "employee_discounts": "",
            "remote_work_policy": {
                "fully_remote_option": False,
                "partial_remote_option": "",
                "work_from_anywhere_program": "Up to 90 days/year",
            },
            "relocation_support": False,
        },
    }

    print(filter_skills_and_job(job_parsed))
