
class TrieNode(object):
    """Trie node 
    """
    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.is_word = False
        self.counter = 1


class Trie(object):

    def __init__(self):
        self.is_trained = False 
        self.root = TrieNode('*')

    @property
    def words(self):
        words = []        
        node = self.root
        self._iterate_until_leave(node, prefix='', words=words)
        return words

    def fit(self, words):
        for word in words:
            self.add_word(word)

    def add_word(self, word):
        node = self.root
        for char in word:
            found_in_children, node = self.__char_in_children_update(char, node)
            if not found_in_children:
                new_node = TrieNode(char)
                node.children.append(new_node)
                node = new_node

        node.is_word = True

    def word_count(self, word: str):
        """Check if a word is in a trie
        """
        node = self.root
        word_counts = 0
        word_finished = False
        for char in word:
            found_in_children, node = self._check_char_in_children(char, node)
            word_counts = node.counter
            word_finished = node.is_word        
            if not found_in_children:
                return 0
            
        return word_counts * word_finished

    def find_words_with_prefix(self, prefix):
        words = []
        root_pref = self._prefix_node_in_trie(self.root, prefix)
        if root_pref:
            self._iterate_until_leave(root_pref, prefix, words)
        
        return words

    def _iterate_until_leave(self, node, prefix, words):
        if node.is_word:
            words.append(prefix)
        for child in node.children:
            self._iterate_until_leave(child, prefix + child.char, words)

    def _prefix_node_in_trie(self, root, word: str):
        """find node that matches a prefix
        """
        node = root
        for char in word:
            found_in_children, node = self._check_char_in_children(char, node)
            if not found_in_children:
                return False
            
        return node

    def _check_char_in_children(self, char, node):
        """Update `node` and `found_in_children` flag variable and return them.
        
        If `char` is in a children of `node` return the matching node and  `found_in_children=True`.
        Otherwise, return the incoming node and `found_in_children=False`
        """
        found_in_children = False
        for node_children in node.children:
            if node_children.char == char:
                node = node_children         # modifies node
                found_in_children = True
                break
        return found_in_children, node

    def __char_in_children_update(self, char, node):
        """Update `node` and `found_in_children` flag variable and return them.
        
        If `char` is in a children of `node` return the matching node and  `found_in_children=True`.
        Otherwise, return the incoming node and `found_in_children=False`
        """
        found_in_children = False
        for node_children in node.children:
            if node_children.char == char:
                node_children.counter += 1
                node = node_children         # modifies node
                found_in_children = True
                break
        return found_in_children, node
