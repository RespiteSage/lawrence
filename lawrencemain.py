#LING380 Final Project
#Chatbot

import random
import pickle
from nltk.corpus import wordnet as wn

from parsing import parser

botDict = {}

#'''
with open('responses.p','rb') as f: # opens (and closes) file to read (r) as bytes (b)
    botDict = pickle.load(f)
#'''

def train(key, sent):
    parsedSent = parser(sent)
    if key in botDict.keys():
        botDict[key].append((sent,parsedSent))
    else:
        botDict[key] = [(sent,parsedSent)]
            

def respond(response): # changed to deal with a list of possible responses
    possibleResponses = []
    for i in response:
        if i[0] in botDict.keys():
            randNum = random.randint(0, len(botDict[i[0]]) - 1)
            possibleResponses.append(botDict[i[0]][randNum])
        elif i[2] != '?': # if not, try hypernyms
            hyper = lambda s: s.hypernyms() # find all hypernyms
            hyperList = list(wn.synset(i[2]).closure(hyper))[0:4]
            fewHyper = [j.name().split('.')[0] for j in hyperList]
            for hyp in fewHyper:
                #print(hyp) #for testing
                if hyp in botDict.keys():
                    randNum = random.randint(0, len(botDict[hyp]) - 1)
                    possibleResponses.append(botDict[hyp][randNum])
                    
    if len(possibleResponses) == 0:
        print("I don't really know much about that.")
        teachInput = input("What subject did you want me to know about? (enter a word as a subject)\n")
        teachInput = teachInput.lower()
        teachInput = teachInput.strip("?")
        teachResponse = input("What should I say about that? (this is what Lawrence will respond with) \n")
        print("Cool, thanks! I'll keep that in mind.")
        train(teachInput, teachResponse)
    
    else:
        myResponse = possibleResponses[random.randint(0,len(possibleResponses)-1)]
        #myResponse = possibleResponses[-1]
        print(myResponse[0])


'''                # original code for giving responses
#train("name", "My name's Lawrence! How are you today?")
train("name", "Hey I'm Lawrence.")


train("science", "Science is my favorite subject.")
train("science", "I hear the jury's still out on science.")
#'''

userInput = input("Hey! My name's Lawrence. Ask me a few questions, like what I think about science!\n")

userInput = userInput.lower()
parsedInput, sentenceType = parser(userInput)

while "bye" not in userInput:
    respond(parsedInput)
    userInput = input("Enter response: ")
    userInput = userInput.lower()
    parsedInput, sentenceType = parser(userInput)
else:
    print("Goodbye! See you later.")

with open('responses.p','wb') as f: # opens (and closes) file to write (w) as bytes (b)
    pickle.dump(botDict,f)