import random
from node import *


def random_list_generator(sort: bool = False, n: int = 8):
    """ Generates a random list of length <n> """

    lst = [Node(int(random.random() * 9)) for _ in range(n)]

    return sorted(lst, key=lambda x: x.val) if sort else lst
