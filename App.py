import streamlit as st
import Preproccessor
import helper as h
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    data=(data.split('\n'))
    df = Preproccessor.preprocess(data)

    # fetch unique users
    user_list = df['Name'].unique().tolist()
    user_list.remove('Meta AI')
    user_list.remove('GPT')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if(st.sidebar.button("Show Analysis")):
        num_matches,num_words,num_media,num_links=h.fetch_stats(selected_user,df)
    
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_matches)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #timelineAnalysis
        st.title("Monthly Timeline")
        x=h.get_timeline(df,selected_user)
        fig,ax=plt.subplots()
        ax.plot(x["new"],x["Messages"],color="blue")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        #timelineAnalysisdaily
        st.title("Daily Timeline")
        x=h.get_timeline_daily(df,selected_user)
        fig,ax=plt.subplots()
        ax.plot(x["Date"],x["Messages"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        if(selected_user=="Overall"):
            st.title("Busiest Users")
            col1,col2=st.columns(2)
            
            a,b=h.fetch_busiest(df)
            fig,ax=plt.subplots()
            with col1:
                ax.bar(a.index,a.values,color='pink')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(b,height=250)
        
        #worldcloud
        st.title("Word Cloud")
        df_wc=h.create_wordcloud(df,selected_user)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most Common Words")
        x=h.most_common_words(df,selected_user)
        st.dataframe(x,height=400,width=300)
        fig,ax=plt.subplots()
        ax.pie(x["count"],labels=x["word"])
        st.pyplot(fig)

        #emojiAnalysis
        st.title("Emojis Used")
        emoji_df=h.emoji_helper(df,selected_user)
        st.dataframe(emoji_df)

        #ActivityMap
        col1,col2=st.columns(2)
        x,y=h.get_activity_map(df,selected_user)
        
        with col1:
            st.title("Daily Map")
            fig,ax=plt.subplots()
            ax.bar(x["day"],x["Messages"],color="yellow")
            plt.xticks(rotation="vertical")
            st.pyplot(fig) 
        with col2:
            st.title("Monthly Map")
            fig,ax=plt.subplots()
            ax.bar(y["Month"],y["Messages"],color="black")
            plt.xticks(rotation="vertical")
            st.pyplot(fig) 
        #HourMap
        st.title("Day vs Hour ActivityMap")
        y=h.get_hourly_map(df,selected_user)
        fig,ax=plt.subplots()
        heatmap_data = y.pivot_table(index="Day", columns="Hour", values="Messages", aggfunc="count")
        ax=sns.heatmap(heatmap_data, cmap="coolwarm", annot=False, fmt=".0f", linewidths=0.5)
        st.pyplot(fig) 










                
            


