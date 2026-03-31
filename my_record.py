
# I have used sys library file

import sys
# defined a class  called Record to define operate on records txt of the program

class Records:
    # defined a constructor to store data from books, members txt files and initialised a variable to store number of dayas a book is borrowed. 
    def __init__(self):
        self.books = []
        self.members = []
        self.borrowed_days = {}

    # defined a method to store the records and books txt files
    def read_records(self, record_file, book_file):
        self.read_book_file(book_file)
        self.read_record_file(record_file)

    # defined a method to read the contents of books txt file
    def read_book_file(self, book_file):
        with open(book_file, 'r') as file:
            for line in file:
                data = line.strip().split(', ')
                book_id, name, book_type, copies, max_days, late_charge = data
                copies = int(copies)
                max_days = int(max_days)
                late_charge = float(late_charge)
                book = Book(book_id, name, book_type, copies, max_days, late_charge)
                if book_type == 'F' and max_days <= 14:
                    print(f"Error: Fiction book '{name}' has maximum borrowing days less than or equal to 14.")
                    sys.exit(1)
                self.books.append(book)

    # defined a method to read the contents of records txt file
    def read_record_file(self, record_file):
        with open(record_file, 'r') as file:
            for line in file:
                data = line.strip().split(', ')
                book_id = data[0]
                book = next((b for b in self.books if b.book_id == book_id), None)
                if book is None:
                    print(f"Error: Book with ID '{book_id}' not found in the book file.")
                    sys.exit(1)
                for i in data[1:]:
                    member_id, days = i.split(': ')
                    book.borrow(member_id, days)
                    if member_id not in self.borrowed_days:
                        self.borrowed_days[member_id] = {}
                    self.borrowed_days[member_id][book_id] = days

    # defined a method to display the information of members txt file
    def display_member_info(self):
        print("\nMEMBER INFORMATION")
        print(" " + "-" * 93)
        print("|MemberID  FName      LName       Type       DOB            Ntextbook   Nfiction   Average|")
        print(" " + "-" * 93)

        month_names = {
            '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
            '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
        }

        for member in self.members:
            borrowed_textbooks = member.get_num_borrowed_textbooks(self)
            reserved_textbooks = member.get_num_reserved_textbooks(self)
            total_textbooks = borrowed_textbooks + reserved_textbooks

            borrowed_fictions = member.get_num_borrowed_fictions(self)
            reserved_fictions = member.get_num_reserved_fictions(self)
            total_fictions = borrowed_fictions + reserved_fictions

            textbook_limit = "!" if not member.check_borrowing_limit(self) and total_textbooks > (2 if member.member_type == 'Premium' else 1) else " "
            fiction_limit = "!" if not member.check_borrowing_limit(self) and total_fictions > (3 if member.member_type == 'Premium' else 2) else " "

            dob_parts = member.dob.split('/')
            month_name = month_names[dob_parts[0]]
            formatted_dob = f"{int(dob_parts[1]):02d}-{month_name}-{dob_parts[2]}"

            print(f"|{member.member_id:<9} {member.first_name:<10} {member.last_name:<11} {member.member_type:<10} {formatted_dob:>11}  {total_textbooks:>9}{textbook_limit} {total_fictions:>8}{fiction_limit}   {member.get_average_borrowed_days(self):>7.2f}  |")
        print(" " + "-" * 93)

        max_borrowed = max(len(self.borrowed_days[m.member_id]) for m in self.members)
        active_members = [m for m in self.members if len(self.borrowed_days[m.member_id]) == max_borrowed]
        print(f"The most active member is {active_members[0].first_name} {active_members[0].last_name} with {max_borrowed} books borrowed/reserved.")

        min_avg_days = min(m.get_average_borrowed_days(self) for m in self.members)
        least_avg_members = [m for m in self.members if m.get_average_borrowed_days(self) == min_avg_days]
        print(f"The member with the least average borrowing days is {least_avg_members[0].first_name} {least_avg_members[0].last_name} with {min_avg_days:.2f} days.")

    # defined a method to display the data in records txt file
    def display_records(self):
        title = [book.book_id for book in self.books]
        print("\nRECORDS")
        print(" " + "-" * 56)
        print('|MemberID   ' + '     '.join(title))
        print(" " + "-" * 56)

        # Create a set to store unique member IDs from the borrowed_days dictionary
        member_ids = set(self.borrowed_days.keys())

        for member_id in member_ids:
            if not any(m.member_id == member_id for m in self.members):
                self.members.append(Member(member_id, "", "", "", ""))
        
        # Add members to the members list if they are not already present
        for member in self.members:
            row = [member.member_id]
            for book in self.books:
                days = book.borrowed_days.get(member.member_id, 'xx')
                if days == 'R':
                    days = '--'
                row.append(str(days).rjust(6, ' '))
            print('\t'.join(row))
        print(" " + "-" * 56)

        total_days = 0
        total_books = 0
        for book in self.books:
            for days in book.borrowed_days.values():
                try:
                    total_days += int(days)
                    total_books += 1
                except ValueError:
                    # If days is not an integer (e.g., 'R'), skip it
                    continue

        num_books = len(self.books)
        num_members = len(self.members)
        avg_days = total_days / total_books if total_books > 0 else 0
        print("RECORDS SUMMARY")
        print(f"There are {num_members} members and {num_books} books.")
        print(f"The average number of borrow days is {avg_days:.2f} (days).")

     # defined a method to display the data in books txt file
    def display_book_info(self):
        print("\nBOOKS INFORMATION")
        print(" " + "-" * 116)
        print("|BookID    Name                Type        Ncopy   Maxday  Lcharge  Nborrow  Nreserv  Range     |   ")
        print(" " + "-" * 116)

        for book in self.books:
            print(f"|{book.book_id:<9} {book.name:<19} {book.book_type:<9} {book.copies:>6}  {book.max_days:>6}  {book.late_charge:>7}  {book.get_num_borrowed():>6}  {book.get_num_reserved():>6}       {book.get_borrow_days_range():<9}|")
        print(" " + "-" * 116)

        max_borrowed_reserved = max(book.get_num_borrowed() + book.get_num_reserved() for book in self.books)
        popular_books = [book for book in self.books if book.get_num_borrowed() + book.get_num_reserved() == max_borrowed_reserved]
        if len(popular_books) == 1:
            print(f"The most popular book is {popular_books[0].name}.")
        else:
            book_names = ', '.join(book.name for book in popular_books)
            print(f"The most popular books are {book_names}.")

        max_borrowed_days = max(book.get_max_borrowed_days() for book in self.books)
        longest_borrowed_books = [book for book in self.books if book.get_max_borrowed_days() == max_borrowed_days]
        if len(longest_borrowed_books) == 1:
            print(f"The book with the longest borrowing days is {longest_borrowed_books[0].name}.")
        else:
            book_names = ', '.join(book.name for book in longest_borrowed_books)
            print(f"The books with the longest borrowing days are {book_names}.")

    # defined a method to save and store the book information
    def save_book_info(self, output_file):
        with open(output_file, 'w') as file:
            file.write("\nBOOK INFORMATION\n")
            file.write(" " + "-" * 116 + "\n")
            file.write("|BookID   Name               Type     |Ncopy  |Maxday |Lcharge |Nborrow|Nreserv|Range    \n")
            file.write(" " + "-" * 116 + "\n")

            for book in self.books:
                file.write(f"|{book.book_id:<9}|{book.name:<19}|{book.book_type:<9}|{book.copies:>6} |{book.max_days:>6} |{book.late_charge:>7} |{book.get_num_borrowed():>6} |{book.get_num_reserved():>6} |{book.get_borrow_days_range():<9}\n")
            file.write(" " + "-" * 116 + "\n")

    # defined a method to read data from member txt file
    def read_member_file(self, member_file):
        with open(member_file, 'r') as file:
            for line in file:
                data = line.strip().split(', ')
                member_id, first_name, last_name, dob, member_type = data
                self.members.append(Member(member_id, first_name, last_name, dob, member_type))

    # defined a method to derive the bookID from book txt file
    def get_book_by_id(self, book_id):
        return next((b for b in self.books if b.book_id == book_id), None)

