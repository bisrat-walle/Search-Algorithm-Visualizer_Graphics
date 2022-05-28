import random
from graphsearch.node import * 
from collections import deque

def randomly_generate_graph():
    randomList = list(range(3, 19))
    random.shuffle(randomList)
    head = Node(random.randint(1, 10))
    temp = deque([head])
    i = 0
    for _ in range(3):
        for _ in range(len(temp)):
            node = temp.popleft()
            node.left = Node(randomList[i])
            node.right = Node(randomList[i+1])
            temp.append(node.left)
            temp.append(node.right)
            i += 2
            
    return head