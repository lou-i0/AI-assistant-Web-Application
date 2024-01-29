
# %%============================= 
# 1 -  Import relevant libraries
#-----------------------------
from openai import OpenAI                   # For using openai tools.
import os                                   # Operating system operations.
import time as tim                          # Tracking and formatting time
# from datetime import datetime as dti      # Datetime manipulation
import datetime as dti
import requests as req                      # API https retrieval
import json                                 # Parsing of Javascript Object Notation files
import pandas as pd                         # Data analysis and manipulation.           
#=============================

#%%======================================================================================
#SECTION  ONE - AI Assistant
#========================================================================================
#////////////////////////////////////////////////////////////////////////////////////////
#========================================================================================
# 2 - Set up Open AI client connection and model to use 
#-----------------------------
oa    = OpenAI(api_key = os.environ.get("OA-ASSIS-API_KEY"))
model = "gpt-3.5-turbo"                     # Select which open ai model to use for the AI Assistant.
# =============================
# 3 - Set up condition that either uses hardcoded values, for the assistant
#     and conversation bucket, created previously, and will be used in future.
#-----------------------------
# Hard code assistant id as the assistant is already created.
#.............................
dave_assis_id = "asst_lUDxxW2xLQuB4aHZFBFvaIlG"

# # Create the assistant and get the id
# #.............................
# dave_assis = oa.beta.assistants.create( model = model, name = "Dave",tools=[{"type":"code_interpreter"}]
#                                         ,instructions   = """You are Dave, a sassy and sarcastic butler, but excellent at data science and analytics. You know best approaches to tackle data problems.\n No code problem phases you, and treated with grace and sassy sarcasm."""
#                                        )
# dave_assis_id = dave_assis.id
# print(f"Assistant ID: {dave_assis_id}")


# Hardcoded thread_id from previous interaction 
#.............................
conv_id = "thread_8HGtjo0oJzYVLHvKw6ZOZUbj"
# Create new thread (conversation bucket) and its id
#.............................
# conv_bucket = oa.beta.threads.create(messages =[{"role": "user","content" : "Can you explain what a normal distribution is in simple terms please?"}])
# conv_id = conv_bucket.id
# print(f"Conversation Bucket: {conv_id}")

# ============================
# 4 - Create New Message for saved conversation bucket (thread)
#----------------------------
msg = input("Please enter your message for D.A.V.E here:")
message = oa.beta.threads.messages.create(thread_id = conv_id, role = "user", content = msg)

# ============================
# 5 - Run assistant, with created conversation, and process the response
dave_run = oa.beta.threads.runs.create(thread_id = conv_id, assistant_id = dave_assis_id
                                       , instructions="Please address the user as a Human")
# ============================
# 6 - Function process message input into conversation bucket, get D.A.V.E
#     to provide response, including how long it took.
#----------------------------
def wait_for_completion(client, thread_id, run_id, sleep_interval = 5):
    '''
    param client        : refers to the open ai connection we have created
    param thread_id     : id of the conversation bucket / thread active
    param run_id        : the id of the run
    param sleep_interval: Time in seconds to wait between checks
    '''
    # counter providing feedback whilst waiting 
    #.............................
    i = 0
    while True:
        try:
            dave_run_get = client.beta.threads.runs.retrieve(thread_id =thread_id, run_id = run_id)
            if dave_run_get.completed_at:
                formatted_elapsed_time = tim.strftime("%H:%M:%S",tim.gmtime(dave_run_get.completed_at - dave_run_get.created_at))
                print(f"D.A.V.E completed in {formatted_elapsed_time}")

                # get messages when run completes
                #.............................
                last_response       = client.beta.threads.messages.list(thread_id = thread_id).data[0].content[0].text.value
                print(f"D.A.V.E's response is : {last_response}")
                break
            
        except Exception as e:
            print(f"An error occurred whilst D.A.V.E was trying to formulate: {e}")
            break
        
        print(f"Waiting for D.A.V.E to finish, {i} seconds passed.")
        i += sleep_interval
        tim.sleep(sleep_interval)

# ============================
# 7 - Call function above to effectively use query and get the response from D.A.V.E
#----------------------------
wait_for_completion(client = oa, thread_id = conv_id, run_id= dave_run.id)
#========================================================================================
#SECTION  ONE COMPLETE- FOR NOW 
#========================================================================================
#////////////////////////////////////////////////////////////////////////////////////////
#========================================================================================

# %%============================
# SECTION TWO - NEWS FEED.
#========================================================================================
#////////////////////////////////////////////////////////////////////////////////////////
#========================================================================================
# 8 - Get news api key ( will tidy this up later )
#----------------------------
news_api_key = os.environ.get("NEWS_API_KEY")

#function to get news from news api based on topic provided.
def news_collect(topic, from_date = '2024-01-28',to_date ='2024-01-28'):

    from_date = (dti.datetime.today() - dti.timedelta(days= 1)).strftime("%Y-%m-%d")
    to_date   = (dti.datetime.today() - dti.timedelta(days= 1)).strftime("%Y-%m-%d")

    # topic = "ChatGPT"
    url = (f'https://newsapi.org/v2/everything?q={topic}&from={from_date}&to={to_date}&sortBy=popularity&apiKey={news_api_key}&pageSize=5')

    try:
        api_call = req.get(url = url)                                               # Perform API Call

        if api_call.status_code == 200:                                             # If successful, retrieve and convert json data into string format
            news_payload = json.dumps(obj = api_call.json(), indent = 4)
            news_raw = json.loads(news_payload)                                     # Separate instance ready for further use

            # Access relevant fields from news_raw
            #.............................
            status = news_raw['status']
            total_results = news_raw['totalResults']
            articles = news_raw['articles']
            news_final = []

            # Loop through articles to get relevant information
            #.............................
            for article in articles:
                source_name = article['source']['name']
                author = article['author']
                title = article['title']
                article_url = article['url']

                news_article = f"""
                                    Title: {title}
                                    ,Author: {author}
                                    ,Source: {source_name}
                                    ,URL: {article_url}
                                    
                                """
                news_final.append(news_article)
            return news_final
        else:                                                                       # If unsuccessful, raise and issue with the call.
            return []
        
    except req.exceptions.RequestException as e:
        print(f"Issue found with API request: {e}")

#  create main and call, that the code will eventually use going forward.
def main():
    news = news_collect(topic = 'ChatGPT')
    print(news[0])

# SECTION TWO - COMPLETE
#========================================================================================
#////////////////////////////////////////////////////////////////////////////////////////
#========================================================================================
# %% SECTION Three - AI Assistant Class? 
#========================================================================================
#////////////////////////////////////////////////////////////////////////////////////////
#========================================================================================
    
# %%
if __name__ =="__main__":
   main()

