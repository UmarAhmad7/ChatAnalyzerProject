import streamlit as st

import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")



    # Process the data and display the DataFrame
    df = preprocessor.preprocess(data)
    st.title("Top Chat Statistics")

    #fetch unique user
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button('Show Analysis'):
        num_messages,words,count,linkCount=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Count")
            st.title(count)
        with col4:
            st.header("Link Count")
            st.title(linkCount)

    if selected_user=='Overall':
        st.title('Most Busy User')
        col1, col2 = st.columns(2)

        x,new_df=helper.most_busy_user(df)
        ind=new_df.shape[0]-1
        new_df.drop(ind,inplace=True)
        fig,ax=plt.subplots()
        with col1:
            ax.bar(x.index, x.values,color='green')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    #WordCloud
    st.title('Word Cloud')
    df_wc=helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    most_common_df=helper.most_common_words(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation="vertical")
    st.title('Most Common Words')
    st.pyplot(fig)
    emoji_df=helper.emoji_helper(selected_user,df)
    st.title('Emoji Analysis')

    col1,col2=st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax=plt.subplots()
        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%0.2f')
        st.pyplot(fig)

    st.title("Monthly Chat analysis")
    timeline=helper.monthly_timeline(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(timeline['time'],timeline['message'])
    st.pyplot(fig)
    st.title("Date Wise Analysis")
    daily_time=helper.daily_timeline(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(daily_time['only_date'],daily_time['message'])
    st.pyplot(fig)

    st.title("Day Wise Analysis")
    day_line=helper.day_analysis(selected_user,df)
    fig,ax=plt.subplots()
    ax.bar(day_line.index,day_line.values,color='orange')
    st.pyplot(fig)



