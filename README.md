# Bank Document parser for calculating monthly budget.

A boring monthly task that I automated. Its a simple rule based system that weirdly works. 

# SBI Savings
For some reason the raw file is not redable. Convert the file to xlsx (from excel for example) and then use the parser.

# ICICI Savings
Buggy. 

# HDFC Credit Card Statements
All the statements from HDFC cards are in a similar structure (thankfully). Because of the billing cycle problem, each month's statement will have previous months transactions as well. For now, this has to be manually corrected after the processing. 

# To start using it:
Create the following files:
 - A `s3cret5.py` file in the root and add `DOCUMENTS_PDF_PASSWORD_REGELIA` and `DOCUMENTS_PDF_PASSWORD_TATA_NEU`. 
 - Add a `KEYWORDS` dict, for example:
```py
KEYWORDS = {
    "Food": ["food", "swiggy", 'kfc'],
     "Travel": ["cab", "ride"],
}
```
The `post_processing.py` script will create new columns for each category in the dict and add the `Debit` values of each transation everytime a `keyword` is present in the discription. I use this as an initial boost to segregate the transaction. While not all the transactions can be handeled, it does cover a major part of my lists. Ofcourse, the keywords can be imporved over time. 