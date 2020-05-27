# Author: Chris Hardison
# Date: 05/27/2020
# Description: Program finds and returns most used words (top_words) within a given text file within a range provided
# by user with word and word count output utilizing a hash map to store/retrieve data.

import re
from hash_map import HashMap


rgx = re.compile("(\w[\w']*\w|\w)")


def hash_function_2(key):
    """
    This is a hash function that can be used for the hash map.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()  # Variable representing empty set.
    ht = HashMap(2500, hash_function_2)  # Variable to represent hash map construct utilizing above function.

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:  # Opens file to be used declaring it as variable 'f'.
        for line in f:  # Loops through each line within file (f).
            words = rgx.findall(line)  # Variable utilized to represent words within each line.
            for w in words:  # Loops through each word within each line.
                lw = w.lower()  # Turns words lowercase to remove case sensitivity.
                keys.add(lw)  # Adds lowercase word to set represented by variable 'key'.
                if ht.contains_key(lw):  # Checks if word is already present in hash map.
                    new_value = (ht.get(lw) + 1)  # Variable represents word count increased by one.
                    ht.put(lw, new_value)  # Inserts word into hash map to have word count be updated.
                else:
                    ht.put(lw, 1)  # Inserts word into hash map with initial count of one.
    keys_list = []  # Variable represents an empty list.
    for values in keys:  # Loops through words present in set represented by variable 'keys'.
        ind = ht._hash_function(values) % ht.capacity
        # Variable to represent number established by chosen function and available capacity.
        temp = ht._buckets[ind]  # Variable to represent position within hash map containing linked list.
        node = temp.contains(values)  # Variable to represent node containing key if already present.
        keys_list.append((node.key, node.value))  # Adds tuple to list containing word, word count.
    keys_list.sort(key=lambda tup: tup[1], reverse=True)  # Sorts list in descending order based on word count.
    return keys_list[0:number]  # Returns list of top words within given range provided by user.

# print(top_words("alice.txt",10))  # Test case.
