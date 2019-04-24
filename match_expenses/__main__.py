from loader import load_csv
from normalize_input import normalize
from printer import print_results
from matcher import match

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

    print "expenses", len(expenses)
    print "transactions", len(transactions)
    print

    transactions = [t for t in transactions
                    if t["Type"] != "Payment"]
    normalize(transactions, TRANSACTIONS_MAP)
    normalize(expenses, EXPENSES_MAP)

    matched_expenses, unmatched_expenses = match(expenses, transactions)

    print_results(matched_expenses, unmatched_expenses, transactions)


if __name__ == "__main__":
    main()
