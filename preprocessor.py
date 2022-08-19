import pandas as pd
import re
def preprocessor(data):
    # pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}\s[a-zA-Z]+: '
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s[a-zA-Z]+ - '
    messages = re.split(pattern, data)[1:]
    # dates = re.findall(pattern, data)
    pattern1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s'
    # datesnew = re.split(pattern1, data)
    dates1 = re.findall(pattern1, data)
    


    df = pd.DataFrame({'user_message': messages, 'message_date': dates1})
    # df['message_date'] = df['message_date'].str.replace('AM:','')
    # df['message_date'] = df['message_date'].str.replace('PM:','')
    
    df.rename(columns={'message_date': 'date'}, inplace=True)
    # df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y, %I:%M:%S %p')
    df['date'] = pd.to_datetime(df['date'])
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split("([a-zA-Z]+):\s", message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['messages'] = messages
    df.drop(columns = ['user_message'], inplace = True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df