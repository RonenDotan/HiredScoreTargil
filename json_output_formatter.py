import json
import copy

def format_output(candidates):
    tmp_candidates = copy.deepcopy(candidates)
    for ind, candidate in enumerate(tmp_candidates):
        if 'LinkedinCVSearch' in candidate:
            del tmp_candidates[ind]['LinkedinCVSearch']
    return json.dumps(tmp_candidates)
