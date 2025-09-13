# IMPORT LIBRARIES
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from random import sample,seed

# # PYSPARK
# import findspark
# findspark.init()

# import pyspark
# from pyspark import SparkContext
# from pyspark.sql import SparkSession
# SparkContext.setSystemProperty('spark.hadoop.dfs.client.use.datanode.hostname', 'true')

# sc = SparkContext(master="local", appName="New Spark Context")
# spark = SparkSession(sc)

# from pyspark.sql.functions import regexp_replace,col,explode
# from pyspark.ml.feature import StringIndexer
# from pyspark.ml.recommendation import ALS,ALSModel

# # PYSPARK
# import findspark
# findspark.init()

# from pyspark.sql import SparkSession
# from pyspark import SparkContext
# from pyspark.sql.functions import regexp_replace, col, explode
# from pyspark.ml.feature import StringIndexer
# from pyspark.ml.recommendation import ALS, ALSModel

# # Thiết lập property nếu cần
# SparkContext.setSystemProperty('spark.hadoop.dfs.client.use.datanode.hostname', 'true')

# # Khởi tạo SparkSession (tự động tạo SparkContext nếu chưa có)
# spark = SparkSession.builder \
#     .appName("New Spark Context") \
#     .master("local") \
#     .getOrCreate()

# # Lấy SparkContext từ SparkSession
# sc = spark.sparkContext





#FUNCTIONS

def readtxt(path):
    with open(path,encoding='utf-8',mode='r') as f:
        list_text=f.readlines()
    text=''.join(list_text)
    return text,list_text


def list_hotels(n):
    df_hotels=pd.read_csv('Hotels_final.csv')
    lst=list(df_hotels['Hotel_Name'].unique())
    seed(42)
    selected_lst=sample(lst,n)
    return selected_lst

def recommmendation_hotel_consine_similarity(ID):
    df_hotels=pd.read_csv('Hotels_final.csv')
    df_recommended_hotel=pd.read_csv('CONSINE_SIMILARITY.CSV',index_col='Unnamed: 0')
    top_6=df_recommended_hotel.drop(columns=ID).loc[ID].nlargest(8).index
    recommended_hotels=df_hotels[df_hotels['Hotel_ID'].isin(top_6)]
    return recommended_hotels



def query_hotels_ID(name):
    df_hotels=pd.read_csv('Hotels_final.csv')
    hotel_id=df_hotels[df_hotels['Hotel_Name']==name]['Hotel_ID'].values[0]
    return hotel_id

def hotels(ID):
    #Query hotel ID in 'Hotels_final.csv'
    df_hotels=pd.read_csv('Hotels_final.csv')
    hotel_information=df_hotels[df_hotels['Hotel_ID']==ID]
    # Overall information 
    name=hotel_information["Hotel_Name"].values[0] # Name of the hotel
    address=hotel_information["Hotel_Address"].values[0] # Address of the hotel
    start=hotel_information["Hotel_Rank"].values[0] # Star of the hotel
    description=hotel_information["Hotel_Description"].values[0] # Overall description of the hotel
    return (name,address,start,description,hotel_information)


def overall_information(ID):
    # RETURN OVERALL INFORMATION OF THE HOTEL
    name,address,start,description,hotel_information = hotels(ID)
    
    # VISUALIZATION
    list_numerical=hotel_information.drop(columns=['num','comments_count']).select_dtypes(include='number').columns #Select score categories
    # if the return dataframe is empty, visualization will be passed ,and vice versa. 
    if hotel_information[list_numerical].isnull().all(axis=1).values[0]:
        pass
    else:
        # Overall score of each category:
        plt.figure(figsize=(10,5))
        plt.title('AVERAGE SCORE BY CATEGORY FOR %s'%name.upper(),size=12,weight=600)
        for i,column in enumerate(list_numerical):
            score_category=hotel_information[column].values[0]
            plt.bar(x=i,height=score_category)
            plt.text(x=i,
                     y=score_category+0.1,
                     s=score_category)
        plt.ylabel('Score',size=10,weight=500)
        plt.ylim([0,12])
        plt.xlabel('Category',size=11,weight=500)
        plt.xticks(range(len(list_numerical)),list_numerical)
        plt.show()

