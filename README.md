
Matches report lines (reimbursements) from Expensify to bank statements.

Matches on
* amount
* approximate date
* (cleaned up) description/merchant

# Input/Output
Expects
* `input/transactions.csv`
* `input/reimbursements.csv` (csv exported from Expensify. Default format.)
* `resources/description.json` (mappings to clean up the transaction/reimbursement descriptions - promote matching)

Outputs the whole venn diagram
* `output/join.csv` - Matches that were found between the two
* `output/unexpensed_transactions.csv` - Transactions without reimbursements
* `output/unmatched_reimbursements.csv` - Reimbursements without transactions.

# Work in progress
It's still a bit particular and hardcoded to my particular workspace.
* filepaths
* description mappings are most relevant to the last city I happened to be in
* csv headers my bank (Chase) uses

Some future iteration might include:
* integration with expensify
* distinguishing between reimbursable and non-reimbursable charges in expensify (who's reporting on non-reimbursable charges on expensify? Why?)

I've also noticed that airlines and hotels don't quite group their charges the same way I'll put things into expensify. For example, I might make 3 separate booking for airbnb and expense them separately, but get charged in lump sum. This script does not match those reimbursements/transactions.

Proceed at your own risk :)

```bash
python match_expenses.py
```

# Credits
Thanks @walkerdb for the inspiration and the starting script!
