import csv
from pprint import pprint
from datetime import datetime

def main():
    with open("transactions.csv", mode="r") as f:
        transactions = list(csv.DictReader(f))
    print "transactions", len(transactions)

    with open("reimbursements.csv", mode="r") as f:
        reimbursements = list(csv.DictReader(f))
    print "reimbursements", len(reimbursements)

    print

    for transaction in transactions:
        transaction["Amount"] = str(transaction["Amount"]).replace(",", "").replace("-","")
        transaction["Date"] = str(datetime.strptime(transaction["Post Date"], "%m/%d/%Y").date())

    for reimbursement in reimbursements:
        reimbursement["Timestamp"] = reimbursement["\xef\xbb\xbfTimestamp"].split(" ")[0]
        reimbursement["Amount"] = str(reimbursement["Amount"]).replace(",", "").replace("-","")

    reimbursed_transactions = []
    for transaction in transactions:
        tcost = transaction["Amount"]
        tdate = transaction["Date"]

        for reimbursement in reimbursements:
            rdate = reimbursement["Timestamp"].split(" ")[0]
            rcost = str(reimbursement["Amount"])

            if tdate == rdate and tcost == rcost:
                reimbursed_transactions.append(tuple(transaction.values()))

    reimbursed_transactions = set(reimbursed_transactions)
    transactions = {tuple(t.values()) for t in transactions}
    reimbursements = {tuple(r.values()) for r in reimbursements}

    unexpensed_transactions = transactions.difference(reimbursed_transactions)
    return reimbursed_transactions, unexpensed_transactions

def write_to_file(payload, filepath):
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerows(payload)

if __name__ == "__main__":
    matches, unexpensed = main()

    print "matches with reimbursements", len(matches)
    write_to_file(matches, "/Users/mindyor/play/finances/matches.csv")

    print "unexpensed transactions", len(unexpensed)
    write_to_file(unexpensed, "/Users/mindyor/play/finances/unexpensed_transactions.csv")

