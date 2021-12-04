import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    cities = ['chicago', 'new york city', 'washington']
    city = str(input('Please enter a city to filter with (chicago, new york city, washington) : ')).lower()
    while city not in cities:
        city = str(input('Please enter a valid city (chicago, new york city, washington) : ')).lower()

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = str(input('Please enter a month to filter with (all, january, february, ... , june) : ')).lower()
    while month not in months:
        month = str(input('Please enter a valid month (all, january, february, ... , june) : ')).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ['All', 'Monday', 'Tuesday', 'Sunday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day = str(input('Please enter a weekday to filter with (all, monday, tuesday, ... sunday) : ')).title()
    while day not in weekdays:
        day = str(input('Please enter a valid weekday (all, monday, tuesday, ... sunday) : ')).title()

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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df.loc[:, 'month'].mode()
    print('The most common month is : {}'.format(common_month[0]))

    # display the most common day of week
    common_day = df.loc[:, 'day_of_week'].mode()
    print('The most common day is : {}'.format(common_day[0]))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    common_hour = df.loc[:, 'start_hour'].mode()
    print('The most common start hour is : {}'.format(common_hour[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df.loc[:, 'Start Station'].mode()
    print('The most common Start Station is : \n{}\n'.format(common_start_station[0]))

    # display most commonly used end station
    common_end_station = df.loc[:, 'End Station'].mode()
    print('The most common End Station is : \n{}\n'.format(common_end_station[0]))

    # display most frequent combination of start station and end station trip
    df['comb_station'] = df.loc[:, 'Start Station'] + " | " + df.loc[:, 'End Station']
    common_comb = df.loc[:, 'comb_station'].mode()
    print('The most common combination of start station and end station is : \n{}\n'.format(common_comb[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df.loc[:, 'Trip Duration'].sum()
    print('The total travel time is :\n{} Mins \n{} Hours \n'.format(
        round(total_travel_time/60), round(total_travel_time/3600)))

    # display mean travel time
    mean_travel_time = round(df.loc[:, 'Trip Duration'].mean())
    print('The mean travel time is :\n{} mins \n{} Hours \n'.format(
        round(mean_travel_time/60), round(mean_travel_time/3600, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_types = df.loc[:, 'User Type'].value_counts()
    print('The counts of user types is :\n{} \n'.format(count_types))

    if city != 'washington':

        # Display counts of gender
        count_gender = df.loc[:, 'Gender'].value_counts()
        print('The counts of gender is :\n{} \n'.format(count_gender))

        # Display earliest, most recent, and most common year of birth
        earliest_year = df.loc[:, 'Birth Year'].min()
        print('The most earliest year of birth is : \n{}\n'.format(int(earliest_year)))

        common_year = df.loc[:, 'Birth Year'].mode()
        print('The most common year of birth is : \n{}\n'.format(int(common_year[0])))

        recent_year = df.loc[:, 'Birth Year'].max()
        print('The most recent year of birth is : \n{}\n'.format(int(recent_year)))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    else:
        print("Sorry, No user genders and birth information available for washington :(")


def display_raw(df):
    """Displays 5 lines of filtered raw data upon user input."""
    start = 0
    n = 5
    while True:
        response = input("Would you like to see 5 lines of raw data ? (Yes / No) : ").lower()
        if response == 'yes':
            print(df.loc[start:n, :])
            start, n = n+1, n+5
        else:
            break



def plotting_stats(df, month, day, city):
    """Plotting the most common statistics in a user friendly formatted plots ."""

    # Plotting time stats
    fig, ax = plt.subplots(1, 3, tight_layout=True)
    fig.suptitle('Time stats')
    fig.set_size_inches([10, 7])

    if month == 'all':
        sns.countplot(ax=ax[0], x="month", data=df, order=df.month.value_counts().index)
        ax[0].set(title="Most common month", xlabel="Month")
        ax[0].bar_label(ax[0].containers[0])

    if day == "All":
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        sns.countplot(ax=ax[1], x="day_of_week", data=df, order=day_order)
        ax[1].set(title="Most common Day", xlabel="Day")
        ax[1].tick_params(axis='x', rotation=90)
        ax[1].bar_label(ax[1].containers[0])

    sns.countplot(x="start_hour", data=df, order=df.start_hour.value_counts().iloc[:22].index)
    ax[2].set(title="Most common Hour", xlabel="Hour")
    ax[2].tick_params(axis='x', rotation=90)
    ax[2].set_xticklabels(ax[2].get_xticklabels(), size=8)

    plt.show(block=True)


    # Plotting stations stats
    fig, ax = plt.subplots(1, 3, tight_layout=True)
    fig.suptitle('Station stats')
    fig.set_size_inches([10, 7])

    sns.countplot(ax=ax[0], x="Start Station", data=df, order=df['Start Station'].value_counts().iloc[:25].index)
    ax[0].set(title="Most common Start Stations", xlabel="Station", ylabel="Frequency")
    ax[0].tick_params(axis='x', rotation=90)
    ax[0].set_xticklabels(ax[0].get_xticklabels(), size=8)

    sns.countplot(ax=ax[1], x="End Station", data=df, order=df['End Station'].value_counts().iloc[:25].index)
    ax[1].set(title="Most common End Stations", xlabel="Station")
    ax[1].tick_params(axis='x', rotation=90)
    ax[1].set_xticklabels(ax[1].get_xticklabels(), size=8)

    sns.countplot(ax=ax[2], x="comb_station", data=df, order=df['comb_station'].value_counts().iloc[:25].index)
    ax[2].set(title="Most common Combinations ", xlabel="Stations")
    ax[2].tick_params(axis='x', rotation=90)
    ax[2].set_xticklabels(ax[2].get_xticklabels(), size=8)

    plt.show(block=True)


    # Plotting user stats
    if city != 'washington':
        fig, ax = plt.subplots(1, 3, tight_layout=True)
        fig.suptitle('User stats')
        fig.set_size_inches([10, 7])

        sns.countplot(ax=ax[0], x="User Type", data=df)
        ax[0].set(title="User types count", xlabel="Type")
        ax[0].bar_label(ax[0].containers[0])

        sns.countplot(ax=ax[1], x="Gender", data=df)
        ax[1].set(title="Gender count", xlabel="Gender")
        ax[1].bar_label(ax[1].containers[0])

        df['Birth Year'] = df['Birth Year'].convert_dtypes()
        sns.countplot(ax=ax[2], x="Birth Year", data=df, order=df['Birth Year'].value_counts().iloc[:21].index)
        ax[2].set(title="The most common year of birth", xlabel="Year")
        ax[2].tick_params(axis='x', rotation=90)
        ax[2].set_xticklabels(ax[2].get_xticklabels(), size=8)

        plt.show(block=True)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        plotting_stats(df, month, day, city)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no : \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
