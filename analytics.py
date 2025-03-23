import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def calculate_cancellation_rate(df):
    #Calculates the cancellation rate as a percentage of total bookings.#
    return df['is_canceled'].mean() * 100

def get_geographical_distribution(df):
    #Returns top 10 countries by booking count.#
    df_country = df['country'].value_counts().reset_index()
    df_country.columns = ['Country', 'Bookings']
    return df_country.head(10).to_dict(orient='records')

def get_revenue_trends(df):
    #Returns revenue trends over time as structured data.#
    df_revenue = df.groupby(['arrival_date_year', 'arrival_date_month'])['adr'].sum().reset_index()
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_revenue['arrival_date_month'] = pd.Categorical(df_revenue['arrival_date_month'], categories=month_order, ordered=True)
    df_revenue.sort_values(['arrival_date_year', 'arrival_date_month'], inplace=True)

    return df_revenue.to_dict(orient='records')

def get_booking_lead_time_distribution(df):
    #Returns booking lead time distribution data.#
    return df['lead_time'].describe().to_dict()

def get_adr_distribution(df):
    #Returns Average Daily Rate (ADR) distribution data.#
    return df['adr'].describe().to_dict()

def plot_and_encode_image(plot_function, df):
    #Generates a plot, encodes it to base64, and returns as a string.#
    plt.figure(figsize=(12, 6))
    plot_function(df)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    base64_image = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return base64_image

def generate_analytics(df):
    #Aggregates all analytics into a structured dictionary.#
    return {
        "cancellation_rate": calculate_cancellation_rate(df),
        "geographical_distribution": get_geographical_distribution(df),
        "revenue_trends": get_revenue_trends(df),
        "booking_lead_time_distribution": get_booking_lead_time_distribution(df),
        "adr_distribution": get_adr_distribution(df),
        "plots": {
            "geographical_distribution": plot_and_encode_image(plot_geographical_distribution, df),
            "revenue_trends": plot_and_encode_image(plot_revenue_trends, df),
            "booking_lead_time_distribution": plot_and_encode_image(plot_booking_lead_time, df),
            "adr_distribution": plot_and_encode_image(plot_adr_distribution, df)
        }
    }

# Visualization functions for API (used for encoding plots)
def plot_geographical_distribution(df):
    df_country = df['country'].value_counts().reset_index()
    df_country.columns = ['Country', 'Bookings']
    sns.barplot(data=df_country.head(10), x='Country', y='Bookings', hue='Country', palette='viridis', legend=False)
    plt.title('Top 10 Countries by Booking Count')
    plt.xlabel('Country')
    plt.ylabel('Number of Bookings')
    plt.xticks(rotation=45)

def plot_revenue_trends(df):
    df_revenue = df.groupby(['arrival_date_year', 'arrival_date_month'])['adr'].sum().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_revenue['arrival_date_month'] = pd.Categorical(df_revenue['arrival_date_month'], categories=month_order, ordered=True)
    df_revenue.sort_values(['arrival_date_year', 'arrival_date_month'], inplace=True)

    sns.lineplot(data=df_revenue, x='arrival_date_month', y='adr', hue='arrival_date_year', marker='o')
    plt.title('Revenue Trends Over Time')
    plt.xlabel('Month')
    plt.ylabel('Total Revenue')
    plt.xticks(rotation=45)

def plot_booking_lead_time(df):
    sns.histplot(df['lead_time'], bins=50, kde=True, color='blue')
    plt.title('Distribution of Booking Lead Time')
    plt.xlabel('Lead Time (Days)')
    plt.ylabel('Frequency')

def plot_adr_distribution(df):
    sns.histplot(df['adr'], bins=50, kde=True, color='green')
    plt.title('Distribution of Average Daily Rate (ADR)')
    plt.xlabel('ADR')
    plt.ylabel('Frequency')
