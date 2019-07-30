#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 15:27:07 2019

@author: chengzhongito
"""

import time
import tflearn
import tensorflow
import pickle
import pandas as pd 
import numpy as np
import json
import nltk


lemma = nltk.wordnet.WordNetLemmatizer()


with open("qa_data.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        train_words, train_labels, training, output = pickle.load(f)
except:
    train_words =[]
    train_labels=[]
    test_words =[]
    test_labels=[]
    doc_x = []
    doc_y = []
    
    lemma = nltk.wordnet.WordNetLemmatizer()
    punctuation = "?:;',.)("
    
    
    for intent in data:
        for question in intent["questions"]:
            question = question.translate(str.maketrans('', '', string.punctuation))
                
            words = nltk.word_tokenize(question)
            
            train_words.extend(words)
            doc_x.append(words)
            doc_y.append(intent["tag"])
    
        if intent["tag"] not in train_labels:
            train_labels.append(intent["tag"])
            
    train_words = [lemma.lemmatize(w.lower()) for w in train_words]
    train_words = list(set(train_words))


    
tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

##try:
model.load("model.tflearn")
##except:
####    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
##    model.save("model.tflearn")

def read_data():
    
    intents = []
    index, max_pointer = 0,0

    for tag in df['tag'].unique().tolist():
        label = tag
        label_dict={'tag':label}
        questions,df_group_dict,answers = [],[],[]

        question_dict, df_group_dict={},{}

        df_group = df.groupby('tag').get_group(tag)
        max_pointer += len(df_group)

        while(index < max_pointer):
            if( not pd.isna(df_group.question[index])):
                questions.append(df_group.question[index])
            if( not pd.isna(df_group.answer[index])):
                answers.append(df_group.answer[index])
            index += 1

        df_group_dict['tag']=label
        df_group_dict['questions'] = questions
        df_group_dict['answers'] = answers
        intents.append(df_group_dict)

    to_json = json.dumps(intents)
    with open("qa_data.json","w") as f:
        f.write(to_json)
        

def bag_of_words(question, words):
    bag = [0 for _ in range(len(words))]

    question_words = nltk.word_tokenize(question)
    question_words = [lemma.lemmatize(word.lower()) for word in question_words]

    for content in question_words:
        for i, w in enumerate(words):
            if w == content:
                bag[i] = 1
            
    return np.array(bag)


def chat(quest):
    
##    model.load("model.tflearn")
    ans_list = []
    result = model.predict([bag_of_words(quest, train_words)])[0]
    result_index = np.array(result).tolist()
    result= sorted(result_index, reverse=True)
   
    if result[0] > 0.8:
        for response in data[result_index.index(result[0])]['answers']:
            ans_list.append(response)
    else:
        ans_list.append("ABC: Did you mean:")
        for response in data[result_index.index(result[1])]['questions']:
            ans_list.append(response)

    return ans_list

