import random
import uuid
import warnings
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from piecash import Account, create_book, Commodity, Transaction, Split, Price, open_book
from piecash.core.factories import create_currency_from_ISO
from faker import Faker
from sqlalchemy.exc import SAWarning


### EDIT per your own requirements

start_year=2023  # EndDate == end of this year
default_currency="USD"



print("\n\n--- Welcome to PRG's Gnucash Sample Database Generator. This has been tested and confirmed compliant with versions: 5.16 & 4.12\n")
print("--- More info/updates at:  https://github.com/PRG-112/gnucash-sample-db-generator\n\n")
warnings.filterwarnings("ignore", category=SAWarning)


def quantize(val):
    return Decimal(str(val)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

uuidGenCounter = 0
def generate_next_uuid():
    global uuidGenCounter
    counter_hex = f"{uuidGenCounter:012x}"
    uuid_string = f"{"10000000000000000000"}{counter_hex}"
    uuidGenCounter += 1
    return uuid.UUID(uuid_string).hex


def guidChange(book, account):    
    account.guid = generate_next_uuid()
    # book.save()
    
    
def setup_book(filename="gnucash_sample_db.gnucash"):
    print("--- Initializing structural GnuCash bookkeeping schema...")
    book = create_book(sqlite_file=filename, currency=default_currency, overwrite=True)
    book.guid = generate_next_uuid()
    # book.root_account.guid = generate_next_uuid()
    # guidChange(book, book.root_account)
   # guidChange(book, book.root_template)
    
        
    
    default_commodity = book.commodities.get(mnemonic=default_currency)
    root = book.root_account
        
    # Liquid Assets
    assets = Account(name="Assets", type="ASSET", parent=root, commodity=default_commodity)
    bank = Account(name="Checking Account", type="BANK", parent=assets, commodity=default_commodity)
    cash = Account(name="Cash", type="CASH", parent=assets, commodity=default_commodity)

    # Sub-Portfolios
    stock_p = Account(name="Stock Portfolio", type="ASSET", parent=assets, commodity=default_commodity)
    metal_p = Account(name="Precious Metals", type="ASSET", parent=assets, commodity=default_commodity)
    crypto_p = Account(name="Cryptocurrency Wallet", type="ASSET", parent=assets, commodity=default_commodity)

    # Liabilities & Revenue
    liabilities = Account(name="Liabilities", type="LIABILITY", parent=root, commodity=default_commodity)
    credit_card = Account(name="Credit Card", type="LIABILITY", parent=liabilities, commodity=default_commodity)
    mortgage = Account(name="Family Credit", type="LIABILITY", parent=liabilities, commodity=default_commodity)

    income = Account(name="Income", type="INCOME", parent=root, commodity=default_commodity)
    salary = Account(name="Salary Income", type="INCOME", parent=income, commodity=default_commodity)
    cap_gains = Account(name="Capital Gains", type="INCOME", parent=income, commodity=default_commodity)

    # Core Operating Expenses
    expenses = Account(name="Expenses", type="EXPENSE", parent=root, commodity=default_commodity)
    groceries = Account(name="Groceries", type="EXPENSE", parent=expenses, commodity=default_commodity)
    leisure = Account(name="Entertainment & Leisure", type="EXPENSE", parent=expenses, commodity=default_commodity)

    accommodation = Account(name="Housing & Accommodation", type="EXPENSE", parent=expenses, commodity=default_commodity)
    rent_mortgage = Account(name="Rent/Mortgage Payment", type="EXPENSE", parent=accommodation, commodity=default_commodity)
    utilities = Account(name="Utilities & Bills", type="EXPENSE", parent=accommodation, commodity=default_commodity)
    phone_internet = Account(name="Phone & Internet", type="EXPENSE", parent=accommodation, commodity=default_commodity)

    transport = Account(name="Transportation", type="EXPENSE", parent=expenses, commodity=default_commodity)
    fuel_transit = Account(name="Fuel & Public Transit", type="EXPENSE", parent=transport, commodity=default_commodity)
    auto_insurance = Account(name="Auto Insurance", type="EXPENSE", parent=transport, commodity=default_commodity)

    taxes = Account(name="Taxes", type="EXPENSE", parent=expenses, commodity=default_commodity)
    income_tax = Account(name="Withholding Income Tax", type="EXPENSE", parent=taxes, commodity=default_commodity)
    property_tax = Account(name="Property Tax", type="EXPENSE", parent=taxes, commodity=default_commodity)

    trading_fees = Account(name="Trading Fees", type="EXPENSE", parent=expenses, commodity=default_commodity)
    brokerage_fees = Account(name="Stock Commission Fees", type="EXPENSE", parent=trading_fees, commodity=default_commodity)
    crypto_gas_fees = Account(name="Crypto Exchange & Gas Fees", type="EXPENSE", parent=trading_fees, commodity=default_commodity)
    
    
    unsaved_accounts = [obj for obj in book.session.new if isinstance(obj, Account)]
    for account in unsaved_accounts:
        if not account.parent: # Skip root
            continue
        
        account.guid = generate_next_uuid()
        
 
    return (book, default_commodity, bank, cash, stock_p, metal_p, crypto_p, credit_card,
            salary, cap_gains, groceries, leisure, rent_mortgage, mortgage,
            utilities, phone_internet, fuel_transit, auto_insurance, income_tax,
            property_tax, brokerage_fees, crypto_gas_fees)


def build_market_registry(book, stock_p, metal_p, crypto_p):
    print("--- Configuring public security and alternative asset mappings...")
    asset_registry = {}
    current_prices = {}

    # 15 Public Equities
    stock_market_pool = [
        ("AAPL", "Apple Inc.", 120.0),
        ("MSFT", "Microsoft Corp.", 170.0),
        ("AMZN", "Amazon.com Inc.", 95.0),
        ("NVDA", "NVIDIA Corp.", 117.0),
        ("GOOGL", "Alphabet Inc.", 115.0),
        ("META", "Meta Platforms", 124.0),
        ("TSLA", "Tesla Inc.", 110.0),
        ("BRK.B", "Berkshire Hathaway", 123.0),
        ("V", "Visa Inc.", 106.0),
        ("JPM", "JPMorgan Chase", 170.0),
        ("UNH", "UnitedHealth Group", 230.0),
        ("XOM", "Exxon Mobil Corp.", 84.0),
        ("LLY", "Eli Lilly & Co", 126.0),
        ("JNJ", "Johnson & Johnson", 147.0),
        ("PRG", "PRG's Software & Gamble", 137.0)
    ]

    for ticker, name, start_price in stock_market_pool:
        comm = Commodity(namespace="NASDAQ", mnemonic=ticker, fullname=name, fraction=10000)
        book.add(comm)
        acc = Account(name=f"{ticker} ({name})", type="STOCK", parent=stock_p, commodity=comm)
        guidChange(book, acc)
        asset_registry[ticker] = {"account": acc, "shares": Decimal("0.0000"), "avg_cost": Decimal("0.0000")}
        current_prices[ticker] = Decimal(str(start_price))

    # Precious Metals (Troy ounces)
    metals_pool = [("XAU", "Gold (troy oz)", 3550.00), ("XAG", "Silver (troy oz)", 23.50)]

    for symbol, name, start_price in metals_pool:
        comm = Commodity(namespace="METALS", mnemonic=symbol, fullname=name, fraction=10000)
        book.add(comm)
        acc = Account(name=name, type="ASSET", parent=metal_p, commodity=comm)
        guidChange(book, acc)
        asset_registry[symbol] = {"account": acc, "shares": Decimal("0.0000"), "avg_cost": Decimal("0.0000")}
        current_prices[symbol] = Decimal(str(start_price))


    # Cryptocurrencies
    crypto_pool = [("BTC", "Bitcoin", 53000.00)]

    for symbol, name, start_price in crypto_pool:
        comm = Commodity(namespace="CRYPTO", mnemonic=symbol, fullname=name, fraction=1000000)
        book.add(comm)
        acc = Account(name=f"{name} ({symbol})", type="ASSET", parent=crypto_p, commodity=comm)
        guidChange(book, acc)
        asset_registry[symbol] = {"account": acc, "shares": Decimal("0.000000"), "avg_cost": Decimal("0.0000")}
        current_prices[symbol] = Decimal(str(start_price))

    return asset_registry, current_prices, stock_market_pool, crypto_pool, metals_pool



def run_simulation():
    # Fetch structures from prior scripts
    (book, dft_currency, bank, cash, stock_p, metal_p, crypto_p, credit_card,
     salary, cap_gains, groceries, leisure, rent_mortgage, mortgage,
     utilities, phone_internet, fuel_transit, auto_insurance, income_tax,
     property_tax, brokerage_fees, crypto_gas_fees) = setup_book()

    asset_registry, current_prices, stock_market_pool, crypto_pool, metals_pool = build_market_registry(
        book, stock_p, metal_p, crypto_p
    )

    fake = Faker('en_US')
    start_date, end_date = datetime(start_year, 1, 1), datetime(datetime.today().date().year, 12, 31, 23, 59, 59)
    daily_expense_pool = [
        (groceries, "Supermarket Run", 5.00, 21.00),
        (leisure, "Coffee & Restaurants", 5.00, 15.00),
        (fuel_transit, "Gas Station / Commute", 5.00, 21.00)
    ]

    current_date = start_date
    total_tx_count = 0
    tax_last_update, fixed_last_update, county_last_update, groceries_last_update = datetime(start_year-1, 1, 1), \
                datetime(start_year-1, 1, 1), datetime(start_year-1, 1, 1), datetime(start_year-1, 1, 1);

    print(f"--- Generating entries (salaries, taxes, stocks, credits, etc.). Time window:  [ {start_date.date()}  -  {end_date.date()} ]")


    #eq = quantize(12664.31)
    #tx = Transaction(currency=dft_currency, post_date=current_date.date(), description="Big Credit / Tax - initial liability")
    #Split(account=mortgage, transaction=tx, value=-eq)
    #Split(account=property_tax, transaction=tx, value=(eq))
    
    
    while current_date <= end_date:
        # Salaries (1st and 15th)
        if current_date.day in [1, 15] and current_date.date() > tax_last_update.date():
            credit_card_toppup = Decimal(str(random.uniform(75, 250)));
            if credit_card.get_balance() <= 300:
                credit_card_toppup = 0

            cash_toppup = 0;
            if cash.get_balance() < 200:
                cash_toppup = 200
                
            mortgage_toppup = Decimal(str(random.uniform(50, 200)));
            if mortgage.get_balance() < 200:
                mortgage_toppup = 0

            gross, tax = quantize(950.00), quantize(100.00)
            tx = Transaction(currency=dft_currency, post_date=current_date.date(), description="Corporate Payroll Settlement")
            Split(account=salary, transaction=tx, value=-gross)
            Split(account=bank, transaction=tx, value=(gross - tax - cash_toppup - credit_card_toppup)) #- mortgage_toppup))
            Split(account=income_tax, transaction=tx, value=tax)
            Split(account=cash, transaction=tx, value=cash_toppup)
            Split(account=credit_card, transaction=tx, value=credit_card_toppup)
            #Split(account=mortgage, transaction=tx, value=mortgage_toppup)
            
            total_tx_count += 1
            tax_last_update = current_date

        # Fixed Bills (1st of Month)
        if current_date.day == 1 and current_date.date() > fixed_last_update.date():
            for acc, desc, amt in [(rent_mortgage, "Rent Payment", Decimal(str(random.uniform(350, 500)))), (utilities, "Municipal Utilities", 50.50)]:
                tx = Transaction(currency=dft_currency, post_date=current_date.date(), description=desc)
                Split(account=bank, transaction=tx, value=-quantize(amt))
                Split(account=acc, transaction=tx, value=quantize(amt))
                total_tx_count += 1
            for acc, desc, amt in [(phone_internet, "Telecom Bundle", 35.00), (auto_insurance, "Car Premium", 55.00)]:
                tx = Transaction(currency=dft_currency, post_date=current_date.date(), description=desc)
                Split(account=credit_card, transaction=tx, value=-quantize(amt))
                Split(account=acc, transaction=tx, value=quantize(amt))
                total_tx_count += 1
            fixed_last_update = current_date

        # Taxes (April & October 15th)
        if current_date.month in [4, 10] and current_date.day == 15 and current_date.date() > county_last_update.date():
            tx = Transaction(currency=dft_currency, post_date=current_date.date(), description="County Property Tax")
            Split(account=bank, transaction=tx, value=-quantize(150.00))
            Split(account=property_tax, transaction=tx, value=quantize(150.00))
            total_tx_count += 1
            county_last_update = current_date

        # Retail Spending Loop
        for _ in range(random.choices([0, 1, 2, 3], weights=[0.15, 0.40, 0.35, 0.10])[0]):
            acc, prefix, low, high = random.choice(daily_expense_pool)
            amt = quantize(random.uniform(low, high))
            tx = Transaction(currency=dft_currency, post_date=current_date.date(), description=f"{prefix} - {fake.company()}")
            Split(account=(random.choice([bank, cash]) if (bank.get_balance() > 50 and cash.get_balance() > 50) else credit_card), transaction=tx, value=-amt)
            Split(account=acc, transaction=tx, value=amt)
            total_tx_count += 1

        # Price Volatility Steps
        for ticker in current_prices:
            drift =  random.uniform(-0.0005, 0.0005) if ticker in ["BTC"] else random.uniform(-0.0025, 0.0025)
            current_prices[ticker] = quantize(current_prices[ticker] * Decimal(str(1 + drift)))

        # Asset Actions Loop
        if random.random() < 0.75:
            chosen = random.choice([t for t in stock_market_pool] + [t for t in crypto_pool] + [t for t in metals_pool])[0]
            asset, price = asset_registry[chosen], current_prices[chosen]
            is_crypto = chosen in ["BTC"]
            fee_acc = crypto_gas_fees if is_crypto else brokerage_fees

            action = "BUY"
            if asset["shares"] > 0.1 and random.random() < 0.25:
                action = "SELL"


            if action == "BUY":
                qty = Decimal(str(round(random.uniform(0.00005, 0.00015), 5))) if is_crypto \
                        else Decimal(str(round(random.uniform(0.005, 0.03), 3))) if chosen in ["XAU"] \
                            else Decimal(str(round(random.uniform(0.3, 1.0), 2)))
                fee = quantize(qty * price * Decimal("0.015")) if is_crypto else quantize(0.95) if chosen in ["XAU", "XAG"] else quantize(0.66)
                cost = quantize(qty * price)

                curr_balance = bank.get_balance()
                if (curr_balance - (cost + fee)) < 300 or curr_balance < 300:
                    current_date += timedelta(minutes=800)
                    print(" .", end='', flush=True)
                    continue

                tx = Transaction(currency=dft_currency, post_date=current_date.date(), description=f"Asset Purchase: {chosen}")
                Split(account=bank, transaction=tx, value=-(cost + fee))
                Split(account=asset["account"], transaction=tx, value=cost, quantity=qty)
                Split(account=fee_acc, transaction=tx, value=fee)
                asset["shares"] += qty
                total_tx_count += 1
                print(" +", end='', flush=True)

            elif action == "SELL":
                qty = Decimal(str(round(random.uniform(0.0005, float(asset["shares"]*0.5)), 4))) if chosen in ["BTC"] \
                        else Decimal(str(round(random.uniform(0.10, float(asset["shares"])*0.5), 3)))
                fee = quantize(qty * price * Decimal("0.015")) if is_crypto else quantize(6.95) if chosen in ["XAU", "XAG"] else quantize(2.95)
                rev = quantize(qty * price)
                basis = quantize(rev + (rev * quantize(random.uniform(-0.29, 0.02))))
                tx = Transaction(currency=dft_currency, post_date=current_date.date(), description=f"Asset Sale: {chosen}")
                Split(account=bank, transaction=tx, value=(rev - fee))
                Split(account=asset["account"], transaction=tx, value=-basis, quantity=-qty)
                Split(account=fee_acc, transaction=tx, value=fee)
                Split(account=cap_gains, transaction=tx, value=-(rev - basis))
                asset["shares"] -= qty
                total_tx_count += 1
                print(" -", end='', flush=True)

        current_date += timedelta(minutes=600)

    usd = book.commodities.get(namespace="CURRENCY", mnemonic="USD")
    eur = create_currency_from_ISO("EUR")
    pln = create_currency_from_ISO("PLN")

    rate_price1 = Price(commodity=usd,currency=eur,date=datetime.today().date(),value=Decimal("0.85"),type="unknown",source="user:price")
    rate_price2 = Price(commodity=usd,currency=pln,date=datetime.today().date(),value=Decimal("3.7"),type="unknown",source="user:price")
    book.add(rate_price1)
    book.add(rate_price2)

    print(f"\n\n--- Compilation finished! Database entries successfully generated: {total_tx_count}", end="\n")
    print("--- Saving database to the file...")
    book.save()
    
    book.root_account.guid = generate_next_uuid()
    for child in book.root_account.children:
        child.parent = book.root_account
    book.save()


if __name__ == "__main__":
    run_simulation()
