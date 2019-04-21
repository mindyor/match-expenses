import csv
from pprint import pprint
from datetime import datetime
from datetime import date
from datetime import timedelta
import re

def main():
    with open("txn_2019_2.csv", mode="r") as f:
        transactions = list(csv.DictReader(f))
    print "transactions", len(transactions)

    with open("reimbursements.csv", mode="r") as f:
        reimbursements = list(csv.DictReader(f))
    print "reimbursements", len(reimbursements)

    print

    transactions = [t for t in transactions
                    if t["Type"] != "Payment"]

    for transaction in transactions:
        transaction["Amount"] = str(transaction["Amount"]).replace(",", "").replace("-","")
        transaction["Date"] = datetime.strptime(transaction["Post Date"], "%m/%d/%Y").date()
        transaction["Description"] = tidy_desc(transaction["Description"])

    for reimbursement in reimbursements:
        reimbursement["Timestamp"] = datetime.strptime(reimbursement["\xef\xbb\xbfTimestamp"].split(" ")[0], "%Y-%m-%d").date()
        reimbursement["Amount"] = str(reimbursement["Amount"]).replace(",", "").replace("-","")
        reimbursement["Merchant"] = tidy_desc(reimbursement["Merchant"])

    reimbursed_transactions = []
    unmatched_reimbursements = []
    for reimbursement in reimbursements:
        rdate = reimbursement["Timestamp"]
        rcost = str(reimbursement["Amount"])
        rdesc = reimbursement["Merchant"]

        found = False
        for transaction in transactions:
            tcost = transaction["Amount"]
            tdate = transaction["Date"]
            tdesc = transaction["Description"]

            if tcost == rcost:
                if tdate - rdate < timedelta(days = 10):
                    if tdesc == rdesc:
                        reimbursed_transactions.append(tuple(transaction.values()))
                        found = True
        if not found:
            unmatched_reimbursements.append(tuple(reimbursement.values()))

    reimbursed_transactions = set(reimbursed_transactions)
    transactions = {tuple(t.values()) for t in transactions}
    reimbursements = {tuple(r.values()) for r in reimbursements}

    unexpensed_transactions = transactions.difference(reimbursed_transactions)
    return reimbursed_transactions, unexpensed_transactions, unmatched_reimbursements

def tidy_desc(description):
    tidied_description = description.upper().replace("SQ *","")
    tidied_description = tidied_description.replace("&AMP;","&")
    tidied_description = tidied_description.replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
    if "LYFT" in tidied_description:
        return "LYFT"
    if "TAXI" in tidied_description:
        return "TAXI"
    if "STARBUCKS" in tidied_description:
        return "STARBUCKS"
    if "AIRBNB" in tidied_description:
        return "AIRBNB"
    if "RESIDENCE INN" in tidied_description:
        return "MARRIOTT"
    if "MARRIOTT" in tidied_description:
        return "MARRIOTT"
    if "DOUBLETREE" in tidied_description:
        return "DOUBLETREE"
    if "WHOTELS" in tidied_description:
        return "W HOTELS"
    if "FLORET" in tidied_description:
        return "FLORET"
    if "ALASKA AIR" in tidied_description:
        return "ALASKA AIRLINES"
    if "RACHEL" in tidied_description:
        return "RACHEL'S GINGER BEER"
    if "THE JUICY CAFE" in tidied_description:
        return "8TH & OLIVE"
    if "GUARDIAN" in tidied_description:
        return "GUARDIAN NEWS & MEDIA"
    if "S TECHNICAL BOOKS" in tidied_description:
        return "ADA'S TECHNICAL BOOKS"
    if "UNITED AIR" in tidied_description:
        return "UNITED AIRLINES"
    if "LUCKY #736 OAKLAND" in tidied_description:
        return "LUCKY SUPERMARKETS"
    if "WALGREENS" in tidied_description:
        return "WALGREENS"
    if "WHOLEFDS" in tidied_description:
        return "WHOLE FOODS"
    if "KING'S CAFE" in tidied_description:
        return "SITKA AND SPRUCE"
    if "KUKAI RAMEN" in tidied_description:
        return "KUKAI RAMEN"
    if "RITE AID" in tidied_description:
        return "RITE AID"
    if "PEET" in tidied_description:
        return "PEET'S COFFEE AND TEAS"
    if "CENTURY CAFE" in tidied_description:
        return "CENTURY CAFE"
    if "SOUND TRANSIT" in tidied_description:
        return "SOUND TRANSIT"
    if bool(re.search("UNITED \d+", tidied_description)):
        return "UNITED AIRLINES"
    if bool(re.search(" CAB$", tidied_description)):
        return "TAXI"
    return tidied_description

def write_to_file(payload, filepath):
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerows(payload)

if __name__ == "__main__":
    matches, unexpensed, unmatched_reimbursements = main()

    print "reimbursement & transaction match:", len(matches)
    write_to_file(matches, "/Users/mindyor/play/finances/join.csv")

    print "transactions without reimbursement:", len(unexpensed)
    write_to_file(unexpensed, "/Users/mindyor/play/finances/unexpensed_transactions.csv")

    print "reimbursement without matching transaction:", len(unmatched_reimbursements)
    write_to_file(unmatched_reimbursements, "/Users/mindyor/play/finances/unmatched_reimbursements.csv")

    print

    print "how's the math?"
    print "transactions ?=", len(matches) + len(unexpensed)
    print "reimbursements ?=", len(matches) + len(unmatched_reimbursements)
