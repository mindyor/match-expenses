import csv
import re
from datetime import datetime
from datetime import timedelta
import json


def main():
    transactions = load_transactions()
    reimbursements = load_reimbursements()

    reimbursed_transactions = []
    unmatched_reimbursements = []
    for reimbursement in reimbursements:
        rdate = reimbursement["Date"]
        rcost = str(reimbursement["Amount"])
        rdesc = reimbursement["Merchant"]

        found = False
        for transaction in transactions:
            tcost = transaction["Amount"]
            tdate = transaction["Date"]
            tdesc = transaction["Description"]

            if tcost == rcost:
                # print(rdesc, tdesc, rdate, tdate, rcost, tcost)
                if tdate - rdate < timedelta(days=5):
                    if tdesc == rdesc:
                        reimbursed_transactions.append(tuple(transaction.values()))
                        found = True
                        break
        if not found:
            print(rdate, rcost, rdesc)
            unmatched_reimbursements.append(tuple(reimbursement.values()))

    reimbursed_transactions = set(reimbursed_transactions)
    transactions = {tuple(t.values()) for t in transactions}

    unexpensed_transactions = transactions.difference(reimbursed_transactions)
    return reimbursed_transactions, unexpensed_transactions, unmatched_reimbursements


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
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerows(payload)


if __name__ == "__main__":
    matches, unexpensed, unmatched_reimbursements = main()

    print "reimbursement & transaction match:", len(matches)
    write_to_file(matches, "/Users/mindyor/play/finances/output/join.csv")

    print "transactions without reimbursement:", len(unexpensed)
    write_to_file(unexpensed, "/Users/mindyor/play/finances/output/unexpensed_transactions.csv")

    print "reimbursement without matching transaction:", len(unmatched_reimbursements)
    write_to_file(unmatched_reimbursements, "/Users/mindyor/play/finances/output/unmatched_reimbursements.csv")

    print

    print "how's the math?"
    print "transactions ?=", len(matches) + len(unexpensed)
    print "reimbursements ?=", len(matches) + len(unmatched_reimbursements)
