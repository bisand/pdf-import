# PDF import

Import special PDF files into SQLite databases and export again to Excel files using SQL statements

## Usage 

```bash
-f FILES [FILES ...], --files FILES [FILES ...]
                        PDF files to parse. Separate with space.
  -d DATABASE, --database DATABASE
                        Output SQLite3 database file.
  -q QUERY, --query QUERY
                        SQL query to export to Excel file.
  -x EXCEL, --excel EXCEL
                        Output Excel file.
  -o, --overwrite       Overwrite Excel file.
```
```bash
> python pdf-import.py --files test.pdf --database test.db --excel test.xlsx --query "select * from commission_report_items" --overwrite
```
