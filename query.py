import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import os
import re
from pathlib import Path
import time
import math
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# This file is used for the HTML version of our search engine

# maps each word to a dictionary of urls (id) mapped to their frequencies
word_top_links = {}
# map for loading the index pointer and file indices
data_dict = {}
# map of all index files ids to their corresponding index file path
file_indices = {}

# number of links we want for each query
MAXLINKS = 5

timer = 0

def getTime():
    global timer
    return timer

def setTime(eTime):
    global timer
    timer = eTime

# gets the total number of documents; used for the tf-idf calculation
def getNumDocs():
    with open(Path('doc_ids.json'), "r") as readfile:
        data = json.loads(readfile.read())
        return len(data.keys())

# main search function
# takes in a user input as a query for the search engine
def search(userInput):
    global word_top_links
    global data_dict
    global file_indices
    userInput = str(userInput)
    linkList = []
    elapsed_time = 0

    # load the index pointer files for faster query searches
    print('Loading index files...')
    with open('index_ptr.json', "r") as readfile:
        data_dict = json.loads(readfile.read())
        index_ptr = data_dict['ptrs']
        file_indices = data_dict['file_indices']
    
    N = getNumDocs()
    ps = PorterStemmer()
    
    # repeatedly take user input
    while True:
        # dictionary for holding the word and their corresponding df values
        word_df = {}

        query = userInput
        
        # start the timer
        start_time = time.time()

        # tokenize and stem the query input
        stemmed_words = [ps.stem(word) for word in word_tokenize(query)]

        # go through each word in the query
        for word in stemmed_words:
            word = word.lower()

            # go through each of the (index file, word position) tuple for this word
            paths = index_ptr.get(word, list())
            for f, word_pos in paths:
                f = file_indices[str(f)]
                with open(f, "r") as readfile:
                    # seek to the word position in the index file
                    readfile.seek(word_pos)

                    # convert the line into a usable data type
                    line = readfile.readline().rstrip('\n')
                    line_json = '{'+line+'}'
                    data = json.loads(line_json)
                    d = data.get(word, None)

                    if d is not None:
                        # retrieve the word frequencies for each url
                        for url_freq in d:
                            top_links = word_top_links.get(word, dict())
                            top_links[url_freq[0]] = top_links.get(url_freq[0], 0) + url_freq[1]
                            word_top_links[word] = top_links
            # update the df value for each word
            word_df[word] = len(word_top_links.get(word, dict()))

        # dictionary for all the urls mapped to their tf-idf scores
        url_scores = {}

        # calculate the tf_idf scores for each url
        # go through each word
        for word, top_link_dict in word_top_links.items():
            # go through each url and their tf value for this word
            for url_id, tf in top_link_dict.items():
                df = word_df[word]
                # print(f'{url_id}: word : {word}, tf : {tf}, df : {df}')

                # caluclate and append the score for the urls
                score = (1+math.log10(tf)) * math.log10(N/df)
                url_scores[url_id] = url_scores.get(url_id, 0) + score

        # get the elapsed time
        elapsed_time = time.time() - start_time
        global timer
        timer = elapsed_time
        print(f'Total elapsed time: {elapsed_time}')

        # get the top results
        with open(Path('doc_ids.json'), "r") as readfile:
            data = json.loads(readfile.read())
            print()

            top_results = []

            for url_id, freq in sorted(url_scores.items(), key=lambda x : -x[1]):
                url = data.get(str(url_id), None)
                if url != None:
                    # print(f'urlid: {url_id}, score: {url_scores[url_id]}')
                    # defragment and check for duplicates:
                    defrag = url.split('#')[0]
                    if defrag not in top_results:
                        top_results.append(defrag)
                if len(top_results) >= MAXLINKS:
                    break
            
            linkList = top_results

            if len(top_results) == 0:
                # print('No links were found')
                return []
        
        # reset dictionaries for future queries
        word_top_links = {}
        data_dict = {}
        return linkList

