from dragonfly import Choice, Impossible

lists = {}


def get_dict(name) -> dict:
    if name in lists:
        return lists[name]
    else:
        return {}


def append_list(name, dictionary):
    if name in lists:
        lists[name].update(dictionary)
    else:
        lists.update({name: dictionary})


def get_list_ref(name):
    dictionary = get_dict(name)
    if dictionary == {}:
        return Impossible(name)
    return Choice(name, dictionary)
