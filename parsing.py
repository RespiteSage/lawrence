# parsing.py
#
# Created by Benjamin Wade
# In April, 2016
#

import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn

def get_wordnet_pos(treebank_tag):
    # converts penn treebank pos tags to wordnet pos tags
    # credit to Suzana_K on Stack Overflow:
    # http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return treebank_tag

def parser(sent):
    #main function of this file
    
    # create variable for verb checking
    vb = False
    
    # start with nltk's default pos tagger
    tagged_sent = pos_tag(word_tokenize(sent))
    
    #print(tagged_sent) #for testing
    
    # convert tuples to lists to allow for mutability
    for i in range(len(tagged_sent)):
        tagged_sent[i] = list(tagged_sent[i])
    
    # set default sentence type and loop variable
    sent_type = 'DEC'
    i = 0
    
    # looping through the sentence
    while i < len(tagged_sent):
        
        #print(i) #for testing
        
        # grab a converted pos tag (penn -> wordnet)
        wn_tag = get_wordnet_pos(tagged_sent[i][1])
        
        #print(tagged_sent) #for testing
        
        # dealing with punctuation (which also affects sentence type)
        if tagged_sent[i][0] in '.,;:?!':
            punct = tagged_sent.pop(i)[0]
            if punct == '.':
                sent_type = 'DEC'
            if punct == '?':
                sent_type = 'INT'
            if punct == '!' and sent_type != 'INT':
                sent_type = 'EXC'
            continue
        
        # handle some common contractions
        if tagged_sent[i][0] == "'s" and tagged_sent[i-1][1][0] != 'N':
            tagged_sent[i][0] = 'is'
        
        if tagged_sent[i][0] == "'re":
            tagged_sent[i][0] = 'are'
        
        if tagged_sent[i][0] == 'ca':
            tagged_sent[i][0] = 'can'
            
        if tagged_sent[i][0] == 'wo' and tagged_sent[i+1][0] == "n't":
            tagged_sent[i][0] = 'will'
        
        if tagged_sent[i][0] == "n't":
            tagged_sent[i][0] = 'not'
        
        # tag for meaning
        if tagged_sent[i][1] not in ('DT','PRP$','PRP'):
            
            # grab meanings from wordnet
            meanings = wn.synsets(tagged_sent[i][0])
            pos_meanings = []
            
            # prioritize meanings of the correct pos and exact word
            for meaning in meanings:
                meaning_name = meaning.name().split('.')
                if meaning.pos() == wn_tag and meaning_name[0] == tagged_sent[i][0]:
                    pos_meanings.insert(0,meaning)
                    break
                elif meaning.pos() == wn_tag:
                    pos_meanings.append(meaning)
            
            # assign meaning (synset), prioritizing pos first
            if len(pos_meanings) > 0:
                tagged_sent[i].append(pos_meanings[0].name())
            elif len(meanings) > 0:
                tagged_sent[i].append(meanings[0].name())
            # handle unknown words
            else:
                tagged_sent[i].append('?')
        # assign pronouns and determiners an unknown meaning
        else:
            tagged_sent[i].append('?')
        
        #print(tagged_sent) #for testing
        
        # concatenate and tag infinitives
        if tagged_sent[i-1][1] == 'TO':
            if tagged_sent[i][1] in ('VB','VBP',):
                new_thing = tagged_sent[i-1][0] + ' ' + tagged_sent[i][0]
                tagged_sent[i-1] = [new_thing,'INF',tagged_sent.pop(i)[2]]
                continue
            else:
                tagged_sent[i-1] = [tagged_sent[i-1][1],'IN']
        
        # check whether the current word is a finite verb
        if tagged_sent[i][1].startswith('V'):
            vb = True
            
        i += 1
        
    #print('Verb: {}'.format(vb)) # for testing
    
    # if there is no verb, run the sentence through the tagger again
    # (assumes that the problem was fixed by joining infinitives)
    if vb == 0:
        new_sent = [i[0] for i in tagged_sent]
        #print('new_sent = {}'.format(new_sent)) #for testing
        new_tagged = pos_tag(new_sent)
        #print('new_tagged = {}'.format(new_tagged)) #for testing
        
        for i in range(len(tagged_sent)):
            if tagged_sent[i][1] != new_tagged[i][1] and new_tagged[i][1].startswith('V'):
                tagged_sent[i][1] = new_tagged[i][1]
    
    return tagged_sent, sent_type
    
    

if __name__ == '__main__':
    sent = input('Write a sentence: ')
    parsed_sent,kind = parser(sent)
    print(parsed_sent)
    print(kind)