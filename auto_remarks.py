 import pandas as pd
import os

# 1. Look for the file in the current folder
input_filename = 'Sample sheet.csv'
output_filename = 'Sample_sheet_processed.csv'

if not os.path.exists(input_filename):
    print(f"ERROR: Could not find '{input_filename}' in this folder.")
    print("Please make sure your raw file is named exactly 'Sample sheet.csv' and placed here.")
    input("\nPress Enter to close...")
    exit()

print("1. Loading raw Tableau data...")
df = pd.read_csv(input_filename)

# 2. Logic to generate compliance remarks based on flags hitting 1
def get_remark(row):
    # Check flags
    ec = row['Early Closure Flag'] == 1
    ea = row['Excess Amount Flag'] == 1
    etx = row['Excess Transactions Flag'] == 1
    ha1_flag = row['Non Cash Repayment >=10l Flag (Daily)'] == 1
    ha2nd_flag = row['Non Cash Repayment >=15l Flag (Monthly)'] == 1
    ec2 = row['Early Closure Flag (More than 2 Accounts)'] == 1
    
    ha1 = False
    ha2nd = False
    ha2 = False
    
    if ha1_flag and ha2nd_flag:
        ha2 = True
    elif ha1_flag:
        ha1 = True
    elif ha2nd_flag:
        ha2nd = True

    # Assemble triggered tags
    tags = set()
    if ec: tags.add('EC')
    if ea: tags.add('EA')
    if etx: tags.add('Etx')
    if ha1: tags.add('HA1')
    if ha2nd: tags.add('HA2nd')
    if ha2: tags.add('HA2')
    if ec2: tags.add('EC2')

    if not tags:
        return "" # Leaves blank if no rules hit

    # Your standard text rules cataloged by combination sets
    rules = [
        ({'EC'}, "The customer has foreclosed the loan paying the remaining EMI amount before the tenure date."),
        ({'EA'}, "The customer has paid the EMI amount in excess (which is more than 100% of Loan Amount, also more than 1L)"),
        ({'EC', 'EA'}, "The customer has foreclosed the Loan paying the remaining EMI amount before the tenure date in excess (which is more than 100% of Loan Amount, also more than 1L)"),
        ({'EC', 'EA', 'HA1'}, "The customer has foreclosed the Loan paying before the tenure date with excess amount (which is more than 100% of Loan Amount, also more than 1L) and high amount (Non-cash 10L daily)"),
        ({'EC', 'EA', 'HA2'}, "The customer has foreclosed the Loan paying before the tenure date with excess amount (which is more than 100% of Loan Amount, also more than 1L) and high amount (Non-cash 10L daily and 15L monthly)"),
        ({'EA', 'HA1'}, "The customer has paid the EMI amount in excess (which is more than 100% of Loan Amount, also more than 1L) and with high amount (Non-cash 10L daily)"),
        ({'EA', 'HA2'}, "The customer has paid the EMI amount in excess (which is more than 100% of Loan Amount, also more than 1L) and with high amount (Non-cash 10L daily and 15L monthly)"),
        ({'EC', 'HA1'}, "The customer has foreclosed the loan paying the remaining EMI amount before the tenure date and with high amount (Non-cash 10L daily)"),
        ({'EC', 'HA2'}, "The customer has foreclosed the loan paying the remaining EMI amount before the tenure date and with high amount (Non-cash 10L daily and 15L monthly)"),
        ({'HA2nd'}, "The customer has paid the EMI with high amount (Non-cash 15L Monthly)"),
        ({'HA1'}, "The customer has paid the EMI with high amount (Non-cash 10L daily)"),
        ({'HA2'}, "The customer has paid the EMI with high amount (Non-cash 10L daily and 15L monthly)"),
        ({'EC', 'EA', 'Etx', 'HA1'}, "The customer has done multiple transactions in a single month to foreclose the Loan paying before the tenure date with excess amount (which is more than 100% of Loan Amount, also more than 1L) and high amount (Non-cash 10L daily)"),
        ({'EC', 'Etx', 'HA2'}, "The customer has done multiple transactions in a single month to foreclose the Loan paying before the tenure date with high amount (Non-cash 10L daily -Non-cash 15L monthly)"),
        ({'EC', 'Etx', 'HA2nd'}, "The customer has done multiple transactions in a single month to foreclose the Loan paying before the tenure date with high amount (Non-cash 15L monthly)"),
        ({'EC', 'EA', 'Etx', 'HA2'}, "The customer has done multiple transactions in a single month to foreclose the Loan paying before the tenure date with excess amount (which is more than 100% of Loan Amount, also more than 1L) and high amount (Non-cash 10L daily and 15L monthly)"),
        ({'Etx'}, "The customer has done multiple transactions in a single month."),
        ({'EC', 'EA', 'Etx'}, "The customer has done multiple transactions in a single month and foreclosed the Loan paying the remaining EMI amount before the tenure date in excess (which is more than 100% of Loan Amount, also more than 1L)"),
        ({'EC', 'Etx'}, "The customer has done multiple transactions in a single month and foreclosed the Loan paying the remaining EMI amount before the tenure date"),
        ({'EA', 'Etx'}, "The customer has done multiple transactions in a single month paying the EMI amount in excess (which is more than 100% of Loan Amount, also more than 1L)"),
        ({'EA', 'Etx', 'HA1'}, "The customer has done multiple transactions in a single month paying the EMI amount in excess (which is more than 100% of Loan Amount, also more than 1L) and with high amount (Non-cash 10L daily)"),
        ({'EA', 'Etx', 'HA2nd'}, "The customer has done multiple transactions in a single month to foreclose the Loan paying before the tenure date with excess amount (which is more than 100% of Loan Amount, also more than 1L)"),
        ({'EA', 'Etx', 'HA2'}, "The customer has done multiple transactions in a single month paying the EMI amount in excess (which is more than 100% of Loan Amount, also more than 1L) and with high amount (Non-cash 10L daily and 15L monthly)"),
        ({'Etx', 'HA2'}, "The customer has done multiple transactions in a single month paying the EMI with high amount (Non-cash 10L daily and 15L monthly)"),
        ({'Etx', 'HA1'}, "The customer has done multiple transactions in a single month paying the EMI with high amount (Non-cash 10L daily)"),
        ({'EC', 'EA', 'EC2'}, "The customer has foreclosed the Loan paying the remaining EMI amount before the tenure date in excess (which is more than 100% of Loan Amount, also more than 1L). Also, the customer has multiple accounts, closed within 30 days"),
        ({'EC', 'EA', 'EC2', 'HA2'}, "The customer has foreclosed the Loan paying the remaining EMI amount before the tenure date in excess (which is more than 100% of Loan Amount, also more than 1L) and high amount (Non-cash 10L daily and 15L monthly). Also, the customer has multiple accounts, closed within 30 days"),
        ({'EC', 'EC2'}, "The customer has foreclosed the Loan paying the remaining EMI amount before the tenure date. Also, the customer has multiple accounts which is closed within 30 days")
    ]
    
    for rule_tags, remark in rules:
        if tags == rule_tags:
            return remark
            
    return f"New Combination Detected: {', '.join(sorted(list(tags)))}"

# 3. Apply the processing rules
print("2. Automatically generating Remarks & filling Status columns...")
df['Compliance Alert Status'] = 'False positive'
df['Compliance Remarks'] = df.apply(get_remark, axis=1)

# 4. Save file
df.to_csv(output_filename, index=False)
print(f"3. DONE! Processed file saved as '{output_filename}'")
input("\nPress Enter to finish...")