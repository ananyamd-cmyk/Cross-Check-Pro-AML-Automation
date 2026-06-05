# Cross-Check-Pro-AML-Automation
Automated Discrepancy &amp; Remark Generator for AML Compliance
1. PURPOSE OF THE PROJECT
In weekly Anti-Money Laundering (AML) monitoring, the operations team downloads a large tracking sheet directly from Tableau. This raw report contains 55 data columns detailing customer loans and repayments. The final two columns—Compliance Alert Status and Compliance Remarks—arrive completely blank and must be populated manually.
Reviewing thousands of transaction logs by hand to identify complex combinations of risk flags is an exhausting and time-consuming process. Cross-Check Pro was developed to eliminate this manual workflow completely by introducing a lightweight, dependable Python automation engine.

2. THE IDEA BEHIND IT
The core philosophy of this project is to turn text-based business guidelines into automated code logic. Instead of asking a human analyst to look across 55 columns, spot combinations of flags, and copy-paste text blocks, the Python script handles it instantly.
The script uses short text codes (Tags) to represent complex compliance events:
Tag Code	Tableau Column Reference	Rule Meaning / Trigger Condition
EC	Early Closure Flag	The customer closed their loan before the maturity date.
EA	Excess Amount Flag	Paid more than 100% of Loan Amount and more than 1 Lakh.
Etx	Excess Transactions Flag	Multiple repayment transactions within a single month.
HA1	Non-Cash Repayment >=10l Flag (Daily)	High-value daily repayment equal to or above 10 Lakhs.
HA2nd	Non-Cash Repayment >=15l Flag (Monthly)	High-value monthly repayment equal to or above 15 Lakhs.
HA2	Combined High Amount Check	Triggers when both daily (HA1) and monthly (HA2nd) are active.
EC2	Early Closure Flag (More than 2 Accounts)	Multiple loan accounts closed within a 30-day window.

3. HOW THE LOGIC WORKS
The system reviews each customer profile row-by-row and runs through a clean sequence:
1. File Detection: It looks for the raw file named exactly 'Sample sheet.csv' in its folder. If the file is missing, it shows a clear warning.
2. Default Clean-up: It sets the 'Compliance Alert Status' column for every record to 'False positive' automatically, matching standard operational protocol.
3. Flag Assembly: It checks which flags are marked as 1. If multiple flags are raised, it bundles them into a code set (for example: {'EC', 'EA'}).
4. Rule Matching: The script scans a catalog of 28 standard combination patterns to extract the matching text block.
5. New Pattern Safety Net: If a unique, uncataloged combination of flags appears, it safely flags it as "New Combination Detected" so the user never misses an unusual case.
Example Walkthrough:
If a row has both Early Closure Flag = 1 and Excess Amount Flag = 1, the code bundles them as {'EC', 'EA'} and instantly applies this exact remark: "The customer has foreclosed the Loan paying the remaining EMI amount before the tenure date in excess (which is more than 100% of Loan Amount, also more than 1L
4. PROJECT IMPACT & OUTCOMES
- Significant Time Reductions: Transitions an intensive, multi-hour manual review task into an automated process that executes in less than 2 seconds.
- Elimination of Errors: Eradicates common human typing mistakes, copy-paste misalignments, or overlooked columns.
- Consistent Compliance: Provides perfectly standard remarks across every weekly file, keeping data fully structured for external audits.
- Accessible Infrastructure: Designed to be simple. Any team member can run the application with a single click—no software experience needed.

5. Conclusion
Cross-Check Pro successfully changes a slow, stressful manual data entry task into a fast, one-click automated process. By using Python to instantly read and match complex compliance flags, the project completely eliminates human typing errors and ensures that every report looks perfectly uniform for company auditors. 
Ultimately, this automation saves the AML compliance team hours of repetitive work every week. It allows team members to stop spending time on manual copy-pasting and focus their energy on actual risk investigation and high-level data analysis. 

