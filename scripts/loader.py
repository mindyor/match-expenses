import csv
from datetime import datetime
import re
import json


def load_reimbursements():
    with open("input/reimbursements.csv", mode="r") as f:
        reimbursements = list(csv.DictReader(f))
    print "reimbursements", len(reimbursements)
    print

    for reimbursement in reimbursements:
        reimbursement["Date"] = datetime.strptime(reimbursement["\xef\xbb\xbfTimestamp"].split(" ")[0],
                                                  "%Y-%m-%d").date()
        reimbursement["Amount"] = str(reimbursement["Amount"]).replace(",", "").replace("-", "")
        reimbursement["Merchant"] = tidy_desc(reimbursement["Merchant"])
    return reimbursements


def load_transactions():
    with open("input/transactions.csv", mode="r") as f:
        transactions = list(csv.DictReader(f))
    print "transactions", len(transactions)

    transactions = [t for t in transactions
                    if t["Type"] != "Payment"]
    for transaction in transactions:
        transaction["Amount"] = str(transaction["Amount"]).replace(",", "").replace("-", "")
        transaction["Date"] = datetime.strptime(transaction["Post Date"], "%m/%d/%Y").date()
        transaction["Description"] = tidy_desc(transaction["Description"])
    return transactions


def tidy_desc(description):
    tidied_description = description.upper() \
        .replace("SQ *", "") \
        .replace("&AMP;", "&")

    tidied_description = re.sub(" +", " ", tidied_description)

    description_map = json.load(open("resources/description.json"))

    for description_matcher, cleaned_description in description_map.iteritems():
        if re.search(description_matcher, tidied_description):
            return cleaned_description

    return tidied_description
