# Presentation Slides & Speaking Script (10 Slides)

**Course:** Discrete Mathematics and Graph Theory (CSE-BCT)  
**Topic 14:** Optimal Prefix Codes and Data Compression Using Huffman Coding  
**Team Members (6):** Nikhil, Piyush, Sakshi, Arushi, Harsh, Khyathi  

---

### Slide 1: Title & Team Overview
* **Title:** Optimal Prefix Codes & Lossless Data Compression Using Huffman Coding
* **Subtitle:** An Information-Theoretic and Graph-Based Approach
* **Programme:** CSE — Blockchain Technology
* **Presenter:** Nikhil (Project Lead)
* **Key Points on Slide:**
  - Problem Statement: Maximizing data compression efficiency using discrete tree structures.
  - Team Members & Assigned Roles.
  - GitHub Repository: `SmoothnOperator/DMGT-Huffman-Coding`.

---

### Slide 2: Real-World Relevance & Motivation
* **Presenter:** Nikhil
* **Key Points on Slide:**
  - Why compression matters: Bandwidth reduction, block-size minimization in distributed networks and blockchains.
  - Real-world deployments of Huffman Coding: DEFLATE (ZIP, gzip), JPEG image encoding, MP3 audio.
  - Project Goal: Implement, verify, and mathematically evaluate Huffman tree construction and lossless recovery.

---

### Slide 3: Discrete Mathematics & Graph Theoretical Formulation
* **Presenter:** Sakshi (Theory & Math)
* **Key Points on Slide:**
  - Graph representation: Directed rooted binary tree $T = (V, E)$.
  - Leaf vertices: $v_i \in \Sigma$ with weight $w(v_i) = \text{freq}(s_i)$.
  - Codeword length $l_i = \text{depth}(v_i)$ from root.
  - Instantaneous Prefix Property: $\forall i \ne j, \; c(s_i) \not\sqsubseteq c(s_j)$ (unique decodability without delimiters).
  - Kraft–McMillan Inequality: $\sum_{i=1}^n 2^{-l_i} \le 1.0$ (Strict equality $= 1.0$ in our full trees).

---

### Slide 4: Information Limits & Shannon Entropy Bound
* **Presenter:** Sakshi
* **Key Points on Slide:**
  - Shannon Entropy: $H(X) = -\sum p_i \log_2(p_i)$ (absolute theoretical limit).
  - Source Coding Theorem: $H(X) \le L(C) < H(X) + 1$.
  - Redundancy: $R = L(C) - H(X) \ge 0$.
  - Greedy choice property & optimal substructure: Merging two lowest-weight nodes guarantees minimum total weighted path length $\sum w(v_i) \cdot \text{depth}(v_i)$.

---

### Slide 5: Algorithm Design & Min-Heap Architecture
* **Presenter:** Nikhil (Core Implementation)
* **Key Points on Slide:**
  - Bottom-up greedy construction using Min-Priority Queue (`heapq`).
  - Step 1: Push leaf nodes into min-heap.
  - Step 2: Greedily extract 2 lowest-frequency subtrees, merge into parent, re-insert.
  - Step 3: DFS walk (Left = `'0'`, Right = `'1'`) generates optimal prefix codes.
  - Time Complexity: $\mathcal{O}(|\Sigma| \log |\Sigma|)$ for tree build; $\mathcal{O}(N)$ for text encoding.
  - Baseline: Shannon–Fano top-down recursive frequency partition.

---

### Slide 6: Bit-Level Codec & Lossless Verification
* **Presenter:** Piyush (Codec & Verification)
* **Key Points on Slide:**
  - Bitstream Packing: Continuous bit sequences packed into 8-bit bytes with padding counter.
  - Tree-Walk Decoder: Bitstream directly walks tree from root; leaf hits emit symbol and reset pointer.
  - Verification: Mathematical idempotency $\mathcal{D}(\mathcal{E}(M)) = M$ proven across all files.
  - Pytest Suite: 6/6 tests passing (lossless roundtrip, Kraft inequality, prefix property, single-symbol edge cases).

---

### Slide 7: Datasets & Information-Theoretic Diversity
* **Presenter:** Arushi (Dataset & Preprocessing)
* **Key Points on Slide:**
  - Guidelines compliance: All datasets exceed $\ge 300$ data points requirement.
  - 4 Datasets analyzed:
    1. English Text ($N = 2,001$, $|\Sigma| = 56$, Entropy $= 4.39$ bits)
    2. Python Code ($N = 1,432$, $|\Sigma| = 53$, Entropy $= 4.39$ bits)
    3. Genomic DNA FASTA ($N = 1,031$, $|\Sigma| = 29$, Entropy $= 2.26$ bits)
    4. Uniform Random Text ($N = 1,140$, $|\Sigma| = 76$, Entropy $= 6.25$ bits)
  - Key Insight: DNA has low symbol entropy $\rightarrow$ yields highest compression.

---

### Slide 8: Experiment 1 Results — Cross-Domain Compression
* **Presenter:** Harsh (Experiments & Comparison)
* **Key Points on Slide:**
  - Show Table 1 (Comparison: Entropy vs. Huffman vs. Shannon–Fano vs. ASCII).
  - DNA Compression: **3.37:1 ratio (70.37% space savings)**.
  - English Text: **1.81:1 ratio (44.78% space savings)** with redundancy $R = 0.0279$ bits/sym.
  - Huffman vs. Shannon–Fano: Huffman achieves equal or strictly lower expected length in all cases ($L_{\text{Huffman}} \le L_{\text{SF}}$).

---

### Slide 9: Experiment 2 Results — Runtime Complexity & Tree Visualization
* **Presenter:** Harsh & Khyathi (Visualization)
* **Key Points on Slide:**
  - Scaling test: $N = 300$ to $100,000$ symbols (execution time $< 3.7$ ms).
  - Display NetworkX Tree Visualization: Root, internal nodes with weights, leaf symbols, edge labels (`0` and `1`).
  - Linear scaling confirms algorithm is suitable for high-throughput streaming environments.

---

### Slide 10: Conclusion, Future Scope & Q&A
* **Presenter:** Khyathi & All Members
* **Key Points on Slide:**
  - Summary: DMGT rooted trees solve optimal prefix coding with provable bounds.
  - Limitations: Codebook header transmission overhead on tiny files ($N < 200$).
  - Future Scope: Adaptive Dynamic Huffman (Vitter/FGK), Arithmetic Coding for non-integer bit allocation.
  - Open for Faculty Questions & Defense.
