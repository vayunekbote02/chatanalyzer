import re
import pandas as pd


def preprocess(data):
    pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s')
    messages = pattern.split(data)[1:]
    dates = pattern.findall(data)

    df = pd.DataFrame({'user_messages': messages, 'date': dates})

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M - ')

    users = []
    messages = []

    for message in df['user_messages']:
        split_at = re.split('([\w\W]+?):\s', message)
        if split_at[1:]:
            users.append(split_at[1])
            messages.append(split_at[2])
        else:
            users.append('group_notification')
            messages.append(split_at[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_no'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df.drop(columns=['date'], inplace=True)

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append('23' + ' - ' + '00')
        elif hour == 0:
            period.append('00' + ' - ' + '01')
        else:
            period.append(str(hour) + ' - ' + str(hour + 1))

    df['period'] = period

    return df
