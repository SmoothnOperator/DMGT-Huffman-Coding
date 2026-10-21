# Information-Theoretic Data Compression via Optimal Prefix Trees: An Empirical and Algorithmic Analysis of Huffman Coding

**Programme:** B.Tech. Computer Science and Engineering — Blockchain Technology (CSE-BCT)  
**Course:** Discrete Mathematics and Graph Theory (DMGT) — Experiential Learning  
**Project Topic 14:** Optimal Prefix Codes and Data Compression Using Huffman Coding  

**Authors & Group Members:**  
1. **Nikhil** (Project Lead & Core Implementation)  
2. **Piyush** (Encoder/Decoder & Verification)  
3. **Sakshi** (Mathematical Formulation & Theory)  
4. **Arushi** (Dataset Collection & Preprocessing)  
5. **Harsh** (Experimental Design & Benchmarking)  
6. **Khyathi** (Visualization, Documentation & Presentation)  

---

## Abstract
Lossless data compression is fundamentally rooted in information theory and discrete mathematics, specifically in the structural properties of rooted weighted trees. This research investigates the mathematical foundations, computational implementation, and empirical performance of Huffman coding—a greedy algorithm that produces optimal prefix-free binary codes. We formally define prefix codes over discrete alphabets, prove adherence to the Kraft–McMillan inequality ($\sum 2^{-l_i} \le 1$), and examine convergence toward the theoretical lower bound dictated by Shannon's Source Coding Theorem ($H(X) \le L(C) < H(X) + 1$). Using Python and min-priority queues, we implement a full compression pipeline and benchmark it against both fixed-length 8-bit ASCII encoding and the top-down Shannon–Fano heuristic. The empirical evaluation spans four diverse datasets exceeding 1,000 data points each: natural language corpus, programming source code, genomic nucleotide sequences (FASTA), and synthetic uniform random sequences. Experimental results confirm that Huffman coding consistently achieves minimal redundancy ($R \le 0.1113$ bits/symbol), reaching a maximum compression ratio of 3.37:1 (70.37% space reduction) on genomic sequences. Runtime scaling tests across problem instances from $N = 300$ to $N = 100,000$ confirm $\mathcal{O}(|\Sigma| \log |\Sigma|)$ tree construction and linear $\mathcal{O}(N)$ encoding complexity. Tree topologies and decision paths are visually rendered via NetworkX.

**Keywords:** Huffman Coding, Optimal Prefix Codes, Rooted Binary Trees, Shannon Entropy, Lossless Data Compression.

---

## 1. Introduction

Data representation and transmission efficiency represent cornerstone challenges in theoretical computer science, information theory, and distributed systems. In modern distributed architectures, including peer-to-peer networks and blockchain ledgers, minimizing block payload and bandwidth consumption directly impacts throughput, propagation delay, and storage costs. Lossless data compression techniques provide mathematically guaranteed space reduction while preserving complete data integrity.

Historically, source coding gained formal footing in 1948 when Claude E. Shannon introduced information entropy as the fundamental absolute limit of compression. In 1952, David A. Huffman introduced an elegant, bottom-up greedy algorithmic formulation that constructs prefix-free binary codes whose expected length is mathematically provable to be optimal for any given symbol frequency distribution.

The primary objectives of this experiential learning project are:
1. To formulate data compression using graph-theoretic structures—specifically weighted, rooted binary trees and directed walks.
2. To mathematically evaluate the prefix property, the Kraft–McMillan inequality, and Shannon entropy bounds.
3. To develop an end-to-end computational pipeline in Python performing tree generation, bitstream serialization, byte-packing, and lossless tree-walk decoding.
4. To conduct rigorous quantitative experiments comparing Huffman coding against fixed-length encoding and Shannon–Fano coding across diverse data distributions exceeding the required 300 data points.
5. To visually analyze prefix tree structures and edge assignments using NetworkX and Matplotlib.

---

## 2. Methodology

### 2.1 Theoretical Foundation & Discrete Structures
Let $\Sigma = \{s_1, s_2, \dots, s_n\}$ denote a finite source alphabet containing $n$ distinct symbols. Each symbol $s_i$ possesses an occurrence frequency $f_i$ across a source text of length $N$, with empirical probability $p_i = \frac{f_i}{N}$ such that:
$$\sum_{i=1}^{n} p_i = 1$$

A code $C$ maps each symbol $s_i \in \Sigma$ to a variable-length binary codeword $c(s_i) \in \{0, 1\}^*$ of length $l_i = |c(s_i)|$. 

