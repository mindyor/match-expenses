from datetime import timedelta

import loader
import printer


def main():
    transactions = loader.load_transactions()
    reimbursements = loader.load_reimbursements()

    reimbursed_transactions, unmatched_reimbursements = match(reimbursements, transactions)
    unexpensed_transactions = find_lonely_transactions(reimbursed_transactions, transactions)

    printer.print_results(reimbursed_transactions, unexpensed_transactions, unmatched_reimbursements)


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
    rdesc = reimbursement["Description"]
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


if __name__ == "__main__":
    main()
