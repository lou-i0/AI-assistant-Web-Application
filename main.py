
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
# conv_bucket = oa.beta.threads.create()
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



# SECTION TWO - COMPLETE
#========================================================================================
#////////////////////////////////////////////////////////////////////////////////////////
#========================================================================================
# %% SECTION THREE - AI Assistant Class? 
#========================================================================================
#////////////////////////////////////////////////////////////////////////////////////////
#========================================================================================
# Create class to manage D.A.V.E
#=============================
class Dave:
    conv_id = None                                      # id for thread_id / Conversation Bucket
    assistant_id = None                                 # id for assistant created in open Ai Assistants

    def __init__(self, model:str = model):              # Create Constructor to set up the class
        self.oa = oa                                    # for Open AI connection with API Key
        self.model = "gpt-3.5-turbo"                    # the model to build the assistant with 
        self.assistant = None                           # The Assistant itself (D.A.V.E!)
        self.conv = None                                # The Thread / Conversation bucket to store messages in
        self.run  = None                                # The run in which to process the queries
        self.summary = None                             # The news feed we parse from News API

    # Retrieve existing IDS if assistant and thread has already been created.
    #----------------------------
    if Dave.assistant_id:
        self.assistant = self.oa.beta.assistants.retrieve(assistant_id = Dave.assistant_id)
    if Dave.conv_id:
        self.conv = self.oa.beta.threads.retrieve(thread_id = Dave.conv_id)

    # Method to Create AI assistant in Open AI if needed.
    #----------------------------
    def create_dave(self):
        if not self.assistant_id:                       # If assistant id is not found, create a new assistant
            dave_obj = self.oa.beta.assistants.create(
                                                        name = 'Dave'
                                                        ,instructions = '''You are Dave, a sassy and sarcastic butler, but excellent at data science and analytics. You know the best approaches to tackle data problems.\n
                                                                           No code problem phases you, and treated with grace and sassy sarcasm.'''
                                                        ,description = '''You are Dave, a sassy and sarcastic butler, but excellent at data science and analytics. You know the best approaches to tackle data problems.\n
                                                                          No code problem phases you, and treated with grace and sassy sarcasm.'''
                                                        ,tools = [{"type":"code_interpreter"}]
                                                        ,model = self.model
                                                     )
            Dave.assistant_id   = dave_obj.id           # Set new assistant id from what was created.
            self.assistant      = dave_obj              # Set the assistant to what was created.
            print(f"Assistant ID: {self.assistant.id}") # Show the assistant Id (for debugging).

    # Method to Create conversation bucket (thread) if needed.
    #----------------------------
    def create_conv_bucket(self):
        if not self.conv:                               # If no previous conversation bucket found, create one.
            conv_obj = self.oa.beta.threads.create()    # Create the conversation bucket.
            Dave.conv_id = conv_obj.id                  # Assign the conv_id based on the new conversation.
            self.conv = conv_obj                        # Set the conversation bucket to what was created.
            print(f"Conversation ID: {self.conv_id}")   # Show the conversation bucket ID (for debugging purposes).

    # Method to add query to conversation bucket, for D.A.V.E to answer.
    #----------------------------
    def ask_dave_something(self, role, content):
        if self.conv:
            self.oa.beta.threads.messages.create(
                                                    thread_id= self.conv.id
                                                    ,role = role
                                                    ,content = content
                                                )
            
    # Method to make D.A.V.E run and the query.
    #----------------------------
    def dave_process_query(self, instructions):
        if self.conv and self.assistant:
            self.run = self.oa.beta.threads.runs.create(
                                                            assistant_id    = self.assistant.id
                                                            ,thread_id      = self.conv.id
                                                            ,instructions   = instructions
                                                       )
            
    # Method to retrieve the query
    #----------------------------
    def dave_give_reponse(self):
        if self.conv:
            responses = self.oa.beta.threads.messages.list(thread_id = self.thread.id)

            summary = []

            last_response = responses.data[0]
            role = last_response.role
            response = last_response.content[0].text.value

            summary.append(response)
            self.summary = "\n".join(summary)

            print(f"D.A.V.E's Response: {role.capitalize()}:{response}")

    # Method to wait for D.A.V.E to finish
    #----------------------------
    def wait_for_dave(self):
        if self.conv and self.run:
            while True:
                tim.sleep(5)
                dave_run_get = self.oa.threads.runs.retrieve(
                                                                thread_id   = self.conv.id
                                                                ,run_id     = self.run.id
                                                            )
                
                print(f"How is D.A.V.E doing: {dave_run_get.model_dump_json(indent = 4)}")
                if dave_run_get.status == "completed":
                    self.dave_process_query
                    break
                elif dave_run_get.status =="requires_action":
                    print("Lets get the news!")
                    self.call_required_functions(self required)

                






# SECTION THREE - COMPLETE
#========================================================================================
#////////////////////////////////////////////////////////////////////////////////////////
#========================================================================================
    
#  %% create main and call, that the code will eventually use going forward.
def main():
    news = news_collect(topic = 'ChatGPT')
    print(news[0])
# %%
if __name__ =="__main__":
   main()

