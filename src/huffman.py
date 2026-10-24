"""
Core Huffman Coding Implementation
Module: src/huffman.py
Role: Nikhil (Project Lead & Core Implementation)
Discrete Mathematics & Graph Theory - Experiential Learning Project
Topic 14: Optimal Prefix Codes and Data Compression Using Huffman Coding
"""

import heapq
import math
from collections import Counter
from typing import Dict, Optional, Tuple, List


class HuffmanNode:
    """
    Represents a vertex v in a weighted rooted binary tree T = (V, E).
    - Leaf nodes represent an alphabet symbol s in Sigma with weight w(s) = freq(s).
    - Internal nodes have no symbol (char=None) and weight equal to the sum of children weights.
    """
    _counter = 0  # Global tie-breaker for priority queue stability

    def __init__(self, char: Optional[str], freq: int):
        self.char: Optional[str] = char
        self.freq: int = freq
        self.left: Optional['HuffmanNode'] = None   # Edge label '0'
        self.right: Optional['HuffmanNode'] = None  # Edge label '1'
        self.node_id: int = HuffmanNode._counter
        HuffmanNode._counter += 1

    def __lt__(self, other: 'HuffmanNode') -> bool:
        """Min-heap ordering based on frequency, with node_id as fallback."""
        if self.freq != other.freq:
            return self.freq < other.freq
        return self.node_id < other.node_id

    def is_leaf(self) -> bool:
        """Returns True if the vertex is an external node (leaf)."""
        return self.left is None and self.right is None


