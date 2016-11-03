from os import walk

def list_filenames():
    f = []
    for (dirpath, dirnames, filenames) in walk('NLM_500/documents'):
        f.extend(filenames)
    return f