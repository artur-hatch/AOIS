import unittest
from unittest.mock import patch
import io
from hash_table import AVLNode, AVLTree, HashTable

class TestAVLNode(unittest.TestCase):
    def test_avl_node_initialization(self):
        node = AVLNode("key", "value")
        self.assertEqual(node.key, "key")
        self.assertEqual(node.value, "value")
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        self.assertEqual(node.height, 1)

class TestAVLTree(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

    def test_insert_and_search(self):
        self.tree.insert("key1", "value1")
        self.assertEqual(self.tree.search("key1"), "value1")
        self.tree.insert("key2", "value2")
        self.assertEqual(self.tree.search("key2"), "value2")

    def test_insert_duplicate_key(self):
        self.tree.insert("key1", "value1")
        self.tree.insert("key1", "value2")
        self.assertEqual(self.tree.search("key1"), "value2")

    def test_search_non_existent_key(self):
        with self.assertRaises(KeyError):
            self.tree.search(" Explorationnonexistent")

    def test_remove_key(self):
        self.tree.insert("key1", "value1")
        self.tree.remove("key1")
        with self.assertRaises(KeyError):
            self.tree.search("key1")

    def test_remove_non_existent_key(self):
        with self.assertRaises(KeyError):
            self.tree.remove("nonexistent")

    def test_balancing_left_left(self):
        self.tree.insert("c", "value3")
        self.tree.insert("b", "value2")
        self.tree.insert("a", "value1")
        self.assertEqual(self.tree.root.key, "b")
        self.assertEqual(self.tree.root.left.key, "a")
        self.assertEqual(self.tree.root.right.key, "c")

    def test_balancing_left_right(self):
        self.tree.insert("c", "value3")
        self.tree.insert("a", "value1")
        self.tree.insert("b", "value2")
        self.assertEqual(self.tree.root.key, "b")
        self.assertEqual(self.tree.root.left.key, "a")
        self.assertEqual(self.tree.root.right.key, "c")

    def test_balancing_right_right(self):
        self.tree.insert("a", "value1")
        self.tree.insert("b", "value2")
        self.tree.insert("c", "value3")
        self.assertEqual(self.tree.root.key, "b")
        self.assertEqual(self.tree.root.left.key, "a")
        self.assertEqual(self.tree.root.right.key, "c")

    def test_balancing_right_left(self):
        self.tree.insert("a", "value1")
        self.tree.insert("c", "value3")
        self.tree.insert("b", "value2")
        self.assertEqual(self.tree.root.key, "b")
        self.assertEqual(self.tree.root.left.key, "a")
        self.assertEqual(self.tree.root.right.key, "c")

    def test_delete_and_rebalance(self):
        self.tree.insert("b", "value2")
        self.tree.insert("a", "value1")
        self.tree.insert("c", "value3")
        self.tree.remove("a")
        self.assertEqual(self.tree.root.key, "b")
        self.assertIsNone(self.tree.root.left)
        self.assertEqual(self.tree.root.right.key, "c")

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(20)

    def test_value_of_key(self):
        self.assertEqual(self.ht._value_of_key("AB"), 1)
        self.assertEqual(self.ht._value_of_key("ZZ"), 675)

    def test_value_of_key_invalid_length(self):
        with self.assertRaises(ValueError):
            self.ht._value_of_key("A")

    def test_value_of_key_invalid_chars(self):
        with self.assertRaises(ValueError):
            self.ht._value_of_key("1A")
        with self.assertRaises(ValueError):
            self.ht._value_of_key("@B")

    def test_hash_function(self):
        self.assertEqual(self.ht._hash("AB"), 1 % 20)
        self.assertEqual(self.ht._hash("ZZ"), 675 % 20)

    def test_insert_and_search(self):
        self.ht.insert("ABC", "value1")
        self.assertEqual(self.ht.search("ABC"), "value1")

    def test_update(self):
        self.ht.insert("ABC", "value1")
        self.ht.update("ABC", "value2")
        self.assertEqual(self.ht.search("ABC"), "value2")

    def test_remove(self):
        self.ht.insert("ABC", "value1")
        self.ht.remove("ABC")
        with self.assertRaises(KeyError):
            self.ht.search("ABC")

    def test_search_non_existent(self):
        with self.assertRaises(KeyError):
            self.ht.search("XYZ")

    def test_collision_handling(self):
        self.ht.insert("ABC", "value1")
        self.ht.insert("ABD", "value2")
        self.assertEqual(self.ht.search("ABC"), "value1")
        self.assertEqual(self.ht.search("ABD"), "value2")

class TestMainFunction(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=[
        '1', 'ABC', 'value1',  # Insert ABC:value1
        '2', 'ABC',            # Search ABC
        '3', 'ABC', 'value2',  # Update ABC to value2
        '2', 'ABC',            # Search ABC again
        '4', 'ABC',            # Remove ABC
        '2', 'ABC',            # Search non-existent ABC
        '1', 'A', 'value1',    # Invalid key
        '6',                   # Invalid choice
        '5'                    # Exit
    ])
    def test_main_operations(self, mock_input, mock_stdout):
        from hash_table import main
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Key "ABC" inserted with value "value1".', output)
        self.assertIn('Value for key "ABC": value1', output)
        self.assertIn('Value for key "ABC" updated to "value2".', output)
        self.assertIn('Value for key "ABC": value2', output)
        self.assertIn('Key "ABC" removed.', output)
        self.assertIn('Validation error: Key must be at least 2 characters long', output)
        self.assertIn('Invalid choice. Please choose 1-5.', output)
        self.assertIn('Program terminated.', output)

if __name__ == '__main__':
    unittest.main()