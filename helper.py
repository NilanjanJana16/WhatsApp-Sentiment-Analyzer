import pandas as pd
from collections import Counter

import emoji

from urlextract import URLExtract

extractor = URLExtract()

from wordcloud import WordCloud


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # fetch number of messages
    num_messages = df.shape[0]

    # fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch urls
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), media_msg, len(links)


def most_busy_users(df):
    x = df['users'].value_counts()
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'users', 'users': 'precent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['users'] != 'group notification']
    temp = temp[temp['message'] != '<Media Omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group notification']
    temp = temp[temp['message'] != '<Media Omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    most_common_df = most_common_df.rename(columns={0: 'words', 1: 'occurences '})
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.distinct_emoji_list(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df = emoji_df.rename(columns={0: 'Emojis', 1: 'Occurences'})

    return emoji_df


# monthly timeline

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

# daily timeline

def dailytimeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

# activity

def week_activity(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    activity_map = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_map