class HuffmanTree:
    """
    Constructs the optimal prefix code tree and extracts binary codewords.
    Demonstrates discrete tree structures, greedy choice property, and optimal substructure.
    """
    def __init__(self):
        self.root: Optional[HuffmanNode] = None
        self.codes: Dict[str, str] = {}
        self.reverse_mapping: Dict[str, str] = {}
        self.frequencies: Dict[str, int] = {}
        self.total_symbols: int = 0

    def compute_frequencies(self, text: str) -> Dict[str, int]:
        """Calculates symbol frequencies and records total text length."""
        if not text:
            raise ValueError("Input text cannot be empty.")
        self.frequencies = dict(Counter(text))
        self.total_symbols = len(text)
        return self.frequencies

    def build_tree(self, text: str) -> HuffmanNode:
        """
        Builds the optimal binary tree using a Min-Heap priority queue.
        Time Complexity: O(n log n) where n is the alphabet size |Sigma|.
        """
        self.compute_frequencies(text)

        # Edge case: Alphabet size = 1 (single unique symbol)
        if len(self.frequencies) == 1:
            char = next(iter(self.frequencies))
            self.root = HuffmanNode(None, self.frequencies[char])
            self.root.left = HuffmanNode(char, self.frequencies[char])
            self.codes = {char: "0"}
            self.reverse_mapping = {"0": char}
            return self.root

        # Step 1: Initialize min-heap with all leaf nodes
        heap: List[HuffmanNode] = [
            HuffmanNode(char, freq) for char, freq in self.frequencies.items()
        ]
        heapq.heapify(heap)

        # Step 2: Greedily extract two smallest subtrees and merge
        while len(heap) > 1:
            node_left = heapq.heappop(heap)   # Smallest frequency
            node_right = heapq.heappop(heap)  # Second smallest frequency

            # Create internal node with summed weight
            merged_weight = node_left.freq + node_right.freq
            parent = HuffmanNode(None, merged_weight)
            parent.left = node_left
            parent.right = node_right

            heapq.heappush(heap, parent)

        # Final remaining node is the root of the optimal tree
        self.root = heapq.heappop(heap)

        # Step 3: Traverse the tree to generate prefix codes
        self.codes = {}
        self.reverse_mapping = {}
        self._generate_codes_dfs(self.root, "")
        return self.root

    def build_tree_with_history(self, text: str) -> Tuple[HuffmanNode, List[dict]]:
        """
        Builds the Huffman tree while capturing every step of the min-heap
        merging process for visual step-by-step explanation.
        """
        self.compute_frequencies(text)
        history: List[dict] = []

        if len(self.frequencies) == 1:
            char = next(iter(self.frequencies))
            self.root = HuffmanNode(None, self.frequencies[char])
            self.root.left = HuffmanNode(char, self.frequencies[char])
            self.codes = {char: "0"}
            self.reverse_mapping = {"0": char}
            history.append({
                "step": 0,
                "action": "Single Unique Character Edge Case",
                "extracted": [],
                "merged": (char, self.frequencies[char]),
                "heap": [(char, self.frequencies[char])]
            })
            return self.root, history

        # Initialize heap
        heap: List[HuffmanNode] = [
            HuffmanNode(char, freq) for char, freq in self.frequencies.items()
        ]
        heapq.heapify(heap)

        step_num = 0
        history.append({
            "step": step_num,
            "action": f"Initial Min-Priority Queue with {len(heap)} leaf vertices",
            "extracted": [],
            "merged": None,
            "heap": [(n.char if n.char is not None else f"Internal(w={n.freq})", n.freq) for n in sorted(heap)]
        })

        while len(heap) > 1:
            step_num += 1
            node_left = heapq.heappop(heap)
            node_right = heapq.heappop(heap)

            merged_weight = node_left.freq + node_right.freq
            parent = HuffmanNode(None, merged_weight)
            parent.left = node_left
            parent.right = node_right

            heapq.heappush(heap, parent)

            left_desc = f"'{node_left.char}' (w={node_left.freq})" if node_left.is_leaf() else f"Internal (w={node_left.freq})"
            right_desc = f"'{node_right.char}' (w={node_right.freq})" if node_right.is_leaf() else f"Internal (w={node_right.freq})"

            history.append({
                "step": step_num,
                "action": f"Extract-Min {left_desc} and {right_desc} -> Merge into Parent (w={merged_weight})",
                "extracted": [left_desc, right_desc],
                "merged": f"Internal Node (w={merged_weight})",
                "heap": [(n.char if n.char is not None else f"Internal(w={n.freq})", n.freq) for n in sorted(heap)]
            })

        self.root = heapq.heappop(heap)
        self.codes = {}
        self.reverse_mapping = {}
        self._generate_codes_dfs(self.root, "")
        return self.root, history

    def _generate_codes_dfs(self, node: Optional[HuffmanNode], current_code: str):
        """Depth-First Search recursive walk to extract prefix-free binary paths."""
        if node is None:
            return

        if node.is_leaf():
            # Leaf node reached: assign code
            self.codes[node.char] = current_code
            self.reverse_mapping[current_code] = node.char
            return

        # Convention: Left branch = '0', Right branch = '1'
        self._generate_codes_dfs(node.left, current_code + "0")
        self._generate_codes_dfs(node.right, current_code + "1")

    def get_codes(self) -> Dict[str, str]:
        """Returns {symbol: prefix_code}."""
        return self.codes

    def calculate_entropy(self) -> float:
        """
        Calculates Shannon Entropy H(X):
        H(X) = - sum_{s in Sigma} p(s) * log2(p(s))
        Theoretical lower bound on expected code length.
        """
        if self.total_symbols == 0:
            return 0.0
        entropy = 0.0
        for freq in self.frequencies.values():
            p = freq / self.total_symbols
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def calculate_average_code_length(self) -> float:
        """
        Calculates Expected Codeword Length L(C):
        L(C) = sum_{s in Sigma} p(s) * length(c(s))
        """
        if self.total_symbols == 0:
            return 0.0
        weighted_len = sum(
            freq * len(self.codes[char])
            for char, freq in self.frequencies.items()
        )
        return weighted_len / self.total_symbols

    def calculate_redundancy(self) -> float:
        """Calculates Code Redundancy R = L(C) - H(X) >= 0."""
        return self.calculate_average_code_length() - self.calculate_entropy()

    def verify_kraft_inequality(self) -> Tuple[bool, float]:
        """
        Verifies Kraft-McMillan Inequality:
        sum_{i=1}^n 2^(-l_i) <= 1
        """
        kraft_sum = sum(2 ** (-len(code)) for code in self.codes.values())
        return (kraft_sum <= 1.0 + 1e-9, kraft_sum)
