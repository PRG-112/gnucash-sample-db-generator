# gnucash-sample-db-generator
GnuCash - Sample Database Generator


I never could find a proper GnuCash sample database to play with. Now, you can generate your own with this tool in no time. It's not perfect, but good enough. A sample database (1-JAN-2023 -> 31-DEC-2026) + premade-settings/reports (GCM) included. (see: EXTRAS)

##

--- PREREQUISITES: LINUX (Debian / Ubuntu):

    sudo apt-get install python3 libdbd-sqlite3
    python3 -m venv example_env
    source example_env/bin/activate
    pip install piecash faker

##

--- USAGE (once the above is satisfied):
        
    python3 -m venv example_env  (if rebooted)
    source example_env/bin/activate  (if rebooted)
    
    python3 gnucash_data_generator.py 
    gnucash gnucash_sample_db.gnucash

##

--- TWEAKS:

By default, the generator is set to USD and starts as of 1-JAN-2023 (WARNING: if your default currency is different, reports won't show anything until you change the commodity in the report's settings / properties). If you're looking for something else, edit the generator's code lines:

    start_year=2023
    default_currency="USD"


##

--- EXTRAS:

A sample database has been included (2023++). The GCM file provides already pre-configured reports.

- copy the GCM file to "GNC_DATA_HOME\books" directory (run GnuCash and click: HELP -> ABOUT -> GNC_CONFIG_HOME to see where it's at) then open the sample database with the same name as the file.
- !!! set the proper period (a must); run GnuCash then go to: EDIT -> PREFERENCES -> Accounting Period and set it accordingly to available data (between 2023-JAN and 2026-DEC). I'd advise to start with 2025-JAN-1 <-> 2025-DEC-31). Some reports have already preconfigured date to look better out of the box.
- to combine these reports with your own generated database (different currency) - open the GCM file and barch-replace all "USD" into chosen (default_currency) - "EUR" for instance

 ##
 --- SCREENSHOTS:

 ![Alt text](https://github.com/PRG-112/gnucash-sample-db-generator/blob/main/screenshots/screenshot_sample_db_assets.jpg "ASSETS")
 ![Alt text](https://github.com/PRG-112/gnucash-sample-db-generator/blob/main/screenshots/screenshot_sample_db_assets_2.jpg "ASSETS")
 ![Alt text](https://github.com/PRG-112/gnucash-sample-db-generator/blob/main/screenshots/screenshot_sample_db_expenses.jpg "EXPENSES")
 ![Alt text](https://github.com/PRG-112/gnucash-sample-db-generator/blob/main/screenshots/screenshot_sample_db_dashboard.jpg "Newly written DASHBOARD (v2)")
 ![Alt text](https://github.com/PRG-112/gnucash-sample-db-generator/blob/main/screenshots/screenshot_sample_db_accounts.jpg "Accounts")
