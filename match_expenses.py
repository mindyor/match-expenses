import csv
import re
from datetime import datetime
from datetime import timedelta


def main():
    with open("transactions.csv", mode="r") as f:
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
        reimbursement["Date"] = datetime.strptime(reimbursement["\xef\xbb\xbfTimestamp"].split(" ")[0], "%Y-%m-%d").date()
        reimbursement["Amount"] = str(reimbursement["Amount"]).replace(",", "").replace("-","")
        reimbursement["Merchant"] = tidy_desc(reimbursement["Merchant"])

    reimbursed_transactions = []
    unmatched_reimbursements = []
    for reimbursement in reimbursements:
        rdate = reimbursement["Date"]
        rcost = str(reimbursement["Amount"])
        rdesc = reimbursement["Merchant"]

        found = False
        for transaction in transactions:
            tcost = transaction["Amount"]
            tdate = transaction["Date"]
            tdesc = transaction["Description"]

            if tcost == rcost:
                # print(rdesc, tdesc, rdate, tdate, rcost, tcost)
                if tdate - rdate < timedelta(days = 5):
                    if tdesc == rdesc:
                        reimbursed_transactions.append(tuple(transaction.values()))
                        found = True
                        break
        if not found:
            print(rdate, rcost, rdesc)
            unmatched_reimbursements.append(tuple(reimbursement.values()))

    reimbursed_transactions = set(reimbursed_transactions)
    transactions = {tuple(t.values()) for t in transactions}

    unexpensed_transactions = transactions.difference(reimbursed_transactions)
    return reimbursed_transactions, unexpensed_transactions, unmatched_reimbursements

def tidy_desc(description):
    tidied_description = description.upper()\
        .replace("SQ *", "")\
        .replace("&AMP;", "&")

    tidied_description = re.sub(" +", " ", tidied_description)

    description_map = {
        "AIRBNB": "AIRBNB",
        "ALASKA AIR": "ALASKA AIRLINES",
        re.compile(" CAB$"): "Taxi",
        "CENTURY CAFE": "CENTURY CAFE",
        "DOUBLETREE": "DOUBLETREE",
        "FLORET": "FLORET",
        "GUARDIAN": "GUARDIAN NEWS & MEDIA",
        "THE JUICY CAFE": "8TH & OLIVE",
        "KING'S CAFE": "SITKA AND SPRUCE",
        "KUKAI RAMEN": "KUKAI RAMEN",
        "LYFT": "LYFT",
        "MARRIOTT": "MARRIOTT",
        "LUCKY #736 OAKLAND": "LUCKY SUPERMARKETS",
        "PEET": "PEET'S COFFEE AND TEAS",
        "RESIDENCE INN": "MARRIOTT",
        "RITE AID": "RITE AID",
        "RACHEL": "RACHEL'S GINGER BEER",
        "S TECHNICAL BOOKS": "ADA'S TECHNICAL BOOKS",
        "SOUND TRANSIT": "SOUND TRANSIT",
        "STARBUCKS": "STARBUCKS",
        "TAXI": "TAXI",
        "UNITED AIR": "UNITED AIRLINES",
        re.compile("UNITED \d+"): "UNITED AIRLINES",
        "WALGREENS": "WALGREENS",
        "WHOLEFDS": "WHOLE FOODS",
        "WHOTELS": "W HOTELS",
    }

    for description_matcher, cleaned_description in description_map.items():
        if re.search(description_matcher, tidied_description):
            return cleaned_description

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
