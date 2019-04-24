import csv
from datetime import datetime
import re
import json

transactions_path = "input/transactions.csv"
reimbursements_path = "input/reimbursements.csv"

reimbursements_date_format = "%Y-%m-%d"
transactions_date_format = "%m/%d/%Y"


def load_reimbursements():
    reimbursements = load_csv(reimbursements_path)
    print "reimbursements", len(reimbursements)

    for reimbursement in reimbursements:
        reimbursement["Date"] = parse_date(reimbursement["\xef\xbb\xbfTimestamp"], reimbursements_date_format)
        reimbursement["Amount"] = normalize_amount(reimbursement["Amount"])
        reimbursement["Merchant"] = normalize_description(reimbursement["Merchant"])
    return reimbursements


def load_transactions():
    transactions = load_csv(transactions_path)
    print "transactions", len(transactions)

    transactions = [t for t in transactions
                    if t["Type"] != "Payment"]
    for transaction in transactions:
        transaction["Date"] = parse_date(transaction["Post Date"], transactions_date_format)
        transaction["Amount"] = normalize_amount(transaction["Amount"])
        transaction["Description"] = normalize_description(transaction["Description"])
    return transactions


def parse_date(date, date_format):
    return datetime.strptime(date.split(" ")[0],date_format).date()


# note: takes the absolute value of the amount
def normalize_amount(amount):
    return str(amount).replace(",", "").replace("-", "")


def normalize_description(description):
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
