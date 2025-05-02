import sqlite3
from datetime import date, datetime
from utils import validate_date


current_date = date.today()


def connect():
    conn = sqlite3.connect('books_storage.db')
    cursor = conn.cursor()
    connection = (conn, cursor)
    return connection


def create_table():
    try:
        conn, cursor = connect()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            author TEXT,
            register_date TEXT

            )
            '''
        )
        conn.commit()
    
    except sqlite3.Error as error:
        print(f'Unexpected error: {error}')
    
    finally:
        conn.close()


def insert_manually():
    try:
        conn, cursor = connect()
        
        book_name = input('Insert the book name: ').strip().capitalize()
        
        while not book_name:
            print('Invalid name. Please use only letters.')
            book_name = input('Insert the book name: ').strip().capitalize()            
        
        author_name = input('Insert the author name: ').strip().title()
        
        while not author_name:
            print('Invalid name. Please use only letters.')
            author_name = input('Insert the author name: ').strip().title()
        
        cursor.execute(
            '''
            INSERT INTO books (name, author, register_date) VALUES (?, ?, ?)
            ''', (book_name, author_name, current_date)
        )
        conn.commit()
        print('-'*45)
        print('Was registered:')
        print()
        print(f"Book title: {book_name} | Author: {author_name} | Register date: {current_date}")
    
    except sqlite3.Error as error:
        print(f'Unexpected error: {error}')
    
    
    finally:
        conn.close()


def delete():
    try:
        conn, cursor = connect()
        

        select = input('Do you want delete records by:\n\n1. Book title\n2. Author name\n3. ID\n4. Mass delete by id\nSelect: ')
        
        while not select or select not in ['1','2','3','4']:
            print('-'*45)
            print('Invalid option. Try again.')
            print('-'*45)
            select = input('Do you want delete records by:\n1. Book title\n2. Author name\n3. ID\n4. Mass delete by id\nSelect: ')
        
        if select == '1':
            print('-'*45)
            book_name = input('Enter the book title: ').strip().capitalize()

            while not book_name or book_name.isalnum() == False:
                print('-'*45)
                print('Invalid format. Please use try again.')
                book_name = input('Insert book name: ').strip().capitalize()
            
            cursor.execute(
                '''
                DELETE FROM books
                WHERE name = (?)
                ''', (book_name,)
            )
            conn.commit()
            
            print('-'*45)
            print(f"The registers in (book title): {book_name} were deleted")
        
        elif select == '2':
            
            author_name = input('Insert author name: ').strip().title()
            
            while not author_name:
                print('Invalid name. Please use only letters.')
                author_name = input('Insert author name: ').strip().title()
            
            cursor.execute(
                '''
                DELETE FROM books
                WHERE author = (?)
                ''', (author_name,)
            )
            conn.commit()

        elif select == '3':
            book_id = input('Enter the book id: ').strip()
            
            while not book_id or book_id.isnumeric() == False:
                print('Invalid format. Please try again with numbers only.')
                book_id = int(input('Enter the book id: ')).strip()
            
            cursor.execute(
                '''
                DELETE FROM books
                WHERE id = (?)
                ''', (book_id,)
            )
            conn.commit()
    
        elif select == '4':
            start_id = input('Set the start of the id range: ').strip()
            
            while not start_id or start_id.isnumeric() == False:
                print('Invalid format. Please try again with numbers only.')
                start_id = input('Set the start of the id range: ').strip()
            
            end_id = input('Set the end of the id range: ').strip()

            while not end_id or end_id.isnumeric() == False:
                print('Invalid format. Please try again with numbers only.')
                end_id = input('Set the end of the id range: ').strip()
            
            cursor.execute(
                '''
                DELETE FROM books
                WHERE id BETWEEN ? AND ?
                ''', (start_id, end_id)
            )
            conn.commit()
            print('-'*45)
            print(f'Records with id {start_id} to {end_id} were deleted')

    except sqlite3.Error as error:
        print(f'Unexpected error: {error}')
    
    finally:
        conn.close()


def list_all_records():
    try:
        conn, cursor = connect()
        query = cursor.execute('SELECT * FROM books').fetchall()
        ti = 'All records'
        print(ti.center(45))
        print('-'*45)
        for q in query:
            print(f'ID: {q[0]} | Book title: {q[1]} | Author name: {q[2]} | Record date: {q[3]}')
    
    
    except sqlite3.Error as error:
        print(f'Unexpected error: {error}')
    
    
    finally:
        conn.close()


def update():
    try:
        conn, cursor = connect()
        select = input('Which field do you want to update?\n\n1. Book title\n2. Author name\n3. Register date\nSelect: ').strip()
        
        while not select or select not in ['1', '2', '3']:
            print('Invalid selection. Please try again.')
            select = input('Which field do you want to update?\n1. Book title\n2. Author name\n3. Register date\nSelect: ').strip()
        
        if select == '1':
            current_name = input('Enter the title of the book to be updated: ').strip().capitalize()
            
            while not current_name or current_name.isalnum() == False:
                print('Invalid current title format. Please try again.')
                current_name = input('Enter the title of the book to be updated: ').strip().capitalize()
            
            new_name = input(f'What title will take the place of {current_name}?\nEnter: ').strip().capitalize()
            
            while not new_name or new_name.isalnum() == False:
                print('Invalid title format. Please try again.')
                new_name = input(f'What title will take the place of {current_name}?\nEnter: ').strip().capitalize()
            

            cursor.execute(
                '''
                UPDATE books
                SET name = ?
                WHERE name = ?
                ''', (new_name, current_name,)
            )
            conn.commit()
            print('-'*45)
            print(f"{new_name} take the place of {current_name}")
        
        elif select == '2':
            current_author = input('Enter the name of the author to be updated: ').strip().title()

            while not current_author or not current_author.isalpha():
                print('Invalid format. Please try again.')
                current_author = input('Enter the name of the author to be updated: ').strip().title()
            
            new_author = input(f'Enter the author name will take the place of {current_author}: ').strip().title()

            while not new_author:
                print('The author new name cannot be empty. Try again.')
                new_author = input(f'Enter the author name will take the place of {current_author}: ').strip().title()
            
            cursor.execute(
                '''
                UPDATE books
                SET author = ?
                WHERE author = ?
                ''', (new_author, current_author)
            )
            conn.commit()
            print('-'*45)
            print(f"{new_author} take the place of {current_author}")

        elif select == '3':
            try:
                c_date = input('Enter the date will be updated: ').strip()
                verify1 = validate_date(c_date)
                
                while not c_date and verify1 == False:
                    print('Invalid format. Please try again.')
                    c_date = input('Enter the date will be updated: ').strip()
                
                
                new_date = input(f'Enter the date will take the place of {c_date}: ').strip()
                verify2 = validate_date(new_date)
                    
                while not new_date and verify2 == False:
                    print('Invalid format. Please try again.')
                    new_date = input(f'Enter the date will take the place of {c_date}: ').strip()

                choice = input('Want to update by title too? [Y/N]:\nChoose: ').strip().lower()
                
                while not choice or choice not in ['y','n']:
                    print('Invalid format. Please answer only with Y or N.')
                    choice = input('Want to update by title too? [Y/N]:\nChoose: ').strip().lower()
                
                if choice == 'n':
                    cursor.execute(
                        '''
                        UPDATE books
                        SET register_date = ?
                        WHERE register_date = ?
                        ''', (new_date, c_date)
                        )
                        
                    conn.commit()
                    
                    print('-'*45)
                    print(f"All resgiter dates on: {c_date}, was converted to {new_date}")
                
                elif choice == 'y':
                    enter_name = input('Enter the book title on which date it will be updated: ').strip().capitalize()
                    
                    while not enter_name or enter_name.isalnum() == False:
                        print('The book title cannot be empty. Please try again.')
                        enter_name = input('Enter the book title on which date it will be updated: ').strip().capitalize()
                    
                    cursor.execute(
                        '''
                        UPDATE books
                        SET register_date = ?
                        WHERE register_date = (?) AND name = ?
                        ''', (new_date, c_date, enter_name)
                    )
                    
                    conn.commit()

                    print('-'*45)
                    print(f"The date: {c_date} recorded in the book: {enter_name} became {new_date}")
            
            except sqlite3.Error as error:
                print(f'Unexpected error: {error}.')
    
    except sqlite3.Error as error:
        print(f'Unexpected error: {error}')
    
    finally:
        conn.close()
                

def specific_query():
    try:
        conn, cursor = connect()
        print('You want:')
        print()
        print('1. Filter by book title\n2. Filter by author name\n3. Filter by register date\n4. Filter by ID\n5. Count books by the author name')
        select = input('Select: ')

        while not select or select not in ['1','2','3','4','5']:
            print('-'*45)
            print('Invalid format. Please try again.')
            print('-'*45)
            print('1. Filter by book title\n2. Filter by author name\n3. Filter by register date\n4. Filter by ID\n5. Count books by the author name')
            select = input('Select: ')
        
        if select == '1':
            search_by_name = input('Enter the book title you want to find records for: ').strip().capitalize()
            
            while not search_by_name or not search_by_name.isalnum():
                print('-'*45)
                print('Invalid format. Please try again.')
                print('-'*45)
                search_by_name = input('Enter the book title you want to find records for: ').strip().capitalize()

            placeholder = f"%{search_by_name}%"

            query = cursor.execute(
                '''
                SELECT * FROM books
                WHERE name LIKE ?
                ''', (placeholder,)
            ).fetchall()

            print('-'*45)
            r = 'Showing query results'
            print(r.center(45))
            print('-'*45)
            
            for q in query:
                print(f'ID: {q[0]} | Book title: {q[1]} | Author name: {q[2]} | Record date: {q[3]}')
        
        if select == '2':
            search_by_author = input('Enter the name of the author you want to find records for: ').strip().title()

            while not search_by_author or not search_by_author.isalpha():
                print('-'*45)
                print('Invalid format. Please try again.')
                print('-'*45)
                search_by_author = input('Enter the name of the author you wanto to find records for: ').strip().title()
            
            placeholder = f"%{search_by_author}%"

            query = cursor.execute(
                '''
                SELECT * FROM books
                WHERE author LIKE ?
                ''', (placeholder,)
            ).fetchall()

            print('-'*45)
            r = 'Showing query results'
            print(r.center(45))
            print('-'*45)

            for q in query:
                print(f'ID: {q[0]} | Book title: {q[1]} | Author name: {q[2]} | Record date: {q[3]}')
        
        if select == '3':
            print('-'*45)
            selec = input('You want to filter by:\n1. Date range\n2. Single date\nSelect: ').strip()
            
            while not selec or selec not in ['1','2']:
                print('-'*45)
                print('Invalid selection. Please enter only 1 or 2.')
                print('-'*45)
                selec = input('You want to filter by:\n1. Date range\n2. Single date\nSelect: ').strip()

            if selec == '1':
                start_range = input('Enter the start of date range you want to filter the books (format: yyyy-mm-dd): ').strip()

                while not start_range or validate_date(start_range) == False:
                    print('Invalid date format. Please try again.')
                    start_range = input('Enter the start of date range you want to filter the books (format: yyyy-mm-dd): ').strip()
                
                end_range = input('Enter the end of date range (format: yyyy-mm-dd): ').strip()

                while not end_range or validate_date(end_range) == False:
                    print('Invalid date format Please try again.')
                    end_range = input('Enter the end of date range (format: yyyy-mm-dd): ').strip()
                
                query = cursor.execute(
                    '''
                    SELECT * FROM books 
                    WHERE register_date BETWEEN ? AND ?
                    ORDER BY register_date ASC
                    
                    ''', (start_range, end_range)
                ).fetchall()

                for q in query:
                    print(f'ID: {q[0]} | Book title: {q[1]} | Author name: {q[2]} | Record date: {q[3]}')

            if selec == '2':
                single_date = input('Enter the date you want to filter the books: ').strip()
                
                valid_single_date = validate_date(single_date)
                
                while not single_date or valid_single_date == False:
                    print('Invalid date format. Please try again.')
                    single_date = input('Enter the date you want to filter the books: ').strip()
                
                query = cursor.execute(
                    '''
                    SELECT * FROM books
                    WHERE register_date = ?
                    ''', (single_date,)
                ).fetchall()
                
                for q in query:
                    print(f'ID: {q[0]} | Book title: {q[1]} | Author name: {q[2]} | Record date: {q[3]}')

        if select == '4':
            print('-'*45)
            enter_id = input('Enter the book id: ').strip()
            
            while not enter_id or enter_id.isnumeric() == False:
                print('-'*45)
                print('Invalid ID format. Please try again.')
                print('-'*45)
                enter_id = input('Enter the book id: ').strip()
            
            query = cursor.execute(
                '''
                SELECT * FROM books
                WHERE id = ?
                ''', (enter_id,)
            ).fetchall()

            r = 'Showing query results'
            print('-'*45)
            print(r.center(45))
            print('-'*45)

            for q in query:
                print(f'ID: {q[0]} | Book title: {q[1]} | Author name: {q[2]} | Record date: {q[3]}')

        if select == '5':
            enter_author = input('You want count books by which author?\nEnter author name: ').strip().title()
            
            while not enter_author or enter_author.isalpha() == False:
                print('Invalid author name format. Please try again.')
                enter_author = input('You want count books by which author?\nEnter author name: ').strip().title()
            
            placeholder = f"%{enter_author}%"
            
            query = cursor.execute(
                '''
                SELECT COUNT (*) FROM books WHERE author LIKE ?
                ''', (placeholder,)
            ).fetchone()
            print('-'*45)
            for q in query:
                print(f'{enter_author} has {q} books in the records.')

    except sqlite3.Error as error:
        print(f'Unexpected error: {error}')
    
    finally:
        conn.close()
