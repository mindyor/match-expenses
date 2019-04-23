import csv
import re
from datetime import datetime, timedelta
import json


def main():
    transactions = load_transactions()
    reimbursements = load_reimbursements()

    reimbursed_transactions, unmatched_reimbursements = match(reimbursements, transactions)
    unexpensed_transactions = find_lonely_transactions(reimbursed_transactions, transactions)
    return reimbursed_transactions, unexpensed_transactions, unmatched_reimbursements


def find_lonely_transactions(reimbursed_transactions, transactions):
    transactions = {tuple(t.values()) for t in transactions}
    unexpensed_transactions = transactions.difference(reimbursed_transactions)
    return unexpensed_transactions


def match(reimbursements, transactions):
    reimbursed_transactions = set()
    unmatched_reimbursements = set()
    for reimbursement in reimbursements:
        found = False
        for transaction in transactions:
            if is_match(reimbursement, transaction):
                reimbursed_transactions.add(tuple(transaction.values()))
                found = True
                break
        if not found:
            print (reimbursement["Date"], reimbursement["Amount"], reimbursement["Merchant"])
            unmatched_reimbursements.add(tuple(reimbursement.values()))
    return reimbursed_transactions, unmatched_reimbursements


def is_match(reimbursement, transaction):
    rdate = reimbursement["Date"]
    rcost = str(reimbursement["Amount"])
    rdesc = reimbursement["Merchant"]
    tcost = transaction["Amount"]
    tdate = transaction["Date"]
    tdesc = transaction["Description"]
    if tcost == rcost and tdate - rdate < timedelta(days=5):
        if tdesc == rdesc:
            return True
        # print description for debugging purposes: maybe your description.json needs more love?
        # else:
        #     print(tdesc)
    return False


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
    tidied_description = description.upper()\
        .replace("SQ *", "")\
        .replace("&AMP;", "&")

    tidied_description = re.sub(" +", " ", tidied_description)

    description_map = json.load(open("resources/description.json"))

    for description_matcher, cleaned_description in description_map.iteritems():
        if re.search(description_matcher, tidied_description):
            return cleaned_description

    return tidied_description


def write_to_file(payload, filepath):
    with open(filepath, mode="w") as f:
        writer = csv.writer(f)
        writer.writerows(payload)


if __name__ == "__main__":
    matches, unexpensed, lonely_reimbursement = main()

    print "reimbursement & transaction match:", len(matches)
    write_to_file(matches, "output/join.csv")

    print "transactions without reimbursement:", len(unexpensed)
    write_to_file(unexpensed, "output/unexpensed_transactions.csv")

    print "reimbursement without matching transaction:", len(lonely_reimbursement)
    write_to_file(lonely_reimbursement, "output/unmatched_reimbursements.csv")

    print

    print "how's the math?"
    print "transactions ?=", len(matches) + len(unexpensed)
    print "reimbursements ?=", len(matches) + len(lonely_reimbursement)
