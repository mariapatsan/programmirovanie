Пацан Мария 2 курс ПОО
Рекурсивное представление бинарного дерева:
``` python
# left_branch = root * 2 + 1
# right_branch = 2 * root - 1
def left_branch(x):
    return x * 2 + 1

def right_branch(x):
    return 2 * x - 1

def g_b_t(height, root, l_b = left_branch, r_b = right_branch):
    
    if height < 0:
        return None

    def build(value, level):
        branch = {value: []}
        if level < height:
            left = build(l_b(value), level + 1)
            right = build(r_b(value), level + 1)
            branch[value] = [left, right]
        return branch

    return build(root, 0)

print(g_b_t(2, 9))
```


Тест:
``` python
import unittest

from gen_bin_tree import g_b_t


class test_gbt(unittest.TestCase):

    def test_height_0(self):
        self.assertEqual(g_b_t(0, 9), {9: []})

    def test_height_1(self):
        self.assertEqual(g_b_t(1, 9), {9: [{19: []}, {17: []}]})

    def test_height_2(self):
        self.assertEqual(g_b_t(2, 9), {
            9: [{19: [{39: []}, {37: []}]}, {17: [{35: []}, {33: []}]},]})

    def test_2(self):
        self.assertIsNone(g_b_t(-1, 9))

if __name__ == "__main__":
    unittest.main()
```
