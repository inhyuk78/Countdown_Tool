import pandas as pd

def enter_final_date(date_str):
    while True:
        try:
            final_date = pd.to_datetime(date_str)
            return final_date
        except Exception:
            raise ValueError('Invalid date format. Please use YYYY-MM-DD')

def enter_specific_date(date_str):
    while True:
        try:
            specific_date = pd.to_datetime(date_str)
            return specific_date
        except Exception:
            raise ValueError('Invalid date format. Please use YYYY-MM-DD')

def get_current_date():
    return pd.Timestamp.now()