def hotels_comments(ID):
    df_comments=pd.read_csv('Comments_final.csv')
    hotel_comments=df_comments[df_comments['Hotel ID']==ID]
    return hotel_comments,df_comments


def vistors_by_nationality(ID):
    hotel_comments,df_comments=hotels_comments(ID)
    name=hotels(ID)[0]
    
    # Nationality information
    nationality=hotel_comments['Nationality'].value_counts().to_frame()
    nationality['count']=nationality['Nationality']
    nationality.drop(columns=['Nationality'],inplace=True)
    nationality['Nationality']=nationality.index
    nationality.reset_index(drop=True,inplace=True)

    # The percentage of vistors
    percentage_value=round(100*nationality['count'].sum()/df_comments.shape[0],2)
    percentage=pd.DataFrame({'Vistors':[name,'Others'],
                             'Percentages':[percentage_value,100-percentage_value]})

    # Visualization
    plt.figure(figsize=(25,15),facecolor='lightgrey')
    #The percentage of vistors
    plt.subplot(2,2,1)
    patches,texts,autotexts=plt.pie(x=percentage['Percentages'],
                                    radius=0.9,
                                    autopct='%1.2f%%')
    plt.title(f'PERCENTAGE OF VISITORS TO {name.upper()}',size=12,weight=600)
    plt.legend(patches,
               percentage['Vistors'],
               loc='upper left',
               title='Hotels')
    # The number of vistors
    nationality.sort_values(by='count',ascending=True,inplace=True) # Sort values by 'count'
    # Visualization
    plt.subplot(2,2,2)
    plt.barh(data=nationality,
             y='Nationality',
             width='count',
             color='crimson')
    plt.title(f'NUMBER OF VISITORS TO {name.upper()} BY NATIONALITY',size=12,weight=600)
    plt.ylabel('Nationality',size=11,weight=500)
    plt.xlabel('Number of visitors',size=11,weight=500)
    plt.show()


def GroupName_RoomType(ID):
    hotel_comments=hotels_comments(ID)[0]
    name=hotels(ID)[0]

    # Group name
    Group_name=hotel_comments['Group Name'].value_counts().to_frame()
    Group_name['count']=Group_name['Group Name']
    Group_name.drop(columns='Group Name',inplace=True)
    Group_name['Group_name']=Group_name.index
    Group_name.reset_index(drop=True,inplace=True)

    # Room type
    Room_type=hotel_comments['Room Type'].value_counts().to_frame()
    Room_type['count']=Room_type['Room Type']
    Room_type.drop(columns=['Room Type'],inplace=True)
    Room_type['Room_Type']=Room_type.index
    Room_type.reset_index(drop=True,inplace=True)

    #VISUALIZATION
    plt.figure(figsize=(20,15),facecolor='Lightgrey')
    #Group name visualization
    Group_name.sort_values(by='count',ascending=True,inplace=True)
    plt.subplot(1,2,1)
    plt.barh(data=Group_name,
             y='Group_name',
             width='count',
             color='Lightgreen',
             edgecolor='dimgrey',
             height=0.9)
    plt.title('TYPE OF GUEST GROUPS IN %s' %name.upper(),size=12,weight=800)
    plt.ylabel('Group name',size=11,weight=600)
    plt.xlabel('Number of groups',size=11,weight=600)
    #Room type visualization
    Room_type.sort_values(by='count',ascending=True,inplace=True)
    plt.subplot(1,2,2)
    plt.barh(data=Room_type,
             y='Room_Type',
             width='count',
             color='Tomato',
             edgecolor='dimgrey',
             height=0.9)
    plt.title('TYPE OF ROOMS IN %s' %name.upper(),size=12,weight=800)
    plt.ylabel('Room types',size=11,weight=600)
    plt.xlabel('Number of rooms',size=11,weight=600)
    plt.tight_layout()
    plt.show()

