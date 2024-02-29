import json
from pathlib import Path

# map for each word with their corresponding list of
# (file_index, word position) tuples as a "pointer"
# of the word position in each file
index_ptr = {}

# map for each unique file index/id with their corresponding index file path
file_indices = {}

# main function for generating the index pointer file
def generate_index_ptr(path):
    folder = Path(path)
    # go through every index file in the given path
    for f in folder.iterdir():
        print(f'Opened file: {str(f)}')
        # assign the index/id of the file found
        file_index = len(file_indices.keys())
        file_indices[file_index] = str(f)

        # read each line in the index file and record the word position
        # for the (file, word position) tuple
        with open(f, "r") as readfile:
            cur_pos = readfile.tell()
            line = readfile.readline()
            while line != '':
                word = line[1:].split("\"")[0]
                index_ptr[word] = index_ptr.get(word, list()) + [(file_index, cur_pos)]

                cur_pos = readfile.tell()
                line = readfile.readline()
    
    # dump the data into a json file
    with open('index_ptr.json', 'w') as outfile:
        out_dict = {'ptrs' : index_ptr, 'file_indices' : file_indices}
        json.dump(out_dict, outfile)

if __name__ == '__main__':
    # generate the indices in the given path
    generate_index_ptr('indices/')