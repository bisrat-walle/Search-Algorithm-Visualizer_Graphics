from collections import deque

class BFS:
    def __init__(self, graph):
        self.graph = graph
    
    def search(self, to_be_searched = -1):
        queue = deque([self.graph])
        while queue:
            current = queue.popleft()
            current.visited = True
            if current.value == to_be_searched:
                current.target = True
                yield True
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
            yield False