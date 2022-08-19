from sqlite3 import Time
import time
from itsdangerous import TimedSerializer
from unittest import result
from numpy import number
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# st.sidebar.title("Whatsapp Chat Analyzer")
#st.title("Whatsapp Chat Analyzer")
st.markdown("<h1 style='text-align: center;'>Whatsapp Chat Analyzer</h1>", unsafe_allow_html=True)


st.image("https://wpleaders.com/wp-content/uploads/2019/10/Best-Live-Chat-Plugins.png")
uploaded_file = st.sidebar.file_uploader("Upload a file")
# uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.075)
        progress.progress(i+1)

    st.balloons()
    st.success("File added successfully")
    
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    

    df = preprocessor.preprocessor(data)
    
    st.title('Top Statistics')
    st.dataframe(df)

    # fetching unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis w.r.t",user_list)

    if st.sidebar.button("Show Analysis"):
        
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # col1, col2, cole3, col4 = st.beta_columns(4)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages) #some error is there
        
        with col4:
            st.header("Links Shared")
            st.title(num_links)

               
        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest users in the group(only Group Level)

        if selected_user == "Overall":
            st.title('Most Active Users')
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='horizontal')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # # Wordcloud 
        # st.title('Wordcloud')
        # df_wc = helper.create_wordcloud(selected_user, df)
        # fig,ax = plt.subplots()
        # ax.imshow(df_wc)
        # st.pyplot(fig)
        # will have to work on wordcloud

        # Most Common Words
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user, df)

        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(most_common_df)

        with col2:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1],color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Emoji Analysis
        st.title('Emojis Analysis')
        emoji_df  = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


        # st.title('Sentiment Analysis Model')
        # sentiment_model_result = helper.sentiment_model(df)
        # st.title(sentiment_model_result)