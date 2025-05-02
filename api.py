from database import connect
from datetime import date
import sqlite3
import requests


def auto_insert(bookname, authorname, currentdate=date.today()):
    try:
        conn, cursor = connect()
        cursor.execute(
            '''
            INSERT INTO books (name, author, register_date)
            VALUES (?, ?, ?)
            ''', (bookname, authorname, currentdate)
        )
        conn.commit()
    
    except sqlite3.Error as error:
        print(f'Unexpected error: {error}')
    
    finally:
        conn.close()


def search():
    try:
        query_api = input('Enter the book title or author name to search for informations: ')
        print('-'*45)
        url = f'https://www.googleapis.com/books/v1/volumes?q={query_api}&maxResults=20'

        response = requests.get(url)
        data = response.json()
        
        if 'items' in data:
            results = data['items']

            for r in results:
                title = r['volumeInfo'].get('title', 'No title')
                authors = r['volumeInfo'].get('authors', ['Unknown author'])
                print(f"Book title: {title} | Author(s): {', '.join(authors)}")
                print('-'*140)
        
        else:
            print('No results found.')
        
        
        choice = input('You want save all this information? [Y/N]:\nEnter: ').strip().lower()
        
        while not choice or choice not in ['y', 'n']:
            print('Invalid option. Please try again with only Y and N.')
            choice = input('Would you like to save all this information? [Y/N]:\nEnter: ').strip().lower()
        
        if choice == 'y':
            try:
                if 'items' in data:
                    results = data['items']
                    count = 0
                    for r in results:
                        title = str(r['volumeInfo'].get('title', 'No title'))
                        authors_list = r['volumeInfo'].get('authors', ['Unknown author'])
                        authors_str = ', '.join(authors_list)
                        auto_insert(title, authors_str)
                        count += 1
                    print('-'*45)
                    print(f'All the information was saved. {count} records were added to the database.')
            
            except sqlite3.Error as error:
                print(f'Unexpected error: {error}')
        
        elif choice == 'n':
            print('-'*45)
            print("The information wasn't saved")

    except requests.HTTPError as error:
        print(f'Unexpected error: {error}')