# created a class book to define and operate on books txt of the program
class Book:
    #defined a constructor to initialize variables to store different values for book information
    def __init__(self, book_id, name, book_type, copies, max_days, late_charge):
        self.book_id = book_id
        self.name = name
        self.book_type = 'Textbook' if book_type == 'T' else 'Fiction'
        self.copies = copies
        self.max_days = max_days
        self.late_charge = late_charge
        self.borrowed_days = {}

    #defined a method to store the days to respective members
    def borrow(self, member_id, days):
        self.borrowed_days[member_id] = days

    # defined a method return the borrrowed days
    def get_num_borrowed(self):
        return sum(1 for days in self.borrowed_days.values() if days != 'R')

    # defined a method to return the reserved days
    def get_num_reserved(self):
        return sum(1 for days in self.borrowed_days.values() if days == 'R')

    # definde a method to return range of days book is borrowed
    def get_borrow_days_range(self):
        days = [int(d) for d in self.borrowed_days.values() if d != 'R']
        if not days:
            return "N/A"
        min_days = min(days)
        max_days = max(days)
        return f"{min_days}-{max_days}"

    #defined a method to return maximum days a book is borrowed
    def get_max_borrowed_days(self):
        days = [int(d) for d in self.borrowed_days.values() if d != 'R']
        return max(days) if days else 0

