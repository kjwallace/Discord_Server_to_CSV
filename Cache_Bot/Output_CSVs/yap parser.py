import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
import datetime

ref_date = datetime.datetime(2023, 12, 8) # Date of server creation. Can be set later if you want to only analyze a specific period
update_date = datetime.datetime(2024, 7, 10) # Set this to the day after today
date_format = '%m/%d/%Y'


# For plotting - defines whether the cumulative daily yaps for all users are posted (true), or the yaps for particular users are analyzed (false, and specify the users)
all_users = False
yappers_in_question = ["spintopirl", "avg"]


class Buddy:
    def __init__(self, username):
        self.username = username
        self.word_count = 0
        self.server_days = 0
        self.yap_avg = 0
        self.yap_median = 0
        self.daily_yaps_array = [[], []] # Format: [[day 1, day 2, ... day n], [yap count 1, yap count 2, ... yap count n]]
        self.date_of_last_message = datetime.datetime(1, 1, 1)
        self.date_index = 0


buddies = [] # will be populated with each person in the server

# manually pasted from bot_main cache status outputs
channels = ["voice",
"welcome-🤗",
"choose-a-colour-🌈",
"organize-🤼",
"standard-🦇",
"pioneer-👺",
"modern-🍆",
"legacy-🧙",
"general",
"cube",
"poker-organizing",
"music-and-media",
"trading-n-shit",
"mystical-disputes",
"quotes",
"its-so-over",
"were-so-back",
"arena-formats",
"pets-🐶-and-andys-baby-and-sleepy-edgar",
"memes-and-dreams",
"sports",
"spoilers",
"outlaws-limited",
"mod-channel",
"foodge",
"events",
"post-lists",
"runescape",
"photos",
"mh3-limited",
"pokemon-and-other-tcgs",
"bookz",
"music-league"]

# ---------------------------------------- Message counts ----------------------------------------

# Per channel
for channel in channels:
    channel += ".csv"
    open_file = pd.read_csv(filepath_or_buffer=channel, delimiter='~')

    # Per message
    for i in range(len(open_file)):
        # Only log messages sent after the ref date
        temp_date_str = (open_file.iloc[i, 5])[0:10]
        temp_date = datetime.datetime.strptime(temp_date_str, date_format)
        if temp_date >= ref_date:
            # See the username of the person who sent the current message, then add them to the list of buddies if they're not already there
            temp_username = open_file.iloc[i, 1]
            user_present = False
            count = 0
            for buddy in buddies:
                if buddy.username == temp_username:
                    user_present = True
                    buddy_index = count # The index is used so that the next part knows which buddy in the list to update the numbers for
                count += 1
            if not user_present:
                buddies.append(Buddy(temp_username))
                user_present = True
                buddy_index = count

            # A cumulative total is kept for each day. This determines which day to add the count to. Adds a new day to the list of dates if it's not there already.
            message = str(open_file.iloc[i, 3])
            if buddies[buddy_index].date_of_last_message != temp_date:
                buddies[buddy_index].date_index = 0
                for day in buddies[buddy_index].daily_yaps_array[0]:
                    if temp_date > day:
                        buddies[buddy_index].date_index += 1

                # This part makes sure the day gets put in chronological order in the array
                if temp_date not in buddies[buddy_index].daily_yaps_array[0]:
                    if buddies[buddy_index].date_index == len(buddies[buddy_index].daily_yaps_array[0]):
                        buddies[buddy_index].daily_yaps_array[0].append(temp_date)
                        buddies[buddy_index].daily_yaps_array[1].append(0)
                    else:
                        buddies[buddy_index].daily_yaps_array[0].insert(buddies[buddy_index].date_index, temp_date)
                        buddies[buddy_index].daily_yaps_array[1].insert(buddies[buddy_index].date_index, 0)
                        
            # Aach space or newline indicates a new word
            for c in message:
                if c == ' ' or c == '\n':
                    buddies[buddy_index].word_count += 1
                    buddies[buddy_index].date_of_last_message = temp_date
                    buddies[buddy_index].daily_yaps_array[1][buddies[buddy_index].date_index] += 1
            # At the end of the message, need to add an extra +1 to the word count because the message won't end in a space
            buddies[buddy_index].word_count += 1
            buddies[buddy_index].date_of_last_message = temp_date
            buddies[buddy_index].daily_yaps_array[1][buddies[buddy_index].date_index] += 1


