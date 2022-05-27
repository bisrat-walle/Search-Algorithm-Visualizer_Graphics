class DFS:
    def __init__(self, graph, to_be_searched):
        self.graph = graph
        self.to_be_searched = to_be_searched
    
    def bfs(graph, to_be_searched = -1):
        print("Entered")
        stack = deque([graph])
        while stack:
            current = stack.pop()
            current.visited = True
            print(current.value, "marked True")
            if current.value == to_be_searched:
                return True
            if current.left:
                stack.append(current.left)
            if current.right:
                stack.append(current.right)
            yield False

