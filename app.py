import matplotlib.pyplot as plt
import streamlit as st

import seaborn as sns

import helper
import preprocessor

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.prepro(data)
    # st.text(data)
    # st.dataframe(df)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, media_msg, num_links = helper.fetch_stats(selected_user, df)
        st.title("Statistics of Your Chat:")

        col1, col2, col3, col4 = st.columns(4)

        st.title("Statistics of Your Chat:")
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media/Stickers Shared")
            st.title(media_msg)
        with col3:
            st.header("Links Shared")
            st.title(num_links)

        # timeline of the chats

        # monthly

        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'white')
        ax.set_facecolor("black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily

        st.title('Daily Timeline')
        daily_timeline = helper.dailytimeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.figure(figsize=(18, 10))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='white')
        ax.set_facecolor("black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map

        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'white')
            ax.set_facecolor("black")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'white')
            ax.set_facecolor("black")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        activity_map = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_map)
        st.pyplot(fig)







        # finding busiest users in the group(Group Level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='white')
                ax.set_facecolor("black")
                # plt.figure(backcolor='black')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # word cloud
        st.title('Word Cloud')
        dt_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(dt_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most Commonly Used Words')
        most_common_df = helper.most_common_words(selected_user, df)
        st.dataframe(most_common_df)

        # emojis analysis

        st.title('Commonly Used Emojis')
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

    # with col2:
    # fig, ax = plt.subplots()
    # ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.2f")
    # st.pyplot(fig)
