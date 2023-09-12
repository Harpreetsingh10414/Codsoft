import re
import time

class RuleBasedChatbot:
    def __init__(self):
        self.rules = {
            "hello": "Hello! How can I assist you, {}?",
            "how are you": "I am good thanks for asking how are you my friend, {}!",
            "bye": "Goodbye, {}! Have a great day!",
            "what's your name": "My name is BuddyBot, {}.",
            "what is the weather today": "I'm sorry, I cannot provide real-time information, {}.",
            "who created you": "I was created by a Harpreet , {}.",
            "how old are you": "I don't have an age, I'm just a program, {}.",
            "what can you do": "I can provide information, answer questions, tell jokes, and more, {}!",
            "default": "I'm sorry, I didn't understand that. Can you please rephrase, {}?"
        }
    
    def get_response(self, message, user_name):
        message = message.lower()
        for keyword in self.rules:
            if re.search(r'\b' + re.escape(keyword) + r'\b', message):
                return self.rules[keyword].format(user_name)
        return self.rules["default"].format(user_name)

def loading_screen():
    print("Loading the Chatbot...")
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\nChatbot loaded!\n")

def get_user_name():
    name = input("Chatbot: Hello there! I'm BuddyBot. What's your name? ")
    print("Chatbot: Nice to meet you, {}!".format(name))
    return name

def main():
    loading_screen()
    print("Welcome to BuddyBot!")
    print("Please wait a moment while we start up.\n")
    
    user_name = get_user_name()
    
    chatbot = RuleBasedChatbot()
    print("Chatbot: Hello, {}! How can I assist you today?".format(user_name))
    
    while True:
        user_input = input("{}: ".format(user_name))
        if user_input.lower() == 'bye':
            print("Chatbot: Goodbye, {}! Have a great day!".format(user_name))
            break
        
        response = chatbot.get_response(user_input, user_name)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
