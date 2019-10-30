# CS3
# Angel Rodriguez II
# Lab 4 - Option B
# Diego Aguirre
# 10-29-2019
# Purpose: The purpose of this code is to utilize a B-tree to store all of the
#              words in the english dictionary. This code contains a method that will create all the permutations of a
#               word and search them in the B-tree.


import sys
import time

def print_anagrams(word, prefix=""):
   if len(word) <= 1:
       str = prefix + word

       if (tree.search(str) == True):
          print(prefix + word)
   else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur

           if cur not in before: # Check if permutations of cur have not been generated.
              print_anagrams(before + after, prefix + cur)

def count_anagrams(word, prefix=""):
   count = 0
   if len(word) <= 1:
       str = prefix + word

       if (tree.search(str) == True):
           return 1 # adds 1 to the recursive call
   else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur

           if cur not in before: # Check if permutations of cur have not been generated.
              count += count_anagrams(before + after, prefix + cur) # recursive call that will add count
   return count


def find_max_anagrams(list): # this method will find the word with the most amount of anagrams given a list
    max = 0
    word = ""
    for i in range(len(list)):
        num = count_anagrams(list[i]) # sets the returned value of the method to num
        if num > max: # if num is greater than max, this if-statement will execute
            max = num
            word = list[i]
    print(word) #prints the word with the most amount of anagrams

class BTreeNode:
    # Constructor
    def __init__(self, keys=[], children=[], is_leaf=True, max_num_keys=5):
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf
        if max_num_keys < 3:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys = 3
        if max_num_keys % 2 == 0:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys += 1
        self.max_num_keys = max_num_keys

    def is_full(self):
        return len(self.keys) >= self.max_num_keys


class BTree:
    # Constructor
    def __init__(self, max_num_keys=5):
        self.max_num_keys = max_num_keys
        self.root = BTreeNode(max_num_keys=max_num_keys)

    def find_child(self, k, node=None):
        # Determines value of c, such that k must be in subtree node.children[c], if k is in the BTree
        if node is None:
            node = self.root

        for i in range(len(node.keys)):
            if k < node.keys[i]:
                return i
        return len(node.keys)

    def insert_internal(self, i, node=None):

        if node is None:
            node = self.root

        # node cannot be Full
        if node.is_leaf:
            self.insert_leaf(i, node)
        else:
            k = self.find_child(i, node)
            if node.children[k].is_full():
                m, l, r = self.split(node.children[k])
                node.keys.insert(k, m)
                node.children[k] = l
                node.children.insert(k + 1, r)
                k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def split(self, node=None):
        if node is None:
            node = self.root
        # print('Splitting')
        # PrintNode(T)
        mid = node.max_num_keys // 2
        if node.is_leaf:
            left_child = BTreeNode(node.keys[:mid], max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], max_num_keys=node.max_num_keys)
        else:
            left_child = BTreeNode(node.keys[:mid], node.children[:mid + 1], node.is_leaf, max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], node.children[mid + 1:], node.is_leaf, max_num_keys=node.max_num_keys)
        return node.keys[mid], left_child, right_child

    def insert_leaf(self, i, node=None):
        if node is None:
            node = self.root

        node.keys.append(i)
        node.keys.sort()

    def leaves(self, node=None):
        if node is None:
            node = self.root
        # Returns the leaves in a b-tree
        if node.is_leaf:
            return [node.keys]
        s = []
        for c in node.children:
            s = s + self.leaves(c)
        return s

    def insert(self, i, node=None):
        if node is None:
            node = self.root
        if not node.is_full():
            self.insert_internal(i, node)
        else:
            m, l, r = self.split(node)
            node.keys = [m]
            node.children = [l, r]
            node.is_leaf = False
            k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])
    def height(self, node=None):  # Quiz question 4
        if node is None:
            node = self.root
        if node.is_leaf:
            return 0
        return 1 + self.height(node.children[0])

    def print(self, node=None):
        # Prints keys in tree in ascending order
        if node is None:
            node = self.root

        if node.is_leaf:
            for t in node.keys:
                print(t)
        else:
            for i in range(len(node.keys)):
                self.print(node.children[i])
                print(node.keys[i])
            self.print(node.children[len(node.keys)])

    def print_d(self, space, node=None):
        if node is None:
            node = self.root
        # Prints keys and structure of B-tree
        if node.is_leaf:
            for i in range(len(node.keys) - 1, -1, -1):
                print(space, node.keys[i])
        else:
            self.print_d(space + '   ', node.children[len(node.keys)])
            for i in range(len(node.keys) - 1, -1, -1):
                print(space, node.keys[i])
                self.print_d(space + '   ', node.children[i])

    def search(self, k, node=None):
        if node is None:
            node = self.root
        # Returns node where k is, or None if k is not in the tree
        if k in node.keys:
            return True
        if node.is_leaf:
            return False
        return self.search(k, node.children[self.find_child(k, node)])

    def _set_x(self, dx, node=None):
        if node is None:
            node = self.root
        # Finds x-coordinate to display each node in the tree
        if node.is_leaf:
            return
        else:
            for c in node.children:
                self._set_x(dx, c)
            d = (dx[node.children[0].keys[0]] + dx[node.children[-1].keys[0]] + 10 * len(node.children[-1].keys)) / 2
            dx[node.keys[0]] = d - 10 * len(node.keys) / 2


list = []
with open("words.txt", "r") as f: # opens the given file name in read mode and closed the file when the code is finished executing
    for line in f:
        # print(line, end="")
        current_line = line.split() # splits the lines in the text file where there is white space
        word = current_line[0]
        list.append(word)  # appends the passwords to a list

test_list = []
with open("test_words.txt", "r") as f: # opens the given file name in read mode and closed the file when the code is finished executing
    for line in f:
        # print(line, end="")
        current_line = line.split() # splits the lines in the text file where there is white space
        word = current_line[0]
        test_list.append(word)  # appends the passwords to a list


tree = BTree(max_num_keys=20)

for each in list:
    tree.insert(each)

# print_anagrams("spot")
# print(count_anagrams("spot"))
# find_max_anagrams(test_list)
# print(tree.search("spot"))

