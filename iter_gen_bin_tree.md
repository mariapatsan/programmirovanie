``` python
def gen_bin_tree(height: int = 6, root: int = 9) -> dict:
    """Создает бинарное дерево заданной высоты.

    height: Высота дерева.
    root: Значение корня дерева.

    Построенное бинарное дерево в виде словаря или None, если height < 0.
    """
    if height < 0:
        return None
    if height == 0:
        return {root: []}

    tree = {root: []}
    current_level = [(root, tree)]

    for _ in range(height):         
        next_level = []

        for value, node in current_level:
            left_value  = value * 2 + 1
            right_value = 2 * value - 1

            left_node  = {left_value: []}
            right_node = {right_value: []}

            node[value] = [left_node, right_node]

            next_level.append((left_value,  left_node))
            next_level.append((right_value, right_node))

        current_level = next_level

    return tree

print(gen_bin_tree(2, 9))
```
test:
``` python
import unittest
from iter_g_b_t import gen_bin_tree


class TestGenBinTree(unittest.TestCase):

    def test_height_0(self):
        self.assertEqual(gen_bin_tree(0, 9), {9: []})

    def test_height_1(self):
        self.assertEqual(gen_bin_tree(1, 9), {
            9: [{19: []}, {17: []}]
        })

    def test_height_2(self):
        self.assertEqual(gen_bin_tree(2, 9), {
            9: [
                {19: [{39: []}, {37: []}]},
                {17: [{35: []}, {33: []}]},
            ]
        })

    def test_negative_height(self):
        self.assertIsNone(gen_bin_tree(-1, 9))

    def test_left_value(self):
        tree = gen_bin_tree(1, 9)
        self.assertIn(19, tree[9][0])

    def test_right_value(self):
        tree = gen_bin_tree(1, 9)
        self.assertIn(17, tree[9][1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
```