#### Definition 1 (Prefix-Free Code)
A code $C$ is a *prefix code* (or instantaneous code) if and only if no codeword $c(s_i)$ forms a prefix of any other codeword $c(s_j)$ for all $i \ne j$:
$$\forall i \ne j, \quad c(s_i) \not\sqsubseteq c(s_j)$$
Prefix codes allow unique, instantaneous decoding without lookahead tokens or delimiters.

#### Theorem 1 (Kraft–McMillan Inequality)
For any uniquely decodable binary code with codeword lengths $l_1, l_2, \dots, l_n$, the lengths must satisfy:
$$\sum_{i=1}^{n} 2^{-l_i} \le 1$$
Equality holds when the associated rooted binary tree is full (every internal node has degree 2).

#### Theorem 2 (Shannon's Source Coding Theorem)
The Shannon entropy $H(X)$ represents the theoretical minimum average number of bits required to represent a symbol emitted by a memoryless source $X$:
$$H(X) = -\sum_{i=1}^{n} p_i \log_2(p_i) \quad \text{(bits/symbol)}$$
For any optimal instantaneous code, the expected code length $L(C) = \sum_{i=1}^n p_i l_i$ is bounded by:
$$H(X) \le L(C) < H(X) + 1$$
The code redundancy is defined as $R = L(C) - H(X) \ge 0$.

### 2.2 Graph-Theoretic Tree Representation
A prefix code is modeled as a directed, rooted binary tree $T = (V, E)$:
* **Leaf Vertices ($V_L \subset V$):** Each leaf represents an alphabet symbol $s_i \in \Sigma$ with weight $w(v) = f_i$. The depth of leaf $v_i$ from the root equals codeword length $l_i$.
* **Internal Vertices ($V_I = V \setminus V_L$):** Each internal vertex has in-degree 1 (except the root with in-degree 0) and out-degree 2. Its weight equals the sum of its children's weights.
* **Edges ($E$):** Left child directed edges are assigned bit label `'0'`; right child directed edges are assigned bit label `'1'`.
* **Codeword Path:** The codeword $c(s_i)$ corresponds to the unique directed path from the root to leaf $v_i$.

The total weighted external path length of the tree corresponds directly to the compressed bit length:
$$W(T) = \sum_{v \in V_L} w(v) \cdot \text{depth}(v) = N \cdot L(C)$$

### 2.3 Proposed Algorithm & Implementation Procedure
Huffman's algorithm constructs $T$ using a bottom-up greedy strategy via a min-priority queue (min-heap):

```
Algorithm 1: Huffman Optimal Tree Construction
Input : Alphabet Sigma with frequencies {f_1, f_2, ..., f_n}
Output: Root vertex of optimal binary tree T

1. Q <- PriorityQueue()
2. for each symbol s in Sigma do
3.     node <- CreateNode(symbol=s, weight=freq[s], left=null, right=null)
4.     Q.Insert(node)
5. while Q.Size() > 1 do
6.     left_child  <- Q.ExtractMin()
7.     right_child <- Q.ExtractMin()
8.     parent <- CreateNode(symbol=null, weight=left_child.weight + right_child.weight)
9.     parent.left <- left_child
10.    parent.right <- right_child
11.    Q.Insert(parent)
12. return Q.ExtractMin()
```

#### Time & Space Complexity
* Initializing the min-heap takes $\mathcal{O}(|\Sigma|)$ time using Floyd's heapify.
* The loop executes $|\Sigma| - 1$ times, with two `ExtractMin` and one `Insert` operations per iteration, taking $\mathcal{O}(|\Sigma| \log |\Sigma|)$.
* Generating codes via Depth-First Search (DFS) visits all $2|\Sigma| - 1$ vertices in $\mathcal{O}(|\Sigma|)$ time.
* Overall tree construction complexity is strictly $\mathcal{O}(|\Sigma| \log |\Sigma|)$, independent of source length $N$. Text encoding and decoding scale as $\mathcal{O}(N)$.

### 2.4 Baseline Comparison: Shannon–Fano Coding
To fulfill the quantitative comparison requirement, Shannon–Fano coding was implemented as an independent baseline. Shannon–Fano operates top-down: symbols are sorted by frequency and recursively partitioned into two subsets with sums as close to equal as possible. Because it makes local decisions at top levels without global information, it can produce suboptimal trees compared to Huffman.

