import pandas as pd
import mysql.connector
import logging
from sqlalchemy import create_engine


logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

#Loading CSV file into dataframe
try :
    dataFrame = pd.read_csv(r'C:\Users\20981\Desktop\Youtube2025Analysis\youtube_2025_dataset.csv')
    logging.info("Yotube 2025 dataset loaded sucessfully")
except FileNotFoundError :
    dataFrame  = pd.DataFrame()
    logging.error("File not found in the directory")

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
logging.info("Renamed columns for clarity")

#Removing duplicates
dataFrame = dataFrame.drop_duplicates(subset = ['channel_name', 'youtuber_name'], keep = 'last')
logging.info("Removed duplicates")

#Converting datatypes and Handling missing or null values
dataFrame['total_videos'] = pd.to_numeric(dataFrame['total_videos'], errors = 'coerce').fillna(0)
dataFrame['avg_video_length_min'] = pd.to_numeric(dataFrame['avg_video_length_min'], errors = 'coerce').fillna(dataFrame['avg_video_length_min'].mean())
dataFrame['total_subscribers'] = pd.to_numeric(dataFrame['total_subscribers'], errors = 'coerce').fillna(0)
dataFrame['members_count'] = pd.to_numeric(dataFrame['members_count'], errors = 'coerce').fillna(0)
dataFrame['ai_generated_content_percent'] = pd.to_numeric(dataFrame['ai_generated_content_percent'], errors = 'coerce').fillna(0)
dataFrame['quantom_computing_topics'] = pd.to_numeric(dataFrame['quantom_computing_topics'], errors = 'coerce').fillna(0)
dataFrame['engagement_score'] = pd.to_numeric(dataFrame['engagement_score'], errors = 'coerce').fillna(0)
dataFrame['content_value_index'] = pd.to_numeric(dataFrame['content_value_index'], errors = 'coerce').fillna(0)

#Handling missing or null values
dataFrame.dropna(subset = ['channel_name','youtuber_name','total_videos'], inplace = True)
logging.info("Converted datatypes and Handled missing or null values")

#Filtering irrelevant or noisy data
dataFrame = dataFrame[dataFrame['total_subscribers']>0]
dataFrame = dataFrame[(dataFrame['ai_generated_content_percent'] >= 0) & (dataFrame['ai_generated_content_percent'] <= 100)]
logging.info("Filtered irrelevant or noisy data")

#-------------------------------------------MySQL Integration--------------------------------------------

try :
    engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/youtube2025")
    dataFrame.to_sql(name = "videos", con = engine, if_exists = 'replace', index = False)
    logging.info("Dataset loaded into Database-youtube2025 table-videos ")
except Exception as e :
    logging.error("Failed to load dataset into mysql {e}")

#-------------------------------------Connection to MySql------------------------------------

try :
    con = mysql.connector.connect(host = "localhost", user = "root", password = "root", database = "youtube2025")
    logging.info("Connected to mysql database 'youtube2025' ")
    cursor = con.cursor()
except mysql.connector.Error as error :
    logging.error("Database connection error {error}")

menu = {
    "1" : ("Total number of videos", "SELECT SUM(total_videos) FROM videos"),
    "2" : ("Video length (minutes) analysis", "select max(avg_video_length_min) as Maximum,round(avg(avg_video_length_min),3) as Average,min(avg_video_length_min) as Minimum from videos"),
    "3" : ("AI content analysis","select max(ai_generated_content_percent) as Maximum,round(avg(ai_generated_content_percent),3) as Average,min(ai_generated_content_percent) as Minimum from videos"),
    "4" : ("Engagement score analysis","select max(engagement_score) as Maximum,round(avg(engagement_score),3) as Average,min(engagement_score) as Minimum from videos;"),
    "5" : ("Neural interface compatability analysis","select neural_interface_compatible,count(*) as no_of_channels from videos group by neural_interface_compatible"),
    "6" : ("Holographics analysis","select holographic_content_rating,count(*) as no_of_channels from videos group by holographic_content_rating order by holographic_content_rating"),
    "7" : ("Metaverse integration analysis","select metaverse_integration_level,count(*) as Value from videos group by metaverse_integration_level order by metaverse_integration_level"),
    "8" : ("Top 5 performing channels","select channel_name,best_video,engagement_score,content_value_index from videos order by engagement_score desc limit 10"),
    "9" : ("Top 10 high content and low volume channels","select channel_name,youtuber_name from videos order by content_value_index desc, total_videos asc limit 10"),
    "10" : ("Get all details for a specific channel","")
}

while True:
    print("\nSelect an analysis option:")

    for key,(msg,_) in menu.items():
        print(f"{key}. {msg}")
    print("0. Exit analysis")

    choice = input("Enter your choice : ")

    if choice == "0" :
        logging.info("User exited the analysis...!!!")
        print("Exiting analysis")
        break
    elif choice in menu :
        msg,query = menu[choice]

        if choice == "10" :
            channel_name = input("Enter channel name : ")
            logging.info(f"User requested for {channel_name} data")
            query = "select * from videos where channel_name = %s"
            try : 
                cursor.execute(query,(channel_name,))
                results = cursor.fetchall()
                columns = [col[0] for col in cursor.description]

                if results :
                    print(f"Details for channel {channel_name} :")
                    for row in results :
                        for col,val in zip(columns,row):
                            print(f"{col} : {val}")
                else : 
                    logging.warning(f"No data found for channel {channel_name}")
                    print("No data found for that channel")
            
            
            except Exception as e :
                logging.error(f"Query execution failed for channel search: {e}")
                print(e)
                print("Something went wrong while fetching channel details")
        
        else :
            logging.info(f"Executing query for {msg}")
            
            try :
                cursor.execute(query)
                results = cursor.fetchall()
                print(msg)

                for row in results :
                    print(row)

            except Exception as e :
                logging.error(f"query execution failed {e}")
    else:
        logging.warning(f"User entered invalid choice: {choice}")

