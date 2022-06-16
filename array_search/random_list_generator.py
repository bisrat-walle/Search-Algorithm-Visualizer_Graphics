import random
from array_search.node import *


def random_list_generator(sort: bool = False, n: int = 10):
    """ Generates a random list of length <n> """

    array = list(map(Node, list(range(0, 10))))
    random.shuffle(array)

    return array