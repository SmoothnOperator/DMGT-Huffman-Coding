"""
Unit Tests for Huffman Coding & Codec Pipeline
Module: tests/test_huffman.py
Role: Piyush & Nikhil
"""

import os
import sys

# Ensure project root is always in sys.path regardless of where pytest is run from
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import math
from src.huffman import HuffmanTree, HuffmanNode
from src.shannon_fano import ShannonFanoTree
from src.codec import HuffmanCodec


def test_basic_lossless_roundtrip():
    text = "this is an experiential learning project in discrete mathematics"
    tree = HuffmanTree()
    root = tree.build_tree(text)
    codes = tree.get_codes()

    # Encode
    bitstring = HuffmanCodec.encode_to_bitstring(text, codes)
    packed_bytes, padding = HuffmanCodec.pad_bitstring(bitstring)

    # Decode
    unpacked_bits = HuffmanCodec.unpad_and_unpack(packed_bytes, padding)
    decoded = HuffmanCodec.decode_from_bitstring(unpacked_bits, root)

    assert decoded == text
    assert HuffmanCodec.verify_lossless(text, decoded)


def test_prefix_property():
    text = "abracadabra$banana$apple$discrete$graph$tree"
    tree = HuffmanTree()
    tree.build_tree(text)
    codes = tree.get_codes()

    # Check that no code is a prefix of another
    code_list = list(codes.values())
    for i, c1 in enumerate(code_list):
        for j, c2 in enumerate(code_list):
            if i != j:
                assert not c2.startswith(c1), f"Prefix violation: {c1} is prefix of {c2}"


def test_kraft_inequality():
    text = "the quick brown fox jumps over the lazy dog 1234567890"
    tree = HuffmanTree()
    tree.build_tree(text)
    is_valid, kraft_sum = tree.verify_kraft_inequality()
    assert is_valid
    assert kraft_sum <= 1.0 + 1e-9


def test_entropy_bound():
    text = "aaabbbcccdddeeefffggghhhiiijjjkkklll"
    tree = HuffmanTree()
    tree.build_tree(text)
    entropy = tree.calculate_entropy()
    avg_len = tree.calculate_average_code_length()

    # By Shannon's Source Coding Theorem: H(X) <= L(C) < H(X) + 1
    assert avg_len >= entropy - 1e-9
    assert avg_len < entropy + 1.0


def test_single_character_edge_case():
    text = "AAAAAAAAAA"
    tree = HuffmanTree()
    root = tree.build_tree(text)
    codes = tree.get_codes()

    assert codes["A"] == "0"
    bitstring = HuffmanCodec.encode_to_bitstring(text, codes)
    decoded = HuffmanCodec.decode_from_bitstring(bitstring, root)
    assert decoded == text


def test_shannon_fano_vs_huffman_optimality():
    text = "AAAAAAAABBBCCCCDDDEEEFFFGGGHHH"
    huffman = HuffmanTree()
    huffman.build_tree(text)
    huff_len = huffman.calculate_average_code_length()

    sf = ShannonFanoTree()
    sf.build_tree(text)
    sf_len = sf.calculate_average_code_length()

    # Huffman is proven mathematically optimal: L_huff <= L_sf
    assert huff_len <= sf_len + 1e-9
