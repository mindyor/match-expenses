import csv
from datetime import datetime
import re
import json

transactions_path = "input/transactions.csv"
reimbursements_path = "input/reimbursements.csv"

reimbursements_map = {
    "amount_header": "Amount",
    "description_header": "Merchant",
    "date_header": "\xef\xbb\xbfTimestamp",
    "date_format": "%Y-%m-%d"
}

transactions_map = {
    "amount_header": "Amount",
    "description_header": "Description",
    "date_header": "Post Date",
    "date_format": "%m/%d/%Y"
}


def load_reimbursements():
    reimbursements = load_csv(reimbursements_path)
    print "reimbursements", len(reimbursements)

    for reimbursement in reimbursements:
        normalize(reimbursement, reimbursements_map)
    return reimbursements


def load_transactions():
    transactions = load_csv(transactions_path)
    print "transactions", len(transactions)

    transactions = [t for t in transactions
                    if t["Type"] != "Payment"]
    for transaction in transactions:
        normalize(transaction, transactions_map)
    return transactions


def normalize(line_item, parse_map):
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

    description_map = json.load(open("resources/description.json"))

    for description_matcher, cleaned_description in description_map.iteritems():
        if re.search(description_matcher, tidied_description):
            return cleaned_description

    return tidied_description


def load_csv(path):
    with open(path, mode="r") as f:
        payload = list(csv.DictReader(f))
    return payload
