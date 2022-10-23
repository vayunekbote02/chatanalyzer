import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file on your device")

if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # for unique users
    unique = df['user'].unique().tolist()
    unique.remove('group_notification')
    unique.sort()
    unique.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for user", unique)

    if st.sidebar.button("Show analysis"):
        num_messages, percentage, media = helper.fetch_stats(selected_user, df)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Total messages")
            st.title(num_messages)

        with col2:
            st.header("As a percentage of total messages")
            st.title(percentage)

        with col3:
            st.header("Total number of media sent")
            st.title(media)

        if selected_user == "Overall":
            st.title("Busiest Users")
            x = helper.fetch_busiest_users(df)

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color="orange")
                plt.xticks(rotation=90)
                plt.xlabel("Users")
                plt.ylabel("Messages")
                st.pyplot(fig)

            with col2:
                fig, ax = plt.subplots()
                y = helper.data_for_pie(df)
                ax.pie(y['Number of messages'],
                       labels=y['Name'], autopct='%.2f%%')
                st.pyplot(fig)

        # WordCloud
        st.title("Most frequently used words")
        df_wc = helper.create_wc(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # Emoji analysis
        col1, col2 = st.columns(2)
        emoji_df = helper.emoji_helper(selected_user, df)
        with col1:
            st.header("Total number of emojis sent")
            st.title(emoji_df.sum()[1])
        with col2:
            st.header("Most frequently used emojis")
            st.dataframe(emoji_df)

        # Timeline
        fig, ax = plt.subplots()
        st.header("Activity per month (For each year)")
        timeline = helper.monthly_timeline(selected_user, df)
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Overall Activity
        col1, col2 = st.columns(2)
        with col1:
            st.header("Weekly Activity")
            weekly_series = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(weekly_series.index, weekly_series.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.header("Mothly Activity")
            monthly_series = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_series.index, monthly_series.values, color='orange')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # Activity Map for each day
        st.header("Daily Usage Heatmap")
        pivot_table = helper.pivot_table(selected_user, df)

        fig, ax = plt.subplots()
        ax = sns.heatmap(pivot_table)
        st.pyplot(fig)
