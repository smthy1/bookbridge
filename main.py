from database import connect, create_table, insert_manually, delete, list_all_records, update, specific_query
from api import search


while True:
    print('-'*45)
    title = 'BookBridge Menu'
    print(title.center(40))
    print('-'*45)
    
    print('You want:')
    print()
    print('1. Search for information about books\n2. List all records in the database\n3. Query an specific record in the database')
    print('4. Manually add new record\n5. Update some record\n6. Delete some record\n7. Exit')
    
    selection = input('Select: ').strip()
        
    while not selection or selection.isnumeric() == False:
        print('-'*45)
        print('Invalid selection. Please try again.')
        print('-'*45)

        selection = input('Select: ').strip()
        
    if selection == '1':
        print('-'*45)
        search()

    elif selection == '2':
        print('-'*45)
        list_all_records()
        
    elif selection == '3':
        print('-'*45)
        specific_query()
        
    elif selection == '4':
        print('-'*45)
        insert_manually()
        
    elif selection == '5':
        print('-'*45)
        update()
        
    elif selection == '6':
        print('-'*45)
        delete()

    elif selection == '7':
        print('-'*45)
        print('Shutting down...')
        break
