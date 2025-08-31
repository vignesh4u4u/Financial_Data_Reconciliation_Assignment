# Data Quality and Summary Report

## Missing Values per Column

| Column Name | NaN Count |
| :---------- | --------: |
| invoice_id  | 20        |
| date_erp    | 20        |
| date_bank   | 20        |
| amount_erp  | 20        |
| amount_bank | 20        |
| amount_diff | 40        |
| discrepancy | 0         |

## Unique Values per Column

| Column Name   | Unique Count |
| :------------ | -----------: |
| discrepancy   | 5            |
| amount_diff   | 8            |
| date_bank     | 59           |
| date_erp      | 60           |
| amount_bank   | 199          |
| invoice_id    | 200          |
| amount_erp    | 200          |

## Dataset Shape

The dataset contains 228 rows and 7 columns.

## Statistical Summary Report

| Statistic | invoice_id | ... | discrepancy           |
| :-------- | :--------- | :-- | :-------------------- |
| count     | 208        | ... | 228                   |
| unique    | 200        | ... | 5                     |
| top       | INV0055    | ... | Amounts Match Exactly |
| freq      | 2          | ... | 181                   |
| mean      | NaN        | ... | NaN                   |
| min       | NaN        | ... | NaN                   |
| 25%       | NaN        | ... | NaN                   |
| 50%       | NaN        | ... | NaN                   |
| 75%       | NaN        | ... | NaN                   |
| max       | NaN        | ... | NaN                   |
| std       | NaN        | ... | NaN                   |

## Discrepancy Column Summary

| Discrepancy Type            | Count |
| :-------------------------- | ----: |
| Amounts Match Exactly       | 181   |
| Transaction Missing in Bank | 20    |
| Transaction Missing in ERP  | 20    |
| Minor Rounding Difference   | 4     |
| Amount Mismatch             | 3     |

## Duplicate Rows

Total duplicate rows count: 8