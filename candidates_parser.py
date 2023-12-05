from datetime import datetime


def parse_candidates(
    candidates_in, search_for_linkedin_address: callable = None, calculate_gaps=True
):
    candidates = []
    for candidate in candidates_in:
        candidate_first_name = (
            candidate.get("contact_info", {}).get("name", {}).get("given_name", "")
            or ""
        )
        candidate_last_name = (
            candidate.get("contact_info", {}).get("name", {}).get("family_name", "")
            or ""
        )
        candidate_email = candidate.get("contact_info", {}).get("email", "") or ""
        candidate_phone = candidate.get("contact_info", {}).get("phone", "") or ""
        if callable(search_for_linkedin_address):
            candidate_linkedin = search_for_linkedin_address(candidate)

        job_experience = []
        last_job_start_time = None
        candidate["experience"] = sorted(
            candidate["experience"],
            key=lambda x: datetime.strptime(x["start_date"], "%b/%d/%Y"),
            reverse=True,
        )
        for job_ind, job in enumerate(candidate["experience"]):
            role = job.get("title", "") or ""
            end_date = job.get("end_date", "") or ""
            end_date_d = datetime.strptime(end_date, "%b/%d/%Y")
            if calculate_gaps and last_job_start_time:
                gap = (last_job_start_time - end_date_d).days
                if gap > 1:
                    # we have a gap between jobs
                    job_experience[job_ind - 1]["Gap"] = f"{gap} days"
            start_date = job.get("start_date", "") or ""
            start_date_d = datetime.strptime(start_date, "%b/%d/%Y")
            last_job_start_time = start_date_d

            location = job.get("location", {}).get("short_display_address", "") or ""
            job_experience.append(
                {
                    "Role": role,
                    "StartDate": start_date,
                    "EndDate": end_date,
                    "Location": location,
                }
            )
        candidates.append(
            {
                "Name": {
                    "FirstName": candidate_first_name,
                    "LastName": candidate_last_name,
                },
                "Email": candidate_email,
                "Phone": candidate_phone,
                "LinkedinCVSearch": candidate_linkedin,
                "JobExperience": job_experience,
            }
        )

    return candidates
