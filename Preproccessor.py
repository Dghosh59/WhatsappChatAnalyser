import pandas as pd
import re
import io
def preprocess(data):
    #data = io.StringIO(data)
    
   # new_data=list(map(strip,data))
    def is_valid(string):
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s.*:'
        return bool(re.match(pattern, string))
    new_data=(list(filter(is_valid,data)))
    date=[]
    for i in new_data:
        date.append(i.split(',')[0])
    time=[]
    for i in new_data:
        time.append(re.findall(r'\d{1,2}:\d{1,2}',i)[0])
    
    name=[]
    for i in new_data:
        name.append(re.findall('-\s.*?:',i)[0].strip()[2:-1])
    
    messages=[]
    for i in new_data:
        messages.append(re.sub('\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s.*:\s',"",i))

    df_dict={"Date":date,"Time":time,"Name":name,"Messages":messages}
    df=pd.DataFrame(df_dict)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Time"]=pd.to_datetime(df["Time"])
    df["Year"]=df["Date"].dt.year
    df["Month"]=df["Date"].dt.month_name()
    df["Day"]=df["Date"].dt.day_name()
    df["Hour"]=df["Time"].dt.hour
    df["Minutes"]=df["Time"].dt.minute
    df["Time"] = pd.to_datetime(df["Time"]).dt.time
    df.to_csv("WhatsappChat",index=False)
    return df



#main