# Now that all channels have been searched, set up each buddy for analysis
for buddy in buddies:
    # Adds a 0 message count for the most recent day (update_date) if this buddy wasn't already yapping on the most recent day
    if buddy.daily_yaps_array[0][len(buddy.daily_yaps_array[0]) - 1] != update_date:
        buddy.daily_yaps_array[0].append(update_date)
        buddy.daily_yaps_array[1].append(0)

    # Fills in 0 message counts for each day that this buddy didn't talk
    temp_index = 1
    while temp_index < len(buddy.daily_yaps_array[0]):
        while buddy.daily_yaps_array[0][temp_index - 1] != buddy.daily_yaps_array[0][temp_index] - datetime.timedelta(days=1):
            buddy.daily_yaps_array[0].insert(temp_index, buddy.daily_yaps_array[0][temp_index] - datetime.timedelta(days=1))
            buddy.daily_yaps_array[1].insert(temp_index, 0)
        temp_index += 1

    # Stats for the table
    buddy.yap_median = np.median(buddy.daily_yaps_array[1])
    buddy.server_days = len(buddy.daily_yaps_array[0])
    buddy.yap_avg = float(buddy.word_count/buddy.server_days)

# ---------------------------------------- Plotting ----------------------------------------

global_dates = []
global_yaps = []
date_ticks = [] # the dates that will be labelled on the plot
freq = 4 # number of days between ticks on the plot
starting_date = datetime.datetime(3000, 1, 1)
ending_date = datetime.datetime(1, 1, 1)

for buddy in buddies:
    for date in buddy.daily_yaps_array[0]:
        if date < starting_date:
            starting_date = date
        if date > ending_date:
            ending_date = date

temp_date_plot = starting_date
count = freq
day_count = 0
while temp_date_plot <= ending_date:
    # Add the date to the list of ticks at the desired frequency
    if count == freq:
        count = 0
        date_ticks.append(temp_date_plot)

    # For each date, add it to the list of dates and set the message count to 0. Then add each buddy's contribution to that day
    global_dates.append(temp_date_plot)
    global_yaps.append(0)
    for buddy in buddies:
        day_count = 0
        for date in buddy.daily_yaps_array[0]:
            if date == temp_date_plot:
                global_yaps[len(global_yaps) - 1] += buddy.daily_yaps_array[1][day_count]
            day_count += 1
    temp_date_plot += datetime.timedelta(days=1)
    count += 1

global_dates = pd.to_datetime(global_dates)

buddy_count = 0

total_server_yaps = 0

# Figure out the total user count and word count of the entire server
for buddy in buddies:
    total_server_yaps += buddy.word_count
    buddy.daily_yaps_array[0] = pd.to_datetime(buddy.daily_yaps_array[0])
    buddy_count += 1

# This was for when we wanted to figure out what portion of all messages in the server were sent by a particular user.
ref_buddy = "shadowz2005"
for buddy in buddies:
    if buddy.username == ref_buddy:
        print(f"Total percentage of all yaps for user {ref_buddy}: {buddy.word_count/total_server_yaps*100}%")

# The default plotting option. Plot the daily sum of all users.
if all_users:
    DF = pd.DataFrame()
    DF['value'] = global_yaps
    DF = DF.set_index(global_dates)
    plt.plot(DF)

# For plotting particular users
else:
    # Plot each buddy being analyzed
    for yapper_name in yappers_in_question:
        for buddy in buddies:
            if yapper_name == buddy.username:
                buddy.DF = pd.DataFrame()
                buddy.DF['value'] = buddy.daily_yaps_array[1]
                buddy.DF = buddy.DF.set_index(buddy.daily_yaps_array[0])
                plt.plot(buddy.DF)

    # Plot the daily average for comparison
    DF = pd.DataFrame()
    for i in range(len(global_yaps)):
        global_yaps[i] = float(global_yaps[i]/buddy_count)
    DF['value'] = global_yaps
    DF = DF.set_index(global_dates)
    plt.plot(DF)

    # Legend
    plt.legend(yappers_in_question)

plt.gcf().autofmt_xdate()
plt.xticks(date_ticks)
plt.title("Pair o' Dice Messages Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Messages")
plt.show()

# ---------------------------------------- Table  ----------------------------------------

# Removes each buddy from the list of buddies in order of their yap count until all buddies are ordered.
yappers_ordered = []

while len(buddies) > 0:
    maximum_yap = 0
    yap_index = 0
    max_index = 0
    for buddy in buddies:
        if buddy.yap_avg > maximum_yap:
            maximum_yap = buddy.yap_avg
            max_index = yap_index
        yap_index += 1
    yappers_ordered.append(buddies[max_index])
    buddies.pop(max_index)

table = [["Yapper Rank", "Discord Username", "Days in Server", "Cumulative Yaps", "Avg. Yaps per Day", "Median Yaps per Day"]]

yapper_count = 1
for yapper in yappers_ordered:
    table.append([yapper_count, yapper.username, yapper.server_days, yapper.word_count, round(yapper.yap_avg, 2), yapper.yap_median])
    yapper_count += 1

tab = PrettyTable(table[0])
tab.add_rows(table[1:])
print(tab)