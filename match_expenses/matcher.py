from datetime import timedelta

from loader import load_csv
from normalize_input import normalize
from printer import print_results

TRANSACTIONS_PATH = "input/transactions.csv"
REIMBURSEMENTS_PATH = "input/reimbursements.csv"

REIMBURSEMENTS_MAP = {
    "amount_header": "Amount",
    "description_header": "Merchant",
    "date_header": "\xef\xbb\xbfTimestamp",
    "date_format": "%Y-%m-%d"
}

TRANSACTIONS_MAP = {
    "amount_header": "Amount",
    "description_header": "Description",
    "date_header": "Post Date",
    "date_format": "%m/%d/%Y"
}


def main():
    reimbursements = load_csv(REIMBURSEMENTS_PATH)
    transactions = load_csv(TRANSACTIONS_PATH)

    print "reimbursements", len(reimbursements)
    print "transactions", len(transactions)
    print

    transactions = [t for t in transactions
                    if t["Type"] != "Payment"]
    normalize(transactions, TRANSACTIONS_MAP)
    normalize(reimbursements, REIMBURSEMENTS_MAP)

    matched_reimbursements, unmatched_reimbursements = match(reimbursements, transactions)

    print_results(matched_reimbursements, unmatched_reimbursements, transactions)


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
    rcost = reimbursement["Amount"]
    rdesc = reimbursement["Description"]
    tdate = transaction["Date"]
    tcost = transaction["Amount"]
    tdesc = transaction["Description"]
    if tcost == rcost and tdate - rdate < timedelta(days=5):
        if tdesc == rdesc:
            return True
        # print description for debugging purposes: maybe your description.json needs more love?
        # else:
        #     print(tdesc)
    return False


if __name__ == "__main__":
    main()
