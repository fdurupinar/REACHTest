# REACHTest
Tests REACH with abstracts of publications

## To run:
Run reach-test.py

## Input:
PubMed ids to test are stored in pmIds.txt. Corresponding PMC ids, abstracts and whole texts are stored in the pm.db database.
If pm.db does not exist, it will be populated the firts time the program is run.

## Output
Runtime performance is recorded in performance.txt, where first column is the number of indexcards from REACH, the second column is the query runtime in seconds.

## To install required libraries:
- pip install requests
- pip install sqlite3
- pip install os
- pip install re
- pip install time
- pip install json
- pip install mathplotlib (optional)