### 2.5 Experimental Setup & Datasets
In compliance with project guidelines requiring instances of $\ge 300$ records, four authentic datasets were curated:
1. **Natural Language Corpus:** English prose excerpt on discrete mathematics ($N = 2,001$ characters, $|\Sigma| = 56$).
2. **Programming Source Code:** Python data processing module ($N = 1,432$ characters, $|\Sigma| = 53$).
3. **Genomic DNA Sequence:** Bacteriophage nucleotide sequence in FASTA format ($N = 1,031$ base pairs, $|\Sigma| = 29$).
4. **Uniform Random Distribution:** Synthetically generated text with uniform symbol probability ($N = 1,140$ characters, $|\Sigma| = 76$).

---

## 3. Results and Discussion

### 3.1 Experiment 1: Compression Efficiency Across Diverse Domains
Table 1 presents the quantitative measurements obtained from running the full compression pipeline on all four domains.

**Table 1: Compression and Information-Theoretic Metrics Across Data Domains**

| Dataset | Symbols ($N$) | Alphabet ($|\Sigma|$) | Entropy $H(X)$ (bits/sym) | Huffman $L(C)$ (bits/sym) | Shannon–Fano $L$ (bits/sym) | Redundancy $R$ (bits/sym) | Compression Ratio | Space Savings (%) | Runtime (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **English Text** | 2,001 | 56 | 4.3894 | **4.4173** | 4.4178 | 0.0279 | 1.81 : 1 | 44.78% | 0.445 |
| **Python Code** | 1,432 | 53 | 4.3887 | **4.4106** | 4.4232 | 0.0219 | 1.81 : 1 | 44.87% | 0.300 |
| **Genomic DNA** | 1,031 | 29 | 2.2593 | **2.3705** | 2.3725 | 0.1113 | **3.37 : 1** | **70.37%** | 0.160 |
| **Uniform Random** | 1,140 | 76 | 6.2479 | **6.3158** | 6.3158 | 0.0679 | 1.27 : 1 | 21.05% | 0.372 |

#### Observations & Interpretation:
1. **Adherence to Shannon's Limit:** Across all datasets, the empirical average code length strictly satisfies $H(X) \le L(C) < H(X) + 1$. In English text, the optimality gap (redundancy) is exceptionally low at $R = 0.0279$ bits/symbol ($< 0.63\%$ above the theoretical minimum).
2. **Huffman Optimality vs. Shannon–Fano:** In every instance, $L_{\text{Huffman}} \le L_{\text{Shannon–Fano}}$, confirming the theoretical proof that Huffman trees achieve optimal weighted external path length.
3. **Domain-Specific Entropy Effects:** Genomic DNA exhibited the lowest entropy ($H = 2.2593$ bits) due to strong non-uniform nucleotide bias, resulting in a **3.37:1 compression ratio (70.37% storage savings)** compared to 8-bit fixed encoding. Conversely, uniformly distributed symbols showed maximum entropy ($H = 6.2479$ bits), yielding the lowest savings (21.05%).
4. **Kraft Inequality Validation:** For all generated prefix codes, $\sum 2^{-l_i} = 1.000000$, validating that the trees are full and uniquely decodable without unused codeword capacity.
5. **Lossless Verification:** The decode-after-encode verification $\mathcal{D}(\mathcal{E}(M)) == M$ returned `True` across all test files.

### 3.2 Experiment 2: Algorithmic Scaling vs. Input Size ($N$)
Table 2 documents execution performance as input size $N$ was scaled over three orders of magnitude ($N = 300$ to $100,000$ symbols).

**Table 2: Execution Runtime Scaling Across Input Sizes**

| Input Size ($N$) | Huffman Time (ms) | Shannon–Fano Time (ms) | Huffman Avg Length $L(C)$ (bits/sym) |
| :---: | :---: | :---: | :---: |
| 300 | 0.177 ms | 0.086 ms | 4.1600 |
| 1,000 | 0.199 ms | 0.127 ms | 4.2880 |
| 5,000 | 0.407 ms | 0.297 ms | 4.4002 |
| 20,000 | 0.897 ms | 1.237 ms | 4.4166 |
| 100,000 | 3.633 ms | 3.604 ms | 4.4171 |

#### Observations:
* Execution time scales linearly with $N$ ($\approx 3.63$ ms for 100,000 symbols), demonstrating high computational throughput.
* The expected code length stabilizes near $4.417$ bits/symbol as $N$ increases, confirming statistical convergence of empirical symbol frequencies to true source distributions.

---

## 4. Conclusion and Future Scope

### 4.1 Conclusion
This project successfully applied Discrete Mathematics and Graph Theory principles to formulate, implement, and analyze optimal prefix codes. Rooted binary trees and min-heap priority queues proved effective in producing minimum-redundancy codes that converge closely to Shannon's theoretical entropy bound. Quantitative benchmarking confirmed that Huffman coding consistently matches or outperforms Shannon–Fano coding, achieving up to 70.37% space savings on non-uniform data while guaranteeing 100% lossless reconstruction.

### 4.2 Limitations & Future Scope
* **Header Overhead:** Static Huffman coding requires transmitting the code tree or frequency table alongside the compressed bitstream, creating overhead for very small files ($N < 200$).
* **Future Extension (Adaptive Huffman):** Implementing Faller–Gallager–Knuth (FGK) or Vitter’s dynamic Huffman algorithm would enable single-pass compression without transmitting tree headers.
* **Higher-Order Models:** Huffman codes assign integer bit-lengths to symbols, limiting efficiency when symbol probabilities are not negative powers of two ($p_i \ne 2^{-k}$). Combining Huffman trees with Run-Length Encoding (RLE) or exploring Arithmetic Coding would allow fractional bit allocations closer to zero redundancy.

---

## Individual Contributions and Learning Reflections

* **Nikhil (Project Lead & Core Implementation):**  
  *Contribution:* Designed repository architecture, implemented min-heap Huffman tree builder (`src/huffman.py`), Shannon–Fano baseline (`src/shannon_fano.py`), and integration pipeline (`main.py`).  
  *Reflection:* Gained hands-on experience in translating abstract discrete graph properties into concrete Python priority queue data structures, and learned how greedy local choices guarantee global path optimality.

* **Piyush (Encoder/Decoder & Verification):**  
  *Contribution:* Developed the bit-level packing, byte conversion, tree-walk decoder (`src/codec.py`), and automated test suite (`tests/test_huffman.py`).  
  *Reflection:* Learned low-level bit manipulation, byte padding techniques, and how the prefix-free property enables unambiguous, instantaneous decoding without delimiters.

* **Sakshi (Mathematical Formulation & Theory):**  
  *Contribution:* Formulated the DMGT mathematical models, Kraft–McMillan inequality proofs, Shannon entropy theorems, and algorithmic pseudocode for Section 2.  
  *Reflection:* Deepened understanding of information theory limits and realized how discrete graph invariants mathematically constrain real-world software compression limits.

* **Arushi (Dataset & Preprocessing):**  
  *Contribution:* Curated and preprocessed four diverse datasets exceeding 1,000 records each (`data/`), and computed empirical frequency and probability tables.  
  *Reflection:* Understood how skewness and entropy directly govern compressibility, seeing why low-entropy biological DNA compresses far more efficiently than text.

* **Harsh (Experiments & Quantitative Comparison):**  
  *Contribution:* Designed and executed Experiment 1 and Experiment 2 (`experiments/benchmark.py`), measured performance metrics, and generated comparison CSVs and Matplotlib plots.  
  *Reflection:* Acquired skills in empirical performance profiling, benchmarking algorithmic scalability, and quantitatively evaluating theoretical bounds against observed results.

* **Khyathi (Visualization, Documentation & Presentation):**  
  *Contribution:* Built NetworkX tree visualization module (`src/visualizer.py`), generated publication graphs, and compiled the final research report and slide deck.  
  *Reflection:* Learned how to map complex nested tree objects into visual graphs with labeled decision edges, greatly improving visual communication of abstract discrete structures.

---

## References

1. **Huffman, D. A.** (1952). *A Method for the Construction of Minimum-Redundancy Codes*. Proceedings of the IRE, 40(9), 1098–1101.
2. **Shannon, C. E.** (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal, 27(3), 379–423.
3. **Rosen, K. H.** (2019). *Discrete Mathematics and Its Applications* (8th ed.). McGraw-Hill Education. (Chapter 11: Trees, Rooted Trees, and Prefix Codes).
4. **Cover, T. M., & Thomas, J. A.** (2006). *Elements of Information Theory* (2nd ed.). Wiley-Interscience.
5. **Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C.** (2022). *Introduction to Algorithms* (4th ed.). MIT Press. (Chapter 15: Greedy Algorithms & Huffman Codes).
