from typing import List, Set, Dict, Tuple


class TrieNode:
    def __init__(self, letter=None) -> None:
        self.letter = letter
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def starts_with(self, prefix: str) -> bool:
        startNode = self.root
        for char in prefix:
            if char not in startNode.children:
                return False
            startNode = startNode.children[char]
        return True

    def generate_tree_from_file(self) -> None:
        words = self._load_words()
        for word in words:
            startNode = self.root
            for char in reversed(word): 
                if char not in startNode.children:
                    startNode.children[char] = TrieNode(char)
                startNode = startNode.children[char]
            startNode.is_end_of_word = True 

    def return_end_of_word_boolean(self, prefix: str) -> bool:
        startNode = self.root
        for char in prefix:
            if char not in startNode.children:
                return False
            startNode = startNode.children[char]
        return startNode.is_end_of_word

    def _load_words(self):
        words = []
        with open("words.txt", "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                words.append(word)
        return words


# Boggle Solver
class Boggled:
    def setup_board(self, max_uses_per_tile: int, board: List[List[str]]) -> None:
        self.board = board
        self.max_uses_per_tile = max_uses_per_tile
        self.rowCount = len(board)
        self.colCount = len(board[0])
        self.trie = Trie()
        self.trie.generate_tree_from_file()
        self.words = set(self.trie._load_words())  

    def get_all_words(self, suffix: str) -> Set[str]:
        validWords = set()
    
        for r in range(self.rowCount):
            for c in range(self.colCount):
                self.get_all_words_recursive(r, c, suffix, "", {}, validWords, self.trie.root, 0)
        if suffix in validWords:
            validWords.remove(suffix)
        return validWords

    def get_all_words_recursive(
        self,
        r: int,
        c: int,
        suffix: str,
        currentWord: str,
        visitedSquares: Dict[Tuple[int, int], int],
        validWords: Set[str],
        node: TrieNode,
        suffix_index: int
    ):
        if r < 0 or r >= self.rowCount or c < 0 or c >= self.colCount:
            return

        if (r, c) in visitedSquares and visitedSquares[(r, c)] >= self.max_uses_per_tile:
            return

        tile = self.board[r][c]
        new_node = node
        added_letters = ""

        # Handle single-letter tiles
        if len(tile) == 1:
            letter = tile
            if suffix_index < len(suffix):
                expected_letter = suffix[::-1][suffix_index]
                if letter != expected_letter:
                    return
            if letter not in new_node.children:
                return
            new_node = new_node.children[letter]
            added_letters = letter

        # Handle multi-letter tiles (e.g., 'qu')
        else:
            reversed_tile = tile[::-1]
            for i in range(len(reversed_tile)):
                if suffix_index + i < len(suffix):
                    if reversed_tile[i] != suffix[::-1][suffix_index + i]:
                        return
                if reversed_tile[i] not in new_node.children:
                    return
                new_node = new_node.children[reversed_tile[i]]
            added_letters = reversed_tile

        currentWord += added_letters
        suffix_index += len(added_letters)

        if new_node.is_end_of_word and suffix_index >= len(suffix):
            validWords.add(currentWord[::-1])

        visitedSquares[(r, c)] = visitedSquares.get((r, c), 0) + 1

        directions = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                    (r, c - 1),             (r, c + 1),
                    (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
        for newRow, newCol in directions:
            self.get_all_words_recursive(
                newRow, newCol, suffix, currentWord,
                visitedSquares, validWords, new_node, suffix_index
            )

        # Backtrack
        visitedSquares[(r, c)] -= 1
        if visitedSquares[(r, c)] == 0:
            del visitedSquares[(r, c)]
