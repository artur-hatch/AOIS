class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _update_height(self, node):
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _insert(self, node, key, value):
        if not node:
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node
        self._update_height(node)
        balance = self._get_balance(node)
        if balance > 1:
            if key < node.left.key:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if key > node.right.key:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
        return node

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        return self._search(node.left, key) if key < node.key else self._search(node.right, key)

    def search(self, key):
        node = self._search(self.root, key)
        if not node:
            raise KeyError("Key not found")
        return node.value

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def _delete(self, node, key):
        if not node:
            raise KeyError("Key not found")
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._find_min(node.right)
            node.key, node.value = temp.key, temp.value
            node.right = self._delete(node.right, temp.key)
        self._update_height(node)
        balance = self._get_balance(node)
        if balance > 1:
            if self._get_balance(node.left) >= 0:
                return self._rotate_right(node)
            else:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(node.right) <= 0:
                return self._rotate_left(node)
            else:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
        return node

    def remove(self, key):
        self.root = self._delete(self.root, key)

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [AVLTree() for _ in range(size)]
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def _value_of_key(self, key):
        if len(key) < 2:
            raise ValueError("Key must be at least 2 characters long")
        first, second = key[0].upper(), key[1].upper()
        if first not in self.alphabet or second not in self.alphabet:
            raise ValueError("First two characters must be Latin letters")
        base = 26
        return self.alphabet.index(first) * base + self.alphabet.index(second)

    def _hash(self, key):
        return self._value_of_key(key) % self.size

    def insert(self, key, value):
        self.table[self._hash(key)].insert(key, value)

    def search(self, key):
        return self.table[self._hash(key)].search(key)

    def update(self, key, value):
        self.insert(key, value)

    def remove(self, key):
        self.table[self._hash(key)].remove(key)

def main():
    ht = HashTable(20)
    while True:
        print("\n=== Hash Table Menu ===")
        print("1. Create (insert key-value)")
        print("2. Read (search by key)")
        print("3. Update (update key's value)")
        print("4. Delete (remove key)")
        print("5. Exit")
        choice = input("Choose operation (1-5): ").strip()
        if choice == '5':
            print("Program terminated.")
            break
        if choice not in {'1', '2', '3', '4'}:
            print("Invalid choice. Please choose 1-5.")
            continue
        try:
            key = input("Enter key: ").strip()
            if choice in {'1', '3'}:
                value = input("Enter value: ").strip()
            if choice == '1':
                ht.insert(key, value)
                print(f'Key "{key}" inserted with value "{value}".')
            elif choice == '2':
                result = ht.search(key)
                print(f'Value for key "{key}": {result}')
            elif choice == '3':
                ht.update(key, value)
                print(f'Value for key "{key}" updated to "{value}".')
            elif choice == '4':
                ht.remove(key)
                print(f'Key "{key}" removed.')
        except ValueError as ve:
            print("Validation error:", ve)
        except KeyError as ke:
            print("Operation error:", ke)
        except Exception as e:
            print("Unknown error:", e)

if __name__ == "__main__":
    main()