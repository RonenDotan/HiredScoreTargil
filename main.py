import get_data_from_url as get_data
import data_reader
import linkedin_address
import candidates_parser
import output_formatter
import enrichment


def activate_targil(
    candidates_url,
    candidates_file_type,
    secondary_data_url,
    secondary_data_file_type,
    matches_config,
    calculate_gaps=True,
):
    try:
        data = get_data.get_data(url=candidates_url)
        candidates_unparsed = data_reader.read_data(data, candidates_file_type)
        candidates = candidates_parser.parse_candidates(
            candidates_in=candidates_unparsed,
            search_for_linkedin_address=linkedin_address.search_for_linkedin_address,
            calculate_gaps=calculate_gaps,
        )
        json_format = output_formatter.format_output(candidates, "json")
        print(json_format)
        text_for_print = output_formatter.format_output(candidates, "print")
        print(text_for_print)
        data_secondary = get_data.get_data(url=secondary_data_url)
        candidates_secondary_data = data_reader.read_data(
            data_secondary, secondary_data_file_type
        )
        enrichment.enrich_candidates_data(
            candidates=candidates,
            secondary_data=candidates_secondary_data,
            matches_config=matches_config,
            linkedin_address_validation=linkedin_address.linkedin_address_validation,
        )
        print(candidates)
        return candidates
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    matches_config = [
        {
            "id": "linkedin-adress-in-cv",
            "candidate_key": lambda candidate: candidate.get("LinkedinCVSearch", "-"),
            "secondary_key": lambda row: "",
            "compare_function": lambda candidate_key, secondary_key: linkedin_address.linkedin_address_validation(
                candidate_key
            ),
            "result_function": lambda candidate, row: candidate.get(
                "LinkedinCVSearch", "-"
            ),
            "priority": 0,
        },
        {
            "id": "email",
            "candidate_key": lambda candidate: candidate["Email"].lower(),
            "secondary_key": lambda row: row["Email"].lower(),
            "priority": 1,
        },
        {
            "id": "phone-basic",
            "candidate_key": "Phone",
            "secondary_key": "Phone Number",
            "priority": 2,
        },
        {
            "id": "phone-with-replace",
            "candidate_key": lambda candidate: candidate["Phone"].replace("-", ""),
            "secondary_key": lambda row: row["Phone Number"].replace("-", ""),
            "priority": 3,
        },
        {
            "id": "name2linkedin",
            "candidate_key": lambda candidate: f'{candidate["Name"]["FirstName"]}{candidate["Name"]["LastName"]}'.lower(),
            "secondary_key": lambda row: row["Linkedin"]
            .lower()
            .replace("https://linkedin.com/in/", "")
            .replace("-", ""),
            "compare_function": lambda candidate_key, secondary_key: candidate_key
            in secondary_key,
            "priority": 4,
        },
        {
            "id": "email2linkedin",
            "candidate_key": lambda candidate: candidate["Email"].lower().split("@")[0],
            "secondary_key": lambda row: row["Linkedin"]
            .lower()
            .replace("https://linkedin.com/in/", "")
            .replace("-", ""),
            "compare_function": lambda candidate_key, secondary_key: candidate_key
            in secondary_key,
            "priority": 5,
        },
    ]

    activate_targil(
        candidates_url="https://bit.ly/3eTzIN4",
        candidates_file_type="json",
        secondary_data_url="https://hs-recruiting-test-resume-data.s3.amazonaws.com/linkedin_source_b1f6-acde48001122.csv",
        secondary_data_file_type="csv",
        matches_config=matches_config,
        calculate_gaps=True,
    )
