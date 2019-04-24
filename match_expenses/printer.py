import csv


def print_results(matched_transaction, unmatched_reimbursement, transactions):
    print "reimbursement & transaction match:", len(matched_transaction)
    write_to_file(matched_transaction, "output/join.csv")

    print "reimbursement without matching transaction:", len(unmatched_reimbursement)
    write_to_file(unmatched_reimbursement, "output/unmatched_reimbursements.csv")

    unmatched_transaction = find_lonely_transactions(transactions, matched_transaction)
    print "transactions without reimbursement:", len(unmatched_transaction)
    write_to_file(unmatched_transaction, "output/unexpensed_transactions.csv")
    print

    print "how's the math?"
    print "total transactions ?=", len(matched_transaction) + len(unmatched_transaction)
    print "total reimbursements ?=", len(matched_transaction) + len(unmatched_reimbursement)


def find_lonely_transactions(transactions, matched_transactions):
    transactions = {tuple(t.values()) for t in transactions}
    unexpensed_transactions = transactions.difference(matched_transactions)
    return unexpensed_transactions


def write_to_file(payload, filepath):
    with open(filepath, mode="w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(payload)
