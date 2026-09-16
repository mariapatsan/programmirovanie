_Выполнила Пацан Мария 2ПОО_
### Решение задачи "в лоб" с помощью циклов
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
print(two_sum(lst, target))
```
### Усложнение 1
``` python    
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 8


def two_sum_hashed(lst, target):
    num_map = {}
    for i in range(len(lst)):
        complement = target - lst[i]
        if complement in num_map:
            return (num_map[complement], i)
        num_map[lst[i]] = i
    return ()

print(two_sum_hashed(lst, target))
```

