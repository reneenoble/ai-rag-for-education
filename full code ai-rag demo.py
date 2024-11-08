import os                       # This is used to access the environment variables
from dotenv import load_dotenv  # This is used to load the .env file
from openai import OpenAI       # This is used to connect to the AI model

###############################################################################################################################
###                                                                                                                         ###         
###                                                Accessing your AI model                                                  ###
###                                                ~~~~~~~~~~~~~~~~~~~~~~~                                                  ###
###                                                                                                                         ###     
### We will be using GitHub Models to get access to an AI Model. **You will need to have a GitHub account and sign in.**    ###
###                                                                                                                         ###
### You'll need to get a GitHub Perosnal Access Token (PAT), you can follow these steps:                                    ###
### 1. Got to this link https://github.com/settings/tokens                                                                  ###
### 2. Click on the "Generate new token" drop down in the top right corner                                                  ###
### 3. Select "Generate New Toekn (Classic)"                                                                                ###
### 4. Sign in to confrim your identity                                                                                     ###
### 5. Add a Note at the top of like "Access GitHub Models"                                                                 ###
### 6. Set the expiration to be long enough for the duration of your project.                                               ###
###    (Don't set it longer than you need it though for improved security)                                                  ###  
### 7. You don't need to tick ANY of the tick boxes. Skip them all.                                                         ###
### 8. Click the green "Generate token" button.                                                                             ###
### 9. Copy the token that has just been generated! (It's in the area with the light green background).                     ###
###    You won't be able to see the token again, so don't leave the page until you have copied it.                          ###
### 10. Paste your token into the file in this project called `.env` in the spot provided.                                  ###    
###                                                                                                                         ### 
### You are now ready to code with GitHub AI models!                                                                        ###
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

# This code conatins the function that will return the search summary for a given question
# It also has the data on the stop words that we will use to remove from the question

# Stop words aren't useful for searching, so we'll remove them from the question
STOP_WORDS = set([
"a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", 
"into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", 
"their", "then", "there", "these", "they", "this", "to", "was", "will", "with"
])


def get_search_summary(question):
    """
    This function takes a question as input and returns a summary of the top 3 search results from the pet_products.txt file.
    It uses the keywords in the question to search for relevant products, removing stop words from the question.
    """
    all_keywords = set([word.lower() for word in question.split(" ")])
    # Remove stop words from the question
    keywords = all_keywords - STOP_WORDS
    
    # We'll score the scores based on the number of keywords in the line
    # eg: {"large dog bed": 2, "dog bed": 1}
    scores = {}
      
    # Open the file and read each line
    with open("pet_products.txt", "r") as f:
        for line in f:
            line = line.strip()
            # Make a list of numbers for each word in the line, 1 if the word is a keyword, 0 if not
            wordhits = [1 if word in line.lower() else 0 for word in keywords]
            # Add up the scores for the line
            line_score = sum(wordhits)
            # Only record the score if it's greater than 0
            if line_score > 0:
                scores[line] = line_score
            
    # Sort the scores, biggest to smallest, and get the top 3
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    search_summmary = [k for k, v in sorted_scores[:(min(3, len(sorted_scores)))]]
    # Join the 3 products together into 1 stirng to return.
    search_summmary = ", ".join(search_summmary)
    return search_summmary


###############################################################################################
###   The main code that will run the chatbot, using the functions we have defined above.   ###
###############################################################################################

# Call the connect_ai() function to connect to the AI model
ai_client = connect_ai()
print("You're connected to the AI model!")
print("You can now start using the client variable to interact with the AI model.")


# Use conversation completion to generate a response to a message
# Set the system message to be the first message in the conversation, this is a prompt to the AI model itself that tells it what it's purpose is and how you want it to sound.
SYSTEM_MESSAGE = "You are a helpful assistant that can answer questions about anything. You are knowledgeable and friendly. You always use the sources provided and always promote our pet shop called 'Pet Paradise'."

# This is the main loop that will keep the chatbot running
while True:
    # Get the user's message
    # What does the user want to know?
    user_question = input("How can I help you today? ")
    print()

    data = get_search_summary(user_question)

    # Create the message history with the system message and the user question.
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
    ]

    # Add the user question to the message history
    messages.append({"role": "user", "content": user_question + "sources: " + data})


    # Generate the next message in the conversation to get an answer. 
    # We have set the model name for you, as well as the temperature and n values. The temperature value controls the randomness of the response. 
    response = ai_client.chat.completions.create(model="gpt-4o-mini",temperature=0.7,n=1,messages=messages)
    answer = response.choices[0].message.content # The answer comes with some other data, we unpack the answre here.
    print(answer)
    print()
    messages.append({"role": "system", "content": answer + "sources: " + data})