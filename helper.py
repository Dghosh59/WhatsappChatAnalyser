from urlextract import URLExtract
import re
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
url_pattern = re.compile(r"https?://\S+|www\.\S+")
extractor=URLExtract()
def fetch_stats(selected_user,df):
    if(selected_user=="Overall"):
        a= df.shape[0]
        b=0
        for i in df["Messages"]:
            b+=len(i)
        c=(df[df["Messages"]=="<Media omitted>"]).shape[0]
        d = df["Messages"].dropna().str.findall(url_pattern).explode().count()




    else:
        x=df[df["Name"]==selected_user]
        a=x.shape[0]
        b=0
        for i in x["Messages"]:
            b+=len(i)
        c=(x[x["Messages"]=="<Media omitted>"]).shape[0]
        d = x["Messages"].dropna().str.findall(url_pattern).explode().count()

    return (a,b,c,d)
def fetch_busiest(df):
    x=df["Name"].value_counts().head(7)
    y=round((df["Name"].value_counts().head(12)/df.shape[0]*100).reset_index().rename(columns={'index':'name','count':'percent'}),2)
    return x,y

def create_wordcloud(df,selected_user):
    if(selected_user!="Overall"):
        df=df[df["Name"]==selected_user]
    df = df[df["Messages"].notna()]  # Remove NaN messages
    df = df[~df["Messages"].str.contains("<Media omitted>")]  # Remove media messages

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    df_wc=wc.generate(df["Messages"].str.cat(sep=" "))
    return df_wc

def most_common_words(df,selected_user):
    if(selected_user!="Overall"):
        df=df[df["Name"]==selected_user]
    temp=df[df["Messages"]!="<Media omitted>"]
    f=open("stopwords.txt","r")
    stop_words=f.read()
    words=[]
    for message in temp["Messages"]:
        for word in message.split():  
            if word not in stop_words:
                words.append(word)

    # Create DataFrame and count word occurrences
    x = pd.DataFrame({"Words": words})
    x = x["Words"].value_counts().reset_index() 
    x.columns = ["word", "count"] 
    return x.head(10)
def emoji_helper(df,selected_user):
    if(selected_user!="Overall"):
        df=df[df["Name"]==selected_user]
    emojis=[]
    for i in df["Messages"]:
        emojis.extend([x for x in i if emoji.is_emoji(x)])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def get_timeline(df,selected_user):
    if(selected_user!="Overall"):
        df=df[df["Name"]==selected_user]
    df["Month_no"]=df["Date"].dt.month
    x=df.groupby(["Year","Month_no","Month"]).count()["Messages"].reset_index()
    x["new"]=[str(x["Month"][i][0:3])+"-"+str(x["Year"][i]) for i in range(x.shape[0])]
    x=x[["new",'Messages']]
    return x
def get_timeline_daily(df,selected_user):
    if(selected_user!="Overall"):
        df=df[df["Name"]==selected_user]
    x=df.groupby(["Date"]).count()["Messages"].reset_index()

    return x

def get_activity_map(df,selected_user):
    if(selected_user!="Overall"):
        df=df[df["Name"]==selected_user]
    df["day"]=df["Date"].dt.day_name()
    x=df.groupby(["day"]).count()["Messages"].reset_index()
    y=df.groupby(["Month"]).count()["Messages"].reset_index()
    return x,y
def get_hourly_map(df,selected_user):
    if(selected_user!="Overall"):
        df=df[df["Name"]==selected_user]
    df["day"]=df["Date"].dt.day_name()
    return df







