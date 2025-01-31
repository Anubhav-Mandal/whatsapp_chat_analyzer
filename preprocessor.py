import re
import pandas as pd  # Ensure pandas is imported

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Splitting the data into messages and dates
    messages = re.split(pattern, data)[1:]  # Exclude the first split as it's empty
    dates = re.findall(pattern, data)

    # Creating a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Converting dates data type
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %H:%M - ")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separating users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # Message has a username
            users.append(entry[1])
            messages.append(entry[2])
        else:  # System notification
            users.append('group notification')
            messages.append(entry[0])

    # Adding users and messages to DataFrame
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extracting additional date and time details
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
