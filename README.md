
Matches report lines (reimbursements) from expensify to bank statements.

Matches on
* amount
* approximate date
* description

# Input/Output
Expects
* transactions.csv
* reimbursements.csv (csv exported from Expensify. Default format.)

Outputs the whole venn diagram
* Matches that were found between the two
* Transactions without reimbursements
* Reimbursements without transactions.

# Work in progress
It's still a bit particular and hardcoded to my particular workspace.
* filepaths
* description mappings are most relevant to the last city I happened to be in

Some future iteration might include:
* integration with expensify
* a more extracted list of description mappings
* distinguishing between reimbursable and non-reimbursable charges in expensify (who's reporting on non-reimbursable charges on expensify? Why?)

I've also noticed that airlines and hotels don't quite group their charges the same way I'll put things into expensify. For example, I might make 3 separate booking for airbnb and expense them separately, but get charged in lump sum. This script does not match those reimbursements/transactions.

Proceed at your own risk :)

```bash
python match_expenses.py
```

# Credits
Thanks @walkerdb for the inspiration and the starting script!
