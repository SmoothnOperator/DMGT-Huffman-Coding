# Information-Theoretic Data Compression via Optimal Prefix Trees: An Empirical and Algorithmic Analysis of Huffman Coding

**Programme:** Bachelor of Technology in Computer Science & Engineering — Blockchain Technology (CSE-BCT)  
**Course:** Discrete Mathematics and Graph Theory (DMGT) — Experiential Learning  
**Project Topic 14:** Optimal Prefix Codes and Data Compression Using Huffman Coding  
**Institution:** School of Computer Science & Engineering  

**Authors & Group Members:**  
1. **Nikhil** (Project Lead & Core Implementation) — *Lead Developer*  
2. **Piyush** (Encoder/Decoder & Verification) — *Systems & Testing Engineer*  
3. **Sakshi** (Mathematical Formulation & Theory) — *Theoretical Mathematician*  
4. **Arushi** (Dataset Collection & Preprocessing) — *Data Engineer*  
5. **Harsh** (Experimental Design & Benchmarking) — *Performance Analyst*  
6. **Khyathi** (Visualization, Documentation & Presentation) — *Visual & Technical Communicator*  

---

## Abstract
Data compression is fundamentally governed by information theory and discrete mathematics, specifically the structural optimization of weighted, rooted binary trees. This research paper presents a rigorous theoretical formulation, computational implementation, and empirical evaluation of Huffman coding—a greedy algorithm that guarantees the construction of optimal prefix-free binary codes for discrete source alphabets. We model prefix codes as directed trees, prove strict adherence to the Kraft–McMillan inequality ($\sum 2^{-l_i} \le 1$), and examine convergence toward the theoretical lower bound established by Shannon's Source Coding Theorem ($H(X) \le L(C) < H(X) + 1$). Implemented in Python using a min-priority queue (min-heap) architecture, our compression engine is benchmarked against both fixed-length 8-bit ASCII representation and the top-down Shannon–Fano heuristic. The empirical evaluation encompasses four diverse datasets exceeding the prescribed 300 data points threshold: natural language text ($N = 2,001$), Python source code ($N = 1,432$), genomic DNA sequences in FASTA format ($N = 1,031$), and synthetically generated uniform random sequences ($N = 1,140$). Experimental results demonstrate that Huffman coding consistently achieves optimal redundancy ($R \le 0.1113$ bits/symbol), reaching a peak compression ratio of 3.37:1 with 70.37% storage savings on genomic data due to low source entropy. Runtime scaling analyses across input sizes ranging from 300 to 100,000 symbols validate an $\mathcal{O}(|\Sigma| \log |\Sigma|)$ tree construction complexity and linear $\mathcal{O}(N)$ encoding throughput. Graph visualizations generated via NetworkX provide clear structural validation of prefix-free decision paths.

**Keywords:** Huffman Coding, Optimal Prefix Codes, Rooted Binary Trees, Shannon Entropy, Lossless Data Compression.

---

## 1. Introduction

### 1.1 Background and Relevance
In contemporary computing architectures, data transmission and storage efficiency represent critical operational bottlenecks. Distributed systems, peer-to-peer communication networks, and decentralized blockchain ledgers must frequently transfer large transaction payloads across bandwidth-constrained channels. Uncompressed transmission increases network latency, exacerbates ledger bloat, and inflates computational overhead for all validating network participants. Lossless data compression provides a mathematically sound solution: reducing the physical footprint of digital information without sacrificing a single bit of fidelity upon decompression.

Discrete Mathematics and Graph Theory (DMGT) provide the structural bedrock for information coding. Rather than treating bitstreams as opaque continuous data, discrete mathematics abstracts digital sequences into finite alphabets, statistical probability distributions, and combinatorial structures. In particular, rooted binary trees serve as the canonical representation for instantaneous, variable-length prefix codes.

### 1.2 Brief Related Work
The foundations of mathematical information theory were established by Claude E. Shannon in his seminal 1948 treatise, *"A Mathematical Theory of Communication"* \cite{shannon1948}. Shannon demonstrated that the fundamental limit of lossless compression for any discrete, memoryless source $X$ is bounded by its information entropy $H(X)$. Shannon, alongside Robert Fano, proposed the Shannon–Fano heuristic, which partitions ordered symbols top-down into equiprobable subsets. However, Shannon–Fano coding does not guarantee an optimal prefix code in all configurations.

