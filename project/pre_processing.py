import os
import re
import time
import pandas as pd
from os import walk

def read_sentences_from_file(file):
    sentences = []
    token_sets = []
    tokens = []
    first_line_found = False
    for line in file:
        res = re.search("(?<=# text_line: ).*", line)
        if res:
            #print("----", ", ".join(tokens))
            if len(tokens) > 0:
                token_sets.append(", ".join(tokens))
                tokens = []
            sentences.append(res.group())
            first_line_found = True
            #print(res.group()) 
        else:
            if first_line_found:
                token = read_token_from_line(line)
                if token and len(token.strip())>0:
                    tokens.append(token.strip())
    #print("----", ", ".join(tokens))
    if len(tokens) > 0:
        token_sets.append(" ".join(tokens))
    return sentences, token_sets

def read_token_from_line(line):
    res = re.search("(?<=([0-9]|_)\t)([^_]*?)(?=\t[^_])", line)
    if res:
        return res.group()
    else:
        return None

def clean_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(filename, "The file does not exist")

start = time.time()
DATA_DIR =   '/home/datascience/sanskrit/dcs/data/conllu/files'
#clean_file("./all_sentences.txt")
clean_file(os.path.join(DATA_DIR, "zip_data.csv"))
data = []
for r, d, f in walk(DATA_DIR, topdown=True):
    for file in f:
        filepath = os.path.join(r, file)
        print(os.path.join(r, file))
        with open(filepath) as input_file:
            #with open("./all_sentences.txt", 'a+') as all_sentences, open("./all_tokens.txt", "a+") as all_tokens:
            sentences, tokens = read_sentences_from_file(input_file)
            if len(sentences) > 0 and len(tokens) > 0:
                for sentence, split in zip(sentences, tokens):
                    data.append(["split", sentence, split])
                    data.append(["combine", split, sentence])
                
eval_df = pd.DataFrame(data, columns=["prefix", "input_text", "target_text"])
eval_df.to_csv(os.path.join("./zip_data.csv"))

end = time.time()
time_elapsed = (end - start)
print("TIME TAKEN TO RUN:::::", time_elapsed)