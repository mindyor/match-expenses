from datetime import datetime
import re
import json

DESCRIPTION_MAP_PATH = "resources/description.json"


def normalize(iterable, parse_map):
    for line_item in iterable:
        normalize_amount(line_item, parse_map["amount_header"])
        normalize_description(line_item, parse_map["description_header"])
        normalize_date(line_item, parse_map["date_header"], parse_map["date_format"])


def normalize_date(line_item, date_header, date_format):
    date = line_item[date_header]
    line_item["Date"] = datetime.strptime(date.split(" ")[0], date_format).date()


# note: takes the absolute value of the amount
def normalize_amount(line_item, amount_header):
    amount = line_item[amount_header]
    line_item["Amount"] = str(amount).replace(",", "").replace("-", "")


def normalize_description(line_item, description_header):
    description = line_item[description_header]
    line_item["Description"] = normalize_description_content(description)


def normalize_description_content(description):
    tidied_description = description.upper() \
        .replace("SQ *", "") \
        .replace("&AMP;", "&")

    tidied_description = re.sub(" +", " ", tidied_description)

    description_map = json.load(open(DESCRIPTION_MAP_PATH))

    for description_matcher, cleaned_description in description_map.iteritems():
        if re.search(description_matcher, tidied_description):
            return cleaned_description

    return tidied_description