In 1952, while a doctoral student at MIT, David A. Huffman developed a bottom-up, greedy algorithm that guarantees absolute mathematical optimality for prefix codes \cite{huffman1952}. Huffman coding was subsequently integrated into widespread industrial standards, serving as the entropy-coding phase in DEFLATE (used in PKZIP, gzip, and PNG), JPEG image compression, and MP3 audio encoding.

### 1.3 Research Problem
While the theoretical optimality of Huffman coding is well-documented in classic literature, questions remain regarding how empirical redundancy $R = L(C) - H(X)$ behaves across domains with radically divergent statistical entropy—such as highly skewed biological sequences versus synthetically uniform random data. Furthermore, evaluating the computational trade-offs between bottom-up optimal Huffman trees and top-down heuristic Shannon–Fano trees under strict memory and runtime constraints is vital for software engineers designing data-intensive distributed applications.

### 1.4 Objectives of the Project
This experiential learning project achieves the following primary engineering and theoretical objectives:
1. **Mathematical Formalization:** Formulate source coding over rooted, weighted binary trees, proving the prefix-free condition, Kraft–McMillan inequality, and Shannon entropy bounds.
2. **Computational Implementation:** Implement an end-to-end Python pipeline using min-priority queues for Huffman tree construction, bit-level stream serialization, byte-packing with padding handling, and tree-walk decoding.
3. **Lossless Verification:** Rigorously verify mathematical idempotency ($\mathcal{D}(\mathcal{E}(M)) = M$) across all test files and edge cases.
4. **Empirical Benchmarking:** Conduct two meaningful experiments comparing Huffman coding against fixed-length ASCII and Shannon–Fano coding across four real-world datasets exceeding 300 data points.
5. **Graph Visualization:** Render rooted tree topologies and labeled decision branches using NetworkX and Matplotlib to provide clear geometric insight into prefix codes.

---

## 2. Methodology

### 2.1 DMGT Theoretical Foundation

#### 2.1.1 Source Alphabet and Probability Space
Let $\Sigma = \{s_1, s_2, \dots, s_n\}$ denote a finite source alphabet consisting of $n = |\Sigma|$ unique symbols. For a source sequence $M \in \Sigma^*$ of length $N$, the frequency of symbol $s_i$ is $f_i = \text{count}(s_i, M)$. The empirical probability of symbol $s_i$ is given by:
$$p_i = \frac{f_i}{N}, \quad \text{such that } \sum_{i=1}^{n} p_i = 1$$

#### 2.1.2 Variable-Length Prefix Codes
A binary code $C$ is an injective mapping $C: \Sigma \to \{0, 1\}^+$, where each symbol $s_i$ is mapped to a codeword $c(s_i)$ of length $l_i = |c(s_i)|$.

**Definition 1 (Prefix-Free Code):**  
A code $C$ is called a *prefix-free code* (or instantaneous code) if no codeword is a proper prefix of any other codeword:
$$\forall i \ne j, \quad c(s_i) \not\sqsubseteq c(s_j)$$
Prefix codes guarantee instantaneous, deterministic decoding without requiring special end-of-symbol delimiters or lookahead buffers.

#### 2.1.3 Graph-Theoretic Tree Formulation
A prefix code is isomorphic to a directed, weighted, rooted binary tree $T = (V, E)$:
* **Root Vertex ($r \in V$):** The entry point with in-degree 0.
* **Internal Vertices ($V_I \subset V$):** Vertices with out-degree 2 and in-degree 1. Each internal node $u \in V_I$ has a left child $u_L$ connected by edge $e_L = (u, u_L)$ with label `'0'`, and a right child $u_R$ connected by edge $e_R = (u, u_R)$ with label `'1'`.
* **Leaf Vertices ($V_L \subset V$):** Vertices with out-degree 0 and in-degree 1. Each leaf $v_i \in V_L$ uniquely corresponds to symbol $s_i \in \Sigma$, possessing weight $w(v_i) = f_i$.
* **Codeword Representation:** The binary codeword $c(s_i)$ is the sequence of edge labels along the unique directed path from root $r$ to leaf $v_i$.
* **Path Length & Depth:** The depth of leaf $v_i$ in tree $T$, denoted $\text{depth}(v_i)$, equals the codeword length $l_i = |c(s_i)|$.

