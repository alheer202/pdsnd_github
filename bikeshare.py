import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

day_dict = {'monday': 1,
            'tuesday': 2,
            'wednesday': 3,
            'thursday': 4,
            'friday': 5,
            'saturday':6,
            'sunday': 7,
            'all': 'all'}

month_dict = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'june': 5,
              'july': 6,
              'all': 'all'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    time.sleep(0)

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to analyze data from Chicago, New York City or Washington? ').lower()
    while True:
        try:
            city = CITY_DATA[city]
            break
        except:
            city = input('Please type either "Chicago", "New York City" or "Washington": ').lower()
    time.sleep(0)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Would you like to analyze a specific month? If yes, please type the respective month\'s name, otherwise type "all": ').lower().strip()
    while True:
        try:
            month = month_dict[month]
            break
        except:
            month = input('Please type either "January", "February", "March", "April", "June", "Juli", or "all": ').lower().strip()
    time.sleep(0)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    weekday = input('Would you like to analyze a specific weekday? If yes, please type the respective day\'s name, otherwise type "all": ').lower().strip()
    while True:
        try:
            weekday = day_dict[weekday]
            break
        except:
            weekday = input('Please type either "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", ,"Sunday", or "all: ').lower().strip()
    time.sleep(0)
    print('-'*40)

    return city, month, weekday


def load_data(city, month, weekday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    parse_dates = ['Start Time','End Time']

    df = pd.read_csv(city, parse_dates= parse_dates)
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ',' + df['End Station']
    df['duration'] = df['End Time'] - df['Start Time']

    if month != 'all':
        df = df[df['Start Time'].dt.month == month]

    if weekday != 'all':
        df = df[df['Start Time'].dt.dayofweek == (weekday-1)]

    return df

def raw_data(df):
    """Displays five random rows of the filtered and enriched dataframe"""
    choice = input('Do you want to see three illustrative datapoints from your selection?: ').lower()
    while choice not in ['yes','no']:
        choice = input("Please answer 'Yes' or No': ").lower()
    if choice == 'yes':
        print(df.sample(3))
    print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df.weekday.mode()[0]
    print('The most common month is: {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day = df.month.mode()[0]
    print('The most common weekday is: {}'.format(common_day))

    # TO DO: display the most common start hour
    common_hour = df.hour.mode()[0]
    print('The most common hour is: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df.groupby('Start Station').size().sort_values(ascending=False).index[0]
    print('The most common start station is: {}'.format(common_start))

    # TO DO: display most commonly used end station
    common_end = df.groupby('End Station').size().sort_values(ascending=False).index[0]
    print('The most common start end is: {}'.format(common_end))

    # TO DO: display most frequent combination of start station and end station trip
    common_trip = df.groupby('trip').size().sort_values(ascending=False).index[0]
    start, end = common_trip.split(',')
    print('The most common route is: from {} to {}'.format(start,end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df.duration.sum()
    print('The total travel time is: {}'.format(total_time))

    # TO DO: display mean travel time
    mean_time = (total_time.total_seconds() /60) / df.shape[0]
    print('The mean travel time is: {} minutes'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    type1 = df['User Type'].value_counts().index[0]
    type2 = df['User Type'].value_counts().index[1]
    count1= df['User Type'].value_counts().values[0]
    count2= df['User Type'].value_counts().values[1]
    print('In the given timeframe, {} trips were made by {}s and {} trips by {}s'.format(count1, type1, count2, type2))

    # TO DO: Display counts of gender
    try:
        type1 = df['Gender'].value_counts().index[0]
        type2 = df['Gender'].value_counts().index[1]
        count1= df['Gender'].value_counts().values[0]
        count2= df['Gender'].value_counts().values[1]
        count3= df['Gender'].isnull().sum()
        print('In the given timeframe, {} trips were made by {} customers and {} trips by {} customers, while for {} trips the gender is unknown'.format(count1, type1, count2, type2, count3))
    except KeyError:
        print('Sorry, there is no Gender information available for your selection')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        common_year = df['Birth Year'].mode()[0]
        print('The most common birth year is: {}'.format(int(common_year)))
        min_year = df['Birth Year'].min()
        print('The earlierst birth year is: {}'.format(int(min_year)))
        max_year = df['Birth Year'].max()
        print('The most recent birth year is: {}'.format(int(max_year)))
    except KeyError:
        print('Sorry, there is no Age information available for your selection')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, weekday = get_filters()
        df = load_data(city, month, weekday)
        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
