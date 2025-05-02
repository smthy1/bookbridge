from datetime import datetime

def validate_date(date_str):
    try:
        valid_date = datetime.strptime(date_str, "%Y-%m-%d")
        return True
    
    except ValueError:
        return False