The **Weighted External Path Length (WEPL)** of tree $T$, denoted $W(T)$, represents the total bit length of the compressed text:
$$W(T) = \sum_{v_i \in V_L} w(v_i) \cdot \text{depth}(v_i) = \sum_{i=1}^{n} f_i \cdot l_i = N \sum_{i=1}^{n} p_i \cdot l_i = N \cdot L(C)$$
Minimizing the expected code length $L(C)$ is equivalent to finding a binary tree with minimum weighted external path length.

#### 2.1.4 Fundamental Theorems and Mathematical Invariants

**Theorem 1 (Kraft–McMillan Inequality):**  
A binary prefix code with codeword lengths $l_1, l_2, \dots, l_n$ exists if and only if:
$$\sum_{i=1}^{n} 2^{-l_i} \le 1$$
*Proof Outline:* In a full binary tree of maximum depth $l_{\max} = \max_i \{l_i\}$, each leaf $v_i$ at depth $l_i$ eliminates $2^{l_{\max} - l_i}$ potential leaf positions at depth $l_{\max}$. Since the total number of leaves at depth $l_{\max}$ is bounded by $2^{l_{\max}}$, summing eliminated positions gives $\sum_{i=1}^n 2^{l_{\max} - l_i} \le 2^{l_{\max}}$. Dividing both sides by $2^{l_{\max}}$ yields $\sum_{i=1}^n 2^{-l_i} \le 1$. Equality strictly holds if and only if the tree is full (every internal node has exactly two children).

