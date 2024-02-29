import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import os
import re
from pathlib import Path
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# global dictionary for mapping a url to a unique document id
doc_ids = {}
# set of all tokens for report data
tokens = set()
# total size of the data in bytes for report data
total_size = 0

# folder in which we will generate the index files
out_folder_name = 'indices/'

# function for adding weights for specific tags within the html page
# such as bolded text or headings
# takes in the soup object, tags and their corresponding weight, the
# token scores dictionary, and the porterstemmer object, and then
# updates the dictionary to add weight for the html tagged word
def add_weighted_frequencies(soup, tags, weight, token_scores, porterstemmer):
    for html_tag in soup.find_all(tags):
        stemmed_words = [porterstemmer.stem(word) for word in word_tokenize(html_tag.text) if word.isalnum()]
        for word in stemmed_words:
            word = word.lower()
            token_scores[word] = token_scores.get(word, 0) + weight
            tokens.add(word)

# the main function to generate the index files
# returns the number of documents found
def generate_index(path):
    dev_folder = Path(path)
    num_docs = 0
    ps = PorterStemmer()
    # go through every sub folder in the DEV folder
    for subdir in dev_folder.iterdir():
        print(f'Generating index files for: {subdir.name}')
        index_map = {}
        # go through every json file within the subdirectory
        for f in subdir.iterdir():
            with open(f, "r") as readfile:
                data = json.loads(readfile.read())
                num_docs += 1
                
                doc_id = len(doc_ids.keys())
                doc_ids[doc_id] = data['url']
                soup = BeautifulSoup(data['content'], 'html.parser')

                # map of all words with their corresponding frequencies/scores
                token_scores = {}

                # first increment word frequency for all words
                stemmed_words = [ps.stem(word) for word in word_tokenize(soup.get_text())]
                for word in stemmed_words:
                    word = word.lower()
                    token_scores[word] = token_scores.get(word, 0) + 1
                    tokens.add(word)

                # add extra weights for bolded words
                add_weighted_frequencies(soup, ['b'], 1, token_scores, ps)
                add_weighted_frequencies(soup, ['strong'], 2, token_scores, ps)
                add_weighted_frequencies(soup, ['h3'], 3, token_scores, ps)
                add_weighted_frequencies(soup, ['h2'], 4, token_scores, ps)
                add_weighted_frequencies(soup, ['h1'], 5, token_scores, ps)
                
                # append the (document id, score) tuple for each word
                for word in token_scores:
                    index_map[word] = index_map.get(word, list()) + [[doc_id, token_scores[word]]]
        
        # write the index map into a file
        with open(out_folder_name+subdir.name+".txt", "w") as outfile:
            # json.dump(index_map, outfile)
            for key, value in index_map.items():
                outfile.write(f'\"{key}\": {value}\n')

    # generate json file for the doc_id map
    with open('doc_ids.json', 'w') as outfile:
        json.dump(doc_ids, outfile)
    
    return num_docs

if __name__ == "__main__":
    # generate the index and get the number of documents found
    num_docs = generate_index('./DEV')

    # generate report file and data
    for f in Path(out_folder_name).iterdir():
        total_size += f.stat().st_size
    total_size += Path('doc_ids.json').stat().st_size
    total_size /= 1000
    num_tokens = len(tokens)
    with open('m1_report.txt', 'w') as write_file:
        write_file.writelines(f'num documents: {num_docs}\nnum tokens: {num_tokens}\ntotal size: {total_size}kB')
    



