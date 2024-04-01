import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

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
    while True:
        city = input("\nEnter city(eis) name(s) from [chicago, new york city or washington]"
                     "\nseparate cities by commas: ")
        if ',' in city:
            city = city.lower().split(',')
            city = [item.strip() for item in city]


    # get user input for month (all, january, february, ... , june)
        month = input("\nEnter month(s) from January to June (sparate months by commas),"
                      "\nif you want select all month, please prompt all:  ") 
        if month != 'all' and ','  in  month:
            month = month.lower().split(',')
            month = [item.strip() for item in month]


    # get user input for day of week (all, monday, tuesday, ... sunday)
        #day = input("Enter day of week, all for all days: ")
        day = input("\nEnter day(s) from Monday to Sunday (sparate months by commas),"
                      "\nif you want select all days, please prompt all:  ") 
        if day != 'all' and ','  in  day:
            day = day.lower().split(',')
            day = [item.strip() for item in day]
            
            
            
        # check user inputs to continue:
        print('\n')
        print('please check your input (including spelling check):')
        
        print(f'\nCity(ies): {city}')

        print(f'\nMonth(s): {month}')

        print(f'\nday(s): {day}')
        
        confirmation = input('\nDo you confirm your inputs?'
                             '\n[y] Yes  '
                             '\n[n] No  ')
        
            
        if confirmation == 'y':
            break
        else:
            print("\nLet's try this again!")
        



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
    # filter the data according to the selected city filters
    if isinstance(city, list):
       df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                      sort=True)
       # reorganize DataFrame columns after a city concat
       try:
           df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                    'Trip Duration', 'Start Station',
                                    'End Station', 'User Type', 'Gender',
                                    'Birth Year'])
       except:
           pass
    else:
       df = pd.read_csv(CITY_DATA[city])

    
    
    
    
    
    # create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        if isinstance(month, list):
            df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month)+1)], month))
        else:
            df = df[df['Month'] == (months.index(month)+1)]
       # month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        #df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        if isinstance(day, list):
            df = pd.concat(map(lambda day: df[df['day_of_week'] == day.title()], day))
        else:
            #day = weekdays.index(day) 
            df = df[df['day_of_week'] == day.title()]
            
        # filter by day of week to create the new dataframe
        #day = weekdays.index(day) 
        #df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
   

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('The month with the most travels is: ' + str(months[most_common_month-1]).title() + '.')


    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is: ' + str(most_common_day) + '.')


    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is: ' + str(most_common_hour) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " + most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common start end is: " + most_common_end_station)


    # display most frequent combination of start station and end station trip
    df['Combined Start-End stations'] = (df['Start Station'] + ' - ' + df['End Station'])
    most_common_start_end_combination = str(df['Combined Start-End stations'].mode()[0])
    print("The most common start-end combination of stations is: " + most_common_start_end_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print(f'The total travel time is : {total_travel_time}.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'The mean travel time is : {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'\nCounts of user types are {user_types}.')

    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_distribution)
    except KeyError:
        print("Oops! No data available for user genders for chosen city.")
    
    # Display earliest, most recent, and most common year of birth
    try:
       earliest_birth_year = str(int(df['Birth Year'].min()))
       print("\nThe oldest person to ride one "
             "bike was born in: " + earliest_birth_year)
       most_recent_birth_year = str(int(df['Birth Year'].max()))
       print("\nThe youngest person to ride one "
             "bike was born in: " + most_recent_birth_year)
       most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
       print("\nThe most common birth year amongst "
             "riders is: " + most_common_birth_year)
    except:
        print("\nOops! No data available for birth year for chosen city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_row_data(df, inital_index):
    # check if user wanrts to see row data
    #print('Do you wan to see row data:')
    
    #see_row = input('\n[y] Yes  '
    #                     '\n[n] No  ')
    
    while True:
        
        for i in range(inital_index, len(df.index)):
            df1 = df.drop(['Month', 'day_of_week', 'Start Hour'], axis = 1)
                
            print("\n")
            print(df1.iloc[inital_index:inital_index+5].to_string())
            inital_index += 5
            print("\n")
            print("\n")
            print('Do you wan to see more row data:')
            see_more_row = input('\n[y] Yes  '
                                    '\n[n] No  ')
            
            if see_more_row == 'y':
                continue
            else:
                break
        break

    return inital_index
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        
        print('Do you wan to see row data:')
        
        see_row = input('\n[y] Yes  '
                            '\n[n] No  ')
        inital_index = 0
        if see_row == 'y':
            
            print_row_data(df, inital_index)

        restart = input('\nWould you like to restart? Enter:'
                        '\n[y] Yes'
                        '\n[n] No.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
