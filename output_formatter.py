import json_output_formatter
import print_output_formatter

def format_output(candidates, type):
    if type == "json":
        return json_output_formatter.format_output(candidates)
    elif type == "print":
        return print_output_formatter.format_output(candidates)
    else:
        raise Exception("Unsupported format type")
