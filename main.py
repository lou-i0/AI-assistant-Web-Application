# %% Import relevant libraries
#=============================
from openai import OpenAI                   # for using openai tools.
from dotenv import find_dotenv, load_dotenv # retrieve .env variables.
import os                                   # Operating system operations.
#=============================
# %%
# Set up Open AI client connection
#-----------------------------
oa = OpenAI(api_key = os.environ.get("OA-ASSIS-API_KEY"))
#-----------------------------
# %%
#============================
# Create the Assistant
#----------------------------
model = "gpt-3.5-turbo"                     # Select which open ai model to use for the AI Assistant.

dave_assis = oa.beta.assistants.create(     # Create Assistant to use
                                    model           = model
                                    ,name           = "Dave"
                                    ,instructions   = """
                                                        You are Dave, a witty butler who is sarcastic, but also excellent at data analysis and knows the best approach to tackle a data problem.\n 
                                                        No code problem phases you, and whether you have seen a similar data problem before or not you treat every new problem with grace, decorum, and snooty sarcasm.
                                                      """
                                    ,tools=[{"type":"code_interpreter"}]
                                    
                                 )

# %%
# get id of the assistant created.
#-----------------------------
dave_assis_id = dave_assis.id
# print(dave_assis.id)
#============================

# %% 
#============================
# Create new thread (conversation bucket)
conv_bucket = oa.beta.threads.create(
                                      messages=
                                      [
                                          
                                      ]
                                    )