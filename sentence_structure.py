import data_structures as ds
import web_scraping as ws
import requests
from bs4 import BeautifulSoup
import csv

def create_lookup_list(user_input):
    yes_particle = ["助詞", "接続詞", "副詞"]
    ignore_particle = ["は", "が"]
    words = ds.create_words_list(user_input)
    dll = ds.populate_doubly_linked_list(words)
    current = dll.get_head()
    lookup_list =  []
    while current is not None:
        if current.get_pos() in yes_particle and current.get_word() not in ignore_particle:
            if current.next and current.next.get_pos() not in yes_particle:
                lookup_list.append(current.get_word()+current.next.get_word())
        current = current.get_next()
    return lookup_list

def corpus_lookup(search_strings):
    string_count = {}
    for s in search_strings:
        string_count[s] = 0
    with open('jpn_sentences.tsv', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            for s in search_strings:
                if s in row[2]:
                    string_count[s] += 1
    return string_count

def analyze_string_count(string_count_dict, feedback_inp):
    wrong_particles = []
    feedback_inp+="Misused particles: "
    for s, count in string_count_dict.items():
        if count <= 20:
           wrong_particles.append(s[0])
           feedback_inp+=s[0]
           feedback_inp+=", "
    if feedback_inp == "Misused particles: ":
        feedback_inp+="None, looks good<br>"
    return(wrong_particles, feedback_inp)

def pre_noun_adjectivals(user_input):
    words = ds.create_words_list(user_input)
    dll = ds.populate_doubly_linked_list(words)
    current = dll.get_head()
    wrong_pna_use= []
    while current is not None:
        if current.get_word() in ws.pna_dict.keys():
            if current.next.get_pos()!="名詞":
                wrong_pna_use.append(current.get_word()+current.next.get_word())


def check_verb_position(user_input, feedback_inp):
    yes_particle = ["助詞", "接続詞", "副詞"]
    verb = ["動詞", "助動詞"]
    words = ds.create_words_list(user_input)
    dll = ds.populate_doubly_linked_list(words)
    tail = dll.get_tail()
    feedback_inp += "Verb usage: "
    if tail.get_pos() in verb:
        feedback_inp += "Verb is at the end of the sentence, looks good<br>"
    else:
        if tail.get_pos() in yes_particle and tail.prev.get_pos() in verb:
            feedback_inp += "This looks like a question, and the verb is at the end, great\n"
        else:
            print(tail.prev.get_pos())
            feedback_inp+= "The sentence ends with a {} not a verb".format(tail.get_pos())
    return feedback_inp

if __name__ == "__main__":
    #python3 sentence_structure.py -u 子供の頃は自転車に乗れませんでしたが、今は乗れます。
    import argparse
    parser = argparse.ArgumentParser(description='Input Sentence')
    parser.add_argument('-u','--UserInput', type=str, required=True)
    args = parser.parse_args()
    feedback = ""
    words = ds.create_words_list(args.UserInput)
    for i in words:
        print(i.get_pos())
    lookup = create_lookup_list(args.UserInput)
    count = corpus_lookup(lookup)
    misused_particles, feedback = analyze_string_count(count, feedback)
    print(check_verb_position(args.UserInput, feedback))
