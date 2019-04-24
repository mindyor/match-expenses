from matchio import load_csv, print_results
from normalize import normalize
from matchmake import match

TRANSACTIONS_PATH = "input/transactions.csv"
EXPENSES_PATH = "input/expenses.csv"

EXPENSES_MAP = {
    "amount_header": "Amount",
    "description_header": "Merchant",
    "date_header": "Timestamp",
    "date_format": "%Y-%m-%d"
}

TRANSACTIONS_MAP = {
    "amount_header": "Amount",
    "description_header": "Description",
    "date_header": "Post Date",
    "date_format": "%m/%d/%Y"
}


def main():
    expenses = load_csv(EXPENSES_PATH)
    transactions = load_csv(TRANSACTIONS_PATH)
    transactions = [t for t in transactions
                    if t["Type"] != "Payment"]

    print "expenses", len(expenses)
    print "transactions", len(transactions)
    print

    normalize(transactions, TRANSACTIONS_MAP)
    normalize(expenses, EXPENSES_MAP)

    matched_expenses, unmatched_expenses = match(expenses, transactions)

    print_results(matched_expenses, unmatched_expenses, transactions)


if __name__ == "__main__":
    main()
