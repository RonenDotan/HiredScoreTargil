def format_output(candidates):
    return_text = ""
    for candidate in candidates:
        return_text += f'Hello {candidate["Name"]["FirstName"]} {candidate["Name"]["LastName"]}\n'
        for job in candidate["JobExperience"]:
            return_text += f'Worked as: {job["Role"]}, From {job["StartDate"]} To {job["EndDate"]} in {job["Location"]}\n'
        return_text += f"\n"
    return return_text