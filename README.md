## Description

Matches report lines (expenses/reimbursements) from Expensify to bank statements.

Matches on
* amount
* approximate date
* (cleaned up) description/merchant

#### Context

Digging through my finances, I wanted to know my _real_ spend rate over time - how much am I spending that I haven't expensed?

@walkerdb said, oh I have a script for that. This script is a fork off of theirs.

After using this script to filter out all of the transactions I had reimbursed, I was able to see a much cleaner picture of my spending.

I could also start to categorize and build pretty graphs (and find an item that had slipped through the cracks)... 
but that's a script for another time.

## Input/Output

Expects
* `input/transactions.csv`
* `input/expenses.csv` (csv exported from Expensify. Default format.)
* `resources/description.json` (mappings to clean up the transaction/expense descriptions - promote matching)

Outputs the whole venn diagram
* `output/join.csv` - Matches that were found between the two
* `output/unexpensed_transactions.csv` - Transactions without expenses
* `output/unmatched_expenses.csv` - Expenses without corresponding transactions.

## Work in progress!

It's still a bit particular and hardcoded to my particular workspace.
* description mappings are most relevant to the last city I happened to be in
* csv headers my bank (Chase) uses

I've also noticed that airlines and hotels don't quite group their charges the same way I'll put things into expensify. 
For example, I might make 3 separate booking for airbnb and expense them separately, but get charged in lump sum. 
This script does not match those expenses/transactions.

Due to some combination of the fuzziness of matching, not taking out transactions when they match), 
and general laziness and wanting to use sets, multiple expenses might be marked as matched even if they match to the same transaction.
So, for example, if you expensed 2 coffees but only bought one, this script would not complain.
And if you got 2 of the same coffees on the same days, and only expensed one of them, this script still would not complain.

Also it's on Python 2. Will probably switch to Python 3.

Proceed at your own risk :)

To run:
```bash
pip install -r requirements.txt
python match_expenses
```

To run:
```bash
pylint match_expenses/
```


## Out of (near term) scope

* integration with Expensify
* distinguishing between reimbursable and non-reimbursable charges (who's reporting on non-reimbursable charges on expensify? Why?)

# Credits

Thanks @walkderdb for initial inspiration and starting script.

Thanks @walkderdb and @Ablexxive for feedback!
