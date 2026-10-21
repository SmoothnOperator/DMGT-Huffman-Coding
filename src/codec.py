"""
Huffman Bitstream Encoder and Decoder (Codec)
Module: src/codec.py
Role: Piyush (Encoder/Decoder & Lossless Verification)
Discrete Mathematics & Graph Theory - Experiential Learning Project
"""

from typing import Dict, Tuple
from src.huffman import HuffmanNode


class HuffmanCodec:
    """
    Handles bit-level serialization, packing, and tree-based decoding.
    Demonstrates lossless data recovery.
    """

    @staticmethod
    def encode_to_bitstring(text: str, codes: Dict[str, str]) -> str:
        """Converts plaintext to a continuous sequence of '0' and '1' characters."""
        return "".join(codes[char] for char in text)

    @staticmethod
    def pad_bitstring(bitstring: str) -> Tuple[bytes, int]:
        """
        Pads the bitstring to a multiple of 8 bits and packs into raw bytes.
        Returns (packed_bytes, padding_amount).
        """
        extra_padding = (8 - len(bitstring) % 8) % 8
        padded_bitstring = bitstring + ("0" * extra_padding)

        byte_arr = bytearray()
        for i in range(0, len(padded_bitstring), 8):
            byte_chunk = padded_bitstring[i:i + 8]
            byte_arr.append(int(byte_chunk, 2))

        return bytes(byte_arr), extra_padding

    @staticmethod
    def unpad_and_unpack(packed_bytes: bytes, extra_padding: int) -> str:
        """Unpacks raw bytes into a bitstring, stripping away the padding bits."""
        bit_chunks = [f"{b:08b}" for b in packed_bytes]
        bitstring = "".join(bit_chunks)
        if extra_padding > 0:
            bitstring = bitstring[:-extra_padding]
        return bitstring

    @staticmethod
    def decode_from_bitstring(bitstring: str, root: HuffmanNode) -> str:
        """
        Traverses the binary tree bit-by-bit from root to leaves.
        - '0' navigates left
        - '1' navigates right
        - Leaf node emits the decoded character and resets navigation to root.
        """
        if not bitstring:
            return ""

        # Special case: single unique character tree
        if root.left and root.left.is_leaf() and root.right is None:
            return root.left.char * len(bitstring)

        decoded_chars = []
        current = root

        for bit in bitstring:
            if bit == "0":
                current = current.left
            elif bit == "1":
                current = current.right
            else:
                raise ValueError(f"Invalid bit in stream: {bit}")

            if current.is_leaf():
                decoded_chars.append(current.char)
                current = root

        return "".join(decoded_chars)

    @classmethod
    def verify_lossless(cls, original_text: str, decoded_text: str) -> bool:
        """Verifies mathematical idempotency: D(E(M)) == M."""
        return original_text == decoded_text
