import pandas as pd
import string
import markovify
import json
import pickle
import msgpack

dataset = pd.read_csv('small_dataset.csv')
lyrics_list = list(dataset['text'])

#convert csv to txt corpus of all songs
with open('corpus_markov.txt', 'w+', encoding='utf-8') as file:
    for song in lyrics_list:
        file.write(str(song))

#Train markov model with state size 2
with open('corpus_markov.txt', encoding="utf-8") as f:
    markov_model = markovify.NewlineText(f.read(), state_size=2)

#Save markov model for later use
with open('small_markov_model_state_2.json', 'w+', encoding='utf-8') as file:
    file.write(markov_model.to_json())

#sample
print(markov_model.make_sentence())

