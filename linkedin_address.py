import re


def search_for_linkedin_address(candidate):
    candidate_as_str = str(candidate)
    linkedin_pos = candidate_as_str.find("linkedin.com")
    pattern = r"[,;|\'}]"
    linkedin_address = re.split(pattern, candidate_as_str[linkedin_pos:])[0]
    if linkedin_address_validation(linkedin_address):
        return linkedin_address
    else:
        return ""


def linkedin_address_validation(linkedin_address):
    if len(linkedin_address) < 20 or len(linkedin_address) > 200:
        return False
    else:
        return True
