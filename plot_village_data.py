import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Connect to the SQLite database
conn = sqlite3.connect('toothbrush_data.db')
cursor = conn.cursor()

# Function to fetch data for a given village ID
def fetch_village_data(village_id):
    # First, get the village_week_ids and dates for the given village_id
    query = '''
    SELECT vw.village_week_id, vw.week_start_date, vws.avg_num_brushes_per_day, vws.avg_time_spent_brushing_per_day
    FROM VillageWeek vw
    JOIN VillageWeeklyStats vws ON vw.village_week_id = vws.village_week_id
    WHERE vw.village_id = ?
    ORDER BY vw.week_start_date
    '''
    cursor.execute(query, (village_id,))
    rows = cursor.fetchall()

    if not rows:
        return pd.DataFrame()

    # Convert the result into a DataFrame
    df = pd.DataFrame(rows, columns=['village_week_id', 'week_start_date', 'avg_num_brushes_per_day',
                                     'avg_time_spent_brushing_per_day'])

    # Convert week_start_date from text to datetime format
    df['week_start_date'] = pd.to_datetime(df['week_start_date'], format='%Y-%m-%d')

    return df

# Function to fetch data for all villages
def fetch_all_village_data():
    query_all_villages = '''
    SELECT vw.village_id, vw.week_start_date, vws.avg_num_brushes_per_day, vws.avg_time_spent_brushing_per_day
    FROM VillageWeek vw
    JOIN VillageWeeklyStats vws ON vw.village_week_id = vws.village_week_id
    ORDER BY vw.village_id, vw.week_start_date
    '''
    cursor.execute(query_all_villages)
    all_data = cursor.fetchall()

    if not all_data:
        return pd.DataFrame()

    all_data_df = pd.DataFrame(all_data, columns=['village_id', 'week_start_date', 'avg_num_brushes_per_day',
                                                  'avg_time_spent_brushing_per_day'])
    # Convert week_start_date from text to datetime format
    all_data_df['week_start_date'] = pd.to_datetime(all_data_df['week_start_date'], format='%Y-%m-%d')

    return all_data_df

# Function to plot the data for a specific village
def plot_village_data(df, plot_type):
    plt.figure(figsize=(10, 6))

    if plot_type == 'number':
        plt.plot(df['week_start_date'], df['avg_num_brushes_per_day'], linewidth=4)  # Thick line
        plt.ylabel('Average Number of Brushes per Day', fontsize=15)  # Font size 15 for y-label
        plt.title('Average Number of Brushes per Day per Week', fontsize=20)  # Font size 20 for title
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

# Function to plot the data for all villages on the same graph
def plot_all_village_data(df, plot_type):
    plt.figure(figsize=(10, 6))
    villages = df['village_id'].unique()

    for village in villages:
        village_data = df[df['village_id'] == village]
        if plot_type == 'number':
            plt.plot(village_data['week_start_date'], village_data['avg_num_brushes_per_day'], label=f'Village {village}', linewidth=4)  # Thick line
        elif plot_type == 'time':
            plt.plot(village_data['week_start_date'], village_data['avg_time_spent_brushing_per_day'], label=f'Village {village}', linewidth=4)  # Thick line
        else:
            print("Invalid plot type. Please enter 'number' or 'time'.")
            return

    if plot_type == 'number':
        plt.ylabel('Average Number of Brushes per Day', fontsize=15)  # Font size 15 for y-label
        plt.title('Average Number of Brushes per Day per Week for All Villages', fontsize=20)  # Font size 20 for title
    elif plot_type == 'time':
        plt.ylabel('Average Time Spent Brushing per Day (seconds)', fontsize=15)  # Font size 15 for y-label
        plt.title('Average Time Spent Brushing per Day per Week for All Villages', fontsize=20)  # Font size 20 for title

    plt.xlabel('Week Start Date', fontsize=15)  # Font size 15 for x-label
    plt.xticks(rotation=0, fontsize=13)  # Font size 13 for x-ticks
    plt.yticks(fontsize=13)  # Font size 13 for y-ticks
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Set interval for x-axis ticks to every other month
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))  # Format x-axis labels as 'Month Year'
    plt.legend(title='Village ID', fontsize=15)  # Font size 15 for legend
    plt.tight_layout()
    plt.show()

# Main function
def main():
    village_id = input("Enter the village ID or 'ALL' for all villages: ").strip()
    plot_type = input("Enter the type of graph ('number' or 'time'): ").strip().lower()

    if village_id.lower() == 'all':
        all_data_df = fetch_all_village_data()
        if all_data_df.empty:
            print("No data found for any villages.")
        else:
            plot_all_village_data(all_data_df, plot_type)
    else:
        df = fetch_village_data(village_id)
        if df.empty:
            print(f"No data found for village ID '{village_id}'.")
        else:
            plot_village_data(df, plot_type)

if __name__ == '__main__':
    main()

# Close the connection
conn.close()
