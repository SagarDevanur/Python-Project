# Library Record System
> A command-line library management system that reads book, member, and borrowing
> records from text files and automatically generates a detailed report — showing
> borrowing stats, member activity, book popularity, and borrowing limit violations.

## Features
-  **File-based Input** — reads records, books & members from `.txt` files
-  **Auto Reports** — saves a full report to `reports.txt` automatically
-  **Limit Warnings** — flags members who exceed their borrowing limits with `!`
-  **Stats & Insights** — most popular books, most active members & day averages

## How to Run
```bash
# Records only
python my_record.py records.txt

# Records + Books
python my_record.py records.txt books.txt

# Full output (Records + Books + Members)
python my_record.py records.txt books.txt members.txt

## Input File Format

| File | Format |
|------|--------|
| `books.txt` | `BookID, Name, Type(T/F), Copies, MaxDays, LateCharge` |
| `members.txt` | `MemberID, FirstName, LastName, DOB, Type(Standard/Premium)` |
| `records.txt` | `BookID, MemberID: Days, ...` (use `R` for reserved) |

## Project Structure

- `Records` — manages all data, reads files, displays & saves reports
- `Book` — models a book with type, copies, borrow/reserve tracking
- `Member` — models a member with type, borrowing limits & averages

## Requirements

- Python 3.x
- No external libraries — only uses the built-in `sys` module
