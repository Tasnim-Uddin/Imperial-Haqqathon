# import sqlite3
# import pandas as pd
#
# # Load the CSV data
# df = pd.read_csv('toothbrush_data.csv')
#
# # Connect to SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect('toothbrush_data.db')
# cursor = conn.cursor()
#
# # Create tables
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Village (
#     village_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     village_name TEXT UNIQUE
# )
# ''')
#
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Toothbrush (
#     toothbrush_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     toothbrush_name TEXT UNIQUE,
#     village_id INTEGER,
#     FOREIGN KEY (village_id) REFERENCES Village (village_id)
# )
# ''')
#
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS ToothbrushDay (
#     toothbrush_day_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     toothbrush_id INTEGER,
#     date TEXT,
#     FOREIGN KEY (toothbrush_id) REFERENCES Toothbrush (toothbrush_id)
# )
# ''')
#
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS ToothbrushDailyStats (
#     toothbrush_day_id INTEGER PRIMARY KEY,
#     num_times_brushed INTEGER,
#     total_time_brushed INTEGER,
#     FOREIGN KEY (toothbrush_day_id) REFERENCES ToothbrushDay (toothbrush_day_id)
# )
# ''')
#
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS VillageWeek (
#     village_week_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     village_id INTEGER,
#     week_start_date DATE,
#     UNIQUE(village_id, week_start_date),
#     FOREIGN KEY(village_id) REFERENCES Village(village_id)
# )
# ''')
#
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS VillageWeeklyStats (
#     village_week_id INTEGER,
#     avg_num_brushes_per_day REAL,
#     avg_time_spent_brushing_per_day REAL,
#     FOREIGN KEY(village_week_id) REFERENCES VillageWeek(village_week_id)
# )
# ''')
#
# # Insert data into Village table
# villages = df['Village ID'].unique()
# village_dict = {name: i + 1 for i, name in enumerate(villages)}
#
# for village in villages:
#     cursor.execute('INSERT OR IGNORE INTO Village (village_name) VALUES (?)', (village,))
#
# # Insert data into Toothbrush, ToothbrushDay, and ToothbrushDailyStats tables
# toothbrush_dict = {}
#
# for _, row in df.iterrows():
#     toothbrush_name = row['Toothbrush ID']
#     village_id = village_dict[row['Village ID']]
#
#     if toothbrush_name not in toothbrush_dict:
#         cursor.execute('INSERT INTO Toothbrush (toothbrush_name, village_id) VALUES (?, ?)',
#                        (toothbrush_name, village_id))
#         toothbrush_id = cursor.lastrowid
#         toothbrush_dict[toothbrush_name] = toothbrush_id
#     else:
#         toothbrush_id = toothbrush_dict[toothbrush_name]
#
#     cursor.execute('''
#         INSERT INTO ToothbrushDay (toothbrush_id, date)
#         VALUES (?, ?)
#     ''', (toothbrush_id, row['Date']))
#     toothbrush_day_id = cursor.lastrowid
#
#     cursor.execute('''
#         INSERT INTO ToothbrushDailyStats (toothbrush_day_id, num_times_brushed, total_time_brushed)
#         VALUES (?, ?, ?)
#     ''', (toothbrush_day_id, row['Number of Times Brushed'], row['Total Time Brushed (s)']))
#
# # Compute weekly stats and insert into VillageWeeklyStats table
# df['Date'] = pd.to_datetime(df['Date'])
# df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
#
# weekly_stats = df.groupby(['Village ID', 'Week']).agg({
#     'Number of Times Brushed': 'mean',
#     'Total Time Brushed (s)': 'mean'
# }).reset_index()
#
# village_week_id_map = {}
# for _, row in weekly_stats.iterrows():
#     village_id = village_dict[row['Village ID']]
#     week_start_date = row['Week'].strftime('%Y-%m-%d')
#     avg_num_brushes = row['Number of Times Brushed']
#     avg_time_brushed = row['Total Time Brushed (s)']
#
#     cursor.execute('''
#         INSERT OR IGNORE INTO VillageWeek (village_id, week_start_date)
#         VALUES (?, ?)
#     ''', (village_id, week_start_date))
#
#     cursor.execute('''
#         SELECT village_week_id FROM VillageWeek
#         WHERE village_id = ? AND week_start_date = ?
#     ''', (village_id, week_start_date))
#
#     village_week_id = cursor.fetchone()[0]
#     village_week_id_map[(village_id, week_start_date)] = village_week_id
#
# for _, row in weekly_stats.iterrows():
#     village_week_id = village_week_id_map[(village_dict[row['Village ID']], row['Week'].strftime('%Y-%m-%d'))]
#     avg_num_brushes = row['Number of Times Brushed']
#     avg_time_brushed = row['Total Time Brushed (s)']
#
#     cursor.execute('''
#         INSERT INTO VillageWeeklyStats (village_week_id, avg_num_brushes_per_day, avg_time_spent_brushing_per_day)
#         VALUES (?, ?, ?)
#     ''', (village_week_id, avg_num_brushes, avg_time_brushed))
#
# # Commit and close connection
# conn.commit()
# conn.close()
#
# print("Data normalized and stored in the SQLite database 'toothbrush_data.db'")


import sqlite3
import pandas as pd

# Load the CSV data
df = pd.read_csv('toothbrush_data.csv')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('toothbrush_data.db')
cursor = conn.cursor()

import os

# Path to the SQLite database file
db_file = 'toothbrush_data.db'

# Close the SQLite connection if it's open
if 'conn' in globals():
    conn.close()

# Check if the database file exists before attempting to delete
if os.path.exists(db_file):
    try:
        os.remove(db_file)
        print(f"Database file '{db_file}' successfully deleted.")
    except Exception as e:
        print(f"Error deleting database file: {str(e)}")
else:
    print(f"Database file '{db_file}' does not exist.")

# Load the CSV data
df = pd.read_csv('toothbrush_data.csv')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('toothbrush_data.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Village (
    village_id INTEGER PRIMARY KEY AUTOINCREMENT,
    village_name TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Toothbrush (
    toothbrush_id INTEGER PRIMARY KEY AUTOINCREMENT,
    toothbrush_name TEXT UNIQUE,
    village_id INTEGER,
    FOREIGN KEY (village_id) REFERENCES Village (village_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ToothbrushDay (
    toothbrush_day_id INTEGER PRIMARY KEY AUTOINCREMENT,
    toothbrush_id INTEGER,
    date TEXT,
    FOREIGN KEY (toothbrush_id) REFERENCES Toothbrush (toothbrush_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ToothbrushDailyStats (
    toothbrush_day_id INTEGER PRIMARY KEY,
    num_times_brushed INTEGER,
    total_time_brushed INTEGER,
    FOREIGN KEY (toothbrush_day_id) REFERENCES ToothbrushDay (toothbrush_day_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS VillageWeek (
    village_week_id INTEGER PRIMARY KEY AUTOINCREMENT,
    village_id INTEGER,
    week_start_date DATE,
    UNIQUE(village_id, week_start_date),
    FOREIGN KEY(village_id) REFERENCES Village(village_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS VillageWeeklyStats (
    village_week_id INTEGER,
    avg_num_brushes_per_day REAL,
    avg_time_spent_brushing_per_day REAL,
    FOREIGN KEY(village_week_id) REFERENCES VillageWeek(village_week_id)
)
''')

# Create tables for Toothbrush weekly stats
cursor.execute('''
CREATE TABLE IF NOT EXISTS ToothbrushWeek (
    toothbrush_week_id INTEGER PRIMARY KEY AUTOINCREMENT,
    toothbrush_id INTEGER,
    week_start_date DATE,
    UNIQUE(toothbrush_id, week_start_date),
    FOREIGN KEY(toothbrush_id) REFERENCES Toothbrush(toothbrush_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ToothbrushWeeklyStats (
    toothbrush_week_id INTEGER,
    avg_num_brushes_per_day REAL,
    avg_time_spent_brushing_per_day REAL,
    FOREIGN KEY(toothbrush_week_id) REFERENCES ToothbrushWeek(toothbrush_week_id)
)
''')

# Insert data into Village table
villages = df['Village ID'].unique()
village_dict = {name: i + 1 for i, name in enumerate(villages)}

for village in villages:
    cursor.execute('INSERT OR IGNORE INTO Village (village_name) VALUES (?)', (village,))

# Insert data into Toothbrush, ToothbrushDay, and ToothbrushDailyStats tables
toothbrush_dict = {}

for _, row in df.iterrows():
    toothbrush_name = row['Toothbrush ID']
    village_id = village_dict[row['Village ID']]

    if toothbrush_name not in toothbrush_dict:
        cursor.execute('INSERT INTO Toothbrush (toothbrush_name, village_id) VALUES (?, ?)',
                       (toothbrush_name, village_id))
        toothbrush_id = cursor.lastrowid
        toothbrush_dict[toothbrush_name] = toothbrush_id
    else:
        toothbrush_id = toothbrush_dict[toothbrush_name]

    cursor.execute('''
        INSERT INTO ToothbrushDay (toothbrush_id, date)
        VALUES (?, ?)
    ''', (toothbrush_id, row['Date']))
    toothbrush_day_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO ToothbrushDailyStats (toothbrush_day_id, num_times_brushed, total_time_brushed)
        VALUES (?, ?, ?)
    ''', (toothbrush_day_id, row['Number of Times Brushed'], row['Total Time Brushed (s)']))

# Compute weekly stats and insert into VillageWeeklyStats table
df['Date'] = pd.to_datetime(df['Date'])
df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)

# Village Weekly Stats
weekly_stats_village = df.groupby(['Village ID', 'Week']).agg({
    'Number of Times Brushed': 'mean',
    'Total Time Brushed (s)': 'mean'
}).reset_index()

village_week_id_map = {}
for _, row in weekly_stats_village.iterrows():
    village_id = village_dict[row['Village ID']]
    week_start_date = row['Week'].strftime('%Y-%m-%d')
    avg_num_brushes = row['Number of Times Brushed']
    avg_time_brushed = row['Total Time Brushed (s)']

    cursor.execute('''
        INSERT OR IGNORE INTO VillageWeek (village_id, week_start_date)
        VALUES (?, ?)
    ''', (village_id, week_start_date))

    cursor.execute('''
        SELECT village_week_id FROM VillageWeek
        WHERE village_id = ? AND week_start_date = ?
    ''', (village_id, week_start_date))

    village_week_id = cursor.fetchone()[0]
    village_week_id_map[(village_id, week_start_date)] = village_week_id

for _, row in weekly_stats_village.iterrows():
    village_week_id = village_week_id_map[(village_dict[row['Village ID']], row['Week'].strftime('%Y-%m-%d'))]
    avg_num_brushes = row['Number of Times Brushed']
    avg_time_brushed = row['Total Time Brushed (s)']

    cursor.execute('''
        INSERT INTO VillageWeeklyStats (village_week_id, avg_num_brushes_per_day, avg_time_spent_brushing_per_day)
        VALUES (?, ?, ?)
    ''', (village_week_id, avg_num_brushes, avg_time_brushed))

# Toothbrush Weekly Stats
weekly_stats_toothbrush = df.groupby(['Toothbrush ID', 'Week']).agg({
    'Number of Times Brushed': 'mean',
    'Total Time Brushed (s)': 'mean'
}).reset_index()

toothbrush_week_id_map = {}
for _, row in weekly_stats_toothbrush.iterrows():
    toothbrush_id = toothbrush_dict[row['Toothbrush ID']]
    week_start_date = row['Week'].strftime('%Y-%m-%d')
    avg_num_brushes = row['Number of Times Brushed']
    avg_time_brushed = row['Total Time Brushed (s)']

    cursor.execute('''
        INSERT OR IGNORE INTO ToothbrushWeek (toothbrush_id, week_start_date)
        VALUES (?, ?)
    ''', (toothbrush_id, week_start_date))

    cursor.execute('''
        SELECT toothbrush_week_id FROM ToothbrushWeek
        WHERE toothbrush_id = ? AND week_start_date = ?
    ''', (toothbrush_id, week_start_date))

    toothbrush_week_id = cursor.fetchone()[0]
    toothbrush_week_id_map[(toothbrush_id, week_start_date)] = toothbrush_week_id

for _, row in weekly_stats_toothbrush.iterrows():
    toothbrush_week_id = toothbrush_week_id_map[(toothbrush_dict[row['Toothbrush ID']], row['Week'].strftime('%Y-%m-%d'))]
    avg_num_brushes = row['Number of Times Brushed']
    avg_time_brushed = row['Total Time Brushed (s)']

    cursor.execute('''
        INSERT INTO ToothbrushWeeklyStats (toothbrush_week_id, avg_num_brushes_per_day, avg_time_spent_brushing_per_day)
        VALUES (?, ?, ?)
    ''', (toothbrush_week_id, avg_num_brushes, avg_time_brushed))

# Commit and close connection
conn.commit()
conn.close()

print("Data normalised and stored in the SQLite database 'toothbrush_data.db'")
