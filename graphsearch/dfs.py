from collections import deque


class DFS:
    def __init__(self, graph):
        self.graph = graph

    def search(self, to_be_searched=-1):
        stack = deque([self.graph])
        while stack:
            current = stack.pop()
            current.visited = True
            if current.value == to_be_searched:
                return True
            if current.left:
                stack.append(current.left)
            if current.right:
                stack.append(current.right)
            yield False
