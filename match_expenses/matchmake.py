from datetime import timedelta


def match(expenses, transactions):
    matched_expenses = set()
    unmatched_expenses = set()
    for expense in expenses:
        found = False
        for transaction in transactions:
            if is_match(expense, transaction):
                matched_expenses.add(tuple(transaction.values()))
                found = True
                break
        if not found:
            print (expense["Date"], expense["Amount"], expense["Merchant"])
            unmatched_expenses.add(tuple(expense.values()))
    print
    return matched_expenses, unmatched_expenses


def is_match(expense, transaction):
    rdate = expense["Date"]
    rcost = expense["Amount"]
    rdesc = expense["Description"]
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
