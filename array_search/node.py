
class Node:

    def __init__(self, val) -> None:
        self.visited = False
        self.val = val
        self.isTarget = False

    def __str__(self):
        return self.val

    def __repr__(self):
        return self.val
