"""
Baseline Shannon-Fano Coding Implementation
Module: src/shannon_fano.py
Role: Baseline implementation for quantitative comparison against Huffman Coding
Discrete Mathematics & Graph Theory - Experiential Learning Project
"""

import math
from collections import Counter
from typing import Dict, List, Tuple


class ShannonFanoTree:
    """
    Shannon-Fano coding is a top-down greedy partitioning technique.
    Unlike Huffman coding (which is bottom-up and mathematically optimal),
    Shannon-Fano can result in suboptimal prefix trees.
    """
    def __init__(self):
        self.codes: Dict[str, str] = {}
        self.frequencies: Dict[str, int] = {}
        self.total_symbols: int = 0

    def build_tree(self, text: str) -> Dict[str, str]:
        """Builds Shannon-Fano prefix codes from input text."""
        if not text:
            raise ValueError("Input text cannot be empty.")

        self.frequencies = dict(Counter(text))
        self.total_symbols = len(text)
        sorted_symbols = sorted(self.frequencies.items(), key=lambda x: x[1], reverse=True)

        self.codes = {char: "" for char, _ in sorted_symbols}
        self._partition(sorted_symbols)
        return self.codes

    def _partition(self, symbol_list: List[Tuple[str, int]]):
        """Top-down recursive partition balancing the sum of frequencies."""
        if len(symbol_list) <= 1:
            return

        if len(symbol_list) == 2:
            self.codes[symbol_list[0][0]] += "0"
            self.codes[symbol_list[1][0]] += "1"
            return

        total_sum = sum(freq for _, freq in symbol_list)
        half_sum = total_sum / 2.0

        running_sum = 0
        split_idx = 0
        min_diff = float("inf")

        for i, (_, freq) in enumerate(symbol_list):
            running_sum += freq
            diff = abs(running_sum - half_sum)
            if diff < min_diff:
                min_diff = diff
                split_idx = i + 1

        # Assign prefix '0' to top partition, '1' to bottom partition
        for char, _ in symbol_list[:split_idx]:
            self.codes[char] += "0"
        for char, _ in symbol_list[split_idx:]:
            self.codes[char] += "1"

        self._partition(symbol_list[:split_idx])
        self._partition(symbol_list[split_idx:])

    def calculate_average_code_length(self) -> float:
        """Expected code length for Shannon-Fano codes."""
        if self.total_symbols == 0:
            return 0.0
        weighted_len = sum(
            freq * len(self.codes[char])
            for char, freq in self.frequencies.items()
        )
        return weighted_len / self.total_symbols
