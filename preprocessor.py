import re
import pandas as pd


def preprocess(data):
    # Adjusted pattern to parse your date format correctly
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Splitting messages based on the pattern
    messages = re.split(pattern, data)[1:]  # Skip the first empty split
    dates = re.findall(pattern, data)

    # Creating a DataFrame with parsed dates and messages
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Adjusted date parsing format for the '31/05/24, 02:15 - ' format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    clean_messages = []

    for message in df['user_message']:
        # Use regex to split based on the first occurrence of ': ', allowing for special characters
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) == 3:
            users.append(entry[1])  # Username
            clean_messages.append(entry[2])  # Message text
        else:
            users.append('group_notification')
            clean_messages.append(entry[0])

    # Adding extracted data to the DataFrame
    df['user'] = users
    df['message'] = clean_messages

    # Drop the original combined column
    df.drop(columns=['user_message'], inplace=True)

    # Add date-related columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()

    return df
