### Co-author-statement-generator
This repository provides a Python script to modify Co-author statements for a PhD thesis based on NTNU Template by replacing placeholders (denoted by CAPITAL) with custom input values. It allows you to automate the process of generating `.odt` documents with dynamic paper titles, co-author names, thesis names.

## Requirements
- Python 3.x


### Run the Script
1. Open `main.py` and configure the `replacements` dictionary with your placeholder values:
   ```python
   replacements = {
       "THESIS NAME": "Hello, World!",
       "PAPER": "Python is awesome!",
       "CONTRIBUTION": "John Doe",
       "CO_AUTHOR_NAME": "WIilly Wonka",
   }
   ```
2. Run the script:
   ```bash
   python main.py
   ```
