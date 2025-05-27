import nltk

from nltk.chat.util import Chat, reflections
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.db.models.functions import Now
from datetime import timedelta


def home(request):
    return render(request, 'codexio_main/index.html')


# Download the nltk data if not already downloaded
nltk.download('punkt')

# Define the chatbot patterns and responses

chatbot_pairs = [
    [
        "hello|hi|hey|good day",
        ["Hi. How can I be of help to you?","Hi my friend. How can I be of help to you?",]
    ],
    [
        r"I love you",
        ["Thanks.","Awww...That's so adorable", "That's so nice of you, thanks.",]
    ],
    [
        r"sup|what's up|how are you",
        ["I'm good. What about you?",]
    ],
    [
        r"Tell me about Codexio|Tell me about this website|I would love to know more about Codexio|What is Codexio",
        ["This is a coding/programming community that is aimed at helping like minds grow. We help those aspiring to be developers get to the point of being job ready. We also encourage the spirit of learning and healthy compitition.",]
    ],
    [
        r"Good too|I'm good too|I'm great|I'm fine|I'm doing well",
        ["Good to know","Great!",]
    ],
    [
        r"What do you love doing|What do you like",
        ["I love to help people who are just like me, a computer guru.",]
    ],
    [
        r"What can you do|I don't know, you tell me",
        ["As a Chat bot, I can only understand little human interaction and give you direct answers. I only recognize questions stored in my database for now, so can only chat with you like you are chatting with my makers. I may not understand complex interactions, but will become better overtime. I can also save chats in case of future reference. I could also tell you some jokes, if you want to laugh just type 'make me laugh'.",]
    ],
    [
        r"Why can't you understand me|What can you answer|What are some questions you answer",
        ["Sorry about that. You could try rephrasing the question or sentence. You could watch this video on my commands and how to use me. Here's the link","I only answer questions that relates to this website, me and programming. You could either rephrase the question or ask another question.",]
    ],
    [
        r"Who made you|by whom|by who",
        ["A team of friendly programmers who loves what they do. Together they made this community.",]
    ],
    [
        r"What is their vision|Why was codexio made|why was codexio created",
        ["Their vision is to grow and help as many people as possible.",]
    ],
    [
        r"I would love to ask you some questions|I want ask something|Can I ask you a question|I want to ask something from you|Can I ask",
        ["Sure","Alright",]
    ],
    [
        r"Okay, thanks|Thanks|Thanks a lot|I really appreciate the help|Thank you",
        ["Happy to help","Don't mention it.","You're welcome.",]
    ],
    [
        r"What year were you born|What year were you made|When were you developed",
        ["The year 2023.",]
    ],
    [
        r"Goodbye|Bye|Alright, talk to you later",
        ["Alright, bye","Yeah, bye", "See you soon",]
    ],
    [
        r"nothing for now|nothing",
        ["Alright",]
    ],
    [
        r"Cool|That's nice|That's wonderful|That's extraordinary|That's funny",
        ["Thanks", "All love",]
    ],
    [
        r"Zillo",
        ["Yes. How may I help you?","Hi. How can I help you?",]
    ],
    [
        r"What is your name?",
        ["My name is Zillow your personal chatbot assistant from codexio, created to help you through this website and any updates that comes up. I am also your buddy incase you just want to chat. You want my help you could just enter Zillow.",]
    ],
    [
        r"Okay|Ok",
        ["Yeah...",]
    ],
    [
        r"Tell me a joke|Make me laugh|another joke",
        ["Why don't scientists trust atoms? Because they make up everything!","Parallel lines have so much in common. It's a shame they'll never meet.", "Why did the math book look sad? Because it had too many problems.", "I used to play piano by ear, but now I use my hands.", "Why did the bicycle fall over? Because it was two-tired!"]
    ],
    [
        r"What schools are great for programming|How can I make my programming skills",
        ["These schools are great schools for learning how to code Udemy, Codeacademy, W3Schools, freecodecamp.", "Choose a Programming Language. Learn the Basics. Practice Regularly. Build Projects. Read Code. Join Programming Communities( this step you have already taken).",]
    ],
    [
        r"I am not feeling so",
        ["You are probably ill. Take a rest from what you are doing. All work and no play makes Jack a dull boy.", "I suggest you visit the doctor as quickly as possible.",]
    ],
    [
        r"I have a compliant to make on the website",
        ["All compliant should go to my makers, I can't help with that for now. Here's their email: . You could also give your compliants in the community you're in. So sorry for the inconvenience.",]
    ],
    [
        r"Can you save my chats|Why don't you save my chats",
        ["Right after a reload the chats are cleared, but I save them on the database for quick learning. Only updates made by me would show up for five days, afterward would disappear.",]
    ],
    [
        r"What is the fastest animal in the world",
        ["The Periguim Falcon.", "The Birds.", "This question is not related to this website."]
    ],

    [
        r"(.*)",
        ["I'm sorry, but I don't understand that, and maybe can't answer that question due to some reasons. You could try rephrasing the question or sentence, or asking another question. You could watch this video on my commands and how to use me. Here's the link: . I can only answer questions that relates to this website, me and programming.",]
    ],
]
def home(request):
    return render(request, 'codexio_main/index.html')





def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('content')
        message = Message.objects.create(content=user_message)
        
        response = get_chatbot_response(user_message)
        Message.objects.create(content=response)
        
        return JsonResponse({'response': response})
    updates_zillow = Update.objects.all()
    context = {}
    context["updates_zillow"] = updates_zillow
    
    # Update.objects.filter(timestamp__lt=Now()-timestamp(days=5)).delete()
    
    
    return render(request, 'codexio_main/chatbot.html', context)

def get_chatbot_response(user_message):
    chatbot = Chat(chatbot_pairs, reflections)
    return chatbot.respond(user_message)







