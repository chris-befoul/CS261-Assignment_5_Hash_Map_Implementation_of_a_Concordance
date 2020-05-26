# Author: Chris Hardison
# Date: 05/26/2020
# Description: Hash Map constructed of linked list within a list utilizing
#               key, value accommodating collisions and table resizing.


class SLNode:
    """Represents node within linked list containing key and value for said node."""

    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        """Returns string format of node."""
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    """Represents linked list within hash map."""

    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)  # Variable that represents new node containing chosen key and value.
        new_node.next = self.head
        self.head = new_node  # Establishes new node as head of chosen linked list.
        self.size = self.size + 1  # Increases size of linked list.

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:  # Checks if there is not a node present in linked list.
            return False
        if self.head.key == key:  # Checks if head key value is equal to chosen key value.
            self.head = self.head.next  # Removes head node and establishes next available node as head.
            self.size = self.size - 1  # Decreases linked list size.
            return True
        cur = self.head.next  # Establishes cur variable as second node in linked list.
        prev = self.head  # Establishes prev variable as head node in linked list.
        while cur is not None:  # Loop that iterates through list searching for chosen key to remove.
            if cur.key == key:  # Checks if cur variable key is equal to desired key.
                prev.next = cur.next  # Reestablishes prev.next as cur.next node to remove cur node.
                self.size = self.size - 1  # Decreases linked list size.
                return True
            prev = cur  # Reestablishes prev variable as cur node.
            cur = cur.next  # Reestablishes cur variable as cur.next node.
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
            key: key of node
        Return:
            node with matching key, otherwise None"""
        if self.head is not None:  # Checks to see if linked list is empty.
            cur = self.head  # Establishes cur variable as head node in linked list.
            while cur is not None:  # Loop that iterates through nodes in linked list for desired key.
                if cur.key == key:  # Checks if cur node key is equal to desired key.
                    return cur  # Returns node containing desired key.
                cur = cur.next  # Reestablishes cur variable as cur.next node.
        return None  # If node is not present in linked list.

    def __str__(self):
        """Returns string format of linked list."""
        out = '['
        if self.head is not None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur is not None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    """Function utilized for placement of keys within hash map."""
    hash = 0
    for i in key:  # Loops through each character in string representing key.
        hash = hash + ord(i)
        # Hash variable equals sum of hash and integer representing the Unicode code point of that character
    return hash


def hash_function_2(key):
    """Function utilized for placement of keys within hash map."""
    hash = 0
    index = 0
    for i in key:  # Loops through each character in string representing key.
        hash = hash + (index + 1) * ord(i)
        # Hash variable equals hash added to index plus one multiplied
        # by integer representing the Unicode code point of that character.
        index = index + 1  # Index is increased by one.
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):  # Loops until reaches capacity established by user.
            self._buckets.append(LinkedList())  # Fills self._buckets with linked list until capacity is reached.
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table in string format.
        """
        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        count = 0  # Establishes count variable as zero.
        for bucket in self._buckets:  # Loops through hash map.
            if bucket.size == 0:  # Checks if bucket or current position is empty.
                count += 1  # Increases count by one.
        return count

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        load = float(self.size / self.capacity)
        return load

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        ind = self._hash_function(key) % self.capacity
        # Variable to represent number established by chosen function and available capacity.
        temp = self._buckets[ind]  # Variable to represent position within hash map containing linked list.
        node = temp.contains(key)  # Variable to represent node containing key if already present.
        if node is not None:  # Checks if key was already present in hash map.
            node.value = value  # Updates value at key to newly chosen value.
            return
        else:
            temp.add_front(key, value)  # New node is added at position represented by temp variable.
            self.size += 1  # Increases hash map size by one.
            return

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        ind = self._hash_function(key) % self.capacity
        # Variable to represent number established by chosen function and available capacity.
        temp = self._buckets[ind]  # Variable to represent position within hash map containing linked list.
        if temp.contains(key) is not None:  # Checks if key was already present in hash map.
            return True
        else:
            return False

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        for bucket in self._buckets:  # Loops through hash map.
            if bucket.size > 0:  # Checks if bucket/current position contains data.
                bucket.head = None  # Removes data from said position.
                bucket.size = 0  # Linked list at current position's size is reduced to zero.
        self.size = 0  # Hash map size is reduced to zero.
        return

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        ind = self._hash_function(key) % self.capacity
        # Variable to represent number established by chosen function and available capacity.
        temp = self._buckets[ind]  # Variable to represent position within hash map containing linked list.
        node = temp.contains(key)  # Variable to represent node containing key if already present.
        if node is not None:  # Checks if key is present in hash map.
            return node.value  # Returns value represented by chosen key.
        else:
            return None  # If key is not present in hash map.

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        ind = self._hash_function(key) % self.capacity
        # Variable to represent number established by chosen function and available capacity.
        temp = self._buckets[ind]  # Variable to represent position within hash map containing linked list.
        if temp.remove(key) is False:  # Checks if chosen key was not present in hash map.
            return
        else:
            self.size = (self.size - 1)  # Decreases hash map size by one.
            return

    def resize_table(self, capacity):
        """
        Resize the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        new = []  # Variable to represent newly designed hash map.
        for i in range(capacity):  # Iterates until newly chosen capacity has been reached.
            new.append(LinkedList())  # Inserts linked list within newly designed hash map.
        self.capacity = capacity  # Reestablishes hash map capacity to newly chosen capacity.
        for bucket in self._buckets:  # Iterates through old hash map.
            if bucket.head is not None:  # Checks if data is present in bucket/current position.
                cur = bucket.head  # Variable to represent head node.
                while cur is not None:  # Loops through current position linked list.
                    ind = self._hash_function(cur.key) % self.capacity
                    # Variable to represent number established by chosen function and available capacity.
                    temp = new[ind]  # Variable to represent position within new hash map containing linked list.
                    temp.add_front(cur.key, cur.value)  # Inserts data from old hash map to new rehashing data.
                    cur = cur.next  # Reestablishes cur variable as next available node in linked list.
        self._buckets = new  # Removes old hash map implementing new hash map with new capacity and rehashed data.
        return
