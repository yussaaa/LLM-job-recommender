def filter_full_job_info(job):
    """
    Filters the given job dictionary to include only specific keys and formats the applyLink field.

    Args:
        job (dict): The job dictionary to be filtered.

    Returns:
        dict: The filtered job dictionary.
    """
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
