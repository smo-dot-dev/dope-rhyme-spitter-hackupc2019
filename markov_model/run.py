import markovify
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from Phyme import Phyme
from Phyme.util import flatten
from pyphonetics import Soundex
nltk.download('cmudict')
ph = Phyme()
soundex = Soundex()

print("Loading model... ")
with open('small_markov_model_state_3.json', 'rb') as f:
    text = f.read()
    markov_model = markovify.NewlineText.from_json(text)

#returns list of words that rhyme
def find_rhymes(word):
    rhyme_list = []
    try:
        rhyme_list.append((list(flatten(ph.get_perfect_rhymes(word).values()))))
        rhyme_list.append((list(flatten(ph.get_partner_rhymes(word).values()))))
        rhyme_list.append((list(flatten(ph.get_family_rhymes(word).values()))))
        rhyme_list.append((list(flatten(ph.get_additive_rhymes(word).values()))))
        rhyme_list.append((list(flatten(ph.get_subtractive_rhymes(word).values()))))
    except KeyError:
        return None
    return list(flatten(rhyme_list))

def any_phrases_rhyme(phrase1, phrase2):
    rhymes = False
    maxim = len(phrase1)
    if len(phrase2) < maxim:
        maxim = len(phrase2)
    i = 0
    while not rhymes and i < maxim:
        try:
            if soundex.sounds_like(phrase1[i], phrase2[i]):
                rhymes = True
                i += 1
        except:
            rhymes = False
            pass
        
    return rhymes

def last_phrases_rhyme(phrase1, phrase2):
    rhymes = False
    while not rhymes:
        try:
            if soundex.sounds_like(phrase1[-1], phrase2[-1]) or soundex.sounds_like(phrase1[-2], phrase2[-2]):
                rhymes = True
        except:
            pass
    return rhymes

def answer(phrase, times):

    for i in range(times):
        tmp_sent = markov_model.make_sentence(test_output=False)
        while not any_phrases_rhyme(phrase, tmp_sent):
            tmp_sent = markov_model.make_sentence(test_output=False)
        print(tmp_sent)

    #if rhyme_list is not None:
    #    count = 4
    #    for rhyme in rhyme_list:
    #        phrase = markov_model.make_sentence(test_output=False)
    #        if rhyme == tokenizer.tokenize(phrase)[-1]:
    #            print(phrase)
    #            count -= 1
    #            if count is 0:
    #                return
    #    print("[WARN] No rhymes found.1")
    #    for i in range(count):
    #        print(markov_model.make_sentence(test_output=False))
    #    return
    #else: 
    #    for i in range(4):
    #        print("[WARN] No rhymes found.1")
    #        print(markov_model.make_sentence(test_output=False))

while True:
    sent = input('$> ')
    if sent == '':
        continue
    tokenizer = RegexpTokenizer(r'\w+')
    #rhyme_list = find_rhymes(tokenizer.tokenize(sent)[-1])
    answer(sent, 8)