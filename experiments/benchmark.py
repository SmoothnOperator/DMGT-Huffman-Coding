"""
Experimental Suite & Quantitative Benchmarking
Module: experiments/benchmark.py
Role: Harsh (Experiments & Comparison)
Discrete Mathematics & Graph Theory - Experiential Learning Project
Topic 14: Optimal Prefix Codes and Data Compression Using Huffman Coding
"""

import os
import sys
import time
import math
import pandas as pd
import matplotlib.pyplot as plt

# Ensure root folder is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.huffman import HuffmanTree
from src.shannon_fano import ShannonFanoTree
from src.codec import HuffmanCodec


def run_experiment_1_data_types():
    """
    Experiment 1: Compression efficiency across distinct data domains.
    Compares: English text, Source code, Genomic DNA, Uniform text.
    Metrics: Shannon Entropy H(X), Huffman Avg Length L(C), Shannon-Fano Avg Length,
             Redundancy R, Compression Ratio, Time (ms).
    """
    print("\n" + "=" * 70)
    print("RUNNING EXPERIMENT 1: EFFICIENCY ACROSS DATA DOMAINS")
    print("=" * 70)

    datasets = {
        "English Text": "data/sample_english.txt",
        "Python Code": "data/sample_code.py",
        "Genomic DNA": "data/sample_dna.fasta",
        "Uniform Random": "data/sample_uniform.txt"
    }

    results = []

    for name, filepath in datasets.items():
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        n_chars = len(text)

        # Huffman
        start_time = time.perf_counter()
        huffman = HuffmanTree()
        root = huffman.build_tree(text)
        codes = huffman.get_codes()
        huff_time_ms = (time.perf_counter() - start_time) * 1000

        # Lossless verification
        encoded_bits = HuffmanCodec.encode_to_bitstring(text, codes)
        decoded_text = HuffmanCodec.decode_from_bitstring(encoded_bits, root)
        assert HuffmanCodec.verify_lossless(text, decoded_text), f"Verification failed for {name}"

        # Shannon-Fano
        sf = ShannonFanoTree()
        sf_codes = sf.build_tree(text)
        sf_avg_len = sf.calculate_average_code_length()

        # Metrics
        entropy = huffman.calculate_entropy()
        huff_avg_len = huffman.calculate_average_code_length()
        redundancy = huffman.calculate_redundancy()
        comp_ratio = (n_chars * 8.0) / len(encoded_bits)
        space_saving_pct = (1.0 - (len(encoded_bits) / (n_chars * 8.0))) * 100

        results.append({
            "Dataset": name,
            "Symbols (N)": n_chars,
            "Alphabet (|Sigma|)": len(huffman.frequencies),
            "Entropy H(X)": round(entropy, 4),
            "Huffman L(C)": round(huff_avg_len, 4),
            "Shannon-Fano L": round(sf_avg_len, 4),
            "Redundancy R": round(redundancy, 4),
            "Comp Ratio": round(comp_ratio, 2),
            "Space Savings (%)": round(space_saving_pct, 2),
            "Time (ms)": round(huff_time_ms, 3)
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    # Save CSV
    os.makedirs("experiments/plots", exist_ok=True)
    df.to_csv("experiments/plots/experiment1_results.csv", index=False)

    # Plot 1: Entropy vs Huffman Avg Length vs Shannon-Fano Avg Length
    plt.figure(figsize=(10, 6))
    x = range(len(df))
    width = 0.25

    plt.bar([i - width for i in x], df["Entropy H(X)"], width=width, label="Shannon Entropy H(X)", color="#2b8cbe")
    plt.bar(x, df["Huffman L(C)"], width=width, label="Huffman Avg Length L(C)", color="#31a354")
    plt.bar([i + width for i in x], df["Shannon-Fano L"], width=width, label="Shannon-Fano Length", color="#e6550d")

    plt.axhline(y=8.0, color="gray", linestyle="--", label="Fixed 8-Bit ASCII")
    plt.xticks(x, df["Dataset"], fontweight="bold")
    plt.ylabel("Bits per Symbol", fontsize=12)
    plt.title("Experiment 1: Information Limit vs. Prefix Code Lengths", fontsize=14, fontweight="bold")
    plt.legend()
    plt.grid(axis="y", linestyle=":", alpha=0.7)
    plt.tight_layout()
    plt.savefig("experiments/plots/exp1_entropy_vs_codelength.png", dpi=300)
    plt.close()
    print("[OK] Plot saved: experiments/plots/exp1_entropy_vs_codelength.png")

    return df


def run_experiment_2_varying_size():
    """
    Experiment 2: Algorithmic scaling across input sizes N.
    Compares: Execution time and code efficiency as N scales.
    Instances: N in [300, 1000, 5000, 20000, 100000] symbols.
    """
    print("\n" + "=" * 70)
    print("RUNNING EXPERIMENT 2: SCALING & RUNTIME VS. INPUT SIZE N")
    print("=" * 70)

    # Read base English text and repeat to generate controlled sizes
    with open("data/sample_english.txt", "r", encoding="utf-8") as f:
        base_text = f.read()

    sizes = [300, 1000, 5000, 20000, 100000]
    results = []

    for target_n in sizes:
        repeats = math.ceil(target_n / len(base_text))
        text = (base_text * repeats)[:target_n]

        # Huffman Benchmark
        t0 = time.perf_counter()
        huffman = HuffmanTree()
        root = huffman.build_tree(text)
        codes = huffman.get_codes()
        huff_time_ms = (time.perf_counter() - t0) * 1000

        # Shannon-Fano Benchmark
        t1 = time.perf_counter()
        sf = ShannonFanoTree()
        sf.build_tree(text)
        sf_time_ms = (time.perf_counter() - t1) * 1000

        results.append({
            "Input Size (N)": target_n,
            "Huffman Time (ms)": round(huff_time_ms, 3),
            "Shannon-Fano Time (ms)": round(sf_time_ms, 3),
            "Huffman Avg Length": round(huffman.calculate_average_code_length(), 4)
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    df.to_csv("experiments/plots/experiment2_results.csv", index=False)

    # Plot 2: Runtime scaling
    plt.figure(figsize=(9, 5))
    plt.plot(df["Input Size (N)"], df["Huffman Time (ms)"], marker="o", linewidth=2, color="#31a354", label="Huffman (Min-Heap)")
    plt.plot(df["Input Size (N)"], df["Shannon-Fano Time (ms)"], marker="s", linewidth=2, color="#e6550d", label="Shannon-Fano")
    plt.xlabel("Input Size N (Symbols)", fontsize=12)
    plt.ylabel("Execution Time (milliseconds)", fontsize=12)
    plt.title("Experiment 2: Execution Time Complexity Scaling", fontsize=14, fontweight="bold")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.tight_layout()
    plt.savefig("experiments/plots/exp2_runtime_scaling.png", dpi=300)
    plt.close()
    print("[OK] Plot saved: experiments/plots/exp2_runtime_scaling.png")

    return df


if __name__ == "__main__":
    run_experiment_1_data_types()
    run_experiment_2_varying_size()
