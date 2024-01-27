
# %%============================= 
# 0 -  Import relevant libraries
#-----------------------------
from openai import OpenAI                   # for using openai tools.
from dotenv import find_dotenv, load_dotenv # retrieve .env variables.
import os                                   # Operating system operations.
import time as tim                          # tracking and formatting time
from datetime import datetime as dti        # datetime manipulation
#=============================

# %%=============================
# 1 - Set up Open AI client connection and model to use 
#-----------------------------
oa    = OpenAI(api_key = os.environ.get("OA-ASSIS-API_KEY"))
model = "gpt-3.5-turbo"                     # Select which open ai model to use for the AI Assistant.
#=============================

# %%=============================
# 2 - Set up condition that either uses hardcoded values, for the assistant
#     and conversation bucket, created previously, and will be used in future.
#-----------------------------
# Hard code assistant id as the assistant is already created.
#.............................
dave_assis_id = "asst_01ZQe75ahNihrJU9mTuTAje1"

# Hardcoded thread_id from previous interaction 
#.............................
conv_id = "thread_u3aglkR6O1ImOP0HnuIUOeKk"
#=============================

# %%============================
# 3 - Create New Message for saved conversation bucket (thread)
#----------------------------
msg = "What is big data?"
message = oa.beta.threads.messages.create(thread_id = conv_id, role = "user", content = msg)
#============================

# %%============================
# 4 - Run assistant, with created conversation, and process the response
dave_run = oa.beta.threads.runs.create(thread_id = conv_id, assistant_id = dave_assis_id
                                       , instructions="Please address the user as a Human")
#============================
# %%============================
# 5 - Function process message input into conversation bucket, get D.A.V.E
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
#============================
# %%============================
# 6 - Call function above to effectively use query and get the response from D.A.V.E
#----------------------------
wait_for_completion(client = oa, thread_id = conv_id, run_id= dave_run.id)
#============================





# %% THIS STUFF LEFT HERE TO CREATE assitant and thread when needed
#========================================================================================
# Create the Assistant and thread 
#----------------------------
# Create the assistant first 
#----------------------------
# dave_assis = oa.beta.assistants.create(     # Create Assistant to use
#                                     model           = model
#                                     ,name           = "Dave"
#                                     ,instructions   = """You are Dave, a witty and sassy butler who is sarcastic, but excellent at data science and analytics. You know the best approach to tackle a data problem.\n No code problem phases you, and treat every problem with grace, decorum, and snooty sassy sarcasm."""
#                                     ,tools=[{"type":"code_interpreter"}]
                                   
#                                  )

# get id of the assistant created.
#-----------------------------
# dave_assis_id = dave_assis.id
#============================

# Create new thread (conversation bucket)
#----------------------------
# conv_bucket = oa.beta.threads.create(
#                                       messages =
#                                       [{"role": "user"
#                                         ,"content" : "Can you explain what a normal distribution is in simple terms please?"}]
#                                     )
# Get the thread id from above 
#-----------------------------
# conv_id = conv_bucket.id
#========================================================================================