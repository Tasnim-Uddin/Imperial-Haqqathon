import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator  # Import MultipleLocator for setting y-axis ticks

# Connect to the SQLite database
conn = sqlite3.connect('toothbrush_data.db')
cursor = conn.cursor()

# Function to fetch data for a given toothbrush ID
def fetch_toothbrush_data(toothbrush_id):
    # First, get the toothbrush_week_ids and dates for the given toothbrush_id
    query = '''
    SELECT tw.toothbrush_week_id, tw.week_start_date, tws.avg_num_brushes_per_day, tws.avg_time_spent_brushing_per_day
    FROM ToothbrushWeek tw
    JOIN ToothbrushWeeklyStats tws ON tw.toothbrush_week_id = tws.toothbrush_week_id
    WHERE tw.toothbrush_id = ?
    ORDER BY tw.week_start_date
    '''
    cursor.execute(query, (toothbrush_id,))
    rows = cursor.fetchall()

    if not rows:
        return pd.DataFrame()

    # Convert the result into a DataFrame
    df = pd.DataFrame(rows, columns=['toothbrush_week_id', 'week_start_date', 'avg_num_brushes_per_day',
                                     'avg_time_spent_brushing_per_day'])

    # Convert week_start_date from text to datetime format
    df['week_start_date'] = pd.to_datetime(df['week_start_date'], format='%Y-%m-%d')

    return df

# Function to fetch data for all toothbrushes
def fetch_all_toothbrush_data():
    query_all_toothbrushes = '''
    SELECT tw.toothbrush_id, tw.week_start_date, tws.avg_num_brushes_per_day, tws.avg_time_spent_brushing_per_day
    FROM ToothbrushWeek tw
    JOIN ToothbrushWeeklyStats tws ON tw.toothbrush_week_id = tws.toothbrush_week_id
    ORDER BY tw.toothbrush_id, tw.week_start_date
    '''
    cursor.execute(query_all_toothbrushes)
    all_data = cursor.fetchall()

    if not all_data:
        return pd.DataFrame()

    all_data_df = pd.DataFrame(all_data, columns=['toothbrush_id', 'week_start_date', 'avg_num_brushes_per_day',
                                                  'avg_time_spent_brushing_per_day'])
    # Convert week_start_date from text to datetime format
    all_data_df['week_start_date'] = pd.to_datetime(all_data_df['week_start_date'], format='%Y-%m-%d')

    return all_data_df

# Function to plot the data for a specific toothbrush
def plot_toothbrush_data(df, plot_type):
    plt.figure(figsize=(10, 6))

    if plot_type == 'number':
        plt.plot(df['week_start_date'], df['avg_num_brushes_per_day'], linewidth=4)  # Thick line
        plt.ylabel('Average Number of Brushes per Day', fontsize=15)  # Font size 15 for y-label
        plt.title('Average Number of Brushes per Day per Week', fontsize=20)  # Font size 20 for title
        plt.gca().yaxis.set_major_locator(MultipleLocator(0.5))  # Set interval for y-axis ticks to every 0.5 units
    elif plot_type == 'time':
        plt.plot(df['week_start_date'], df['avg_time_spent_brushing_per_day'], linewidth=4)  # Thick line
        plt.ylabel('Average Time Spent Brushing per Day (seconds)', fontsize=15)  # Font size 15 for y-label
        plt.title('Average Time Spent Brushing per Day per Week', fontsize=20)  # Font size 20 for title
    else:
        print("Invalid plot type. Please enter 'number' or 'time'.")
        return

    plt.xlabel('Week Start Date', fontsize=15)  # Font size 15 for x-label
    plt.xticks(rotation=0, fontsize=13)  # Font size 13 for x-ticks
    plt.yticks(fontsize=13)  # Font size 13 for y-ticks
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Set interval for x-axis ticks to every other month
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))  # Format x-axis labels as 'Month Year'
    plt.tight_layout()
    plt.show()

# Function to plot the data for all toothbrushes on the same graph
def plot_all_toothbrush_data(df, plot_type):
    plt.figure(figsize=(10, 6))
    toothbrushes = df['toothbrush_id'].unique()

    for toothbrush in toothbrushes:
        toothbrush_data = df[df['toothbrush_id'] == toothbrush]
        if plot_type == 'number':
            plt.plot(toothbrush_data['week_start_date'], toothbrush_data['avg_num_brushes_per_day'], label=f'Toothbrush {toothbrush}', linewidth=4)  # Thick line
        elif plot_type == 'time':
            plt.plot(toothbrush_data['week_start_date'], toothbrush_data['avg_time_spent_brushing_per_day'], label=f'Toothbrush {toothbrush}', linewidth=4)  # Thick line
        else:
            print("Invalid plot type. Please enter 'number' or 'time'.")
            return

    if plot_type == 'number':
        plt.ylabel('Average Number of Brushes per Day', fontsize=15)  # Font size 15 for y-label
        plt.title('Average Number of Brushes per Day per Week for All Toothbrushes', fontsize=20)  # Font size 20 for title
        plt.gca().yaxis.set_major_locator(MultipleLocator(0.5))  # Set interval for y-axis ticks to every 0.5 units
    elif plot_type == 'time':
        plt.ylabel('Average Time Spent Brushing per Day (seconds)', fontsize=15)  # Font size 15 for y-label
        plt.title('Average Time Spent Brushing per Day per Week for All Toothbrushes', fontsize=20)  # Font size 20 for title

    plt.xlabel('Week Start Date', fontsize=15)  # Font size 15 for x-label
    plt.xticks(rotation=0, fontsize=13)  # Font size 13 for x-ticks
    plt.yticks(fontsize=13)  # Font size 13 for y-ticks
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Set interval for x-axis ticks to every other month
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))  # Format x-axis labels as 'Month Year'
    plt.legend(title='Toothbrush ID', fontsize=15)  # Font size 15 for legend
    plt.tight_layout()
    plt.show()

# Main function
def main():
    toothbrush_id = input("Enter the toothbrush ID or 'ALL' for all toothbrushes: ").strip()
    plot_type = input("Enter the type of graph ('number' or 'time'): ").strip().lower()

    if toothbrush_id.lower() == 'all':
        all_data_df = fetch_all_toothbrush_data()
        if all_data_df.empty:
            print("No data found for any toothbrushes.")
        else:
            plot_all_toothbrush_data(all_data_df, plot_type)
    else:
        df = fetch_toothbrush_data(toothbrush_id)
        if df.empty:
            print(f"No data found for toothbrush ID '{toothbrush_id}'.")
        else:
            plot_toothbrush_data(df, plot_type)

if __name__ == '__main__':
    main()

# Close the connection
conn.close()
