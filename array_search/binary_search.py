
def binary_search(arr, target: int = -1):

    l, r = 0, len(arr) - 1

    while l <= r:

        mid = (l + r)//2
        
        arr[mid].visiting = True
        yield False
        
        if arr[mid].val == target:
            arr[mid].isTarget = True
            return True

        if l == r:
            return False

        if arr[mid].val < target:
            while l <= mid:
                arr[l].visited = True
                l += 1
        else:
            while r >= mid:
                arr[r].visited = True
                r -= 1

        yield False

    return False