def StayDetails(ID):
    hotel_comments=hotels_comments(ID)[0]
    name=hotels(ID)[0]

    # Dates
    Dates=hotel_comments['Date_of_stay'].value_counts().to_frame()
    Dates['count']=Dates['Date_of_stay']
    Dates.drop(columns=['Date_of_stay'],inplace=True)
    Dates['Date_of_stay']=Dates.index
    Dates['Date_of_stay']=pd.to_datetime(Dates.index,format='%m/%Y')
    Dates.reset_index(drop=True,inplace=True)

    #VISUALIZATION
    plt.figure(figsize=(15,5),facecolor='lightgrey')
    #Number of nights
    plt.subplot(1,2,1)
    sns.violinplot(hotel_comments[['Number_of_nights']])
    plt.title('NUMBER OF NIGHTS STAYED AT\n %s'%name.upper(),size=12,weight=600)
    plt.ylabel('Number of nights',size=11,weight=600)
    # Frequency of vistors across a period of times
    plt.subplot(1,2,2)
    sns.lineplot(data=Dates,
                 x='Date_of_stay',
                 y='count')
    plt.title('NUMBER OF VISITORS TO %s \nOVER A PERIOD OF TIMES' %name.upper(),size=12,weight=600)
    plt.ylabel('Number of visitors',size=11,weight=600)
    plt.xlabel('Years',size=11,weight=600)
    plt.tight_layout()
    plt.show()

def Score(ID):
    hotel_comments,df_comments=hotels_comments(ID)
    name=hotels(ID)[0]

    # AVERAGE SCORE OF EACH HOTEL
    average_score_each_hotels=df_comments.groupby('Hotel ID')[['Score']].mean()
    average_score_each_hotels['Hotel_ID']=average_score_each_hotels.index
    average_score_each_hotels.reset_index(drop=True,inplace=True)
    average_score=average_score_each_hotels['Score'].mean()

    # Scores level
    Scores_level=hotel_comments['Score Level'].value_counts().to_frame()
    Scores_level['count']=Scores_level['Score Level']
    Scores_level.drop(columns=['Score Level'],inplace=True)
    Scores_level['Score_level']=Scores_level.index
    Scores_level.reset_index(drop=True,inplace=True)

    
    #VISUALIZATION
    plt.figure(figsize=(16,14),facecolor='lightgrey')
    # Score
    plt.subplot(2,2,1)
    sns.violinplot(df_comments['Score'],color='orangered')
    plt.title('SCORE OF %s'%name.upper(),size=12,weight=600)
    plt.ylim([6,11])
    # Average Score
    plt.subplot(2,2,(3,4))
    sns.barplot(x=[0],
                y=[average_score],
                color='blueviolet',
                label='Average score')
    sns.scatterplot(x=[0]*len(average_score_each_hotels),
                    y=average_score_each_hotels['Score'],
                    color='hotpink',
                    label='Other hotels')
    sns.scatterplot(x=[0],
                    y=average_score_each_hotels[average_score_each_hotels['Hotel_ID']==ID]['Score'],
                    marker='*',
                    s=200,
                    label=name,
                    color='crimson',edgecolor='black')
    plt.legend(facecolor='lightgray')
    plt.title('COMPARISON BETWEEN MEAN SCORE OF %s \nAND OTHER HOTEL' %name.upper(),size=12,weight=600)
    plt.ylabel('')
    plt.ylim([6,11])
    #Score level
    plt.subplot(2,2,2)
    patches,texts,autotexts=plt.pie(x=Scores_level['count'],
                                    radius=0.9,
                                    autopct='%1.1f%%')
    plt.legend(patches,
               Scores_level['Score_level'],
               title='SCORE LEVEL',
               title_fontsize=9,
               fontsize=6,
               loc='upper right')
    plt.title(f'SCORE LEVEL OF\n {name.upper()}',size=12,weight=600)
    
    plt.tight_layout()
    plt.show()

