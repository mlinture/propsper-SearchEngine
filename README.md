# propsper-SearchEngine
The search engine contains three main parts, each of which are in their
own modules. There is the indexing.py module, which will generate all the 
index files used in the search engine. Then there is the ptr_generator.py
module, which will generate the index file pointers, which is used to 
speed up the queries. Then there is the main query.py module, which is what
the user will ultimately run (for the terminal version) to use our search engine.

In order to properly run the given python files, make sure to open the terminal
into the folder which contains all the modules. Then, copy or move the DEV folder
(the corpus given by the instructor of the course in developer.zip) into this 
directory. If the indices folder does not exist in this directory, make an empty 
folder named indices.

We will also assume that a conda evironment is activated.
Make sure that all the basic libraries for this project (ntlk, beautifulsoup4, requests, etc.)
are installed. Also make sure to install openai and flask for the HTML version
of the search engine.

To first generate the index files, run:
python3 indexing.py

Then to generate the index pointer file, run:
python3 ptr_generator.py

Our engine has two versions: the terminal, and the html version.

To run the terminal version, run:
python3 query_terminal.py

To run the html version, run:
flask --app "words.py" run
and then cmd/ctrl click on the link given.
The link will shown on the line similar to:
Running on http://127.0.0.1:5000

NOTE: the HTML version of the search engine uses the openai chatgpt api, which has rules
which prevents from frequent requests. This means that we are forced to give results in a
delayed manner, which does not portray the actual query time. The html version shows the time
taken for the query itself on the side.
