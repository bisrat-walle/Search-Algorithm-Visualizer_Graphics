
def linear_search(arr: list, target: int = -1):
    """ Searches whether <target> exists inside <arr> """

    for i in range(len(arr)):

        if arr[i].val == target:
            arr[i].isTarget = True
            return True

        arr[i].visited = True

        yield False
