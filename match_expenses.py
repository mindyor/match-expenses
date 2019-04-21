import csv
from pprint import pprint
from datetime import datetime

def main():
    with open("reimbursements.csv", mode="r") as f:
        reimbursements = list(csv.DictReader(f))
    print "reimbursements", len(reimbursements)

    with open("transactions.csv", mode="r") as f:
        transactions = list(csv.DictReader(f))
    print "transactions", len(transactions)

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

    print "transactions", len(transactions)
    print "reimbursed transactions", len(reimbursed_transactions)
    print

    return transactions.difference(reimbursed_transactions), reimbursements.difference(transactions)


if __name__ == "__main__":
    results, leftovers = main()
    print "results", len(results)
    with open("/Users/mindyor/play/finances/output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(results)

    print "leftovers", len(leftovers)
    with open("/Users/mindyor/play/finances/leftovers.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(leftovers)

