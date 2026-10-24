"""
Generate Publication-Quality PowerPoint Presentation (.pptx)
Course: Discrete Mathematics and Graph Theory (DMGT)
Institution: Faculty of Engineering and Technology, JAIN (Deemed-to-be University)
Topic 14: Optimal Prefix Codes and Data Compression Using Huffman Coding
Evaluator: Dr. Priya Satish
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "docs")
    plots_dir = os.path.join(base_dir, "experiments", "plots")
    output_pptx = os.path.join(docs_dir, "PRESENTATION_SLIDES.pptx")
    logo_path = os.path.join(docs_dir, "jain_logo.png")

    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    NAVY = RGBColor(16, 44, 87)
    BLUE = RGBColor(31, 78, 120)
    ACCENT = RGBColor(230, 85, 13)
    GREEN = RGBColor(49, 163, 84)
    DARK = RGBColor(30, 30, 30)
    LIGHT_BG = RGBColor(248, 249, 250)
    WHITE = RGBColor(255, 255, 255)
    GRAY = RGBColor(100, 100, 100)
    BORDER_COLOR = RGBColor(220, 224, 230)

    def set_cell_background(cell, hex_or_rgb):
        cell.fill.solid()
        if isinstance(hex_or_rgb, str):
            r = int(hex_or_rgb[0:2], 16)
            g = int(hex_or_rgb[2:4], 16)
            b = int(hex_or_rgb[4:6], 16)
            cell.fill.fore_color.rgb = RGBColor(r, g, b)
        else:
            cell.fill.fore_color.rgb = hex_or_rgb

    def add_header(slide, title_text, category="TOPIC 14: EXPERIENTIAL LEARNING PROJECT", speaker=None):
        # Top banner background accent
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = NAVY
        top_bar.line.color.rgb = NAVY

        # Category / Mini Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(8), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(240, 173, 78)

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(9.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

        # Speaker Tag (Right side)
        if speaker:
            spk_box = slide.shapes.add_textbox(Inches(9.2), Inches(0.35), Inches(3.4), Inches(0.6))
            tf_spk = spk_box.text_frame
            tf_spk.word_wrap = True
            p_spk = tf_spk.paragraphs[0]
            p_spk.alignment = PP_ALIGN.RIGHT
            p_spk.text = f"Presenter: {speaker}"
            p_spk.font.name = "Arial"
            p_spk.font.size = Pt(11)
            p_spk.font.bold = True
            p_spk.font.color.rgb = RGBColor(220, 235, 252)

        # Footer
        footer = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        tf_f = footer.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "Discrete Mathematics & Graph Theory (DMGT) | CSE - Blockchain Technology | JAIN (Deemed-to-be University)"
        p_f.font.name = "Calibri"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = GRAY

    def add_card(slide, left, top, width, height, bg_color=LIGHT_BG, border_color=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ==========================================
    # SLIDE 1: TITLE COVER
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    # Background
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(250, 252, 255)
    bg1.line.color.rgb = RGBColor(250, 252, 255)

    # University Logo
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(0.8), Inches(0.6), width=Inches(3.8))

    # Title Card
    c_title = add_card(s1, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.5), bg_color=NAVY, border_color=NAVY)
    tb_t = s1.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(2.1))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "DISCRETE MATHEMATICS & GRAPH THEORY — EXPERIENTIAL LEARNING"
    p_t1.font.name = "Arial"
    p_t1.font.size = Pt(12)
    p_t1.font.bold = True
    p_t1.font.color.rgb = RGBColor(240, 173, 78)

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Optimal Prefix Codes and Data Compression Using Huffman Coding"
    p_t2.font.name = "Arial"
    p_t2.font.size = Pt(25)
    p_t2.font.bold = True
    p_t2.font.color.rgb = WHITE
    p_t2.space_before = Pt(6)

    p_t3 = tf_t.add_paragraph()
    p_t3.text = "An Information-Theoretic and Graph-Based Algorithmic Approach to Lossless Encoding"
    p_t3.font.name = "Calibri"
    p_t3.font.size = Pt(14)
    p_t3.font.italic = True
    p_t3.font.color.rgb = RGBColor(200, 220, 245)
    p_t3.space_before = Pt(4)

    # Left Card: Evaluation Details
    add_card(s1, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4))
    tb_eval = s1.shapes.add_textbox(Inches(1.0), Inches(4.6), Inches(5.2), Inches(2.2))
    tf_ev = tb_eval.text_frame
    tf_ev.word_wrap = True

    p_e1 = tf_ev.paragraphs[0]
    p_e1.text = "ACADEMIC EVALUATION DETAILS"
    p_e1.font.name = "Arial"
    p_e1.font.size = Pt(11)
    p_e1.font.bold = True
    p_e1.font.color.rgb = NAVY

    p_e2 = tf_ev.add_paragraph()
    p_e2.text = "Submitted to:\nDr. Priya Satish\nAssistant Professor, Department of Mathematics\nFaculty of Engineering & Technology, JAIN (Deemed-to-be University)"
    p_e2.font.size = Pt(10.5)
    p_e2.font.color.rgb = DARK
    p_e2.space_before = Pt(4)

    p_e3 = tf_ev.add_paragraph()
    p_e3.text = "Branch: CSE - BLOCKCHAIN  •  Date: 10-11-2026"
    p_e3.font.size = Pt(9.5)
    p_e3.font.bold = True
    p_e3.font.color.rgb = BLUE
    p_e3.space_before = Pt(4)

    # Right Card: Group Members Summary
    add_card(s1, Inches(6.6), Inches(4.5), Inches(5.933), Inches(2.4))
    tb_grp = s1.shapes.add_textbox(Inches(6.8), Inches(4.6), Inches(5.5), Inches(2.2))
    tf_g = tb_grp.text_frame
    tf_g.word_wrap = True

    p_g1 = tf_g.paragraphs[0]
    p_g1.text = "SUBMITTED BY (TEAM MEMBERS):"
    p_g1.font.name = "Arial"
    p_g1.font.size = Pt(11)
    p_g1.font.bold = True
    p_g1.font.color.rgb = NAVY

    members_summary = [
        ("Nikhil Kumar (25BTRBT026)", "Project Lead & Core Implementation"),
        ("Piyush Kumar (25BTRBT030)", "Encoder/Decoder & Verification"),
        ("Sakshi Kumari (25BTRC0045)", "Mathematical Formulation & Theory"),
        ("Arushi Pramanik (25BTRBT008)", "Dataset Collection & Preprocessing"),
        ("Harsh R Rao (25BTRBT017)", "Experimental Design & Benchmarking"),
        ("Khyathi Jain (25BTRBT021)", "Visualization & Presentation")
    ]
    for name, role in members_summary:
        p_m = tf_g.add_paragraph()
        p_m.text = f"• {name}  —  {role}"
        p_m.font.size = Pt(9)
        p_m.font.color.rgb = DARK
        p_m.space_before = Pt(1)

    s1.notes_slide.notes_text_frame.text = "Slide 1 Speaker: Nikhil Kumar\nWelcome faculty evaluator Dr. Priya Satish and introduce our topic on Optimal Prefix Codes and Huffman Compression."

    # ==========================================
    # SLIDE 2: TEAM WORK BREAKDOWN (6 ROLES)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Team Task Distribution & Responsibility Allocation", speaker="Nikhil Kumar")

    # 6 Member Cards in a 3x2 Grid
    roles_detail = [
        ("Nikhil Kumar", "25BTRBT026", "Project Lead & Core Algorithm", [
            "Min-heap greedy Huffman tree builder (heapq)",
            "DFS recursive prefix code extractor",
            "Baseline Shannon-Fano algorithm implementation",
            "Central pipeline integration & GitHub management"
        ], NAVY),
        ("Piyush Kumar", "25BTRBT030", "Codec & Lossless Verification", [
            "Bitstream serialization & 8-bit byte chunk packing",
            "Bitstream padding & trimming calculations",
            "Tree-walk decoder with zero delimiter overhead",
            "Pytest test suite (6/6 tests passing)"
        ], BLUE),
        ("Sakshi Kumari", "25BTRC0045", "Mathematical Formulation & Theory", [
            "Discrete tree structures & path length definitions",
            "Kraft–McMillan inequality proofs & verification",
            "Shannon Source Coding Theorem bounds H(X) <= L(C)",
            "Greedy-choice & optimal substructure proofs"
        ], GREEN),
        ("Arushi Pramanik", "25BTRBT008", "Dataset & Preprocessing", [
            "Curated 4 corpora exceeding >= 300 records rule",
            "NCBI GenBank bacteriophage DNA FASTA sequence",
            "Project Gutenberg English text & CPython source code",
            "Statistical frequency distribution tables"
        ], ACCENT),
        ("Harsh R Rao", "25BTRBT017", "Experiments & Benchmarking", [
            "Designed Exp 1: Cross-domain efficiency metrics",
            "Designed Exp 2: Runtime scaling (300 to 100k items)",
            "Compared Huffman vs. Shannon-Fano vs. ASCII",
            "Generated CSV results & Matplotlib charts"
        ], NAVY),
        ("Khyathi Jain", "25BTRBT021", "Visualization & Documentation", [
            "NetworkX rooted binary tree layout generator",
            "Visual decision edge labeling ('0' and '1')",
            "Compiled research report (Word, HTML, LaTeX)",
            "Presentation slides design & coordination"
        ], BLUE),
    ]

    for idx, (m_name, usn, role, tasks, col) in enumerate(roles_detail):
        col_idx = idx % 3
        row_idx = idx // 3
        left = Inches(0.8 + col_idx * 3.95)
        top = Inches(1.5 + row_idx * 2.7)
        width = Inches(3.75)
        height = Inches(2.5)

        card = add_card(s2, left, top, width, height)
        # Header strip inside card
        header_strip = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.6))
        header_strip.fill.solid()
        header_strip.fill.fore_color.rgb = col
        header_strip.line.color.rgb = col

        # Card Title
        tb_c = s2.shapes.add_textbox(left + Inches(0.1), top + Inches(0.05), width - Inches(0.2), Inches(0.5))
        tf_c = tb_c.text_frame
        p_n = tf_c.paragraphs[0]
        p_n.text = f"{m_name} ({usn})"
        p_n.font.size = Pt(10.5)
        p_n.font.bold = True
        p_n.font.color.rgb = WHITE
        p_r = tf_c.add_paragraph()
        p_r.text = role
        p_r.font.size = Pt(8.5)
        p_r.font.color.rgb = RGBColor(230, 230, 230)

        # Card Bullets
        tb_b = s2.shapes.add_textbox(left + Inches(0.1), top + Inches(0.65), width - Inches(0.2), height - Inches(0.7))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for t in tasks:
            p_t = tf_b.add_paragraph() if tf_b.paragraphs[0].text else tf_b.paragraphs[0]
            p_t.text = f"• {t}"
            p_t.font.size = Pt(8.5)
            p_t.font.color.rgb = DARK
            p_t.space_before = Pt(2)

    s2.notes_slide.notes_text_frame.text = "Slide 2 Speaker: Nikhil Kumar\nExplain the balanced task distribution. All 6 members have clear, verifiable technical roles aligned with the rubric."

    # ==========================================
    # SLIDE 3: PROBLEM IDENTIFICATION & SIGNIFICANCE
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Stage 1: Problem Identification & Real-World Relevance", speaker="Nikhil Kumar")

    # Card 1: The Core Technical Problem
    add_card(s3, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    tb_p1 = s3.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf_p1 = tb_p1.text_frame
    tf_p1.word_wrap = True

    p = tf_p1.paragraphs[0]
    p.text = "THE CORE ENGINEERING BOTTLENECK"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_p1.add_paragraph()
    p.text = "Fixed-Length Encoding Redundancy:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_before = Pt(8)

    p = tf_p1.add_paragraph()
    p.text = (
        "• Standard computer architectures represent data using fixed 8-bit ASCII or 16-bit Unicode.\n"
        "• Under fixed-length encoding, every symbol consumes an identical bit depth (8 bits), "
        "ignoring non-uniform symbol occurrence frequencies.\n"
        "• Frequent characters (like 'e', spaces, or 'A' in DNA) consume the exact same capacity as rare characters ('z', '$').\n"
        "• Result: Massive statistical redundancy R = 8 - H(X), wasting up to 70% of storage and bandwidth."
    )
    p.font.size = Pt(10)
    p.space_before = Pt(4)

    p = tf_p1.add_paragraph()
    p.text = "The Mathematical Challenge:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.space_before = Pt(8)

    p = tf_p1.add_paragraph()
    p.text = "How to construct a variable-length prefix code that guarantees instantaneous decoding, approaches Shannon Entropy H(X), and achieves 100% lossless recovery (D(E(M)) = M)?"
    p.font.size = Pt(10)
    p.font.italic = True
    p.space_before = Pt(4)

    # Card 2: Blockchain & Engineering Relevance
    add_card(s3, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.3))
    tb_p2 = s3.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.9))
    tf_p2 = tb_p2.text_frame
    tf_p2.word_wrap = True

    p = tf_p2.paragraphs[0]
    p.text = "RELEVANCE TO BLOCKCHAIN & SYSTEMS (CSE-BCT)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_p2.add_paragraph()
    p.text = "1. P2P Block Propagation Latency:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_before = Pt(8)

    p = tf_p2.add_paragraph()
    p.text = "In decentralized blockchains, uncompressed transaction payloads inflate block sizes. Larger blocks take longer to broadcast across peer nodes, causing network desynchronization and higher orphan block/fork rates."
    p.font.size = Pt(10)
    p.space_before = Pt(2)

    p = tf_p2.add_paragraph()
    p.text = "2. Immutable State Ledger Bloat:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_before = Pt(8)

    p = tf_p2.add_paragraph()
    p.text = "Blockchain full nodes must permanently store entire transaction histories. Lossless compression significantly reduces persistent hardware requirements for validators."
    p.font.size = Pt(10)
    p.space_before = Pt(2)

    p = tf_p2.add_paragraph()
    p.text = "3. Biological Big Data & Cloud Economics:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_before = Pt(8)

    p = tf_p2.add_paragraph()
    p.text = "Storing genomic DNA in fixed 8-bit ASCII wastes >70% capacity. Optimal prefix coding reduces file sizes by 3.37x, cutting cloud egress and storage expenses."
    p.font.size = Pt(10)
    p.space_before = Pt(2)

    s3.notes_slide.notes_text_frame.text = "Slide 3 Speaker: Nikhil Kumar\nExplain why uncompressed fixed-length data is redundant. Connect this directly to our branch: Blockchain Technology (CSE-BCT), block propagation, and ledger storage."

    # ==========================================
    # SLIDE 4: OBJECTIVES & MATHEMATICAL FORMULATION
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Stage 2: Mathematical Formulation & Project Objectives", speaker="Sakshi Kumari")

    # Left: 5 Objectives
    add_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3))
    tb_ob = s4.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.9))
    tf_ob = tb_ob.text_frame
    tf_ob.word_wrap = True

    p = tf_ob.paragraphs[0]
    p.text = "PROJECT OBJECTIVES"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    objectives_list = [
        ("1. Graph Modeling", "Formulate prefix codes over directed, rooted weighted binary trees T = (V, E)."),
        ("2. Mathematical Invariants", "Verify Kraft–McMillan inequality (sum 2^-l <= 1) and Shannon entropy bound H(X) <= L(C)."),
        ("3. Pipeline Implementation", "Build end-to-end Python engine (min-heap, bit-packing, lossless tree-walk decoder)."),
        ("4. Quantitative Benchmarking", "Conduct 2 experiments comparing Huffman vs. Shannon-Fano vs. ASCII across 4 datasets (N >= 300)."),
        ("5. Graph Visualization", "Render hierarchical tree structures with edge labels ('0' and '1') using NetworkX.")
    ]
    for title, desc in objectives_list:
        p = tf_ob.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = BLUE
        p.space_before = Pt(6)
        p = tf_ob.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK
        p.space_before = Pt(1)

    # Right: Graph Theoretic Formulation
    add_card(s4, Inches(6.7), Inches(1.5), Inches(5.833), Inches(5.3))
    tb_mf = s4.shapes.add_textbox(Inches(6.9), Inches(1.7), Inches(5.4), Inches(4.9))
    tf_mf = tb_mf.text_frame
    tf_mf.word_wrap = True

    p = tf_mf.paragraphs[0]
    p.text = "DMGT DISCRETE GRAPH FORMULATION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    math_points = [
        ("Alphabet & Probabilities", "Finite alphabet Sigma = {s_1, ..., s_n} with frequencies f_i and probabilities p_i = f_i / N where sum(p_i) = 1."),
        ("Rooted Binary Tree T = (V, E)", "• Leaf nodes V_L: Symbols s_i with weight w(v_i) = f_i at depth l_i.\n• Internal nodes V_I: Out-degree 2 with weight w(u) = w(u_left) + w(u_right).\n• Directed edges: Left branch labeled '0', right branch labeled '1'."),
        ("Prefix-Free Condition", "No codeword c(s_i) is a prefix of another c(s_j). Guaranteed by placing all symbols strictly at tree leaves (V_L)."),
        ("Weighted External Path Length (WEPL)", "Total compressed bits: W(T) = sum_{v in V_L} w(v) * depth(v) = N * L(C).\nMinimizing expected codeword length L(C) is mathematically identical to finding a tree with minimum WEPL.")
    ]
    for title, desc in math_points:
        p = tf_mf.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = GREEN
        p.space_before = Pt(6)
        p = tf_mf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK
        p.space_before = Pt(1)

    s4.notes_slide.notes_text_frame.text = "Slide 4 Speaker: Sakshi Kumari\nExplain the 5 project objectives and how graph theory models compression: leaves hold symbols, root-to-leaf paths give codewords, and WEPL equals total compressed length."

    # ==========================================
    # SLIDE 5: THEORETICAL THEOREMS & BOUNDS
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Stage 2 (Cont.): Information-Theoretic Limits & Optimality Proof", speaker="Sakshi Kumari")

    # 3 Theorem Cards
    thm_data = [
        ("Theorem 1: Kraft–McMillan Inequality",
         "For any uniquely decodable binary prefix code with lengths l_1, l_2, ..., l_n:\n\n"
         "        sum_{i=1}^n  2^(-l_i)  <=  1.0\n\n"
         "• Strict equality (= 1.0) holds if and only if the rooted binary tree is full (every internal node has out-degree 2).\n"
         "• In our project: Evaluated sum = 1.000000 across all 4 datasets, proving zero wasted codeword space.",
         NAVY),
        ("Theorem 2: Shannon's Source Coding Theorem",
         "The Shannon entropy H(X) is the theoretical lower limit of lossless compression:\n\n"
         "        H(X) = - sum_{i=1}^n  p_i * log2(p_i)   (bits/symbol)\n\n"
         "For any optimal instantaneous code, expected length L(C) satisfies:\n\n"
         "        H(X)  <=  L(C)  <  H(X) + 1\n\n"
         "• Redundancy R = L(C) - H(X) >= 0 measures efficiency gap.\n"
         "• Huffman coding achieves R < 0.03 bits/sym on English text.",
         BLUE),
        ("Proof Sketch: Huffman Optimality",
         "Huffman coding achieves minimum WEPL via two graph invariants:\n\n"
         "1. Greedy-Choice Property: Two symbols with lowest frequencies appear as sibling leaves at maximum tree depth.\n\n"
         "2. Optimal Substructure: Merging two lowest-weight nodes u, v into parent z reduces alphabet size from n to n-1:\n"
         "        W(T) = W(T') + w(u) + w(v)\n"
         "Minimizing W(T) is equivalent to minimizing W(T'), proving global optimality by induction.",
         GREEN)
    ]

    for idx, (t_title, t_body, col) in enumerate(thm_data):
        left = Inches(0.8 + idx * 3.95)
        top = Inches(1.5)
        width = Inches(3.75)
        height = Inches(5.3)

        add_card(s5, left, top, width, height)
        # Top banner
        b = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.65))
        b.fill.solid()
        b.fill.fore_color.rgb = col
        b.line.color.rgb = col

        tb_th = s5.shapes.add_textbox(left + Inches(0.1), top + Inches(0.08), width - Inches(0.2), Inches(0.55))
        p = tb_th.text_frame.paragraphs[0]
        p.text = t_title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

        tb_tb = s5.shapes.add_textbox(left + Inches(0.15), top + Inches(0.75), width - Inches(0.3), height - Inches(0.85))
        tf = tb_tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t_body
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK

    s5.notes_slide.notes_text_frame.text = "Slide 5 Speaker: Sakshi Kumari\nWalk through Kraft's inequality (sum 2^-l <= 1), Shannon's entropy bound H(X) <= L < H+1, and explain why bottom-up greedy merging is mathematically optimal."

    # ==========================================
    # SLIDE 6: ALGORITHM DESIGN & MIN-HEAP
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Stage 3: Algorithm Architecture & Min-Heap Priority Queue", speaker="Nikhil Kumar")

    # Left: Algorithm Steps
    add_card(s6, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.3))
    tb_al = s6.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(4.9))
    tf_al = tb_al.text_frame
    tf_al.word_wrap = True

    p = tf_al.paragraphs[0]
    p.text = "HUFFMAN GREEDY MIN-HEAP PIPELINE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    steps = [
        ("Step 1: Frequency Counting", "Scan input text M of length N to build frequency map in O(N) time."),
        ("Step 2: Min-Heap Initialization", "Instantiate |Sigma| leaf nodes and build min-priority queue using heapq.heapify() in O(|Sigma|) time."),
        ("Step 3: Greedy Tree Merging", "While heap size > 1:\n  1. u = heappop(Q)  (smallest weight)\n  2. v = heappop(Q)  (2nd smallest)\n  3. parent = Node(weight=u.freq + v.freq, left=u, right=v)\n  4. heappush(Q, parent)\nLoop executes |Sigma|-1 times in O(|Sigma| log |Sigma|) time."),
        ("Step 4: DFS Prefix Code Extraction", "Traverse from root to leaves: going Left appends '0', Right appends '1'. Leaf node records codeword in O(|Sigma|) time.")
    ]
    for s_title, s_desc in steps:
        p = tf_al.add_paragraph()
        p.text = s_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = BLUE
        p.space_before = Pt(6)
        p = tf_al.add_paragraph()
        p.text = s_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK
        p.space_before = Pt(1)

    # Right: Complexity & Baseline
    add_card(s6, Inches(6.9), Inches(1.5), Inches(5.633), Inches(5.3))
    tb_cx = s6.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(4.9))
    tf_cx = tb_cx.text_frame
    tf_cx.word_wrap = True

    p = tf_cx.paragraphs[0]
    p.text = "TIME COMPLEXITY & COMPARISON BASELINE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_cx.add_paragraph()
    p.text = "Computational Complexity Analysis:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_before = Pt(8)

    p = tf_cx.add_paragraph()
    p.text = (
        "• Tree Construction: O(|Sigma| log |Sigma|)\n"
        "• Text Encoding: O(N) via hash table lookup\n"
        "• Tree-Walk Decoding: O(N) - 1 step per bit\n"
        "• Total Time: O(N + |Sigma| log |Sigma|)\n"
        "• Space Complexity: O(|Sigma|) tree nodes\n"
        "Because |Sigma| <= 256 for ASCII, tree build is instant (~0.18 ms), rendering runtime strictly linear with text size N."
    )
    p.font.size = Pt(9.5)
    p.space_before = Pt(4)

    p = tf_cx.add_paragraph()
    p.text = "Baseline: Shannon–Fano Coding"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.space_before = Pt(8)

    p = tf_cx.add_paragraph()
    p.text = (
        "• Top-down recursive frequency partitioning.\n"
        "• Sorts symbols, divides list into 2 subsets of equal cumulative frequency, assigns '0' and '1'.\n"
        "• Suboptimal: Top-down local splits cannot foresee bottom combinations, yielding longer codes than Huffman."
    )
    p.font.size = Pt(9.5)
    p.space_before = Pt(4)

    s6.notes_slide.notes_text_frame.text = "Slide 6 Speaker: Nikhil Kumar\nExplain the min-heap implementation, time complexity O(N + |Sigma| log |Sigma|), and how Shannon-Fano works as our comparison baseline."

    # ==========================================
    # SLIDE 7: BIT-LEVEL CODEC & TESTING
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Stage 4: Bitstream Codec & Automated Lossless Verification", speaker="Piyush Kumar")

    # Left: Bit Packing Architecture
    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.3))
    tb_cd = s7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(4.9))
    tf_cd = tb_cd.text_frame
    tf_cd.word_wrap = True

    p = tf_cd.paragraphs[0]
    p.text = "BITSTREAM PACKING & SERIALIZATION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_cd.add_paragraph()
    p.text = "The Memory Alignment Challenge:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_before = Pt(6)

    p = tf_cd.add_paragraph()
    p.text = "Modern storage drives read/write in 8-bit bytes, not individual bits. Concatenating variable prefix codes produces bitstreams whose lengths are not multiples of 8."
    p.font.size = Pt(9.5)
    p.space_before = Pt(2)

    p = tf_cd.add_paragraph()
    p.text = "Our Codec Solution (src/codec.py):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_before = Pt(6)

    p = tf_cd.add_paragraph()
    p.text = (
        "1. Padding Calculation: Extra bits P = (8 - (len mod 8)) mod 8.\n"
        "2. Byte Packing: Packs 8-bit chunks into bytearray().\n"
        "3. Header Protocol: Stores padding count P for clean stripping.\n"
        "4. Tree-Walk Decoding: Reads bitstream bit-by-bit:\n"
        "   • Bit '0' -> navigate to current.left\n"
        "   • Bit '1' -> navigate to current.right\n"
        "   • Leaf node reached -> emit character & reset to root.\n"
        "   • Zero delimiter overhead required!"
    )
    p.font.size = Pt(9.5)
    p.space_before = Pt(2)

    # Right: Pytest Suite
    add_card(s7, Inches(6.9), Inches(1.5), Inches(5.633), Inches(5.3))
    tb_ts = s7.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(4.9))
    tf_ts = tb_ts.text_frame
    tf_ts.word_wrap = True

    p = tf_ts.paragraphs[0]
    p.text = "PYTEST VERIFICATION SUITE (6/6 PASSING)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    tests_list = [
        ("test_basic_lossless_roundtrip", "Verifies mathematical idempotency: D(E(M)) == M."),
        ("test_prefix_property", "Asserts no generated codeword is a prefix of any other codeword."),
        ("test_kraft_inequality", "Validates sum(2^-l_i) <= 1.0 (evaluates to exactly 1.000000)."),
        ("test_entropy_bound", "Confirms empirical expected length satisfies H(X) <= L(C) < H(X)+1."),
        ("test_single_character_edge_case", "Verifies graceful handling of inputs with alphabet size |Sigma| = 1 ('AAAA...')."),
        ("test_shannon_fano_optimality", "Proves Huffman code length <= Shannon-Fano length (L_Huffman <= L_SF).")
    ]
    for t_name, t_desc in tests_list:
        p = tf_ts.add_paragraph()
        p.text = f"[PASS] {t_name}"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = GREEN
        p.space_before = Pt(4)
        p = tf_ts.add_paragraph()
        p.text = t_desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = DARK
        p.space_before = Pt(1)

    s7.notes_slide.notes_text_frame.text = "Slide 7 Speaker: Piyush Kumar\nExplain bit packing into raw bytes, padding handling, tree-walk decoding, and our 6 passing unit tests proving 100% lossless reconstruction."

    # ==========================================
    # SLIDE 8: DATASETS & PROVENANCE
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Stage 5: Benchmark Datasets & Public Provenance (N >= 300)", speaker="Arushi Pramanik")

    # Table of 4 Datasets
    t_ds = s8.shapes.add_table(5, 5, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.7)).table
    t_ds.columns[0].width = Inches(1.6)
    t_ds.columns[1].width = Inches(3.6)
    t_ds.columns[2].width = Inches(1.4)
    t_ds.columns[3].width = Inches(1.5)
    t_ds.columns[4].width = Inches(3.633)

    headers_d = ["Dataset", "Domain Description", "Records (N)", "Alphabet (|Sigma|)", "Public Source / Data Link"]
    for j, h in enumerate(headers_d):
        cell = t_ds.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1F4E78")
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    d_data = [
        ["Dataset A", "Natural Language English Text\n(Academic discrete math literature)", "2,001", "56", "Project Gutenberg & MacTutor Archive\n(sample_english.txt)"],
        ["Dataset B", "Python Source Code\n(DataProcessor class & utilities)", "1,432", "53", "CPython Standard Library Repository\n(sample_code.py)"],
        ["Dataset C", "Genomic DNA Nucleotide Sequence\n(Bacteriophage T4 genome fragment)", "1,031", "29", "NCBI GenBank Accession: NC_000866.4\n(sample_dna.fasta)"],
        ["Dataset D", "Uniform Random Baseline Text\n(Balanced ASCII symbol generator)", "1,140", "76", "Algorithmic Uniform Generator\n(sample_uniform.txt)"]
    ]
    for i, row in enumerate(d_data):
        bg = "F9FBFD" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            cell = t_ds.cell(i+1, j)
            cell.text = val
            set_cell_background(cell, bg)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = DARK
            p.alignment = PP_ALIGN.CENTER if j not in (1, 4) else PP_ALIGN.LEFT
            if j == 0:
                p.font.bold = True

    # Bottom Cards explaining entropy differences
    add_card(s8, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3))
    tb_d1 = s8.shapes.add_textbox(Inches(1.0), Inches(4.6), Inches(5.2), Inches(2.0))
    tf1 = tb_d1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "WHY GENOMIC DNA ACHIEVES 70% COMPRESSION:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p = tf1.add_paragraph()
    p.text = (
        "• DNA features a severely skewed 4-nucleotide alphabet (A, C, G, T).\n"
        "• Theoretical entropy drops to only H = 2.26 bits/symbol.\n"
        "• Huffman assigns short 1-to-2 bit paths to frequent bases.\n"
        "• Result: Massive 3.37x compression ratio (70.37% storage savings)!"
    )
    p.font.size = Pt(9.5)
    p.space_before = Pt(4)

    add_card(s8, Inches(6.8), Inches(4.5), Inches(5.733), Inches(2.3))
    tb_d2 = s8.shapes.add_textbox(Inches(7.0), Inches(4.6), Inches(5.3), Inches(2.0))
    tf2 = tb_d2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "UNIFORM RANDOM CONTROL GROUP:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p = tf2.add_paragraph()
    p.text = (
        "• In uniform text, all 76 symbols occur with equal probability (p_i = 1/76).\n"
        "• Maximum entropy H = 6.25 bits/symbol.\n"
        "• Tree leaves sit at nearly identical depths (depth approx log2 76 = 7).\n"
        "• Proves that prefix compression requires non-uniformity to excel."
    )
    p.font.size = Pt(9.5)
    p.space_before = Pt(4)

    s8.notes_slide.notes_text_frame.text = "Slide 8 Speaker: Arushi Pramanik\nPresent our 4 datasets exceeding the >= 300 data points rule. Highlight the NCBI GenBank biological accession and explain why DNA compresses by 70% while uniform random only compresses by 21%."

    # ==========================================
    # SLIDE 9: EXPERIMENT 1 RESULTS & BAR CHART
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Stage 6 & 7: Experiment 1 — Cross-Domain Compression Efficiency", speaker="Harsh R Rao")

    # Left: Results Table
    t_res = s9.shapes.add_table(11, 5, Inches(0.8), Inches(1.4), Inches(6.5), Inches(5.4)).table
    t_res.columns[0].width = Inches(2.5)
    t_res.columns[1].width = Inches(1.0)
    t_res.columns[2].width = Inches(1.0)
    t_res.columns[3].width = Inches(1.0)
    t_res.columns[4].width = Inches(1.0)

    headers_r = ["Metric", "English", "Code", "DNA", "Uniform"]
    for j, h in enumerate(headers_r):
        cell = t_res.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1F4E78")
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    res_data_p = [
        ["Records (N)", "2,001", "1,432", "1,031", "1,140"],
        ["Alphabet (|Sigma|)", "56", "53", "29", "76"],
        ["Shannon Entropy H(X)", "4.389", "4.389", "2.259", "6.248"],
        ["Huffman L(C) (bits)", "4.417", "4.411", "2.371", "6.316"],
        ["Shannon-Fano L", "4.418", "4.423", "2.373", "6.316"],
        ["Fixed 8-Bit ASCII", "8.000", "8.000", "8.000", "8.000"],
        ["Redundancy (R)", "0.028", "0.022", "0.111", "0.068"],
        ["Compression Ratio", "1.81x", "1.81x", "3.37x", "1.27x"],
        ["Space Savings (%)", "44.78%", "44.87%", "70.37%", "21.05%"],
        ["Kraft Sum (sum 2^-l)", "1.000", "1.000", "1.000", "1.000"]
    ]
    for i, row in enumerate(res_data_p):
        bg = "F9FBFD" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            cell = t_res.cell(i+1, j)
            cell.text = val
            set_cell_background(cell, bg)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5)
            p.font.color.rgb = DARK
            p.alignment = PP_ALIGN.CENTER if j != 0 else PP_ALIGN.LEFT
            if j == 0 or "Huffman" in row[0] or "Savings" in row[0]:
                p.font.bold = True

    # Right: Plot Image
    chart1_path = os.path.join(plots_dir, "exp1_entropy_vs_codelength.png")
    if os.path.exists(chart1_path):
        s9.shapes.add_picture(chart1_path, Inches(7.5), Inches(1.4), width=Inches(5.0))

    # Bottom observations note
    tb_no = s9.shapes.add_textbox(Inches(7.5), Inches(5.1), Inches(5.0), Inches(1.7))
    tf_no = tb_no.text_frame
    tf_no.word_wrap = True
    p = tf_no.paragraphs[0]
    p.text = "KEY QUANTITATIVE OBSERVATIONS:"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p = tf_no.add_paragraph()
    p.text = (
        "• Near-Zero Redundancy: In English text, redundancy is only R = 0.028 bits/sym (< 0.63% above theoretical limit).\n"
        "• Huffman Dominates Shannon-Fano: In every dataset, L_Huffman <= L_SF.\n"
        "• Kraft Completeness: sum(2^-l) = 1.000000 confirms trees are full."
    )
    p.font.size = Pt(8.5)
    p.space_before = Pt(2)

    s9.notes_slide.notes_text_frame.text = "Slide 9 Speaker: Harsh R Rao\nPresent the results of Experiment 1. Walk through the table and bar chart showing how Huffman code length hugs the Shannon entropy line across all domains."

    # ==========================================
    # SLIDE 10: EXPERIMENT 2 & TREE VISUALIZATION
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Stage 6 (Cont.): Tree Visualization & Runtime Complexity Scaling", speaker="Harsh R Rao & Khyathi Jain")

    # Left: NetworkX Tree Graph
    tree_img_path = os.path.join(plots_dir, "huffman_tree_visualization.png")
    if os.path.exists(tree_img_path):
        s10.shapes.add_picture(tree_img_path, Inches(0.8), Inches(1.4), width=Inches(5.7))

    tb_tc = s10.shapes.add_textbox(Inches(0.8), Inches(5.7), Inches(5.7), Inches(1.2))
    tf_tc = tb_tc.text_frame
    tf_tc.word_wrap = True
    p = tf_tc.paragraphs[0]
    p.text = "NetworkX Tree Visualization (Khyathi Jain):"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p = tf_tc.add_paragraph()
    p.text = "Visualizes rooted binary tree: Blue circles = internal nodes (merged weights); Green squares = leaf symbols. Red edge labels '0' (left) and '1' (right) trace prefix paths."
    p.font.size = Pt(8.5)
    p.space_before = Pt(2)

    # Right: Experiment 2 Scaling Plot
    chart2_path = os.path.join(plots_dir, "exp2_runtime_scaling.png")
    if os.path.exists(chart2_path):
        s10.shapes.add_picture(chart2_path, Inches(6.8), Inches(1.4), width=Inches(5.733))

    tb_sc = s10.shapes.add_textbox(Inches(6.8), Inches(5.7), Inches(5.733), Inches(1.2))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    p = tf_sc.paragraphs[0]
    p.text = "Experiment 2 Scaling Findings (Harsh R Rao):"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p = tf_sc.add_paragraph()
    p.text = "Tested N = 300 up to 100,000 symbols. Total execution time scales linearly (3.63 ms for 100k symbols), proving high-speed processing (>27,000 chars/ms) suitable for blockchain streaming."
    p.font.size = Pt(8.5)
    p.space_before = Pt(2)

    s10.notes_slide.notes_text_frame.text = "Slide 10 Speakers: Harsh R Rao & Khyathi Jain\nHarsh explains the linear scaling curve (Exp 2). Khyathi explains the NetworkX tree visualization with internal nodes, leaf nodes, and decision edges."

    # ==========================================
    # SLIDE 11: 8-STAGE CURRICULUM COMPLIANCE
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Experiential Learning 8-Stage Syllabus Compliance", speaker="Khyathi Jain")

    t_stg = s11.shapes.add_table(9, 3, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3)).table
    t_stg.columns[0].width = Inches(2.2)
    t_stg.columns[1].width = Inches(4.3)
    t_stg.columns[2].width = Inches(5.233)

    headers_stg = ["Curriculum Stage", "Prescribed Syllabus Activity", "Project Implementation & Proof"]
    for j, h in enumerate(headers_stg):
        cell = t_stg.cell(0, j)
        cell.text = h
        set_cell_background(cell, "1F4E78")
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    stages_data_p = [
        ["1. Problem Identification", "Define real-world engineering problem & significance.", "Uncompressed block payload bottleneck in blockchain & genomic repositories."],
        ["2. Math Formulation", "Represent using discrete structures: trees, Kraft inequality.", "Modeled as rooted binary tree T=(V,E); proved Kraft sum = 1.000000 & entropy bound."],
        ["3. Algorithm Development", "Select DMGT technique; provide pseudocode.", "Greedy bottom-up min-heap priority queue construction & DFS prefix extraction."],
        ["4. Implementation", "Implement proposed method using Python.", "Modular Python codebase (heapq, NetworkX, Matplotlib, codec.py, main.py)."],
        ["5. Experimental Analysis", "Conduct at least 2 meaningful experiments.", "Exp 1: 4 data domains (N >= 300); Exp 2: Runtime scaling (300 to 100,000 symbols)."],
        ["6. Results & Interpretation", "Present results using tables, graphs, visualizations.", "Delivered Tables 2 & 3, Figure 1 (Bar chart), Figure 2 (Tree), Figure 3 (Scaling)."],
        ["7. Comparison & Discussion", "Compare two algorithms and discuss behavior.", "Compared Huffman vs. Shannon-Fano vs. ASCII, mathematically proving L_Huffman <= L_SF."],
        ["8. Conclusion & Scope", "Summarize findings, explain contribution, limitations.", "Confirmed Shannon convergence, noted header overhead, proposed dynamic adaptive coding."]
    ]
    for i, row in enumerate(stages_data_p):
        bg = "F9FBFD" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            cell = t_stg.cell(i+1, j)
            cell.text = val
            set_cell_background(cell, bg)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5)
            p.font.color.rgb = DARK
            p.alignment = PP_ALIGN.CENTER if j == 0 else PP_ALIGN.LEFT
            if j == 0:
                p.font.bold = True

    s11.notes_slide.notes_text_frame.text = "Slide 11 Speaker: Khyathi Jain\nPresent the 8-stage compliance matrix showing Dr. Priya Satish that every single required syllabus stage has been completely satisfied."

    # ==========================================
    # SLIDE 12: CONCLUSION, SCOPE & Q&A
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Stage 8: Conclusion, Future Scope & Team Reflections", speaker="All Team Members")

    # Left: Findings & Scope
    add_card(s12, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.3))
    tb_c1 = s12.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(4.9))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True

    p = tf_c1.paragraphs[0]
    p.text = "PROJECT FINDINGS & LIMITATIONS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_c1.add_paragraph()
    p.text = "Major Findings:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_before = Pt(6)

    p = tf_c1.add_paragraph()
    p.text = (
        "• Huffman coding guarantees mathematically optimal prefix codes.\n"
        "• Delivers up to 70.37% storage savings on skewed genomic data.\n"
        "• Consistently matches or outperforms Shannon-Fano coding (L_Huffman <= L_SF).\n"
        "• Operates within 0.63% of Shannon theoretical entropy limit on text."
    )
    p.font.size = Pt(9.5)
    p.space_before = Pt(2)

    p = tf_c1.add_paragraph()
    p.text = "Limitations & Future Scope:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    p.space_before = Pt(6)

    p = tf_c1.add_paragraph()
    p.text = (
        "• Header Overhead: Storing codebook tables adds overhead on tiny files (N < 200).\n"
        "• Future Extension 1: Adaptive Dynamic Huffman (Vitter's algorithm) to compress real-time streams with zero header overhead.\n"
        "• Future Extension 2: Arithmetic Coding for non-integer bit allocation.\n"
        "• Future Extension 3: Integration into blockchain node transaction pooling."
    )
    p.font.size = Pt(9.5)
    p.space_before = Pt(2)

    # Right: Thank You & Q&A Box
    add_card(s12, Inches(6.9), Inches(1.5), Inches(5.633), Inches(5.3))
    tb_c2 = s12.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(4.9))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True

    p = tf_c2.paragraphs[0]
    p.text = "OPEN FOR QUESTIONS & VIVA DEFENSE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_c2.add_paragraph()
    p.text = "GitHub Repository Link:\ngithub.com/SmoothnOperator/Dmgt-Huffman-Coding"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_before = Pt(10)

    p = tf_c2.add_paragraph()
    p.text = (
        "Team Members Ready for Q&A:\n\n"
        "• Nikhil Kumar (Lead, Priority Queue & Heap Architecture)\n"
        "• Piyush Kumar (Codec, Bitstream Serialization & Unit Tests)\n"
        "• Sakshi Kumari (DMGT Theory, Kraft Inequality & Entropy)\n"
        "• Arushi Pramanik (Datasets, NCBI GenBank & Skewness)\n"
        "• Harsh R Rao (Experiments 1 & 2, Benchmarks & Scaling)\n"
        "• Khyathi Jain (Tree Visualizations, Slides & Documentation)\n\n"
        "Special thanks to our course faculty Dr. Priya Satish for guidance."
    )
    p.font.size = Pt(9.5)
    p.space_before = Pt(6)

    s12.notes_slide.notes_text_frame.text = "Slide 12: All Members\nConclude the presentation, invite questions from Dr. Priya Satish, and let each member answer questions related to their technical role."

    prs.save(output_pptx)
    print(f"[OK] Successfully generated presentation at: {output_pptx}")

if __name__ == "__main__":
    create_deck()
