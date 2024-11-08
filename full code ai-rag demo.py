import os
from dotenv import load_dotenv
from openai import OpenAI


###############################################################################################################################
###                                                                                                                         ###         
###                                                Accessing your AI model                                                  ###
###                                                ~~~~~~~~~~~~~~~~~~~~~~~                                                  ###
###                                                                                                                         ###     
### To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.         ###
### Create your PAT token by following instructions here:                                                                   ###
### https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens     ###
###                                                                                                                         ###
### We'll store the PAT in a .env file so that it is not exposed in the code.                                               ###
### You shoud never commit your keys and secrets to a public repository.                                                    ###
###                                                                                                                         ###     
###                                                                                                                         ###     
###############################################################################################################################



def connect_ai():
    # Load the .env file where the GITHUB_TOKEN is stored
    load_dotenv()
    # Get the GITHUB_TOKEN from the .env file
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    # Create a client that is connects to the AI model you selected using the GITHUB_TOKEN
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=GITHUB_TOKEN,
    )

    return client

# Call the connect_ai() function to connect to the AI model
ai_client = connect_ai()

while True:

    # Make a request to the AI model and provide some previous messages and the model you want to use
    response = ai_client.chat.completions.create(

        # When we prompt the model we are asking it "what comes next?" based on the previous messages.
        # We provide the previous conversation (it doesn't have to have actually happened) and the model will generate a response that should come next.
        # The "System" is the AI model that we are using to generate the response. The "User" is the person who is asking the question.
        # If you are starting a real converstaion with a user, you usually provide the first message as the "System" and tell the AI what it's purpose is and how you want it to sound.
        messages=[
            {
                "role": "system",
                "content": "you are a helpful chatbot that always provides answers from the sources provided.",
            },
            {
                "role": "user",
                "content": "What is the best dessert? Give me a recipe, make sure there are no lemons, I'm alergic. sources: the best dessert is well known to be lemon mirangue pie. chcolate cake is the second best dessert, according to a survey of 1000 people in kenya. Other disagree and say it is ice cream, but that is unsubstantiated.",
            }
        ],
        model="gpt-4o-mini", # This is the type of model you want to use, like we set up on GitHub models
        temperature=.5, # Temperature is a hyperparameter that controls the randomness of the model. Lower values make the model more deterministic and higher values make the model more random. (max 1, min 0)
        max_tokens=4096, # The response length from the model in tokens (default 2048) won't be longer than this. A token is a word, part of a longer word, or a symbol or number.
        top_p=1 # Top p is how much of the data you want to sample from. It's a way to make the model less repetitive and more creative. higher values make the model more random. (max 1, min 0)
    )

   
    # Print the response from the AI model
    print(response.choices[0].message.content)
