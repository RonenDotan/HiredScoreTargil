def enrich_candidates_data(
    candidates,
    secondary_data,
    matches_config,
    linkedin_address_validation: callable = None,
    save_linkdin_match_config_id=False,
):
    for candidate in candidates:
        min_priority = float("inf")
        curr_candidate_matches_config = matches_config[:]
        for row in secondary_data:
            match_config_id, match_priority, match_value = match_candidate(
                candidate=candidate,
                secondary_data_item=row,
                matches_config=curr_candidate_matches_config,
                linkedin_address_validation=linkedin_address_validation,
            )
            if match_priority < min_priority:
                candidate["Linkedin_url"] = match_value
                # We might want to save the match config id, so it would be clear how did we get the match
                # for now - we wold not save it (not in the requirements)
                if save_linkdin_match_config_id:
                    candidate["LinkedinMatchConfigId"] = match_config_id
                min_priority = match_priority
                # We can filter our configs that with worse priority than the current match
                curr_candidate_matches_config = list(
                    filter(
                        lambda x: x["priority"] < min_priority,
                        curr_candidate_matches_config,
                    )
                )


def match_candidate(
    candidate,
    secondary_data_item,
    matches_config,
    linkedin_address_validation: callable = lambda x: len(x) > 0,
):
    if not linkedin_address_validation(secondary_data_item["Linkedin"]):
        return ("NoMatch", float("inf"), None)

    for config in matches_config:
        if callable(config["candidate_key"]):
            candidate_key = config["candidate_key"](candidate)
        else:
            candidate_key = candidate[config["candidate_key"]]

        if callable(config["secondary_key"]):
            second_key = config["secondary_key"](secondary_data_item)
        else:
            second_key = secondary_data_item[config["secondary_key"]]

        if "result_function" in config:
            linkedin_address = config["result_function"](candidate, secondary_data_item)
        else:
            linkedin_address = secondary_data_item["Linkedin"]

        if "compare_function" in config:
            if config["compare_function"](candidate_key, second_key):
                return (
                    config["id"],
                    config["priority"],
                    linkedin_address,
                )
        elif candidate_key == second_key:
            return (config["id"], config["priority"], linkedin_address)
    return ("NoMatch", float("inf"), None)
