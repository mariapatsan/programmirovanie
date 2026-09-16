``` python
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 8

def two_sum(lst, target):
    if len(lst) > 1:
        for i in range(len(lst)-1):
            for j in range(i + 1, len(lst)):
                if lst[i] + lst[j] == target:
                 return(i, j)


    return ()
```
    
