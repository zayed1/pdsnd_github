import time
import pandas as pd
import statistics as st

CITY_NAMES = { 'washington': 'washington.csv',
              'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
             }

def get_information():
    print("Ciao!, Let's explore some United Nation bikeshare data today!")

    city_value = input("\nFrom which city today you wanted to see the data, list of available cities are  NEW YORK , CHICAGO , WASHINGTON/n \n").lower()

    while city_value not in ['new york', 'chicago', 'washington', 'all']:
        city_value = input("\nPlease Enter The Correct city *please see the upper list for valid city: \n").lower()

    month_value = input("\nEnter which month? January, February, March, April, May, or June?, \n").lower()

    while month_value not in ['january', 'february', 'march', 'april', 'may', 'june', 'all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']:
        month_value = input('Please enter the valid month* for details please see above\n').lower()

    day_value =  input('Which day  monday, tuesday, wednesday, thursday, friday, saturday , sunday or all to display data of all days?\n').lower()

    while day_value not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'm', 't', 'w', 'r', 'f', 's', 'u']:
        day_value = input('Please enter the Correct day: ').lower()

    print("All Data Successfully Recorded")
    print('-'*100)

    return city_value, month_value, day_value

def calculate_data(city, month, day):
    cd = pd.read_csv(CITY_NAMES[city])

    cd['Start Time'] = pd.to_datetime(cd['Start Time'])
    cd['End Time'] = pd.to_datetime(cd['End Time'])

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1 if month in months else months.index(month[:3]) + 1
        cd = cd[cd['Start Time'].dt.month == month]

    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'm', 't', 'w', 'r', 'f', 's', 'u']
        day = days.index(day) if day in days else days.index(day[:3])
        cd = cd[cd['Start Time'].dt.weekday == day]

    return cd

def display_data(cd):
    current_line = 0
    while True:
        display_more = input('\nDo you want to see the next 5 rows of data? Enter yes or no:\n').lower()
        if display_more != 'yes':
            return
        print(cd.iloc[current_line : current_line + 5])
        current_line += 5

def stats_of_time(cd, month, day):
    print('\nNow Calculating The Most Frequent Times of Travel.........\n')
    start_time = time.time()

    if(month == 'all'):
        most_common_month = cd['Start Time'].dt.month.value_counts().idxmax()
        print('Most common month is ' + str(most_common_month))

    if(day == 'all'):
        most_common_day = cd['Start Time'].dt.weekday_name.value_counts().idxmax()
        print('Most common day is ' + str(most_common_day))

    most_common_hour = cd['Start Time'].dt.hour.value_counts().idxmax()
    print('Most popular hour is ' + str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    


def stats_of_station(cd):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = st.mode(cd['Start Station'])
    print('\nMost common start station is {}\n'.format(most_common_start_station))

    # It display most commonly used end stations
    most_common_end_station = st.mode(cd['End Station'])
    print('\nMost common end station is {}\n'.format(most_common_end_station))

    # It display most frequent combination of start station and end station trip
    combination_trip = cd['Start Station'].astype(str) + " to " + cd['End Station'].astype(str)
    most_frequent_trip = combination_trip.value_counts().idxmax()
    print('\nMost popular trip is from {}\n'.format(most_frequent_trip))

    print("\nThis can take %s seconds." % (time.time() - start_time))
    

def stats_trip_duration_(ds):
    #It Displays the stastics average or total duration

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays the  total travel time 
    total_travel_time = ds['Trip Duration'].sum()
    first_time = total_travel_time
    day = first_time // (24 * 3600)
    first_time = first_time % (24 * 3600)
    hour = first_time // 3600
    first_time %= 3600
    minutes = first_time // 60
    first_time %= 60
    seconds = first_time
    print('\nTotal travel timing is {} days {} hours {} minutes {} seconds'.format(day, hour, minutes, seconds))


    # Here it displays mean travel time
    mean_travel_time = ds['Trip Duration'].mean()
    second_time = mean_travel_time
    second_day = second_time // (24 * 3600)
    second_time = second_time % (24 * 3600)
    second_hour = second_time // 3600
    second_time %= 3600
    second_minute = second_time // 60
    second_time %= 60
    seconds2 = second_time
    print('\nMean travel timing is {} hours {} minutes {} seconds'.format(second_hour, second_minute, seconds2))


    print("\nThis took %s seconds." % (time.time() - start_time))


def stats_user(us1):
    #To display the stastics of bikeshare data

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    no_of_subscribers = us1['User Type'].str.count('Subscriber').sum()
    no_of_customers = us1['User Type'].str.count('Customer').sum()
    print('\nNumber of subscribers are {}\n'.format(int(no_of_subscribers)))
    print('\nNumber of customers are {}\n'.format(int(no_of_customers)))

    # Display counts of gender
    if('Gender' in us1):
        male_count = us1['Gender'].str.count('Male').sum()
        female_count = us1['Gender'].str.count('Female').sum()
        print('\nNumber of male users are {}\n'.format(int(male_count)))
        print('\nNumber of female users are {}\n'.format(int(female_count)))


    if('Birth Year' in us1):
        earliest_year = us1['Birth Year'].min()
        recent_year = us1['Birth Year'].max()
        most_common_birth_year = st.mode(us1['Birth Year'])
        print('\n Oldest Birth Year is {}\n Youngest Birth Year is {}\n Most popular Birth Year is {}\n'.format(int(earliest_year), int(recent_year), int(most_common_birth_year)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    

def main():
    while True:
        city, month, day = get_information()
        cd = calculate_data(city, month, day)

        display_data(cd)

        stats_of_time(cd, month, day)
        stats_of_station(cd)
        stats_trip_duration_(cd)
        stats_user(cd)

        restart = input('\nWould you like to restart, choose to Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
    