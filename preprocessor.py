import re
import pandas as pd

def prepro(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    patterns = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s\w{2}'
    dates = re.findall(patterns, data)
    df = pd.DataFrame({'user_msg': messages, 'msg_date': dates})
    df['msg_date'] = pd.to_datetime(df['msg_date'], format='%m/%d/%y, %H:%M %p')
    df.rename(columns={'msg_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages

    df.drop(columns=['user_msg'], inplace=True)
    # adding year
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
