import pandas as pd

def load_and_clean_data():
    file_path = "D:/Vedant/Projects/LLM-Booking-Analytics/data/hotel_bookings.csv"
    df = pd.read_csv(file_path)

    # Handle missing values
    df = df.assign(
        children=df['children'].fillna(0),
        country=df['country'].fillna('Unknown'),
        agent=df['agent'].fillna(0)
    )

    df.drop(columns=['company'], inplace=True)

    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')

    # Remove outliers and invalid data
    df = df[df['adr'] > 0]
    df = df[df['lead_time'] >= 0]

    return df
