from datetime import timedelta


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
