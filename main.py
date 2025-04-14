import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

#Loading CSV file into dataframe
try :
    dataFrame = pd.read_csv(r'C:\Users\20981\Desktop\Youtube2025Analysis\youtube_2025_dataset.csv')
    print('Yotube 2025 dataset loaded sucessfully')
except FileNotFoundError :
    dataFrame  = pd.DataFrame()
    print('File not found in the directory')

#--------------------------------Data Cleaning & Sanitization-----------------------

#Renaming columns for clarity
dataFrame.columns = [
    'channel_name',
    'youtuber_name',
    'total_videos',
    'best_video',
    'avg_video_length_min',
    'total_subscribers',
    'members_count',
    'ai_generated_content_percent',
    'neural_interface_compatible',
    'metaverse_integration_level',
    'quantom_computing_topics',
    'holographic_content_rating',
    'engagement_score',
    'content_value_index'
]

#Removing duplicates
dataFrame = dataFrame.drop_duplicates(subset = ['channel_name', 'youtuber_name'], keep = 'last')

#Converting datatypes and Handling missing or null values
dataFrame['total_videos'] = pd.to_numeric(dataFrame['total_videos'], errors = 'coerce').fillna(0)
dataFrame['avg_video_length_min'] = pd.to_numeric(dataFrame['avg_video_length_min'], errors = 'coerce').fillna(dataFrame['avg_video_length_min'].mean())
dataFrame['total_subscribers'] = pd.to_numeric(dataFrame['total_subscribers'], errors = 'coerce').fillna(0)
dataFrame['members_count'] = pd.to_numeric(dataFrame['members_count'], errors = 'coerce').fillna(0)
dataFrame['ai_generated_content_percent'] = pd.to_numeric(dataFrame['ai_generated_content_percent'], errors = 'coerce').fillna(0)
dataFrame['metaverse_integration_level'] = pd.to_numeric(dataFrame['metaverse_integration_level'], errors = 'coerce').fillna(0)
dataFrame['quantom_computing_topics'] = pd.to_numeric(dataFrame['quantom_computing_topics'], errors = 'coerce').fillna(0)
dataFrame['holographic_content_rating'] = pd.to_numeric(dataFrame['holographic_content_rating'], errors = 'coerce').fillna(0)
dataFrame['engagement_score'] = pd.to_numeric(dataFrame['engagement_score'], errors = 'coerce').fillna(0)
dataFrame['content_value_index'] = pd.to_numeric(dataFrame['content_value_index'], errors = 'coerce').fillna(0)

#Handling missing or null values
dataFrame.dropna(subset = ['channel_name','youtuber_name','total_videos'], inplace = True)

#Filtering irrelevant or noisy data
dataFrame = dataFrame[dataFrame['total_subscribers']>0]
dataFrame = dataFrame[(dataFrame['ai_generated_content_percent'] >= 0) & (dataFrame['ai_generated_content_percent'] <= 100)]

#-------------------------------------------MySQL Integration--------------------------------------------

engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/youtube2025")
dataFrame.to_sql(name = "videos", con = engine, if_exists = 'replace', index = False)
print("Dataframe migrated to mysql")

#-------------------------------------------------------------------------
con = mysql.connector.connect(host = "localhost", user = "root", password = "root", database = "youtube2025")
cursor = con.cursor()
res = cursor.execute()