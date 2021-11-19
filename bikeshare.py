# Import libraries
import time
import pandas as pd
import random

# Variables
city_data = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

months_data = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_data = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']


def get_filters():
    """
    This function asks the user to specify a city, month, and day to analyze.

    Returns:
        city: String - name of the city to analyze.
        month: String - name of the month to filter by, or "all" to apply no month filter.
        day: String - name of the day of week to filter by, or "all" to apply no day filter.
    """
    print('Hello! Let\'s explore some bikeshare data for the US for the year 2017!')

    # Ask for the city
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        if city not in city_data:
            print('Invalid city name, please enter one of these options: Chicago, New York or Washington.')
            continue
        else:
            break

    # Ask for the month
    while True:
        month = input('Which month you want to choose from? (January, Feburary, .. , June)'
                      ' Type all if you want to choose all months.\n').lower()
        if month not in months_data:
            print('Invalid month name .. Please choose from the given list:\n', months_data)
            continue
        else:
            break

    # Ask for the day
    while True:
        day = input('Which day of the week you want to filter by? (Sunday, Monday, .. , Saturday)'
                    ' Type all if you want to choose all days.\n').lower()
        if day not in day_data:
            print('Invalid day name .. Please choose from the given list\n', day_data)
            continue
        else:
            break

    print('-'*45)
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
    df = pd.read_csv(city_data[city])

    # convert the Start and End Time columns to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day and start hour from Start Time column
    df['month'] = df['Start Time'].dt.month
    df['week_day'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month = months_data.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['week_day'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args: df - Pandas DataFrame
    returns: None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # The most common month
    popular_month = df['month'].mode()[0]

    # The most common day of week
    popular_day = df['week_day'].mode()[0]

    # The most common start hour
    popular_hour = df['start_hour'].mode()[0]

    print(f'Popular month is: {popular_month},\nPopular day is: {popular_day},\nPopular hour is: {popular_hour}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*45)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # Most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # Most frequent combination of start station and end station trip
    frequent_stations_combination = (df['Start Station'] + ' --> ' + df['End Station']).mode()[0]

    print(f'Popular start station is: {popular_start_station},\nPopular end station is: {popular_end_station},\n'
          f'Most frequent route is: {frequent_stations_combination}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*45)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_trip_duration = df['Trip Duration'].sum()

    # Mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    # Longest travel time
    longest_travel_time = df['Trip Duration'].max()

    print(f'Total trip duration is: {total_trip_duration} seconds,'
          f'\nLongest trip is: {longest_travel_time} seconds,'
          f'\nMean Travel time is: {mean_travel_time}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*45)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_type_counts = df['User Type'].value_counts()
    print(f'In this dataset, we have:\n{user_type_counts.to_string()}')

    # Display counts of gender, earliest, most recent, and most common year of birth
    try:
        gender_counts = df['Gender'].value_counts()
        min_year_of_birth = df['Birth Year'].min()
        max_year_of_birth = df['Birth Year'].max()
        common_year_of_birth = df['Birth Year'].mode()[0]
        print(f'\nGender counts in this dataset is:\n{gender_counts.to_string()}')
        print(f"Earliest year of birth is {int(min_year_of_birth)}, "
              f"Most recent year of birth is {int(max_year_of_birth)}. "
              f"However, the most common year of birth is {int(common_year_of_birth)}.")
    # When we don't have genders or birth year columns in the dataset.
    except KeyError:
        pass
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*45)


def get_some_data(df):
    """
    Asks the user if they want some raw data and accordingly it chooses the data for 5 random users.
    Args: df - Pandas DataFrame
    """

    max = 0
    count_of_rows = len(df.index)
    while max <= count_of_rows:
        get_data = input("Would you like to get some raw data for some users? Enter yes or no?\n")
        if get_data.lower() not in ['yes', 'no']:
            print("Invalid input, please enter yes or no")
            continue
        elif get_data.lower() == "yes":
            max += 5
            df_json = df.to_json(orient='records', lines=True, date_format='iso').splitlines()
            # Print 5 random unique users from the list
            print(random.sample(df_json, 5), end="\n")
            continue
        elif get_data.lower() == "no":
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_some_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Closing the program...")
            break


if __name__ == "__main__":
    main()
