import re
from collections import defaultdict

def calculate_daily_totals(text):
    daily_totals = defaultdict(lambda: {"riel": 0, "usd": 0.0})

    # Match each line with a date and amount
    lines = text.strip().splitlines()
    for line in lines:
        # Extract the date (e.g., "Jul 25")
        date_match = re.search(r'on (\w+ \d{1,2})', line)
        if not date_match:
            continue
        date = date_match.group(1)

        # Extract Riel (៛) amount
        riel_match = re.search(r'៛([\d,]+)', line)
        if riel_match:
            riel_amount = int(riel_match.group(1).replace(',', ''))
            daily_totals[date]["riel"] += riel_amount

        # Extract USD ($) amount
        usd_match = re.search(r'\$([\d,]+(?:\.\d+)?)', line)
        if usd_match:
            usd_amount = float(usd_match.group(1).replace(',', ''))
            daily_totals[date]["usd"] += usd_amount

    return daily_totals

# # Example input
# text = """
# Prem: ៛14,000 paid by NAY BOREY (*154) on Jul 25, 09:02 AM via ABA PAY at SAM SOKKOEUN. Trx. ID: 175340892771112, APV: 766398.
# Prem: ៛10,000 paid by NU CHANTOM (*364) on Jul 25, 10:52 AM via ABA PAY at SAM SOKKOEUN. Trx. ID: 175341554952709, APV: 619977.
# Prem: ៛1,500 paid by HOUR CHAN DARA (*164) on Jul 25, 11:02 AM via ABA PAY at SAM SOKKOEUN. Trx. ID: 175341613232328, APV: 141988.
# Prem: ៛17,000 paid by LUN VANDY (*403) on Jul 25, 11:06 AM via ABA PAY at SAM SOKKOEUN. Trx. ID: 175341638939336, APV: 675409.
# Prem: ៛7,000 paid by SUN BUNKREASFA (*555) on Jul 25, 01:02 PM via ABA PAY at SAM SOKKOEUN. Trx. ID: 175342333469387, APV: 761246.
# """

# # Calculate and print results
# daily_totals = calculate_daily_totals(text)
# for date, totals in daily_totals.items():
#     print(f"Date: {date} → ៛{totals['riel']:,} | ${totals['usd']:.2f}")
