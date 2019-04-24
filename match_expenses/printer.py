import csv


def write_to_file(payload, filepath):
    with open(filepath, mode="w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(payload)


def print_results(matches, unexpensed, lonely_reimbursement):
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
