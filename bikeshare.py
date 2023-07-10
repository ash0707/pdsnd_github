import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': './data/chicago.csv',
              'new york city': './data/new_york_city.csv',
              'washington': './data/washington.csv' }
VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA.keys():
        city = input("Enter one of the cities to analyze data - chicago, new york city or washington:")
        city = city.lower()
        
        if city not in CITY_DATA.keys():
            print("City Input not accepted, please check your input and try again ...")
    
    print(f"The chosen city is {city}")

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in VALID_MONTHS:
        print("Enter a month between January and June (inclusive) for which you would like to view data")
        print("Enter all in case you want to see data for all the months")
        month = input('Enter your input:').lower()
        
        if month not in VALID_MONTHS:
            print("Month input not accepted, please check your input and try again ...")
            
    print(f"The chosen month is {month}")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in VALID_DAYS:
        print("Enter a day of the week (monday to sunday) for which you want to analyze data. ")
        print("Enter all in case you want to see data for all the days")
        day = input('Enter your input:').lower()
        
        if day not in VALID_DAYS:
            print("Day input not accepted, please check your input and try again ...")

    print(f"The chosen day is {day}")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # already checked that month != all, so can index in VALID_MONTHS
        month = VALID_MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"The most common month is {VALID_MONTHS[most_common_month - 1].title()}")

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of the week is {most_common_day.title()}")

    # Add a column with hour data
    df['start_hour'] = df['Start Time'].dt.hour 
    # display the most common start hour
    most_common_hour = df['start_hour'].mode()[0]
    print(f"The most common start hour is: {most_common_hour} hrs")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most common start stationis : {most_common_start_station}")

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most common end station is: {most_common_end_station}")

    # display most frequent combination of start station and end station trip
    df['start_to_end'] = df['Start Station'] + " to " + df['End Station']
    most_common_route = df['start_to_end'].mode()[0]
    print(f"The most frequent combination of start station and end station trip is {most_common_route}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time in seconds is: {total_travel_time}")
    print(f"Equivalent to {str(datetime.timedelta(seconds=int(total_travel_time)))} in hh:mm:ss")
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The average travel time in seconds is: {mean_travel_time}")
    print(f"Equivalent to {str(datetime.timedelta(seconds=int(mean_travel_time)))} in hh:mm:ss")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"The types of users by number are given below:\n{user_type}")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"The types of users by gender are given below:\n{gender}")
        print(f"Additionally count of users where Gender data is not available is {df['Gender'].isnull().sum()}")
    except:
        print("No Gender data is available for the selected city")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"The earliest year of birth: {earliest}\nThe most recent year of birth: {recent}\nThe most common year of birth: {common_year}")
        print(f"Additionally count of users where Gender data is not available is {df['Birth Year'].isnull().sum()}")
    except:
        print("There are no birth year details in this file.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
              

def display_data(df):
    '''
    Display 5 rows of data to the user at a time if he would like to see the raw data.
    Prompt if he would like to see more data
    '''
    raw_data_options = ['yes', 'no']
    view_raw_data = ''
    counter = 0
    print("Would you like to see raw data?")
    while counter < len(df):
        view_raw_data = input("See next 5 rows of raw data (Enter yes or no)?:").lower()
        if view_raw_data == 'yes':
            if counter + 5 < len(df):
                print(df[counter:counter+5].to_json(orient='records'))
            else:
                print(df[counter:])
            counter += 5
        elif view_raw_data == 'no':
            break
        else:
            print("Not a valid input, please check your input and try again ...")
    
    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
