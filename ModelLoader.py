import pickle

def save_dna(file_name,_object):
    with open(file_name, 'wb') as _file:
        pickle.dump(_object, _file)

def load_dna(file_name):
    with open(file_name, 'rb') as _file:
        dna = pickle.load(_file)
    return dna