import markovify
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from Phyme import Phyme
from Phyme.util import flatten
from pyphonetics import Soundex
from subprocess import Popen
nltk.download('cmudict')
ph = Phyme()
soundex = Soundex()

from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC917b6ce16bde7f0db7ca3a6b6dad0d1e'
auth_token = '3d1489c2afb9294a1a993cb2713e6f56'
client = Client(account_sid, auth_token)

print("Loading model... ")
with open('small_markov_model_state_2.json', 'rb') as f:
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
        except:
            pass
        i += 1
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
def make_sent():
    tmp_sent = markov_model.make_short_sentence(20,test_output=False)
    

def answer(phrase, times):
    s= ''
    for i in range(times):
        tmp_sent = markov_model.make_short_sentence(20,test_output=False)
        while not any_phrases_rhyme(phrase, tmp_sent):
            tmp_sent = markov_model.make_short_sentence(20, test_output=False)
        s += tmp_sent + '\n'
    return s

    #if rhyme_list is not None:
    #    count = 4
    #    for rhyme in rhyme_list:
    #        phrase = markov_model.make_short_sentence(test_output=False)
    #        if rhyme == tokenizer.tokenize(phrase)[-1]:
    #            print(phrase)
    #            count -= 1
    #            if count is 0:
    #                return
    #    print("[WARN] No rhymes found.1")
    #    for i in range(count):
    #        print(markov_model.make_short_sentence(test_output=False))
    #    return
    #else: 
    #    for i in range(4):
    #        print("[WARN] No rhymes found.1")
    #        print(markov_model.make_short_sentence(test_output=False))

while True:
    sent = input('Spit your rhymes: ')
    phone = input('Phone number?: ')
    if sent == '':
        continue
    tokenizer = RegexpTokenizer(r'\w+')
    #rhyme_list = find_rhymes(tokenizer.tokenize(sent)[-1])
    text = answer(sent, 4)
    with open('./twiliosucks/twiml.xml', 'w+', encoding='utf-8') as file:
        file.write('''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{}</Say>
</Response>'''.format(text))

    p = Popen("twiliosucks.bat", cwd=r"./")
    stdout, stderr = p.communicate()


    call = client.calls.create(
                        url='http://raw.githubusercontent.com/smunozdev/twiliosucks/master/twiml.xml',
                        to=phone,
                        from_='+46101956921'
                    )
    print(call.sid)