def WordCloud_Hotels(ID):
    hotel_comments=hotels_comments(ID)[0]
    name=hotels(ID)[0]

    # Group by sentiment
    dict_words=dict()
    df_grouped_comments_by_sentiment=hotel_comments[~hotel_comments['Body'].isnull()].groupby('Sentiment').agg({'Body':'sum','Sentiment':'count'})
    if len(df_grouped_comments_by_sentiment)==2:
        dict_words['positive']=df_grouped_comments_by_sentiment.loc['positive','Body'] # String of positive words
        dict_words['negative']=df_grouped_comments_by_sentiment.loc['negative','Body'] # String of negative words
    else:
        dict_words[df_grouped_comments_by_sentiment.index[0]]=df_grouped_comments_by_sentiment.iloc[0,0]

    # Visualization
    # Wordcloud of postive words
    plt.figure(figsize=(14,12))
    if 'positive' in dict_words.keys():
        plt.subplot(2,2,1)
        wc=WordCloud(max_words=60,
                     background_color='black',
                     random_state=42,
                     colormap=plt.cm.autumn,
                     width=600,
                     height=400)
        wc.generate(dict_words.get('positive'))
        plt.imshow(wc,interpolation='bilinear')
        plt.title(f"POSITIVE COMMENTS'REVIEWERS ON \n{name.upper()}",size=12,weight=600)
        plt.axis('off')
        # Wordcloud of negative words
    if 'negative' in dict_words.keys():
        plt.subplot(2,2,3)
        wc=WordCloud(max_words=40,
                     background_color='black',
                     random_state=42,
                     max_font_size=100,
                     colormap=plt.cm.Blues,
                     width=600,
                     height=400)
        wc.generate(dict_words.get('negative'))
        plt.imshow(wc,interpolation='bilinear')
        plt.title(f"NEGATIVE COMMENTS'REVIEWERS ON \n{name.upper()}",size=12,weight=600)
        plt.axis('off')
    plt.subplot(2,2,(2,4))
    patches,texts,autotexts=plt.pie(x=df_grouped_comments_by_sentiment['Sentiment'],
                                    autopct='%1.2f%%',radius=0.9)
    plt.legend(patches,df_grouped_comments_by_sentiment.index,loc='lower right',title='Comments by sentiment')
    plt.title(f'A PERCENTAGE OF COMMENTS BY SENTIMENT ON\n{name.upper()}',size=11,weight=600)
    plt.tight_layout()
    plt.show()

# def Collaborative_filtering_recommender_system(Name,Nationality,n):
#     # READ HOTEL COMMENTS
#     df=spark.read.csv('Comments_final.csv',header=True,inferSchema=True)
#     df=df.select('Hotel ID', 'Reviewer_ID_new','Reviewer Name','Nationality' ,'Score')

#     # READ HOTEL INFORMATION
#     df_hotel=spark.read.csv('temp_hotel.csv',header=True,inferSchema=True)
#     df=df.join(df_hotel,df_hotel.Hotel_ID==df['Hotel ID'],how='inner')

#     # Define string indexer
#     index=StringIndexer(inputCols=['Hotel_ID','Reviewer_ID_new'],outputCols=['Hotel_ID_indexed','Reviewer_ID_new_indexed'])
#     # Build string indexer
#     indexer=index.fit(df)
#     df=indexer.transform(df)

#     # IMPORT MODEL
#     BestModel=ALSModel.load('Models/ALS_MODELS')

#     # RECOOMENDATION SYSTEM

#     # Find the index of natinality and name
#     nationality_index=df.select('Reviewer_ID_new','Reviewer_ID_new_indexed','Reviewer Name','Nationality').distinct()

#     # Find the index of hotel
#     Hotel_index=df.select('Hotel_ID','Hotel_ID_indexed','Hotel_Name').distinct()

#     target_nationality_index=nationality_index.filter(nationality_index['Reviewer Name'].isin(Name)).filter(nationality_index['Nationality'].isin(Nationality))

#     user_rec=BestModel.recommendForUserSubset(target_nationality_index.select('Reviewer_ID_new_indexed'),n)
#     user_rec=user_rec.select(user_rec.Reviewer_ID_new_indexed,explode(user_rec.recommendations))
    
#     user_rec=user_rec.withColumns({'Hotel_ID_indexed':user_rec.col.getField('Hotel_ID_indexed'),
#                                    'rating':user_rec.col.getField('rating')})


#     # Final result
#     final_recommendation=user_rec.select('Reviewer_ID_new_indexed',col('Hotel_ID_indexed').cast('double'))
#     final_recommendation=final_recommendation.join(target_nationality_index,on='Reviewer_ID_new_indexed',how='inner')
#     final_recommendation=final_recommendation.join(Hotel_index,on='Hotel_ID_indexed',how='left')
#     #final_recommendation.select('Nationality','Hotel_name').show()
#     recommended_hotels=final_recommendation.select('Reviewer Name','Nationality','Hotel_Name')
#     df=recommended_hotels.toPandas()


#     return df


