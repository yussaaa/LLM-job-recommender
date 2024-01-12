def filter_full_job_info(job):
    keys_to_filter = [
        "title",
        "companyName",
        "location",
        "via",
        "description",
        "metadata",
        # "applyLink",
    ]
    job_filtered = {key: job[key] for key in keys_to_filter}
    job_filtered["applyLink"] = job["applyLink"]["link"]
    # job_filtered["metadata"] = "".join(job["metadata"].values())

    return job_filtered
