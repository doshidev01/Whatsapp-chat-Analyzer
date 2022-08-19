from turtle import width
from urlextract import URLExtract
# from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import nltk
# nltk.download('all')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiments=SentimentIntensityAnalyzer()

extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    # fetching number of messages
    num_messages = df.shape[0]

    # fetching number of words
    word = []
    for message in df['messages']:
            word.extend(message.split())

    # fetching number of media messages
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    # fetching number of links shared
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return df.shape[0], len(word), num_media_messages, len(links)


def most_active_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x, df

# def create_wordcloud(selected_user, df):
#     f = open('stop_hinglish.txt', 'r')
#     stop_words = f.read()

#     if selected_user != 'Overall':
#         df = df[df['users'] == selected_user]
    
#     temp = df[df['users'] != 'group_notification']
#     temp = temp[temp['messages'] != '<Media omitted\n>']

#     def remove_stop_words(message):
#         y=[]
#         for word in message.split():
#             if word not in stop_words:
#                 y.append(word)
#         return ' '.join(y)

#     wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
#     df_wc = wc.generate(df['message'].str.cat(sep=' '))
#     return df_wc
# error in generatin wordcloud because of python version




def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted\n>']

    words = []

    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.extend(message.split())
    
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    df['day_name'] = df['date'].dt.day_name()
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str(00) + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap

# def sentiment_model(df):
#     df["HAPPY"]=[sentiments.polarity_scores(i)["pos"] for i in df["messages"]]
#     df["SAD"]=[sentiments.polarity_scores(i)["neg"] for i in df["messages"]]
#     df["ANGRY"]=[sentiments.polarity_scores(i)["neu"] for i in df["messages"]]

#     # df.head()
#     x=sum(df["HAPPY"])
#     y=sum(df["SAD"])
#     z=sum(df["ANGRY"])

#     def score(a,b,c):
#         if (a>b) and (a>c):
#             print("Happy ")
#         if (b>a) and (b>c):
#             print("Sad")
#         if (c>a) and (c>b):
#             print("Angry")

    
#     return score(x,y,z)