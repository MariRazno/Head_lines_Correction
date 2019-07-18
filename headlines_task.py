import spacy
import json
import re

with open(r"C:\git_project\summer-school-2019\classes\6_full_cycle\task-headlines\test-set.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)
nlp = spacy.load("en_core_web_md", disable=['textcat', 'ner'])

def start_end(headline):
    nlp_headline = nlp(headline)
    start,end = 0, len(headline)-1
    for item in nlp_headline:
        if item.text[0].isalpha:
            start = item.i
            break
    for item in reversed(nlp_headline):
        if item.text[0].isalpha:
            end = item.i
            break
    return start, end


def format_headline(headline):
    nlp_headline = nlp(headline)
    start, end = start_end(headline)
    formatted_headline = ''
    for token in nlp_headline:
        word = token.text
        if re.findall(r"'[a-z]+|[A-z][A-Z]|[A-Z]+", word):
            formatted_headline += word
        elif re.match(r"n't", word):
            formatted_headline += word
        elif token.i == start or token.i == end:
            formatted_headline += word.title()
        elif token.dep_ == 'mark':
            formatted_headline += word.title()
        elif len(word) > 3:
            formatted_headline += word.title()
        elif token.pos_ in {"ADV", "NOUN", "PRONOUN", "ADJ", "VERB", "NUM"}:
            formatted_headline += word.title()
        elif token.pos_ in {"DET", "CCONJ", "PART", "INTJ"}:
            formatted_headline += word.lower()
        else:
            formatted_headline += word.lower()
        formatted_headline += token.whitespace_
    print(headline, formatted_headline)
    return formatted_headline

print(format_headline("Pondering the parable: Who is the foreman?"
"My Sisterwife's Closet updates fans that the site can't keep up tonight"
"Turkey workshop for hunters and photographers March 20 at O'Bannon Woods State Park near Corydon"
"Justin Bieber's Ferrari: Lending the car doesn't help his tainted image?"
"Let's Add More Color to Our Life!"
"DVR Alert: How the KSDK Grinch stole 'Community'"
"How NASCAR's Chase field stacks up after New Hampshire"))

def accuracy(test_data):
    tp = 0
    for sample in test_data:
        formatted_headlines = format_headline(sample[0])
        if formatted_headlines == sample[1]:
            tp += 1
    return tp/len(test_data)

print(accuracy(test_data))
