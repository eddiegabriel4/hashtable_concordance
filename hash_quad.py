from typing import List, Any, Optional

class info:
    
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return 'info({0}, {1})'.format(self.key, self.value)

class HashTable:

    def __init__(self, table_size: int):            # can add additional attributes
        self.table_size = table_size                # initial table size
        self.hash_table: List = [None]*table_size   # hash table
        self.num_items = 0                          # empty hash table

    def insert(self, key: str, value: Any) -> None:
        """ Inserts an entry into the hash table (using Horner hash function to determine index, 
        and quadratic probing to resolve collisions).
        The key is a string (a word) to be entered, and value is any object (e.g. Python List).
        If the key is not already in the table, the key is inserted along with the associated value
        If the key is is in the table, the new value replaces the existing value.
        When used with the concordance, value is a Python List of line numbers.
        If load factor is greater than 0.5 after an insertion, hash table size should be increased (doubled + 1)."""
        hash_key =  self.horner_hash(key)
        if self.hash_table[hash_key] == None:
            self.hash_table[hash_key] = info(key, value)
            self.num_items += 1
            if self.get_load_factor() > 0.5:
                prev_hash = self.hash_table
                prev_size = self.table_size
                self.hash_table = [None] * (2 * prev_size + 1)
                self.table_size = (2 * prev_size + 1)
                self.num_items = 0
                for i in range(0, prev_size):
                    temp = prev_hash[i]
                    if temp != None:
                        self.insert(temp.key, temp.value)
            return
        if self.hash_table[hash_key].key == key:
            self.hash_table[hash_key].value = value
            return
        """in case of collision"""
        j = 1
        k = (hash_key + j**2) % self.table_size
        while self.hash_table[k] != None:
            if self.hash_table[k].key == key:
                self.hash_table[k].value = value
                return
            k = (k + j**2) % self.table_size
            j += 1
        self.num_items += 1
        self.hash_table[k] = info(key, value)
        if self.get_load_factor() > 0.5:
            prev_hash = self.hash_table
            prev_size = self.table_size
            self.hash_table = [None] * (2 * prev_size + 1)
            self.table_size = (2 * prev_size + 1)
            self.num_items = 0
            for i in range(0, prev_size):
                temp = prev_hash[i]
                if temp != None:
                    self.insert(temp.key, temp.value)



    def horner_hash(self, key: str) -> int:
        """ Compute and return an integer from 0 to the (size of the hash table) - 1
        Compute the hash value by using Horner’s rule, as described in project specification.
        """
        n = min(len(key), 8)
        idx = 0
        for i in range(0, n):
            idx = idx + (ord(key[i]) * 31**(n - 1 - i))
        yeah = idx % self.table_size
        return int(yeah)


    def in_table(self, key: str) -> bool:
        """ Returns True if key is in an entry of the hash table, False otherwise. Must be O(1)."""
        hash_key = self.horner_hash(key)
        if self.hash_table[hash_key] != None:
            if self.hash_table[hash_key].key == key:
                return True
            j = 1
            k = (hash_key + j**2) % self.table_size
            while self.hash_table[k] != None:
                if self.hash_table[k].key == key:
                    return True
                k = (k + j**2) % self.table_size
                j += 1
        return False

    def get_index(self, key: str) -> Optional[int]:
        """ Returns the index of the hash table entry containing the provided key. 
        If there is not an entry with the provided key, returns None. Must be O(1)."""
        hash_key = self.horner_hash(key)
        if self.hash_table[hash_key] != None:
            if self.hash_table[hash_key].key == key:
                return hash_key
            else:
                """in case of collision"""
                j = 1
                k = (hash_key + j**2) % self.table_size
                while self.hash_table[k] != None:
                    if self.hash_table[k].key == key:
                        return k
                    k = (k + j**2) % self.table_size
                    j += 1
        return None


    def get_all_keys(self) -> List:
        """ Returns a Python list of all keys in the hash table."""
        keys = []
        for i in range(0, self.table_size):
            if self.hash_table[i] != None:
                if self.hash_table[i].key != None:
                    keys.append(self.hash_table[i].key)
        return keys

    def get_value(self, key: str) -> Any:
        """ Returns the value (for concordance, list of line numbers) associated with the key.
        If key is not in hash table, returns None. Must be O(1)."""
        hash_key = self.horner_hash(key)
        if self.hash_table[hash_key] != None:
            if self.hash_table[hash_key].key == key:
                return self.hash_table[hash_key].value
            else:
                """in case of collison"""
                j = 1
                k = (hash_key + j**2) % self.table_size
                while self.hash_table[k] != None:
                    if self.hash_table[k].key == key:
                        return self.hash_table[k].value
                    k = (k + j**2) % self.table_size
                    j += 1
        return None


    def get_num_items(self) -> int:
        """ Returns the number of entries (words) in the table. Must be O(1)."""
        return self.num_items

    def get_table_size(self) -> int:
        """ Returns the size of the hash table."""
        return self.table_size

    def get_load_factor(self) -> float:
        """ Returns the load factor of the hash table (entries / table_size)."""
        return self.num_items / self.table_size


