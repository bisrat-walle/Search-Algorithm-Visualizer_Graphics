class Node:
    def __init__(self, value):
        self.value = value
        self.visited = False
        self.right = None
        self.left = None
        self.target = False
    
    
    def __str__(self):
        return self.value
    
    
    def __repr__(self):
        return self.value