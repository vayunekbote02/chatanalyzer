from wordcloud import WordCloud
import pandas as pd
import advertools as adv
from collections import Counter


def fetch_stats(user, df):
    df1 = df

    if user != "Overall":
        df1 = df[df['user'] == user]

    nom = df1.shape[0]

    pom = round((nom / df.shape[0]) * 100, 2)

    media = df1[df1['message'] == "<Media omitted>\n"].shape[0]
    return nom, pom, media


def fetch_busiest_users(df):
    x = df['user'].value_counts().head()
    return x


def create_wc(selected_user, df):
    #df = df.replace('<Media omitted>\n', 'Media')
    df = df[df['message'] != '<Media omitted>\n']

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=350, min_font_size=10,
                   background_color="white")
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def data_for_pie(df):
    x = df['user'].value_counts()
    x1 = df['user'].value_counts().head().index
    y = pd.DataFrame(x).reset_index()
    y.columns = ['Name', 'Number of messages']
    name = y["Name"].where(y["Name"].isin(x1), "Other")

    y = y.groupby(name)["Number of messages"].sum()
    y = y.to_frame().reset_index()
    return y


def emoji_helper(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    emojis = []
    for message in df['message']:
        emoji_summary = adv.extract_emoji(message.split())
        for emoji in emoji_summary['emoji']:
            if emoji:
                emojis.extend(emoji)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))

    return emoji_df


def monthly_timeline(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    timeline = df.groupby(['year', 'month_no', 'month']).count()[
        'message'].reset_index().sort_values(['month_no'])

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + ' - ' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def week_activity(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    return df['day_name'].value_counts()


def month_activity(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    return df['month'].value_counts()


def pivot_table(user, df):
    if user != "Overall":
        df = df[df['user'] == user]

    pivot_table = df.pivot_table(
        index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return pivot_table
