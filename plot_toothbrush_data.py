import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Connect to the SQLite database
conn = sqlite3.connect('toothbrush_data.db')
cursor = conn.cursor()


# Function to fetch data for a given toothbrush ID
def fetch_data(toothbrush_id):
    # First, get the toothbrush_day_ids and dates for the given toothbrush_id
    query = '''
    SELECT td.toothbrush_day_id, td.date, tds.num_times_brushed, tds.total_time_brushed
    FROM ToothbrushDay td
    JOIN Toothbrush t ON td.toothbrush_id = t.toothbrush_id
    LEFT JOIN ToothbrushDailyStats tds ON td.toothbrush_day_id = tds.toothbrush_day_id
    WHERE t.toothbrush_id = ?
    ORDER BY td.date
    '''
    cursor.execute(query, (toothbrush_id,))
    rows = cursor.fetchall()

    if not rows:
        return pd.DataFrame()

    # Convert the result into a DataFrame
    df = pd.DataFrame(rows, columns=['toothbrush_day_id', 'date', 'num_times_brushed', 'total_time_brushed'])

    # Convert date from text to datetime format
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    return df


# Function to plot the data
def plot_data(df, plot_type):
    plt.figure(figsize=(10, 6))
    if plot_type == 'number':
        plt.plot(df['date'], df['num_times_brushed'], marker='o')
        plt.ylabel('Number of Brushes')
        plt.title('Number of Brushes per Day')
    elif plot_type == 'time':
        plt.plot(df['date'], df['total_time_brushed'], marker='o')
        plt.ylabel('Time Spent Brushing (seconds)')
        plt.title('Time Spent Brushing per Day')
    else:
        print("Invalid plot type. Please enter 'number' or 'time'.")
        return

    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=20))  # Set interval for x-axis ticks
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format x-axis labels
    plt.tight_layout()
    plt.show()


# Main function
def main():
    toothbrush_id = input("Enter the toothbrush ID: ").strip()
    plot_type = input("Enter the type of graph ('number' or 'time'): ").strip().lower()

    df = fetch_data(toothbrush_id)
    if df.empty:
        print(f"No data found for toothbrush ID '{toothbrush_id}'.")
    else:
        plot_data(df, plot_type)


if __name__ == '__main__':
    main()

# Close the connection
conn.close()