**Theorem 2 (Shannon's Source Coding Theorem):**  
For a discrete memoryless source $X$ with alphabet $\Sigma$ and probabilities $P$, the Shannon entropy $H(X)$ is defined as:
$$H(X) = -\sum_{i=1}^{n} p_i \log_2(p_i) \quad \text{(bits/symbol)}$$
For any uniquely decodable prefix code, the expected codeword length $L(C) = \sum_{i=1}^n p_i l_i$ satisfies:
$$H(X) \le L(C) < H(X) + 1$$
*Proof Outline:* By Gibbs' inequality, $-\sum p_i \log_2 p_i \le -\sum p_i \log_2 q_i$ for any distribution $q$. Setting $q_i = \frac{2^{-l_i}}{\sum 2^{-l_k}}$ and applying Kraft's inequality demonstrates $L(C) \ge H(X)$. Choosing optimal non-integer lengths $l_i^* = -\log_2 p_i$ gives $L(C) = H(X)$. Rounding up to integers $l_i = \lceil -\log_2 p_i \rceil < -\log_2 p_i + 1$ proves the upper bound $L(C) < H(X) + 1$.

**Definition 2 (Redundancy):**  
The coding redundancy $R$ quantifies the inefficiency of the code relative to the Shannon limit:
$$R = L(C) - H(X) \ge 0$$

#### 2.1.5 Proof Sketch of Huffman Optimality
Huffman's algorithm achieves the minimum WEPL by satisfying two structural properties:
1. **Greedy-Choice Property:** There exists an optimal binary prefix tree in which the two symbols with the lowest frequencies appear as sibling leaves at the maximum depth of the tree.
2. **Optimal Substructure:** Merging the two lowest-frequency nodes $u$ and $v$ into a parent node $z$ with weight $w(z) = w(u) + w(v)$ transforms an alphabet $\Sigma$ of size $n$ into an alphabet $\Sigma'$ of size $n-1$. The WEPL of tree $T$ satisfies $W(T) = W(T') + w(u) + w(v)$. Thus, minimizing $W(T)$ is strictly equivalent to minimizing $W(T')$, enabling recursive solution via mathematical induction.

---

### 2.2 Datasets and Problem Instances
To fulfill the requirement of using datasets with $\ge 300$ data points, four real-world and synthetic corpora were assembled:

**Table 1: Statistical Profiles of Evaluated Datasets**

| Dataset Identifier | Domain / Source Description | Total Records ($N$) | Alphabet Size ($|\Sigma|$) | Shannon Entropy $H(X)$ |
| :--- | :--- | :---: | :---: | :---: |
| **Dataset A** | Natural Language English Corpus (Academic prose on DMGT) | 2,001 characters | 56 symbols | 4.3894 bits/symbol |
| **Dataset B** | Python Source Code (Data processing class and methods) | 1,432 characters | 53 symbols | 4.3887 bits/symbol |
| **Dataset C** | Genomic DNA Nucleotide Sequence (Bacteriophage genome FASTA) | 1,031 base pairs | 29 symbols | 2.2593 bits/symbol |
| **Dataset D** | Synthetic Uniform Random Distribution (Balanced ASCII symbols) | 1,140 characters | 76 symbols | 6.2479 bits/symbol |

All four datasets comfortably exceed the mandatory 300 records threshold, spanning entropy values from $2.26$ to $6.25$ bits/symbol.

---

### 2.3 Proposed Algorithm: Huffman Tree Construction

#### 2.3.1 Algorithmic Procedure
The implementation utilizes Python's standard `heapq` module to maintain a min-priority queue of tree vertices.

```
Algorithm 1: Optimal Prefix Tree Construction (Huffman's Algorithm)
Input : Source text M of length N over alphabet Sigma
Output: Root node of the optimal binary prefix tree T

1.  frequencies <- ComputeFrequencies(M)
2.  Q <- MinPriorityQueue()
3.  node_counter <- 0
4.  for each (symbol, freq) in frequencies do
5.      leaf <- CreateNode(symbol=symbol, freq=freq, left=null, right=null, id=node_counter++)
6.      Q.Insert(leaf)
7.  if Q.Size() == 1 then
8.      single_leaf <- Q.ExtractMin()
9.      root <- CreateNode(symbol=null, freq=single_leaf.freq, left=single_leaf, right=null, id=node_counter++)
10.     return root
11. while Q.Size() > 1 do
12.     left_node  <- Q.ExtractMin()   // Smallest weight
13.     right_node <- Q.ExtractMin()   // Second-smallest weight
14.     merged_weight <- left_node.freq + right_node.freq
15.     parent <- CreateNode(symbol=null, freq=merged_weight, left=left_node, right=right_node, id=node_counter++)
16.     Q.Insert(parent)
17. root <- Q.ExtractMin()
18. return root
```

```
Algorithm 2: Prefix Code Extraction via Depth-First Search
Input : Current node v, Current bitstring code_prefix, Global dictionary Codes
Output: Populated dictionary Codes mapping Sigma -> {0, 1}^+

1. if v is null then
2.     return
3. if v.left is null and v.right is null then
4.     Codes[v.symbol] <- code_prefix
5.     return
6. TraverseDFS(v.left,  code_prefix + "0", Codes)
7. TraverseDFS(v.right, code_prefix + "1", Codes)
```

#### 2.3.2 Algorithmic Complexity Analysis
* **Frequency Calculation:** Counting symbol occurrences across $N$ characters requires a single linear scan: $\mathcal{O}(N)$ time and $\mathcal{O}(|\Sigma|)$ space.
* **Heap Initialization:** Inserting $|\Sigma|$ leaf nodes into the min-heap using bottom-up heapification (`heapify`) requires $\mathcal{O}(|\Sigma|)$ time.
* **Greedy Tree Merging:** The loop runs $|\Sigma| - 1$ times. In each iteration, two `ExtractMin` operations and one `Insert` operation are performed. Each priority queue operation on a heap of size $\le |\Sigma|$ requires $\mathcal{O}(\log |\Sigma|)$ time. The total merging cost is strictly $\mathcal{O}(|\Sigma| \log |\Sigma|)$.
* **Code Extraction:** The DFS tree walk visits each of the $2|\Sigma| - 1$ vertices exactly once, consuming $\mathcal{O}(|\Sigma|)$ time.
* **Text Encoding:** Encoding the original text replaces each character with its binary codeword via table lookup, requiring $\mathcal{O}(N)$ time.
* **Decoding:** Reading through the compressed bitstream of length $B = N \cdot L(C)$ and descending the tree takes exactly 1 step per bit, giving $\mathcal{O}(B) = \mathcal{O}(N)$ decoding time.
* **Total Time Complexity:** $\mathcal{O}(N + |\Sigma| \log |\Sigma|)$. Because $|\Sigma| \le 256$ for standard byte alphabets, $|\Sigma| \log |\Sigma|$ is a small constant, rendering the pipeline practically linear $\mathcal{O}(N)$.

---

### 2.4 Baseline Comparison Algorithm: Shannon–Fano Coding
To provide the quantitative algorithmic comparison mandated by the guidelines, Shannon–Fano coding was implemented as an independent baseline. Shannon–Fano employs a top-down divide-and-conquer strategy:
1. Compute symbol frequencies and sort symbols in descending order of frequency.
2. Partition the sorted list into two contiguous subsets such that the difference between their total frequency sums is minimized.
3. Assign prefix bit `'0'` to the top subset and `'1'` to the bottom subset.
4. Recursively apply steps 2 and 3 to each subset until all subsets contain exactly one symbol.

Because Shannon–Fano makes greedy partitioning decisions at the upper levels of the tree without foreseeing lower-level combinations, it can produce suboptimal prefix trees with larger expected codeword lengths than Huffman trees.

---

### 2.5 Implementation Architecture and Codec Pipeline

The engineering architecture is partitioned into modular Python components:

```
maths-exp-huffman/
├── data/                      <- Preprocessed raw input corpora (>= 300 data points)
├── src/
│   ├── huffman.py             <- HuffmanNode and HuffmanTree (Min-Heap Greedy Algorithm)
│   ├── shannon_fano.py        <- ShannonFanoTree (Top-down Partitioning Baseline)
│   ├── codec.py               <- Bitstream packing, padding handling, and lossless decoder
│   └── visualizer.py          <- NetworkX directed graph layout and Matplotlib renderer
├── experiments/
│   ├── benchmark.py           <- Automated suite for Experiments 1 & 2
│   └── plots/                 <- Generated high-res figures and CSV tables
├── tests/
│   └── test_huffman.py        <- Pytest suite (6/6 passing unit tests)
└── main.py                    <- Integrated pipeline execution entry point
```

#### Bit Packing and Stream Alignment
Because microprocessors address storage in 8-bit bytes rather than individual bits, the `HuffmanCodec` module:
1. Concatenates variable-length codewords into a continuous binary bitstring.
2. Calculates padding bits: $P = (8 - (\text{length} \bmod 8)) \bmod 8$.
3. Appends $P$ zero-bits to form an exact multiple of 8 bits.
4. Serializes chunks of 8 bits into raw unsigned bytes using Python `bytearray`.
5. Upon decompression, the packed bytes are unpacked, padding bits $P$ are trimmed, and the bitstream navigates the tree from the root to reconstruct the original plaintext.

---

## 3. Results and Discussion

### 3.1 Experiment 1: Compression Efficiency Across Diverse Domains
The complete compression and verification suite was executed across the four corpora. Table 2 summarizes the quantitative DMGT metrics obtained.

**Table 2: Quantitative Experimental Evaluation Across Data Domains**

| Metric | Dataset A: English Text | Dataset B: Python Code | Dataset C: Genomic DNA | Dataset D: Uniform Random |
| :--- | :---: | :---: | :---: | :---: |
| **Sample Size ($N$)** | 2,001 symbols | 1,432 symbols | 1,031 symbols | 1,140 symbols |
| **Alphabet Size ($|\Sigma|$)** | 56 symbols | 53 symbols | 29 symbols | 76 symbols |
| **Shannon Entropy $H(X)$** | 4.3894 bits/sym | 4.3887 bits/sym | 2.2593 bits/sym | 6.2479 bits/sym |
| **Huffman Average Length $L(C)$** | **4.4173 bits/sym** | **4.4106 bits/sym** | **2.3705 bits/sym** | **6.3158 bits/sym** |
| **Shannon–Fano Average Length** | 4.4178 bits/sym | 4.4232 bits/sym | 2.3725 bits/sym | 6.3158 bits/sym |
| **Fixed ASCII Code Length** | 8.0000 bits/sym | 8.0000 bits/sym | 8.0000 bits/sym | 8.0000 bits/sym |
| **Coding Redundancy ($R$)** | **0.0279 bits/sym** | **0.0219 bits/sym** | **0.1113 bits/sym** | **0.0679 bits/sym** |
| **Compression Ratio (CR)** | **1.81 : 1** | **1.81 : 1** | **3.37 : 1** | **1.27 : 1** |
| **Storage Space Savings (%)** | **44.78%** | **44.87%** | **70.37%** | **21.05%** |
| **Kraft Sum ($\sum 2^{-l_i}$)** | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| **Lossless Check ($\mathcal{D}(\mathcal{E}(M)) == M$)** | **True (PASSED)** | **True (PASSED)** | **True (PASSED)** | **True (PASSED)** |
| **Tree Build & Encode Time** | 0.445 ms | 0.300 ms | 0.160 ms | 0.372 ms |

#### Mathematical & Empirical Observations:
1. **Convergence to Shannon Limit:** In all test scenarios, the Huffman average codeword length strictly satisfies Shannon's Source Coding Theorem:
   $$H(X) \le L(C) < H(X) + 1$$
   In English text and Python code, the redundancy is extraordinarily low ($R = 0.0279$ and $R = 0.0219$ bits/symbol), demonstrating that Huffman codes operate within $0.63\%$ of theoretical perfection.
2. **Impact of Domain Entropy on Compressibility:**
   * **Genomic DNA (Dataset C):** Displays the lowest entropy ($H = 2.2593$ bits) due to extreme frequency skewness (adenine, cytosine, guanine, and thymine dominate the 29-symbol alphabet). Consequently, the average codeword length drops to $2.3705$ bits/symbol, delivering an outstanding **3.37:1 compression ratio (70.37% space reduction)** compared to standard 8-bit ASCII.
   * **Uniform Random Text (Dataset D):** Possesses the highest entropy ($H = 6.2479$ bits) because all 76 symbols occur with approximately equal probability. Under uniform distribution, tree leaf depths become nearly uniform ($l_i \approx \lceil \log_2 76 \rceil = 7$), yielding minimal space savings (21.05%).
3. **Quantitative Superiority over Shannon–Fano:** Across all datasets, Huffman coding achieves an average codeword length equal to or strictly strictly smaller than Shannon–Fano coding:
   $$L_{\text{Huffman}} \le L_{\text{Shannon–Fano}}$$
   In English text, Huffman achieves $4.4173$ vs. Shannon–Fano's $4.4178$; in Python code, $4.4106$ vs. $4.4232$. This empirical evidence supports the theoretical theorem that top-down partitioning can make suboptimal choices.
4. **Kraft Inequality & Tree Completeness:** Across every generated codebook, the Kraft sum evaluated to exactly $\sum_{i=1}^n 2^{-l_i} = 1.000000 \pm 10^{-9}$. This proves that the resulting rooted binary trees are *full* binary trees without any unallocated codeword capacity.

---

### 3.2 Graphical Analysis and Visualizations

```
+-------------------------------------------------------------------------------+
| Figure 1: Entropy Limit vs. Prefix Code Lengths Across Evaluated Datasets      |
| [Stored on disk: experiments/plots/exp1_entropy_vs_codelength.png]            |
+-------------------------------------------------------------------------------+
```

The bar chart in Figure 1 illustrates the relationship between theoretical Shannon Entropy $H(X)$, Huffman expected codeword length $L(C)$, Shannon–Fano codeword length, and fixed 8-bit ASCII. Across all domains, the Huffman bars (green) sit directly on top of the Shannon Entropy bars (blue), visibly demonstrating near-zero coding redundancy.

```
+-------------------------------------------------------------------------------+
| Figure 2: NetworkX Visualization of the Rooted Optimal Prefix Code Tree       |
| [Stored on disk: experiments/plots/huffman_tree_visualization.png]            |
+-------------------------------------------------------------------------------+
```

The graph in Figure 2 displays the rooted tree structure generated by `src/visualizer.py`. Internal vertices (blue circles) show combined subtree weights, while leaf vertices (green squares) display the alphabet characters and their original weights. Directed edge annotations clearly indicate `'0'` for left branches and `'1'` for right branches, showing how higher-frequency symbols are positioned closer to the root (shorter paths), while lower-frequency symbols are pushed deeper into the tree.

---

### 3.3 Experiment 2: Execution Runtime Scaling vs. Input Size ($N$)
To assess scalability, the benchmark engine tested problem instances from $N = 300$ up to $N = 100,000$ symbols.

**Table 3: Algorithmic Scaling Performance with Input Size**

| Problem Instance ($N$) | Huffman Runtime (ms) | Shannon–Fano Runtime (ms) | Huffman Expected Length $L(C)$ (bits) |
| :---: | :---: | :---: | :---: |
| **300 symbols** | 0.177 ms | 0.086 ms | 4.1600 bits/symbol |
| **1,000 symbols** | 0.199 ms | 0.127 ms | 4.2880 bits/symbol |
| **5,000 symbols** | 0.407 ms | 0.297 ms | 4.4002 bits/symbol |
| **20,000 symbols** | 0.897 ms | 1.237 ms | 4.4166 bits/symbol |
| **100,000 symbols** | 3.633 ms | 3.604 ms | 4.4171 bits/symbol |

```
+-------------------------------------------------------------------------------+
| Figure 3: Execution Runtime Scaling Across Input Sizes N                      |
| [Stored on disk: experiments/plots/exp2_runtime_scaling.png]                  |
+-------------------------------------------------------------------------------+
```

#### Observations on Computational Scalability:
* **Linear Time Scaling:** Processing 100,000 symbols requires only $3.63$ milliseconds. Because tree construction depends solely on alphabet size $|\Sigma|$ (which remains constant at 56 symbols), tree construction time remains constant ($\sim 0.1$ ms), while encoding time scales strictly as $\mathcal{O}(N)$.
* **Statistical Convergence:** As $N$ increases from 300 to 100,000, the average code length smoothly converges from $4.1600$ to $4.4171$ bits/symbol, reflecting the law of large numbers where sample symbol frequencies stabilize around the underlying source distribution.

---

## 4. Conclusion and Future Scope

### 4.1 Major Findings and DMGT Contributions
This research demonstrated the practical and theoretical power of Discrete Mathematics and Graph Theory in engineering optimal data compression systems. By modeling variable-length codes as rooted, weighted binary trees, Huffman's greedy min-heap algorithm was shown to mathematically guarantee minimal weighted path lengths. 

The empirical findings confirm:
1. Huffman coding consistently achieves near-optimal redundancy ($R \le 0.1113$ bits/symbol across all domains).
2. Compression gains are governed by source entropy: biological sequences with skewed character distributions achieve up to **70.37% space savings**, whereas high-entropy uniform data achieves only $21.05%$.
3. Huffman coding strictly dominates top-down Shannon–Fano coding in average codeword length across all non-trivial problem instances.
4. The computational pipeline processes over 27,000 symbols per millisecond, ensuring suitability for high-throughput distributed systems and blockchain transaction encoding.

### 4.2 Limitations
* **Codebook Transmission Overhead:** Static Huffman coding requires storing or transmitting the frequency table / tree topology alongside the compressed bitstream. For small files ($N < 200$), this header overhead can exceed the compression savings.
* **Integer Bit-Length Constraint:** Huffman coding assigns an integer number of bits $l_i \in \mathbb{Z}^+$ to each symbol. When a symbol's true information content is fractional ($-\log_2 p_i \notin \mathbb{Z}$), Huffman coding cannot achieve $R = 0$.

### 4.3 Future Scope
1. **Adaptive (Dynamic) Huffman Coding:** Implementing the Faller–Gallager–Knuth (FGK) or Vitter dynamic tree update algorithm will allow real-time codebook adaptation on streaming data without transmitting a header table.
2. **Arithmetic Coding Integration:** Arithmetic coding eliminates the integer bit constraint by mapping the entire message to a single sub-interval in $[0, 1)$, theoretically achieving $L(C) \to H(X)$ even for symbols with probabilities approaching 1.
3. **Blockchain Payload Serialization:** Applying canonical Huffman trees to Ethereum or Hyperledger state serialization formats to minimize block propagation latency across peer nodes.

---

## Individual Contributions and Learning Reflections

### 1. Nikhil (Project Lead & Core Implementation)
* **Specific Contribution:** Formulated project architecture, implemented the core greedy min-heap tree construction algorithm and DFS code extraction in `src/huffman.py`, implemented the baseline `src/shannon_fano.py`, built the central execution pipeline in `main.py`, and managed the GitHub repository workflow.
* **Learning Reflection:** *"Implementing Huffman coding from scratch bridged the gap between abstract graph definitions and concrete systems programming. I developed a deep appreciation for how min-priority queues reduce tree construction from quadratic to $\mathcal{O}(|\Sigma| \log |\Sigma|)$ time, and how local greedy node merges mathematically enforce global optimality."*

### 2. Piyush (Encoder/Decoder & Verification)
* **Specific Contribution:** Engineered the bitstream serialization, padding calculations, byte-packing operations, and tree-walk decoding engine in `src/codec.py`. Developed the comprehensive unit testing suite in `tests/test_huffman.py` covering edge cases and mathematical invariants.
* **Learning Reflection:** *"Working on the codec module taught me the nuances of low-level bit manipulation and memory alignment. Verifying that the tree-walk decoder is mathematically idempotent ($\mathcal{D}(\mathcal{E}(M)) == M$) across single-character edge cases and large corpora reinforced the elegance of prefix-free codes."*

### 3. Sakshi (Mathematical Formulation & Theory)
* **Specific Contribution:** Formulated the discrete mathematical framework in Section 2, drafted formal definitions of rooted weighted trees, derived the Kraft–McMillan inequality proofs, formulated Shannon's Source Coding Theorem, and structured the Huffman optimality proof sketch.
* **Learning Reflection:** *"This project allowed me to explore how discrete graph invariants directly govern information-theoretic limits. Proving that our empirical Kraft sum evaluates to exactly $1.000000$ provided satisfying proof that our binary trees were mathematically full and contained no wasted codeword space."*

### 4. Arushi (Dataset Collection & Preprocessing)
* **Specific Contribution:** Sourced, sanitized, and formatted the four benchmark datasets in `data/` (English, Python code, DNA FASTA, and Uniform random text) to strictly exceed the 300 data points threshold. Computed empirical symbol frequency distributions and source entropy tables.
* **Learning Reflection:** *"Analyzing diverse data domains gave me practical insight into how statistical skewness governs compressibility. Seeing the genomic DNA sequence achieve over 70% space savings due to its low 2.26-bit entropy visually demonstrated the power of source coding theory."*

### 5. Harsh (Experimental Design & Benchmarking)
* **Specific Contribution:** Designed and executed Experiment 1 (cross-domain efficiency) and Experiment 2 (runtime scaling from 300 to 100,000 symbols) in `experiments/benchmark.py`. Extracted quantitative metrics, performed comparative statistical analysis, and generated CSV tables and Matplotlib plots.
* **Learning Reflection:** *"Conducting quantitative experiments comparing Huffman against Shannon–Fano and ASCII gave me valuable experience in empirical benchmarking. Seeing the runtime scale linearly at over 27,000 characters per millisecond demonstrated that theoretical efficiency does not come at the cost of practical speed."*

### 6. Khyathi (Visualization, Documentation & Presentation)
* **Specific Contribution:** Developed `src/visualizer.py` utilizing NetworkX and Matplotlib to render hierarchical directed trees with labeled decision edges. Compiled the complete research-article technical report and created the 10-slide presentation deck in `docs/PRESENTATION_SLIDES.md`.
* **Learning Reflection:** *"Translating recursive binary tree objects into readable, publication-quality NetworkX directed graphs was an illuminating challenge. Visually illustrating how high-frequency symbols reside near the root while rare symbols are placed deeper made the abstract mathematics intuitively obvious to our audience."*

---

## References

1. **Huffman, D. A.** (1952). *A Method for the Construction of Minimum-Redundancy Codes*. Proceedings of the Institute of Radio Engineers (IRE), 40(9), 1098–1101. DOI: [10.1109/JRPROC.1952.273898](https://doi.org/10.1109/JRPROC.1952.273898).
2. **Shannon, C. E.** (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal, 27(3), 379–423. DOI: [10.1002/j.1538-7305.1948.tb01338.x](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x).
3. **Rosen, K. H.** (2019). *Discrete Mathematics and Its Applications* (8th ed.). McGraw-Hill Education. ISBN: 978-1259676512. (Chapter 11: Trees, Rooted Binary Trees, and Tree Traversal).
4. **Cover, T. M., & Thomas, J. A.** (2006). *Elements of Information Theory* (2nd ed.). John Wiley & Sons, Inc. ISBN: 978-0471241959. (Chapter 5: Data Compression & Kraft Inequality).
5. **Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C.** (2022). *Introduction to Algorithms* (4th ed.). MIT Press. ISBN: 978-0262046305. (Chapter 15: Greedy Algorithms and Huffman Codes).
6. **Fano, R. M.** (1949). *The Transmission of Information*. Technical Report No. 65, Research Laboratory of Electronics, Massachusetts Institute of Technology (MIT).
7. **Knuth, D. E.** (1985). *Dynamic Huffman Coding*. Journal of Algorithms, 6(2), 163–180. DOI: [10.1016/0196-6774(85)90036-7](https://doi.org/10.1016/0196-6774(85)90036-7).
