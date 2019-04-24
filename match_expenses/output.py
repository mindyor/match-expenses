import csv


def print_results(matched_transactions, unmatched_expenses, transactions):
    unmatched_transaction = find_lonely_transactions(transactions, matched_transactions)

    print "expense & transaction match:", len(matched_transactions)
    print "expenses without matching transaction:", len(unmatched_expenses)
    print "transactions without expense:", len(unmatched_transaction)
    print

    write_to_file(matched_transactions, "output/join.csv")
    write_to_file(unmatched_expenses, "output/unmatched_expenses.csv")
    write_to_file(unmatched_transaction, "output/unexpensed_transactions.csv")

    print_debug(matched_transactions, unmatched_expenses, unmatched_transaction)


def find_lonely_transactions(transactions, matched_transactions):
    transactions = {tuple(t.values()) for t in transactions}
    unexpensed_transactions = transactions.difference(matched_transactions)
    return unexpensed_transactions


def write_to_file(payload, filepath):
    with open(filepath, mode="w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(payload)


def print_debug(matched_transactions, unmatched_expenses, unmatched_transaction):
    print "how's the math?"
    print "total transactions ?=", len(matched_transactions) + len(unmatched_transaction)
    print "total expenses ?=", len(matched_transactions) + len(unmatched_expenses)
    print
