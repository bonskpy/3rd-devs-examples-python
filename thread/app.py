import logging
import os
from OpenAIService import OpenAIService
from dotenv import load_dotenv

def generate_summary_prompt(user_message: str, assistant_response: str, previous_summary: str = "This is our first conversation!") -> list:
    """
    Generate a summary of the conversation.

    Variables:
    user_message (str): The user's input
    assistant_response (str): The AI generated response.
    previous_summary (str): The current summary of the conversation.

    Returns:
    list: A list of two dictionaries containing the system and user prompts.
    """
    summary_prompt = [{
        "role": "system", 
        "content": "Please provide a concise summary of the entire conversation. Focus only on the key points discussed. Make sure to capture relevant information. Do not include the full previous summary - instead, incorporate its information into a new, unified summary."
        },
        {
        "role": "user", 
        "content": f"""Please create/update our conversation summary.
             Previous_summary: {previous_summary}

             Last exchange:
             User: {user_message} 
             Assistant: {assistant_response}"""
        }
    ]

    return summary_prompt

def create_system_prompt(previous_summary: str) -> dict:
    """
    Create a system prompt for the AI.
    
    Variables:
    previous_summary (str): The current summary of the conversation.

    Returns:
    dict: A dictionary containing the system prompt.
    """
    system_prompt = {
        "role": "system", 
        "content": f"Dear Robot, you a helpful assistant who speaks using as few words as possible. Being consice is key. Here is a summary of the conversation so far: <conversation_summary>{previous_summary}</conversation_summary>"
        }
    
    return system_prompt

def create_user_prompt(user_message: str) -> dict:

    user_prompt = {
        "role": "user",
        "content": user_message
    }

    return user_prompt

def load_env_variables():
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=dotenv_path)

def main():
    """
    Main function to run the conversation.
    """

    logging.basicConfig(filename=f'{os.path.dirname(__file__)}/conversation.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    load_env_variables()
    openai = OpenAIService()

    previous_summary = "We have just started our conversation!"

    while True:

        system_prompt = create_system_prompt(previous_summary)
        user_input = input("You: >>> ")
        logging.info(f'User input: {user_input}')
        user_prompt = create_user_prompt(user_input)

        messages=[system_prompt, user_prompt]
        
        assistant_response = openai.completion(messages)
        logging.info(f'Assistant response: {assistant_response}')

        logging.info('-' * 50)
        logging.info('Updating conversation summary...')

        summarise_messages = generate_summary_prompt(user_input, assistant_response, previous_summary)
        previous_summary = openai.completion(summarise_messages)

        logging.info('CONVERSATION SUMMARY:')
        logging.info(previous_summary)
        logging.info('-' * 50)
        
        print("Robot: >>>", assistant_response)

if __name__ == "__main__":
    main()
