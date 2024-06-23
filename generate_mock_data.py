# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# import random
#
# # Parameters
# num_villages = 5
# villages = [f'village{i+1}' for i in range(num_villages)]
# num_people = 50  # Total number of people across all villages
# days_in_year = 365
# start_date = datetime(2023, 1, 1)
#
# # Generate data
# data = []
#
# for person in range(1, num_people + 1):
#     toothbrush_id = f'toothbrush{person}'
#     village = random.choice(villages)
#     for day in range(days_in_year):
#         date = start_date + timedelta(days=day)
#         num_times_brushed = random.randint(0, 2)
#         total_time_brushed = sum(random.randint(30, 120) for _ in range(num_times_brushed))
#         data.append([toothbrush_id, village, date.strftime('%Y-%m-%d'), num_times_brushed, total_time_brushed])
#
# # Create DataFrame
# df = pd.DataFrame(data, columns=['Toothbrush ID', 'Village ID', 'Date', 'Number of Times Brushed', 'Total Time Brushed (s)'])
#
# # Save to CSV
# df.to_csv('toothbrush_data.csv', index=False)
#
# print("Mock data generated and saved to 'toothbrush_data.csv'")


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Parameters
num_villages = 5
villages = [f'village{i+1}' for i in range(num_villages)]
num_people = 50  # Total number of people across all villages
days_in_six_months = 180
start_date = datetime(2023, 1, 1)  # Set start date to 3 months before today

# Generate data
data = []

for person in range(1, num_people + 1):
    toothbrush_id = f'toothbrush{person}'
    village = random.choice(villages)
    for day in range(days_in_six_months):
        date = start_date + timedelta(days=day)
        num_times_brushed = random.randint(0, 2)
        total_time_brushed = sum(random.randint(30, 120) for _ in range(num_times_brushed))
        data.append([toothbrush_id, village, date.strftime('%Y-%m-%d'), num_times_brushed, total_time_brushed])

# Create DataFrame
df = pd.DataFrame(data, columns=['Toothbrush ID', 'Village ID', 'Date', 'Number of Times Brushed', 'Total Time Brushed (s)'])

# Save to CSV
df.to_csv('toothbrush_data.csv', index=False)

print("Mock data generated and saved to 'toothbrush_data.csv'")
