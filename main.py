import os
import pandas as pd
import sqlalchemy as db
from googleapiclient.discovery import build


# This function hides my secret YouTube api key using the os module.
def my_api_key():
    """Returns my secret environmental api key"""
    api_key = os.environ.get('API_KEY')
    return api_key


# This function uses the user id to give a response as the statistics of that particular user's YouTube
def req_response(user_id):
    """Takes in the users youtube id, makes a request and returns a response"""
    youtube = build('youtube', 'v3', developerKey=my_api_key())
    # makes a request using the users_id in order to obtain statistics
    request = youtube.channels().list(
        part='statistics',
        id=user_id
    )

    my_response = request.execute()
    return my_response


# This function deals with converting the response from a dictionary to a dataframe
def my_dataframe(response):
    """ chooses vital information from the response, adds it to a list and returns a dataframe"""
    response = response['items'][0]['statistics']
    my_list = [response]
    df = pd.DataFrame(my_list)
    return df


# This function works with converting the response from a dataframe to a database
def df_to_db():
    """converts the dataframe to a sqlalchemy"""
    # line below creates an engine object
    engine = db.create_engine('sqlite:///youtube_channels.db')
    # line below creates and sends SQLtable from the dataframe
    my_dataframe(answer).to_sql('channel_statistics', con=engine, if_exists='replace', index=False)
    # writes a query
    query_result = engine.execute("SELECT * FROM channel_statistics;").fetchall()
    # returns a query_result as a database
    return pd.DataFrame(query_result)


# Takes the users YouTube id in order to generate a repose for them
user = "UC-6OweszSfFnDCq3F_Dw67w"  # input("Enter your youtube id: ")
answer = req_response(user)
my_dataframe(answer)
print(df_to_db())