# created a class to define and operate the member data from the members txt file
class Member:
    # defind a constructor to initaialize variables to store fields of memeber txt file
    def __init__(self, member_id, first_name, last_name, dob, member_type):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.member_type = member_type

    # defined a method to extract the borrowed textbooks
    def get_num_borrowed_textbooks(self, records):
        return sum(1 for book_id, days in records.borrowed_days[self.member_id].items()
                   if records.get_book_by_id(book_id).book_type == 'Textbook' and days != 'R')

    # defined a method to reserve the textbooks
    def get_num_reserved_textbooks(self, records):
        return sum(1 for book_id, days in records.borrowed_days[self.member_id].items()
                   if records.get_book_by_id(book_id).book_type == 'Textbook' and days == 'R')

    # defined a method to extract the borrowed fiction books
    def get_num_borrowed_fictions(self, records):
        return sum(1 for book_id, days in records.borrowed_days[self.member_id].items()
                   if records.get_book_by_id(book_id).book_type == 'Fiction' and days != 'R')

    # defined a method to reserve fiction books
    def get_num_reserved_fictions(self, records):
        return sum(1 for book_id, days in records.borrowed_days[self.member_id].items()
                   if records.get_book_by_id(book_id).book_type == 'Fiction' and days == 'R')

    # defined a method to store the average of book borrowed
    def get_average_borrowed_days(self, records):
        days = [int(d) for book_id, d in records.borrowed_days[self.member_id].items() if d != 'R']
        return sum(days) / len(days) if days else 0

    # definde a method to check the type of member and type of books taken
    def check_borrowing_limit(self, records):
        if self.member_type == 'Standard':
            max_textbooks = 1
            max_fictions = 2
        else:  # Premium member
            max_textbooks = 2
            max_fictions = 3

        borrowed_textbooks = self.get_num_borrowed_textbooks(records)
        borrowed_fictions = self.get_num_borrowed_fictions(records)

        return borrowed_textbooks <= max_textbooks and borrowed_fictions <= max_fictions

# defined main method to accept the records, books, members txt files from user command prompt
def main():
    if len(sys.argv) < 2:
        print("Usage: python my_record.py <record file> [book file] [member file]")
        return

    record_file = sys.argv[1]
    records = Records()

    if len(sys.argv) == 4:
        book_file = sys.argv[2]
        member_file = sys.argv[3]
        records.read_records(record_file, book_file)
        records.read_member_file(member_file)
        records.display_records()
        records.display_book_info()
        records.display_member_info()
        records.save_book_info("reports.txt")
    elif len(sys.argv) == 3:
        book_file = sys.argv[2]
        records.read_records(record_file, book_file)
        records.display_records()
        records.display_book_info()
        records.save_book_info("reports.txt")
    else:
        records.read_record_file(record_file)
        records.display_records()

if __name__ == "__main__":
    main()


# Coding Process:
# I started my coding by initializing the creating required class and initializing constructors and defining methods by passing the txt file from command prompt.
# I then developed functions for handling and displaying the data in the respective txt files and other task-specific operations.
# To ensure correct input validation, I used for loops, try-except block and if-else structures, integrating these checks into the main function to maintain accuracy and integrity.
# I tested the program to confirm that it performed as expected and has appropriate validation checks throughout the program.

# Challenges Faced:
# Validating and modifiying the function to get the exact expected outcomes from input txt files posed me some difficulty and structuring the member information to display clearly was also a challenge.
# Managing errors across the program and ensuring detailed testing required extra attention and effort.


# Thank You
