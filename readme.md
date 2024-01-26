# Web Application with Open AI's AI Assistant - WAOA

## Introduction
The Idea of this (WAOA) was to learn a few things:

- How to create a web application using the python library - streamlit.
- Additionally, how to use a AI assistant API from open AI; and understand how that works within the Web application.

This work conducted here will go toward my understanding of a way to create a web app. Furthermore, the use of the ai assistant will provide a predicate into how a llm can be used, created and applied into a useful scenario - to help me learn for future work.

The Assistant API has benefits such a level of abstraction from an llm , but keeping conversation context, and adding more data to enrich the knowledge base. Additionally, it will be able to access multiple tools ion parallel to do stuff. There is some more info here that explains more in a visual format:
![Benefits](assis_api_benefits.png)

the assistant API can be set up with a defined characteristic and capabilities and more in comparison to the chat completions api as shown in the below screenshot:
![Assisant API vs Completions API](assis_vs_completion_api_comparison.png)

## Table of Contents

1. [Getting Started](#getting-started)

## Pre-requisites before creating the web application/ assistant.
1. Api Key Creation: 
    1. Go to [OpenAI](https://openai.com/)
    2. Log in to your account (or create one!)
    3. Click on API on the right hand side 
    4. This will bring you to the main api page. From there, click on API keys (that is a little lock icon on the left hand side).
2. Set up Billing:
to proceed in this exercise I had to add payment details and pay an amount i was comfortable with in order to use the functionalities in open AI. for testing purposes and later infrequent use, the prices are pretty reasonsable and even more so on the older llm models you can adopt. To set up billing, go the [billing settings](https://platform.openai.com/account/billing/overview), add a payment method, and add an amount to begin. 

## Steps Taken
1. [How to build the Assistant API](#how-to-build-the-assistant-api)


### How to build the Assistant API
#### Context 
Please see below screenshot to illustrate the steps needed to build the assistants API from open AI into my web application:
![assis_Api_building blocks](assis_api_building_blocks.png)

It consists of 4 main building blocks:
1. Assistant - the entity or thing that will be built then use to get information.
2. Thread -  All messages between Assistant and user get tracked. Think of it as a conversation bucket where all you messages go to in a session :).
3. Message(s) - the inputs outputs conversation between the Assistant and the user.
3. Run Entity - which makes the process and returns to the Assistant with information. Need a few things set up to run relevant queries received:
    1. Needs access to the Assistant -  potentially shows as an ID?
    2. Reference to the thread where the relevant messages are.
    3. Triggered to run steps based on context/decisions.

#### Creating the AI Assistant in open AI playgound.
Now I have the context understood as what needs to be done to create the AI Assistant, it is time to put the plan to action. Therefore I went back into the OpenAI API page [OpenAI Developer Platform](https://platform.openai.com/docs/overview) to go and create an assistant by clicking the robot icon to the right of the screen. From there I cam e across a screen similar to the below:
![assis_page](dave_assis1.png)
Where I went and created an assistant called Dave; a sassy butler, to help me with all my data analysis needs and wants!

From there I decided to go an test the assistant before going any further, by clicking on the 'Test' button at the right top right of the assistant selected screen.
![Dave Testing](assis_testing.png)
Which brings you to a playground to test how Dave is working. To my amazement, it is performing ( intially at least) how I like it to be :). You can see the assistant configuration on the left, the testing area in the middle, and the requests made as part of the queries on the right.

#### Creating the assistant in code form
Now we have tested the art of the possible to create an AI assistant in the Open AI playground, I am now going to replicate this same lovely data butler in code form. In such a case I plan to create this all in python via VS code. to continue.


## Glossary
 Left a list below of key terms, in case it helps:
 - AI - Artificial Intelligence
 - LLM - Large Language Model
 - Assistants API -  A tool for developers from open ai platform to craft powerful AI assistants to do a an array of tasks.


 I would like to thank the folks at freecode camp for the inspiration behind this exercise, with the following tutorial to help me learn this area :
 [OpenAI Assistants API tutorial](https://www.youtube.com/watch?v=qHPonmSX4Ms)


