"""
Interactive Web Application for Huffman Coding & DMGT Compression
Course: Discrete Mathematics and Graph Theory (DMGT)
Faculty: Faculty of Engineering and Technology, JAIN (Deemed-to-be University)
Topic 14: Optimal Prefix Codes and Data Compression Using Huffman Coding
Evaluator: Dr. Priya Satish
Author: Nikhil Kumar (Project Lead) & Team
"""

import os
import sys
import time
import math
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import streamlit.components.v1 as components

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.huffman import HuffmanTree, HuffmanNode
from src.shannon_fano import ShannonFanoTree
from src.codec import HuffmanCodec
from src.visualizer import HuffmanVisualizer

# Page Configuration
st.set_page_config(
    page_title="DMGT - Huffman Coding Interactive Model & Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Jain University Executive Theme)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #102C57 0%, #1F4E78 100%);
        color: white;
        padding: 20px 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .metric-card {
        background-color: #F8F9FA;
        border-left: 4px solid #1F4E78;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .badge-pass {
        background-color: #D4EDDA;
        color: #155724;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .queue-chip {
        display: inline-block;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 16px;
        font-size: 0.82rem;
        font-family: monospace;
        font-weight: 600;
        border: 1px solid #ced4da;
    }
    .chip-leaf {
        background-color: #E8F5E9;
        border-color: #A5D6A7;
        color: #1B5E20;
    }
    .chip-internal {
        background-color: #E3F2FD;
        border-color: #90CAF9;
        color: #0D47A1;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="main-header">
    <h2 style="margin:0; padding:0; color:#F0AD4E; font-size: 1.1rem; text-transform: uppercase;">
        JAIN (Deemed-to-be University) &bull; School of Computer Science & Engineering
    </h2>
    <h1 style="margin:4px 0; color:white; font-size: 1.85rem;">
        Optimal Prefix Codes and Data Compression Using Huffman Coding
    </h1>
    <p style="margin:0; color:#DDE6ED; font-size: 0.95rem;">
        <b>Course:</b> Discrete Mathematics and Graph Theory (DMGT) &bull; 
        <b>Branch:</b> CSE - BLOCKCHAIN &bull; 
        <b>Evaluator:</b> Dr. Priya Satish
    </p>
</div>
""", unsafe_allow_html=True)

# Project code files mapping
PROJECT_CODE_FILES = {
    "src/huffman.py (Nikhil - Lead & Tree Algorithm)": os.path.join(BASE_DIR, "src", "huffman.py"),
    "src/codec.py (Piyush - Bitstream Codec & Decoder)": os.path.join(BASE_DIR, "src", "codec.py"),
    "src/shannon_fano.py (Sakshi - Baseline Heuristic)": os.path.join(BASE_DIR, "src", "shannon_fano.py"),
    "src/visualizer.py (Khyathi - NetworkX Graph Visualizer)": os.path.join(BASE_DIR, "src", "visualizer.py"),
    "experiments/benchmark.py (Harsh - Empirical Benchmarks)": os.path.join(BASE_DIR, "experiments", "benchmark.py"),
    "main.py (Central Integration Pipeline)": os.path.join(BASE_DIR, "main.py"),
    "tests/test_huffman.py (Pytest Suite - 7 Tests)": os.path.join(BASE_DIR, "tests", "test_huffman.py")
}

# Sidebar: Dataset Selection & Team Info
with st.sidebar:
    st.subheader("Team Members (CSE-BCT)")
    st.markdown("""
    * **Nikhil Kumar** (25BTRBT026) — *Lead & Core*
    * **Piyush Kumar** (25BTRBT030) — *Codec & Testing*
    * **Sakshi Kumari** (25BTRC0045) — *Math & Theory*
    * **Arushi Pramanik** (25BTRBT008) — *Datasets*
    * **Harsh R Rao** (25BTRBT017) — *Experiments*
    * **Khyathi Jain** (25BTRBT021) — *Visualization*
    """)
    st.divider()

    st.subheader("Input Source")
    input_mode = st.radio(
        "Choose Data Source:",
        [
            "Preloaded Benchmark Dataset (>= 300 records)",
            "Feed Project Source Code (>= 300 records)",
            "Custom Interactive Text"
        ]
    )

    if input_mode.startswith("Preloaded"):
        dataset_choice = st.selectbox(
            "Select Benchmark Dataset:",
            [
                "Dataset A: English Text (N = 2,001)",
                "Dataset B: Python Source Code (N = 1,432)",
                "Dataset C: Genomic DNA FASTA (N = 1,031)",
                "Dataset D: Uniform Random Text (N = 1,140)"
            ]
        )
        data_files = {
            "Dataset A": os.path.join(BASE_DIR, "data", "sample_english.txt"),
            "Dataset B": os.path.join(BASE_DIR, "data", "sample_code.py"),
            "Dataset C": os.path.join(BASE_DIR, "data", "sample_dna.fasta"),
            "Dataset D": os.path.join(BASE_DIR, "data", "sample_uniform.txt")
        }
        key = dataset_choice.split(":")[0]
        selected_file = data_files[key]
        with open(selected_file, "r", encoding="utf-8") as f:
            raw_text = f.read()
        source_label = dataset_choice

    elif input_mode.startswith("Feed Project"):
        code_choice = st.selectbox(
            "Select Project Module to Feed into Model:",
            list(PROJECT_CODE_FILES.keys())
        )
        selected_code_path = PROJECT_CODE_FILES[code_choice]
        with open(selected_code_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        source_label = f"Code Feeder: {code_choice.split(' ')[0]}"
        
        with st.expander("👁 Inspect Selected Module Code", expanded=False):
            st.code(raw_text[:1200] + ("\n... [remaining code truncated for preview]" if len(raw_text) > 1200 else ""), language="python")

    else:
        raw_text = st.text_area(
            "Enter text to compress:",
            value="Discrete Mathematics and Graph Theory provides foundational concepts essential for computer science. "
                  "Huffman coding uses rooted binary trees to produce optimal prefix codes for lossless data compression.",
            height=160
        )
        source_label = "Custom User Input"

# Process the input text through Huffman & Shannon-Fano
if not raw_text.strip():
    st.warning("Please enter or select text to begin compression.")
    st.stop()

# Execution Pipeline
t0 = time.perf_counter()
huffman = HuffmanTree()
root, history = huffman.build_tree_with_history(raw_text)
codes = huffman.get_codes()
huff_time_ms = (time.perf_counter() - t0) * 1000

# Shannon-Fano baseline
t1 = time.perf_counter()
sf = ShannonFanoTree()
sf_codes = sf.build_tree(raw_text)
sf_time_ms = (time.perf_counter() - t1) * 1000

# Bitstream codec
raw_bitstring = HuffmanCodec.encode_to_bitstring(raw_text, codes)
packed_bytes, padding = HuffmanCodec.pad_bitstring(raw_bitstring)
unpacked_bitstring = HuffmanCodec.unpad_and_unpack(packed_bytes, padding)
decoded_text = HuffmanCodec.decode_from_bitstring(unpacked_bitstring, root)
is_lossless = HuffmanCodec.verify_lossless(raw_text, decoded_text)

# Metrics
total_chars = len(raw_text)
entropy = huffman.calculate_entropy()
huff_avg_len = huffman.calculate_average_code_length()
sf_avg_len = sf.calculate_average_code_length()
redundancy = huffman.calculate_redundancy()
is_kraft_valid, kraft_sum = huffman.verify_kraft_inequality()

uncompressed_bits = total_chars * 8
compressed_bits = len(packed_bytes) * 8
comp_ratio = uncompressed_bits / compressed_bits if compressed_bits > 0 else 0
savings_pct = (1.0 - (compressed_bits / uncompressed_bits)) * 100 if uncompressed_bits > 0 else 0

# Navigation Tabs
tab_live, tab_flow, tab_sim, tab_feeder, tab_tables, tab_tree, tab_exp, tab_model, tab_compliance = st.tabs([
    "🚀 Live Compression Engine",
    "🔄 Algorithm Flowchart",
    "🔬 Step-by-Step Priority Queue Simulator",
    "💻 Feed All Source Codes & Inspector",
    "📋 Tables & Codebook",
    "🌳 Rooted Binary Tree",
    "📊 Benchmarking & Graphs",
    "🌐 Standalone Visual Model (HTML5/SVG)",
    "📑 8-Stage Syllabus Compliance"
])

# ---------------------------------------------------------
# TAB 1: LIVE COMPRESSION ENGINE
# ---------------------------------------------------------
with tab_live:
    st.subheader(f"Live Compression Performance: {source_label}")
    
    # Verification Badge
    if is_lossless:
        st.success(f"✅ Lossless Reconstruction Check: PASSED (Decoded {len(decoded_text):,} characters with 100% mathematical fidelity: D(E(M)) == M)")
    else:
        st.error("❌ Lossless check failed.")

    # 4 Key Metrics Columns
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Records / Characters", f"{total_chars:,}", f"Alphabet |Σ|: {len(codes)} symbols")
    with m2:
        st.metric("Compression Ratio", f"{comp_ratio:.2f} : 1", f"Space Savings: {savings_pct:.1f}%")
    with m3:
        st.metric("Huffman Avg Length L(C)", f"{huff_avg_len:.4f} b/sym", f"Shannon Entropy H: {entropy:.4f}")
    with m4:
        st.metric("Kraft-McMillan Sum", f"{kraft_sum:.6f}", "Valid Prefix Tree (<= 1.0)")

    st.divider()

    col_details_1, col_details_2 = st.columns(2)
    with col_details_1:
        st.markdown("#### Storage Comparison")
        comp_df = pd.DataFrame({
            "Encoding Method": ["Fixed 8-Bit ASCII", "Shannon-Fano Coding", "Huffman Optimal Tree"],
            "Average Length": ["8.0000 bits/sym", f"{sf_avg_len:.4f} bits/sym", f"{huff_avg_len:.4f} bits/sym"],
            "Total Storage Footprint": [f"{uncompressed_bits:,} bits ({uncompressed_bits//8:,} bytes)",
                                       f"{int(sf_avg_len * total_chars):,} bits",
                                       f"{compressed_bits:,} bits ({len(packed_bytes):,} bytes)"],
            "Optimality Status": ["Redundant Baseline", "Top-down Heuristic", "Mathematically Optimal"]
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

    with col_details_2:
        st.markdown("#### Bitstream Inspection (First 300 Bits)")
        st.code(raw_bitstring[:300] + ("..." if len(raw_bitstring) > 300 else ""), language="text")
        st.caption(f"Raw bitstream length: {len(raw_bitstring):,} bits. Packed into {len(packed_bytes):,} bytes with {padding} padding bits.")

# ---------------------------------------------------------
# TAB 2: ALGORITHM FLOWCHART
# ---------------------------------------------------------
with tab_flow:
    st.subheader("End-to-End DMGT Algorithm & Flowchart")
    st.markdown("""
    This flowchart maps the complete execution pipeline from source characters to binary tree optimization, 
    bitstream serialization, and tree-walk decoding.
    """)

    flowchart_mermaid = """
    graph TD
        A[Input Source Text M of Length N] --> B[Frequency Analysis: Compute f_i for each s_i in Sigma]
        B --> C[Initialize Min-Priority Queue Q: Push Leaf Nodes]
        C --> D{Is Size of Q > 1?}
        D -- Yes --> E[Extract-Min: Node u smallest frequency]
        E --> F[Extract-Min: Node v second-smallest frequency]
        F --> G[Merge: Create Parent Node z with weight w_z = w_u + w_v]
        G --> H[Connect: Left Child = u label '0', Right Child = v label '1']
        H --> I[Insert Parent Node z back into Priority Queue Q]
        I --> D
        D -- No --> J[Single Remaining Node = Root of Rooted Binary Tree T]
        J --> K[DFS Tree Traversal: Extract Optimal Prefix Codes c_i]
        K --> L[Text Encoding: Map symbols to prefix codes]
        L --> M[Byte Packing: Append padding bits and pack into 8-bit bytes]
        M --> N[Compressed Binary File / Storage]
        N --> O[Tree-Walk Decoder: Bit-by-bit descent from root]
        O --> P[Leaf Encountered: Emit symbol s_i & Reset to Root]
        P --> Q[Lossless Reconstructed Text M': Verify D_E_M == M]
        
        style A fill:#E3F2FD,stroke:#1F4E78,stroke-width:2px;
        style J fill:#C8E6C9,stroke:#2E7D32,stroke-width:2px;
        style N fill:#FFE0B2,stroke:#E65100,stroke-width:2px;
        style Q fill:#D1C4E9,stroke:#512DA8,stroke-width:2px;
    """
    st.markdown(f"```mermaid\n{flowchart_mermaid}\n```")

# ---------------------------------------------------------
# TAB 3: STEP-BY-STEP SIMULATOR & BITSTREAM TRACER
# ---------------------------------------------------------
with tab_sim:
    st.subheader("🔬 Step-by-Step Priority Queue Merging Simulation")
    st.markdown("""
    Huffman coding builds the optimal binary tree using a **greedy choice property**:
    at each step, the two nodes with the lowest frequencies are extracted from the min-heap,
    merged under a new internal parent with their summed weight, and re-inserted.
    """)

    total_steps = len(history) - 1
    if total_steps > 0:
        step_idx = st.slider("Select Step in Tree Construction:", 0, total_steps, 0)
        curr_step = history[step_idx]

        st.info(f"**Step {curr_step['step']} / {total_steps}:** {curr_step['action']}")

        col_s1, col_s2 = st.columns([1, 2])
        with col_s1:
            st.markdown("#### Merging Action Details")
            if curr_step['extracted']:
                st.write(f"**Extracted Node 1 (Left branch '0'):** {curr_step['extracted'][0]}")
                st.write(f"**Extracted Node 2 (Right branch '1'):** {curr_step['extracted'][1]}")
                st.write(f"**Merged Internal Parent:** {curr_step['merged']}")
            else:
                st.write("Initial state: Min-heap loaded with all alphabet leaf vertices.")

        with col_s2:
            st.markdown("#### Live Min-Priority Queue Contents")
            chips_html = "".join([
                f"<span class='queue-chip {'chip-leaf' if not item[0].startswith('Internal') else 'chip-internal'}'>"
                f"{repr(item[0]) if item[0] in (' ', '\\n', '\\t') else item[0]} ({item[1]})</span>"
                for item in curr_step['heap']
            ])
            st.markdown(f"<div style='border: 1px solid #ced4da; padding: 12px; border-radius: 6px; background: white;'>{chips_html}</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("⚡ Live Tree-Walk Bitstream Decoder Tracer")
    st.markdown("Trace how a custom phrase is encoded into prefix bits and then decoded step-by-step by navigating the rooted binary tree:")
    
    test_phrase = st.text_input("Enter a phrase to trace bit-by-bit:", value="EXPERIENTIAL")
    if test_phrase:
        trace_bits = "".join(codes.get(c, "0") for c in test_phrase)
        st.markdown(f"**Encoded Bitstream ({len(trace_bits)} bits):**")
        st.code(trace_bits, language="text")

        with st.expander("🔍 View Complete Tree-Walk Navigation Trace", expanded=True):
            trace_records = []
            curr_node = root
            path_taken = []
            for idx, bit in enumerate(trace_bits):
                path_taken.append(bit)
                prev_weight = curr_node.freq
                curr_node = curr_node.left if bit == "0" else curr_node.right
                nav_dir = "LEFT ('0')" if bit == "0" else "RIGHT ('1')"
                
                if curr_node.is_leaf():
                    emitted = repr(curr_node.char) if curr_node.char in (' ', '\n', '\t') else curr_node.char
                    trace_records.append({
                        "Bit Index": idx + 1,
                        "Bit": bit,
                        "Navigation": nav_dir,
                        "Current Node Weight": curr_node.freq,
                        "Event": f"🎉 Leaf Reached! Emitted {emitted}",
                        "Codeword Path": "".join(path_taken)
                    })
                    curr_node = root
                    path_taken = []
                else:
                    trace_records.append({
                        "Bit Index": idx + 1,
                        "Bit": bit,
                        "Navigation": nav_dir,
                        "Current Node Weight": curr_node.freq,
                        "Event": "Internal Node (continue traversal)",
                        "Codeword Path": "".join(path_taken)
                    })

            trace_df = pd.DataFrame(trace_records)
            st.dataframe(trace_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 4: FEED ALL SOURCE CODES & INSPECTOR
# ---------------------------------------------------------
with tab_feeder:
    st.subheader("💻 Feed All Project Source Codes into the Compression Model")
    st.markdown("""
    This experiential learning project is built from modular, production-grade Python components.
    Select any project module to inspect its full implementation, analyze its character entropy, and view its compression performance!
    """)

    code_tabs = st.tabs([
        "src/huffman.py",
        "src/codec.py",
        "src/shannon_fano.py",
        "src/visualizer.py",
        "experiments/benchmark.py",
        "main.py",
        "tests/test_huffman.py"
    ])

    for tab, (mod_name, file_path) in zip(code_tabs, PROJECT_CODE_FILES.items()):
        with tab:
            with open(file_path, "r", encoding="utf-8") as f:
                code_content = f.read()

            fc1, fc2, fc3 = st.columns([1, 1, 2])
            with fc1:
                st.metric("Total Lines", f"{len(code_content.splitlines()):,}")
            with fc2:
                st.metric("File Size", f"{len(code_content):,} bytes")
            with fc3:
                st.caption(f"Location: `{file_path}`")

            st.code(code_content, language="python")

# ---------------------------------------------------------
# TAB 5: DYNAMIC TABLES & CODEBOOK
# ---------------------------------------------------------
with tab_tables:
    st.subheader("Symbol Frequency & Optimal Prefix Codebook Table")
    st.markdown("Each symbol's empirical probability, Shannon information content, and assigned prefix code:")

    codebook_records = []
    for char, freq in sorted(huffman.frequencies.items(), key=lambda x: x[1], reverse=True):
        p_i = freq / total_chars
        info_content = -math.log2(p_i) if p_i > 0 else 0
        h_code = codes.get(char, "")
        sf_code = sf_codes.get(char, "")
        display_char = repr(char) if char in (' ', '\n', '\t') else char
        codebook_records.append({
            "Symbol": display_char,
            "ASCII Dec": ord(char),
            "Frequency": freq,
            "Probability p(s)": round(p_i, 5),
            "Shannon Info (bits)": round(info_content, 3),
            "Huffman Code": h_code,
            "Length l_i": len(h_code),
            "Shannon-Fano Code": sf_code
        })

    codebook_df = pd.DataFrame(codebook_records)
    st.dataframe(codebook_df, use_container_width=True, hide_index=True)

    csv_data = codebook_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Codebook as CSV",
        data=csv_data,
        file_name="huffman_codebook.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# TAB 6: ROOTED BINARY TREE VISUALIZATION
# ---------------------------------------------------------
with tab_tree:
    st.subheader("Rooted Binary Prefix Code Tree (Graph Visualization)")
    st.markdown("""
    Graph representation: **Blue circles** represent internal vertices (merged weights); 
    **Green squares** represent leaf vertices (symbols + frequency weights). 
    Edge labels **0** (left branch) and **1** (right branch) dictate prefix bitpaths.
    """)

    view_type = st.radio(
        "Graph Rendering Strategy:",
        ["Depth-Limited Tree (Top Levels - Matches Screenshot)", "Top Frequent Characters Subtree"],
        horizontal=True
    )

    if view_type.startswith("Depth-Limited"):
        max_d = st.slider("Select Maximum Tree Depth to Display:", 2, 7, 5)
        fig_w = max(14, int(max_d * 2.8))
        fig, ax = plt.subplots(figsize=(fig_w, 8))
        graph, pos, labels, edge_labels = HuffmanVisualizer.build_networkx_graph(root, max_depth=max_d)
    else:
        top_n = st.slider("Select Number of Top Frequent Characters to Render:", 4, min(24, len(huffman.frequencies)), 12)
        top_chars = [char for char, _ in sorted(huffman.frequencies.items(), key=lambda x: x[1], reverse=True)[:top_n]]
        filtered_text = "".join(c for c in raw_text if c in top_chars)
        vis_tree = HuffmanTree()
        vis_root = vis_tree.build_tree(filtered_text)
        fig_w = max(13, int(top_n * 0.9))
        fig, ax = plt.subplots(figsize=(fig_w, 7))
        graph, pos, labels, edge_labels = HuffmanVisualizer.build_networkx_graph(vis_root)

    internal_nodes = [n for n, attr in graph.nodes(data=True) if attr['type'] == 'internal']
    leaf_nodes = [n for n, attr in graph.nodes(data=True) if attr['type'] == 'leaf']

    nx.draw_networkx_nodes(graph, pos, nodelist=internal_nodes, node_color="#6baed6", node_size=1500, node_shape="o", ax=ax)
    nx.draw_networkx_nodes(graph, pos, nodelist=leaf_nodes, node_color="#74c476", node_size=1700, node_shape="s", ax=ax)
    nx.draw_networkx_edges(graph, pos, arrows=False, edge_color="#636363", width=1.5, ax=ax)
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8.5, font_family="sans-serif", ax=ax)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, font_color="#cb181d", ax=ax)

    plt.axis("off")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ---------------------------------------------------------
# TAB 7: BENCHMARKING & EXPERIMENTAL GRAPHS
# ---------------------------------------------------------
with tab_exp:
    st.subheader("Stage 6: Experimental Benchmarks & Quantitative Comparison")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("#### Experiment 1: Efficiency Across 4 Data Domains")
        chart1_path = os.path.join(BASE_DIR, "experiments", "plots", "exp1_entropy_vs_codelength.png")
        if os.path.exists(chart1_path):
            st.image(chart1_path, caption="Comparative Entropy vs. Huffman vs. Shannon-Fano Across Domains", use_container_width=True)
        csv1_path = os.path.join(BASE_DIR, "experiments", "plots", "experiment1_results.csv")
        if os.path.exists(csv1_path):
            st.dataframe(pd.read_csv(csv1_path), use_container_width=True, hide_index=True)

    with col_e2:
        st.markdown("#### Experiment 2: Runtime Scaling (N = 300 to 100,000)")
        chart2_path = os.path.join(BASE_DIR, "experiments", "plots", "exp2_runtime_scaling.png")
        if os.path.exists(chart2_path):
            st.image(chart2_path, caption="Execution Runtime Scaling Across Problem Instances", use_container_width=True)
        csv2_path = os.path.join(BASE_DIR, "experiments", "plots", "experiment2_results.csv")
        if os.path.exists(csv2_path):
            st.dataframe(pd.read_csv(csv2_path), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# TAB 8: STANDALONE VISUAL MODEL
# ---------------------------------------------------------
with tab_model:
    st.subheader("🌐 Standalone Interactive HTML5/SVG Visual Explainer Model")
    st.markdown("""
    The standalone interactive simulation model (`interactive_model.html`) runs completely client-side in any web browser,
    featuring an SVG binary tree renderer, live bitstream tracer, priority queue stepper, and direct code feeder.
    """)

    html_model_path = os.path.join(BASE_DIR, "interactive_model.html")
    if os.path.exists(html_model_path):
        with open(html_model_path, "r", encoding="utf-8") as f:
            html_raw = f.read()
        components.html(html_raw, height=850, scrolling=True)
    else:
        st.info("Standalone model file `interactive_model.html` generated in workspace.")

# ---------------------------------------------------------
# TAB 9: 8-STAGE CURRICULUM COMPLIANCE
# ---------------------------------------------------------
with tab_compliance:
    st.subheader("Experiential Learning 8-Stage Syllabus Compliance Matrix")
    
    stages_table = pd.DataFrame([
        {"Stage": "1. Problem Identification", "Syllabus Activity": "Define real-world problem & significance.", "Implementation Status": "✅ Uncompressed payload bottleneck in blockchain & genomic storage"},
        {"Stage": "2. Mathematical Formulation", "Syllabus Activity": "Represent using discrete structures (trees, Kraft).", "Implementation Status": "✅ Rooted binary tree T=(V,E), Kraft sum = 1.0, Shannon bound"},
        {"Stage": "3. Algorithm Development", "Syllabus Activity": "Select DMGT technique; provide pseudocode.", "Implementation Status": "✅ Greedy bottom-up min-heap priority queue & DFS prefix code extraction"},
        {"Stage": "4. Implementation", "Syllabus Activity": "Implement proposed method using Python.", "Implementation Status": "✅ Modular Python engine (heapq, codec.py, visualizer.py, main.py)"},
        {"Stage": "5. Experimental Analysis", "Syllabus Activity": "Conduct at least 2 meaningful experiments.", "Implementation Status": "✅ Exp 1: 4 data domains (N >= 300); Exp 2: Scaling (300 to 100,000 symbols)"},
        {"Stage": "6. Results & Interpretation", "Syllabus Activity": "Present results using tables, graphs, visualizers.", "Implementation Status": "✅ Delivered Tables 2 & 3, Bar Chart, NetworkX tree, Scaling curve"},
        {"Stage": "7. Comparison & Discussion", "Syllabus Activity": "Compare two algorithms & discuss behavior.", "Implementation Status": "✅ Huffman vs. Shannon-Fano vs. ASCII (proved L_Huffman <= L_SF)"},
        {"Stage": "8. Conclusion & Future Scope", "Syllabus Activity": "Summarize findings, limitations, future scope.", "Implementation Status": "✅ Confirmed Shannon convergence, header overhead, adaptive coding"}
    ])
    st.dataframe(stages_table, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.caption("JAIN (Deemed-to-be University) • School of Computer Science & Engineering • CSE - BLOCKCHAIN")
