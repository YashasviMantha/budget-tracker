# Bank Document parser for calculating monthly budget.

A boring monthly task that I automated. Its a simple rule based system that weirdly works. 

# SBI Savings
For some reason the raw file is not redable. Convert the file to xlsx (from excel for example) and then use the parser.

# ICICI Savings
Works out of the box.

# HDFC Credit Card Statements
All the statements from HDFC cards are in a similar structure (thankfully). Because of the billing cycle problem, each month's statement will have previous months transactions as well. For now, this has to be manually corrected after the processing. 

# SBI Cash Back card
A bit unstable. But works out of box. The SBI guys seems to have changed their PDF generation mid of the year.

# ICICI Amazon Card
Work in progress

# To start using it:
Create a file called `s3cret5.py` and:
 - Add `DOCUMENTS_PDF_PASSWORD_REGELIA` and `DOCUMENTS_PDF_PASSWORD_TATA_NEU` and other passwords. 
 - Add a `KEYWORDS` dict, for example:
```py
KEYWORDS = {
    "Food": ["food", "swiggy", 'kfc'],
     "Travel": ["cab", "ride"],
}
```
The `post_processing.py` script will create new columns for each category in the dict and add the `Debit` values of each transation everytime a `keyword` is present in the discription. I use this as an initial boost to segregate the transaction. While not all the transactions can be handeled, it does cover a major part of my lists. Ofcourse, the keywords can be imporved over time. 

Then store all your statements in a singe directory. Like this:
```
statements
  icici.xls
  sbi.xlsx
  hdfc_regelia.pdf
  hdfc_neu.pdf
```

And use the `test.ipynb` to process. Names of the statements are used to detect the type of statement