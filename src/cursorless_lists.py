from dragonfly import DictList, DictListRef, Choice, Impossible
        
lists = {}

def get_dict(name) -> dict:
    for key in lists:
        if key == name:
            return lists[key]
    return {}

def append_list(name, dictionary):
    found = False
    for key in lists:
        if key == name:
            lists[key].update(dictionary)
            found = True
    if not found:
        lists.update({name: dictionary})
        
def get_ref(name):
    dictionary = get_dict(name)
    if dictionary == {}:
        return Impossible(name)
    return Choice(name, dictionary)
