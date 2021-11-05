import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tweepy
from tweepy import OAuthHandler
import re
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import openpyxl
import time
import tqdm

#To hide Warnings

st.set_option('deprecation.showfileUploaderEncoding',False)
st.set_option('deprecation.showPyplotGlobalUse',False)


st.title("Twitter Sentiment analysis")

from PIL import Image
image=Image.open('https://github.com/sou35/Twitter-Sentiment-Analysis-Deployed/blob/main/Hero-Twitter-search.png')
st.image(image,caption='Twitter for Analytics',use_column_width=True)
    
html_temp ="""
     <div style="background-color:tomato;"><p style="color:white;font-size:40px;padding;9px">Live twitter sentiment analysis</p></div>
      """
st.markdown(html_temp,unsafe_allow_html=True)
st.subheader("Select a topic which you'd like to get the sentiment analysis on :")

##### TWITTER API connection #######


consumer_key="Ievvx6xKz38neB78JBg0GBoxl"
consumer_secret="SskcIrCedDELpE7PGgz820HbSyixoIrUIBhdkZeOH7JGE2SoM9"
access_token="1394858173476052995-8PMCa1g1gQd1QFI4teI6xKNaZzsu4n"
access_token_secret="NO5vH7uR29b4NqcpvheZzlmOP4A46gZxLMvfa9I7u4DMA"
#use the above credentials to authenticate the API.

auth =tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

 
df=pd.DataFrame(columns=["Date","User","IsVerified","Tweet","Links","RT","User_location"])
print(df)

#########################################################################################################


def get_tweets(Topic,Count):
    i=0
    for tweet in tweepy.Cursor(api.search, q=Topic,count=100,lang="en",exclude='retweets').items():
        print(i, end='/r')
        df.loc[i,"Date"]=tweet.created_at
        df.loc[i,"User"]=tweet.user.name
        df.loc[i,"IsVerified"]=tweet.user.verified
        df.loc[i,"Tweet"]=tweet.text
        df.loc[i,"Likes"]=tweet.favorite_count
        df.loc[i,"RT"]=tweet.retweet_count
        df.loc[i,"User_location"]=tweet.user.location
   #  save as csv file   
    #df.to_csv("TWeeteDataset.csv",index=False)
        i=i+1
        if i>Count:
               break
                
                
# Function to Clean the Tweet          
def cleanTxt(text):
    text=re.sub(r'@[A-Za-z0-9]+','',text) #removed @mentions
    text=re.sub(r'#','',text) # removing the # symbol
    text=re.sub(r'RT[\s]+','',text) #Removing RT
    text=re.sub(r'https?:\/\/s+','',text) # Removing the hyper link
    return text   

# Function to analyze sentiment

from textblob import TextBlob
def analyze_sentiment(tweet):
    analysis=TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'
    
         
    #Function to Pre-process data for Worlcloud
def prepCloud(Topic_text,Topic):
    Topic = str(Topic).lower()
    Topic=' '.join(re.sub('([^0-9A-Za-z \t])', ' ', Topic).split())
    Topic = re.split("\s+",str(Topic))
    stopwords = set(STOPWORDS)
    stopwords.update(Topic) ### Add our topic in Stopwords, so it doesnt appear in wordClous
    text_new = " ".join([txt for txt in Topic_text.split() if txt not in stopwords])
     
 
 #collect Input from User:
Topic=str()
Topic=str(st.text_input("Enter the topic you are intersted in (Press Enter once Done)"))

if len(Topic) > 0:
    

#call the function to extract the data.pass the topic and filename ypu want the data to be stored in.
 with st.spinner("Please wait,Tweets are being extracted"):
        get_tweets(Topic,Count=100)
        st.success('Tweets have been Extracted !!!')    
    
#  To get clean tweets

df['Tweet']=df['Tweet'].apply(cleanTxt)

##To get sentiments
df["Sentiment"]=df["Tweet"].apply(lambda x : analyze_sentiment(x))
#Write Summary of The Tweets
st.write("Total Tweets Extracted for Topic : {}".format(Topic,len(df['Tweet'])))
st.write("Total Positive Tweets are : {}".format(len(df[df["Sentiment"]=="Positive"])))
st.write("Total Negative Tweets are : {}".format(len(df[df["Sentiment"]=="Negative"])))
st.write("Total Neutral Tweets are : {}".format(len(df[df["Sentiment"]=="Neutral"])))


#see the Extracted Data
if st.button("See the Extracted Data"):
    st.success("Generating A Count Plot")
    st.write(df.head(50))
    
 #get Countplot
if st.button ("Get Count Plot for Different Sentiments"):
    st.success("Generating A count plot")
    st.subheader("Count plot for DIfferent Sentiments")
    st.write(sns.countplot(df["Sentiment"]))
    st.pyplot()
    
#piechart
if st.button("Get Pie Chart for Different Sentiments"):
    st.success("Generating A Pie Chart")
    a=len(df[df["Sentiment"]=="Positive"])
    b=len(df[df["Sentiment"]=="Negative"])
    c=len(df[df["Sentiment"]=="Neutral"])
    d=np.array([a,b,c])
    explode=(0.1,0.0,0.1)
    st.write( plt.pie(d,shadow=True,explode=explode,labels=["Positive","Negative","Neutral"],autopct='%1.2f%%'))
    st.pyplot()
    
#if st.button("Get WordCloud for all Positive Tweets about {}".format(Topic)):
    #st.success("Generating A wordCloud for all Positive Tweets about {}".format(Topic)) 
    #text_positive=" ".join(review for review in df[df["Sentiment"]=="Positive"].Tweet)
    #stopwords=set(STOPWORDS)
    #text_new_positive= prepCloud(text_positive,Topic)
    #wordcloud= WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_new_positive)
    #st.write(plt.imshow(wordcloud,interpolation='bilinear'))
    #st.pyplot()
      
             
    
 


    
    
    

    
st.sidebar.header("About App")
st.sidebar.info("A Twitter Sentiment analysis Project which will scrap twiiter for the topic select by the user.The extracted tweets will then be used to determine the sentiments of those tweets.The different visualization will help us get a feel of the overall mood of the people on Twitter regarding the topic we select.")
st.sidebar.text("Built with Streamlit")
st.sidebar.header("For any Quries/Suggection Please reach out at:")
st.sidebar.info("soumitramanna441@gmail.com")

    
    

    
