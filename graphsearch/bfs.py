class BFS:
    def __init__(self, graph, to_be_searched):
        self.graph = graph
        self.to_be_searched = to_be_searched
    
    def bfs(graph, to_be_searched = -1):
        print("Entered")
        queue = deque([self.graph])
        while queue:
            current = queue.popleft()
            current.visited = True
            print(current.value, "marked True")
            if current.value == to_be_searched:
                return True
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
            yield False