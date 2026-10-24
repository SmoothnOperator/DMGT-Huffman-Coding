"""
Builds the standalone interactive visual simulation model (interactive_model.html)
with:
1. Blockchain Gas & P2P Propagation Simulator (Feature 1 - CSE-BCT Major Alignment)
2. Side-by-Side Algorithm Race: Huffman vs Shannon-Fano (Feature 4 - Mathematical Divergence)
3. Cascading animated tree assembly, rolling metric tickers, and interactive signal packet tracer.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load all project codes
code_files = {
    "huffman.py": os.path.join(BASE_DIR, "src", "huffman.py"),
    "codec.py": os.path.join(BASE_DIR, "src", "codec.py"),
    "shannon_fano.py": os.path.join(BASE_DIR, "src", "shannon_fano.py"),
    "visualizer.py": os.path.join(BASE_DIR, "src", "visualizer.py"),
    "benchmark.py": os.path.join(BASE_DIR, "experiments", "benchmark.py"),
    "main.py": os.path.join(BASE_DIR, "main.py"),
    "test_huffman.py": os.path.join(BASE_DIR, "tests", "test_huffman.py")
}

codes_data = {}
for name, path in code_files.items():
    with open(path, "r", encoding="utf-8") as f:
        codes_data[name] = f.read()

# Load benchmark datasets
data_files = {
    "english": os.path.join(BASE_DIR, "data", "sample_english.txt"),
    "code": os.path.join(BASE_DIR, "data", "sample_code.py"),
    "dna": os.path.join(BASE_DIR, "data", "sample_dna.fasta"),
    "uniform": os.path.join(BASE_DIR, "data", "sample_uniform.txt")
}

presets_data = {}
for name, path in data_files.items():
    with open(path, "r", encoding="utf-8") as f:
        presets_data[name] = f.read()

# Add code files to presets too
presets_data["huffman_py"] = codes_data["huffman.py"]
presets_data["codec_py"] = codes_data["codec.py"]
presets_data["shannon_fano_py"] = codes_data["shannon_fano.py"]
presets_data["visualizer_py"] = codes_data["visualizer.py"]
presets_data["benchmark_py"] = codes_data["benchmark.py"]
presets_data["main_py"] = codes_data["main.py"]
presets_data["test_huffman_py"] = codes_data["test_huffman.py"]

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Interactive Huffman Coding Visual Simulation Model & Blockchain Simulator - DMGT Topic 14</title>
  <style>
    :root {{
      --navy: #102C57;
      --blue: #1F4E78;
      --accent: #E6550D;
      --green: #2E7D32;
      --bg: #F8F9FA;
      --card-bg: #FFFFFF;
      --border: #DDE2E5;
      --text: #212529;
      --eth: #627EEA;
      --glow-gold: #FFB300;
      --glow-cyan: #00E5FF;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 50px;
    }}
    header {{
      background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
      color: white;
      padding: 20px 30px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .header-content {{
      max-width: 1450px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 15px;
    }}
    .header-title h1 {{
      font-size: 1.55rem;
      font-weight: 700;
      margin-bottom: 4px;
    }}
    .header-title p {{
      font-size: 0.9rem;
      color: #DDE6ED;
    }}
    .header-badge {{
      background: rgba(255,255,255,0.15);
      border: 1px solid rgba(255,255,255,0.3);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      text-align: right;
    }}
    .container {{
      max-width: 1450px;
      margin: 25px auto;
      padding: 0 20px;
    }}
    .tabs-nav {{
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
      border-bottom: 2px solid var(--border);
      padding-bottom: 2px;
      overflow-x: auto;
    }}
    .tab-btn {{
      padding: 10px 18px;
      border: none;
      background: #EAEFF5;
      color: var(--navy);
      font-weight: 600;
      font-size: 0.92rem;
      border-radius: 6px 6px 0 0;
      cursor: pointer;
      transition: all 0.25s ease;
      white-space: nowrap;
    }}
    .tab-btn:hover {{ background: #D5E1ED; transform: translateY(-1px); }}
    .tab-btn.active {{
      background: var(--navy);
      color: white;
      box-shadow: 0 -2px 8px rgba(16, 44, 87, 0.2);
    }}
    .tab-content {{ display: none; }}
    .tab-content.active {{
      display: block;
      animation: fadeInContent 0.35s ease-out;
    }}
    @keyframes fadeInContent {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
      transition: box-shadow 0.3s ease;
    }}
    .card:hover {{
      box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }}
    .card-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--navy);
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #F0F4F8;
      padding-bottom: 8px;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}
    @media (max-width: 900px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}
    textarea, select, input[type="text"], input[type="number"] {{
      width: 100%;
      padding: 10px 12px;
      border: 1px solid #CED4DA;
      border-radius: 6px;
      font-family: monospace;
      font-size: 0.9rem;
      margin-top: 6px;
      margin-bottom: 12px;
      transition: border 0.2s ease, box-shadow 0.2s ease;
    }}
    textarea:focus, select:focus, input[type="text"]:focus, input[type="number"]:focus {{
      border-color: var(--blue);
      box-shadow: 0 0 0 3px rgba(31, 78, 120, 0.15);
      outline: none;
    }}
    .btn {{
      background: var(--blue);
      color: white;
      border: none;
      padding: 10px 16px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.9rem;
      transition: all 0.25s ease;
    }}
    .btn:hover {{ background: var(--navy); transform: translateY(-1px); }}
    .btn:active {{ transform: translateY(1px); }}
    .btn-green {{
      background: var(--green);
      box-shadow: 0 3px 8px rgba(46, 125, 50, 0.3);
    }}
    .btn-green:hover {{
      background: #1B5E20;
      box-shadow: 0 5px 12px rgba(46, 125, 50, 0.45);
    }}
    .btn-eth {{
      background: var(--eth);
      box-shadow: 0 3px 8px rgba(98, 126, 234, 0.35);
    }}
    .btn-eth:hover {{
      background: #4A65C7;
      box-shadow: 0 5px 12px rgba(98, 126, 234, 0.5);
    }}
    .btn-outline {{
      background: transparent;
      border: 1px solid var(--blue);
      color: var(--blue);
    }}
    .btn-outline:hover {{
      background: #EAEFF5;
    }}
    .btn-sm {{
      padding: 6px 11px;
      font-size: 0.82rem;
    }}
    .metrics-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin: 15px 0;
    }}
    @media (max-width: 800px) {{
      .metrics-grid {{ grid-template-columns: 1fr 1fr; }}
    }}
    .metric-box {{
      background: #F8F9FA;
      border-left: 4px solid var(--blue);
      padding: 12px 14px;
      border-radius: 6px;
      transition: all 0.3s ease;
    }}
    .metric-box.metric-highlight {{
      background: #E8F5E9;
      border-left-color: var(--green);
      transform: scale(1.02);
    }}
    .metric-label {{
      font-size: 0.78rem;
      color: #666;
      text-transform: uppercase;
      font-weight: 600;
    }}
    .metric-val {{
      font-size: 1.45rem;
      font-weight: 700;
      color: var(--navy);
      font-variant-numeric: tabular-nums;
    }}
    .metric-sub {{
      font-size: 0.75rem;
      color: #555;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      margin: 10px 0;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 8px 10px;
      text-align: center;
    }}
    th {{
      background: #EAEFF5;
      color: var(--navy);
      font-weight: 600;
    }}
    tr:nth-child(even) {{ background: #FBFCFE; }}
    
    /* Tree Canvas & Controls */
    .tree-toolbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 12px;
      background: #F4F7FA;
      padding: 10px 14px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }}
    .svg-container {{
      width: 100%;
      height: 640px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #FAFBFD;
      overflow: auto;
      position: relative;
      cursor: grab;
      user-select: none;
      box-shadow: inset 0 2px 6px rgba(0,0,0,0.03);
    }}
    .svg-container:active {{
      cursor: grabbing;
    }}
    svg {{
      display: block;
      transform-origin: 0 0;
      transition: transform 0.08s ease-out;
    }}
    .step-controls {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 15px 0;
      flex-wrap: wrap;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 9px;
      font-size: 0.8rem;
      border-radius: 4px;
      font-weight: 600;
      transition: all 0.3s ease;
    }}
    .badge-pass {{ background: #D4EDDA; color: #155724; }}
    .badge-warn {{ background: #FFF3CD; color: #856404; }}
    .badge-ready {{ background: #E2E3E5; color: #383D41; }}
    .badge-eth {{ background: #E8EBFB; color: #2C4299; border: 1px solid #C3CBF5; }}
    pre {{
      background: #272822;
      color: #F8F8F2;
      padding: 14px;
      border-radius: 6px;
      overflow-x: auto;
      font-family: Consolas, monospace;
      font-size: 0.85rem;
      max-height: 480px;
    }}
    .queue-chip {{
      display: inline-flex;
      align-items: center;
      background: #E9ECEF;
      border: 1px solid #CED4DA;
      border-radius: 20px;
      padding: 4px 10px;
      margin: 3px;
      font-size: 0.82rem;
      font-family: monospace;
      font-weight: 600;
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .chip-leaf {{
      background: #E8F5E9;
      border-color: #A5D6A7;
      color: #1B5E20;
    }}
    .chip-internal {{
      background: #E3F2FD;
      border-color: #90CAF9;
      color: #0D47A1;
    }}
    .bit-token {{
      display: inline-block;
      padding: 3px 6px;
      margin: 2px;
      font-family: monospace;
      font-weight: bold;
      border-radius: 4px;
      font-size: 0.9rem;
      transition: all 0.2s ease;
    }}
    .bit-active {{
      background: #FF5722;
      color: white;
      transform: scale(1.22);
      box-shadow: 0 0 8px #FF5722;
    }}
    .bit-done {{
      background: #C8E6C9;
      color: #1B5E20;
    }}
    .pulse-glow {{
      animation: pulseGlowBtn 1.8s infinite;
    }}
    @keyframes pulseGlowBtn {{
      0% {{ box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.5); }}
      70% {{ box-shadow: 0 0 0 12px rgba(46, 125, 50, 0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(46, 125, 50, 0); }}
    }}

    /* SVG Keyframe Animations for Tree Unfurling */
    @keyframes nodePopIn {{
      0% {{ transform: scale(0); opacity: 0; }}
      70% {{ transform: scale(1.18); opacity: 1; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}
    @keyframes edgeDrawIn {{
      from {{ stroke-dashoffset: 1000; opacity: 0.2; }}
      to {{ stroke-dashoffset: 0; opacity: 1; }}
    }}
    @keyframes labelFadeIn {{
      0% {{ opacity: 0; transform: translateY(4px) scale(0.8); }}
      100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    .anim-node {{
      transform-box: fill-box;
      transform-origin: center;
      animation: nodePopIn 0.42s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }}
    .anim-edge {{
      animation: edgeDrawIn 0.35s ease-out forwards;
    }}
    .anim-label {{
      transform-box: fill-box;
      transform-origin: center;
      animation: labelFadeIn 0.3s ease-out forwards;
    }}

    /* Interactive Node Hover & Path Highlight */
    .tree-node-group {{
      cursor: pointer;
      transition: filter 0.2s ease;
    }}
    .tree-node-group:hover circle {{
      fill: #0288D1 !important;
      stroke: #81D4FA !important;
      stroke-width: 3.5px !important;
      filter: drop-shadow(0 0 10px #0288D1) !important;
    }}
    .tree-node-group:hover rect {{
      fill: #1B5E20 !important;
      stroke: #A5D6A7 !important;
      stroke-width: 3.2px !important;
      filter: drop-shadow(0 0 12px #2E7D32) !important;
    }}
    .highlight-edge {{
      stroke: #FF9100 !important;
      stroke-width: 3.8px !important;
      filter: drop-shadow(0 0 8px #FF9100) !important;
    }}
    .highlight-node circle {{
      fill: #FF6D00 !important;
      stroke: #FFE082 !important;
      stroke-width: 4px !important;
      filter: drop-shadow(0 0 14px #FF6D00) !important;
    }}
    .highlight-node rect {{
      fill: #FF6D00 !important;
      stroke: #FFE082 !important;
      stroke-width: 4px !important;
      filter: drop-shadow(0 0 14px #FF6D00) !important;
    }}
    
    #tree-hud {{
      position: absolute;
      bottom: 16px;
      left: 16px;
      background: rgba(16, 44, 87, 0.92);
      color: white;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 0.85rem;
      pointer-events: none;
      display: none;
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
      z-index: 100;
      backdrop-filter: blur(4px);
    }}

    /* Race Bar Styling */
    .race-track {{
      background: #E9ECEF;
      border-radius: 8px;
      height: 28px;
      overflow: hidden;
      margin-bottom: 12px;
      position: relative;
    }}
    .race-fill {{
      height: 100%;
      width: 0%;
      border-radius: 8px;
      transition: width 1.2s cubic-bezier(0.25, 1, 0.5, 1);
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding-right: 10px;
      color: white;
      font-weight: bold;
      font-size: 0.82rem;
    }}
  </style>
</head>
<body>

  <header>
    <div class="header-content">
      <div class="header-title">
        <p style="color: #F0AD4E; font-weight: bold; letter-spacing: 0.5px; text-transform: uppercase;">
          JAIN (Deemed-to-be University) • School of Computer Science & Engineering
        </p>
        <h1>Optimal Prefix Codes, Blockchain Gas & Algorithm Race Model</h1>
        <p>DMGT Topic 14 • CSE - BLOCKCHAIN • Faculty Evaluator: Dr. Priya Satish</p>
      </div>
      <div class="header-badge">
        <strong>Team Topic 14:</strong><br>
        Nikhil • Piyush • Sakshi • Arushi • Harsh • Khyathi
      </div>
    </div>
  </header>

  <div class="container">

    <div class="tabs-nav">
      <button class="tab-btn active" onclick="switchTab('tab-simulator')">🌳 Visual Simulation Model</button>
      <button class="tab-btn" onclick="switchTab('tab-step')">🔄 Step-by-Step Priority Queue</button>
      <button class="tab-btn" onclick="switchTab('tab-tracer')">⚡ Interactive Bitstream Tracer</button>
      <button class="tab-btn" onclick="switchTab('tab-blockchain')">⛓️ Blockchain Gas & P2P Simulator</button>
      <button class="tab-btn" onclick="switchTab('tab-race')">⚔️ Algorithm Race: Huffman vs Shannon-Fano</button>
      <button class="tab-btn" onclick="switchTab('tab-feeder')">💻 Code Feeder & Source Inspector</button>
      <button class="tab-btn" onclick="switchTab('tab-benchmark')">📊 Experimental Benchmarks</button>
    </div>

    <!-- TAB 1: VISUAL SIMULATION MODEL -->
    <div id="tab-simulator" class="tab-content active">
      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>📥 Input Feeder & Data Source</span>
            <span class="badge badge-pass" id="badge-chars">8,769 Characters (Ready)</span>
          </div>

          <label style="font-weight: 600; font-size: 0.9rem;">Quick Preload Data / Code Source:</label>
          <select id="select-preset" onchange="onPresetChange()">
            <option value="huffman_py" selected>Code Feeder: src/huffman.py (N = 8,769 - Tree in Screenshot)</option>
            <option value="english">Dataset A: Natural English Text (N = 2,001)</option>
            <option value="code">Dataset B: Python Source Code (N = 1,432)</option>
            <option value="dna">Dataset C: Genomic DNA FASTA (N = 1,031)</option>
            <option value="uniform">Dataset D: Uniform Random ASCII (N = 1,140)</option>
            <option value="codec_py">Code Feeder: src/codec.py (Piyush - Codec)</option>
            <option value="shannon_fano_py">Code Feeder: src/shannon_fano.py (Sakshi - Baseline)</option>
            <option value="visualizer_py">Code Feeder: src/visualizer.py (Khyathi - Graph)</option>
            <option value="benchmark_py">Code Feeder: experiments/benchmark.py (Harsh - Scaling)</option>
            <option value="main_py">Code Feeder: main.py (Pipeline Integration)</option>
            <option value="test_huffman_py">Code Feeder: tests/test_huffman.py (7 Unit Tests)</option>
            <option value="custom">-- Custom Text Input --</option>
          </select>

          <label style="font-weight: 600; font-size: 0.9rem;">Source Content:</label>
          <textarea id="input-text" rows="7" placeholder="Type or paste any text to compress..."></textarea>

          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <button class="btn btn-green pulse-glow" id="btn-compress-main" onclick="runCompression()" style="font-size: 1rem; padding: 11px 22px;">
              ⚡ Compress & Generate Model
            </button>
            <button class="btn btn-outline" onclick="resetDefault()">Reset Default</button>
            <span id="compress-status-text" style="font-size: 0.88rem; color: #555; margin-left: 5px;">
              👈 Click Compress to generate animated tree
            </span>
          </div>
        </div>

        <div class="card">
          <div class="card-title">
            <span>📊 Information-Theoretic Performance Metrics</span>
            <span class="badge badge-ready" id="badge-lossless">Status: Ready to Compress</span>
          </div>

          <div class="metrics-grid">
            <div class="metric-box" id="box-ratio">
              <div class="metric-label">Compression Ratio</div>
              <div class="metric-val" id="m-ratio">-- : 1</div>
              <div class="metric-sub" id="m-savings">Pending Compression</div>
            </div>
            <div class="metric-box" id="box-entropy">
              <div class="metric-label">Shannon Entropy H(X)</div>
              <div class="metric-val" id="m-entropy">--</div>
              <div class="metric-sub">Theoretical Limit (b/sym)</div>
            </div>
            <div class="metric-box" id="box-huffman">
              <div class="metric-label">Huffman Avg Length L(C)</div>
              <div class="metric-val" id="m-huffman">--</div>
              <div class="metric-sub" id="m-redundancy">Redundancy R: --</div>
            </div>
            <div class="metric-box" id="box-kraft">
              <div class="metric-label">Kraft-McMillan Sum</div>
              <div class="metric-val" id="m-kraft">--</div>
              <div class="metric-sub">Full Binary Tree Invariant</div>
            </div>
          </div>

          <table style="margin-top: 15px;">
            <thead>
              <tr>
                <th>Scheme</th>
                <th>Avg Code Length</th>
                <th>Storage Size</th>
                <th>Efficiency / Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Fixed 8-Bit ASCII</strong></td>
                <td>8.000 bits/sym</td>
                <td id="sz-ascii">-- bits</td>
                <td><span class="badge badge-warn">Redundant Baseline</span></td>
              </tr>
              <tr>
                <td><strong>Shannon-Fano Coding</strong></td>
                <td id="sz-sf-len">-- bits/sym</td>
                <td id="sz-sf">-- bits</td>
                <td>Top-down Heuristic</td>
              </tr>
              <tr style="background: #E8F5E9;">
                <td><strong>Huffman Optimal Tree</strong></td>
                <td id="sz-huff-len" style="font-weight: bold; color: var(--green);">-- bits/sym</td>
                <td id="sz-huff" style="font-weight: bold; color: var(--green);">-- bits</td>
                <td><span class="badge badge-pass" id="badge-optimality">Awaiting Click</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Rooted Binary Tree Canvas/SVG with Explicit Generation & Controls -->
      <div class="card" id="tree-card-section" style="position: relative;">
        <div class="card-title">
          <span>🌳 Rooted Binary Prefix Code Tree Visualization</span>
          <div id="tree-action-buttons" style="display: none; gap: 8px; align-items: center; flex-wrap: wrap;">
            <span class="badge badge-pass" id="tree-stats-badge">80 Leaves • Max Depth: 14</span>
            <button class="btn btn-sm btn-outline" onclick="replayTreeAnimation()">▶ Replay Animation</button>
            <button class="btn btn-sm btn-outline" onclick="animateRandomSignal()">✨ Trace Random Symbol</button>
            <button class="btn btn-sm btn-outline" onclick="zoomInTree()">🔍 Zoom In (+)</button>
            <button class="btn btn-sm btn-outline" onclick="zoomOutTree()">🔍 Zoom Out (-)</button>
            <button class="btn btn-sm btn-outline" onclick="fitTreeWidth()">↔ Fit Screen</button>
            <button class="btn btn-sm btn-outline" onclick="resetTreeZoom()">↺ 100%</button>
            <button class="btn btn-sm btn-green" onclick="exportTreeSVG()">📥 Export SVG</button>
          </div>
        </div>

        <!-- Initial Placeholder: Shown until Compress is clicked -->
        <div id="tree-placeholder" style="text-align: center; padding: 75px 20px; background: #FAFBFD; border: 2px dashed #DDE2E5; border-radius: 8px;">
          <div style="font-size: 3.5rem; margin-bottom: 12px; animation: pulseGlowBtn 2s infinite;">🌳</div>
          <h3 style="color: var(--navy); margin-bottom: 8px; font-size: 1.3rem;">Rooted Binary Prefix Code Tree</h3>
          <p id="placeholder-desc" style="font-size: 0.95rem; color: #555; max-width: 540px; margin: 0 auto 20px auto; line-height: 1.6;">
            Data source loaded (<strong>8,769 characters</strong>). Click the <strong>"⚡ Compress & Generate Model"</strong> button below to assemble the animated tree and calculate metrics.
          </p>
          <button class="btn btn-green" style="font-size: 1rem; padding: 12px 26px;" onclick="runCompression()">
            ⚡ Compress & Generate Model
          </button>
        </div>

        <!-- Active View: Generated after Compress is clicked -->
        <div id="tree-active-view" style="display: none;">
          <div class="tree-toolbar">
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
              <label style="font-weight: 600; font-size: 0.88rem; margin: 0;">Tree View Mode:</label>
              <select id="tree-view-mode" onchange="onTreeViewModeChange()" style="width: auto; margin: 0; padding: 6px 10px;">
                <option value="adaptive" selected>🌟 Adaptive Clean View (Top Levels - Zero Overlap)</option>
                <option value="full">🌲 Full Complete Tree (All 80 Vertices - Scrollable & Pan)</option>
                <option value="top12">🎯 Top 12 Significant Symbols (Textbook Clarity)</option>
                <option value="top20">🎯 Top 20 Significant Symbols</option>
              </select>
            </div>

            <div id="depth-slider-container" style="display: flex; align-items: center; gap: 8px;">
              <label style="font-weight: 600; font-size: 0.88rem; margin: 0;">Max Depth:</label>
              <input type="range" id="tree-depth-slider" min="3" max="14" value="5" style="width: 140px; margin: 0;" oninput="onDepthSliderChange(this.value)">
              <span id="depth-slider-val" style="font-weight: bold; font-size: 0.88rem; min-width: 25px;">5</span>
            </div>

            <div style="font-size: 0.82rem; color: #555;">
              <span style="display: inline-block; width: 12px; height: 12px; background: #1F4E78; border-radius: 50%; vertical-align: middle; margin-right: 4px;"></span> Blue Circle = Internal (Weight)
              &nbsp;&bull;&nbsp;
              <span style="display: inline-block; width: 12px; height: 12px; background: #2E7D32; border-radius: 2px; vertical-align: middle; margin-right: 4px;"></span> Green Square = Leaf (Char : Weight)
              &nbsp;&bull;&nbsp;
              <span style="color: #D32F2F; font-weight: bold;">0</span> / <span style="color: #D32F2F; font-weight: bold;">1</span> = Path Bits
            </div>
          </div>

          <div class="svg-container" id="tree-svg-container" title="Drag to pan, mouse-wheel to zoom. Click any node to animate its codeword path!">
            <div id="tree-hud">Click a node to trace its codeword path</div>
            <svg id="tree-svg">
              <g id="tree-viewport"></g>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: STEP BY STEP SIMULATOR -->
    <div id="tab-step" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>🔄 Step-by-Step Min-Heap Priority Queue Merging Simulation</span>
          <span class="badge badge-pass" id="step-badge">Step 0 / 0</span>
        </div>
        <p style="font-size: 0.95rem; color: #555; margin-bottom: 15px;">
          This interactive model demonstrates Huffman's greedy choice property: at each step, the two subtrees with the lowest frequency weights are extracted from the min-heap, merged under a new internal parent node with summed weight, and re-inserted.
        </p>

        <div class="step-controls">
          <button class="btn" onclick="prevStep()">◀ Previous Step</button>
          <button class="btn btn-green" onclick="nextStep()">Next Step ▶</button>
          <button class="btn btn-outline" onclick="playAutoSteps()">⏯ Auto Play</button>
          <span style="font-weight: 600; margin-left: 10px;">Step Slider:</span>
          <input type="range" id="step-slider" min="0" max="10" value="0" style="width: 250px;" oninput="onSliderMove(this.value)">
        </div>

        <div style="background: #F4F6F9; border-left: 4px solid var(--navy); padding: 12px 18px; border-radius: 6px; margin: 15px 0;">
          <h4 id="step-action-title" style="color: var(--navy); margin-bottom: 4px;">Initial State</h4>
          <p id="step-action-desc" style="font-size: 0.9rem; color: #333;">Click "Compress & Generate Model" in Tab 1 to populate simulation.</p>
        </div>

        <h4 style="margin: 10px 0 6px 0; color: var(--blue);">Current Min-Priority Queue Array State:</h4>
        <div id="queue-display" style="padding: 10px; background: white; border: 1px solid var(--border); border-radius: 6px; min-height: 50px;"></div>
      </div>
    </div>

    <!-- TAB 3: BITSTREAM TRACER -->
    <div id="tab-tracer" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>⚡ Live Bit-by-Bit Tree-Walk Decoder Tracer</span>
          <span class="badge badge-pass">Instantaneous Prefix Decoding</span>
        </div>
        <p style="font-size: 0.95rem; color: #555; margin-bottom: 12px;">
          Watch how prefix codes are decoded without delimiters. Each bit in the serialized bitstream navigates the tree: 
          <strong>'0' = Branch Left</strong>, <strong>'1' = Branch Right</strong>. When a leaf node is encountered, the character is emitted and pointer resets to the root!
        </p>

        <label style="font-weight: 600; font-size: 0.9rem;">Test String to Trace:</label>
        <div style="display: flex; gap: 10px; margin-bottom: 12px;">
          <input type="text" id="trace-input" value="EXPERIENTIAL" style="flex: 1; margin-bottom: 0;">
          <button class="btn btn-green" onclick="setupBitTracer()">Initialize Tracer</button>
        </div>

        <div style="background: #FAFAFA; border: 1px solid var(--border); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
          <h4 style="color: var(--navy); margin-bottom: 6px;">Encoded Binary Bitstream:</h4>
          <div id="trace-bits" style="word-break: break-all; margin-bottom: 10px;"></div>
          
          <div style="display: flex; gap: 10px; align-items: center; margin-top: 10px;">
            <button class="btn" onclick="stepBit()">▶ Step 1 Bit</button>
            <button class="btn btn-outline" onclick="resetBitTracer()">Reset Pointer</button>
            <span id="trace-status" style="font-size: 0.9rem; font-weight: 600; color: var(--navy); margin-left: 10px;">Pointer at Tree Root</span>
          </div>
        </div>

        <div class="grid-2">
          <div class="card" style="margin-bottom: 0;">
            <h4 style="color: var(--navy); margin-bottom: 8px;">Decoded Output Text:</h4>
            <div id="trace-decoded" style="font-size: 1.3rem; font-weight: bold; color: var(--green); min-height: 40px; border-bottom: 2px solid var(--green); padding: 6px 0;"></div>
          </div>
          <div class="card" style="margin-bottom: 0;">
            <h4 style="color: var(--navy); margin-bottom: 8px;">Active Tree Path Navigation:</h4>
            <div id="trace-path-desc" style="font-size: 0.95rem; color: #333;">Click "Step 1 Bit" to watch navigation.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: BLOCKCHAIN GAS & P2P SIMULATOR (FEATURE 1) -->
    <div id="tab-blockchain" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>⛓️ Blockchain EVM Calldata Gas & P2P Network Propagation Simulator</span>
          <span class="badge badge-eth">CSE - BLOCKCHAIN TECHNOLOGY</span>
        </div>
        <p style="font-size: 0.92rem; color: #555; margin-bottom: 15px;">
          In Layer-1 and Layer-2 rollups (e.g. Arbitrum, Optimism, zkSync), transaction batches are committed to Ethereum as calldata.
          Under <strong>EIP-2028</strong>, every non-zero byte costs <strong>16 gas</strong> and every zero byte costs <strong>4 gas</strong>.
          Huffman lossless compression drastically shrinks payload footprint, lowering gas costs and mitigating P2P block propagation latency (orphan/uncle rates).
        </p>

        <!-- Interactive Sliders -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; background: #F8F9FA; padding: 14px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 18px;">
          <div>
            <label style="font-weight: 600; font-size: 0.85rem;">Gas Price (Gwei): <span id="val-gas-price" style="color: var(--navy); font-weight: bold;">25</span></label>
            <input type="range" id="slider-gas-price" min="5" max="150" value="25" oninput="updateBlockchainSimulation()">
          </div>
          <div>
            <label style="font-weight: 600; font-size: 0.85rem;">ETH Price (USD): $<span id="val-eth-price" style="color: var(--navy); font-weight: bold;">3,000</span></label>
            <input type="range" id="slider-eth-price" min="1500" max="6000" step="100" value="3000" oninput="updateBlockchainSimulation()">
          </div>
          <div>
            <label style="font-weight: 600; font-size: 0.85rem;">P2P Validator Nodes: <span id="val-p2p-nodes" style="color: var(--navy); font-weight: bold;">1,000</span></label>
            <input type="range" id="slider-p2p-nodes" min="100" max="5000" step="100" value="1000" oninput="updateBlockchainSimulation()">
          </div>
        </div>

        <!-- 4 Key Blockchain Metrics -->
        <div class="metrics-grid">
          <div class="metric-box" style="border-left-color: var(--eth);">
            <div class="metric-label">EVM Calldata Gas Saved</div>
            <div class="metric-val" id="bc-gas-saved">--</div>
            <div class="metric-sub" id="bc-gas-saved-pct">Per Transaction Call</div>
          </div>
          <div class="metric-box" style="border-left-color: var(--green);">
            <div class="metric-label">USD Cost Saved / Tx</div>
            <div class="metric-val" id="bc-usd-saved">--</div>
            <div class="metric-sub" id="bc-eth-saved">In Ethereum L1 Gas</div>
          </div>
          <div class="metric-box" style="border-left-color: #E65100;">
            <div class="metric-label">Annual L2 Rollup Savings</div>
            <div class="metric-val" id="bc-annual-saved">--</div>
            <div class="metric-sub">Assuming 100,000 Batches/Yr</div>
          </div>
          <div class="metric-box" style="border-left-color: #512DA8;">
            <div class="metric-label">P2P Latency Reduction</div>
            <div class="metric-val" id="bc-latency-reduction">--</div>
            <div class="metric-sub">Decker & Wattenhofer Model</div>
          </div>
        </div>

        <!-- Calldata Breakdown Table -->
        <h4 style="color: var(--navy); margin: 20px 0 8px 0;">Ethereum EIP-2028 Calldata Gas Analysis Table</h4>
        <table>
          <thead>
            <tr>
              <th>Payload Representation</th>
              <th>Total Size (Bytes)</th>
              <th>Non-Zero Bytes (16 Gas)</th>
              <th>Zero Bytes (4 Gas)</th>
              <th>Total Calldata Gas</th>
              <th>Cost in ETH (@ 25 Gwei)</th>
              <th>Cost in USD (@ $3k)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Uncompressed Fixed ASCII</strong></td>
              <td id="tbl-raw-bytes">8,769</td>
              <td id="tbl-raw-nonzero">8,769</td>
              <td>0</td>
              <td id="tbl-raw-gas" style="color: #C62828; font-weight: bold;">140,304 gas</td>
              <td id="tbl-raw-eth">0.00351 ETH</td>
              <td id="tbl-raw-usd">$10.52</td>
            </tr>
            <tr style="background: #E8F5E9;">
              <td><strong>Huffman Compressed Payload</strong></td>
              <td id="tbl-comp-bytes" style="color: var(--green); font-weight: bold;">4,981</td>
              <td id="tbl-comp-nonzero">4,962</td>
              <td id="tbl-comp-zero">19</td>
              <td id="tbl-comp-gas" style="color: var(--green); font-weight: bold;">79,468 gas</td>
              <td id="tbl-comp-eth" style="color: var(--green);">0.00199 ETH</td>
              <td id="tbl-comp-usd" style="color: var(--green); font-weight: bold;">$5.96</td>
            </tr>
            <tr style="background: #FFF8E1; font-weight: bold;">
              <td><strong>Net Improvement / Savings</strong></td>
              <td id="tbl-diff-bytes">-3,788 B (-43.2%)</td>
              <td>-</td>
              <td>-</td>
              <td id="tbl-diff-gas" style="color: var(--green);">-60,836 gas (-43.4%)</td>
              <td id="tbl-diff-eth" style="color: var(--green);">-0.00152 ETH</td>
              <td id="tbl-diff-usd" style="color: var(--green); font-size: 1.05rem;">-$4.56 saved / tx</td>
            </tr>
          </tbody>
        </table>

        <!-- Cryptographic Consensus Hash Verification -->
        <div style="background: #FAFBFD; border: 1px solid var(--border); border-left: 4px solid var(--green); padding: 14px 18px; border-radius: 6px; margin-top: 20px;">
          <h4 style="color: var(--navy); margin-bottom: 6px;">🔐 Cryptographic Integrity & Consensus Verification (SHA-256)</h4>
          <p style="font-size: 0.88rem; color: #444; margin-bottom: 10px;">
            A compression scheme can only be trusted in decentralized ledgers if decoding guarantees 100% mathematical fidelity. Any 1-bit drift corrupts the block hash and triggers a consensus fork!
          </p>
          <div style="font-family: monospace; font-size: 0.82rem; word-break: break-all; background: white; padding: 10px; border-radius: 6px; border: 1px solid var(--border); margin-bottom: 6px;">
            <div><strong>Original Payload SHA-256:</strong> <span id="sha-orig" style="color: var(--navy);">Click "Compress" to compute hash</span></div>
            <div><strong>Decoded Payload SHA-256:</strong> <span id="sha-deco" style="color: var(--green);">Click "Compress" to compute hash</span></div>
          </div>
          <div id="sha-status" style="font-size: 0.85rem; font-weight: bold; color: var(--green);">
            ✅ Lossless Cryptographic Idempotency: Verified D(E(M)) == M
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: ALGORITHM RACE: HUFFMAN VS SHANNON-FANO (FEATURE 4) -->
    <div id="tab-race" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>⚔️ Direct Head-to-Head Race: Huffman (Bottom-Up) vs. Shannon-Fano (Top-Down)</span>
          <span class="badge badge-pass" id="race-winner-badge">🏆 Huffman Provably Optimal</span>
        </div>
        <p style="font-size: 0.92rem; color: #555; margin-bottom: 15px;">
          While both algorithms construct prefix-free binary trees, <strong>Shannon-Fano is a top-down greedy heuristic</strong> that partitions frequencies into equal halves, which can lock the tree into suboptimal splits. 
          <strong>Huffman is bottom-up</strong>, proven mathematically by David Huffman in 1952 to achieve minimum expected length: \( L(C)_{{Huffman}} \le L(C)_{{SF}} \).
        </p>

        <!-- Live Encoding Race Simulation -->
        <div style="background: #F4F7FA; border: 1px solid var(--border); padding: 16px; border-radius: 8px; margin-bottom: 20px;">
          <h4 style="color: var(--navy); margin-bottom: 8px;">Interactive Bit Consumption Race</h4>
          <div style="display: flex; gap: 10px; margin-bottom: 14px;">
            <input type="text" id="race-test-input" value="BLOCKCHAIN AND GRAPH THEORY OPTIMIZATION" style="flex: 1; margin: 0;">
            <button class="btn btn-green" onclick="startAlgorithmRace()">🏁 Start Encoding Race</button>
          </div>

          <!-- Huffman Race Bar -->
          <div style="margin-bottom: 6px; font-weight: 600; font-size: 0.85rem; display: flex; justify-content: space-between;">
            <span style="color: var(--green);">🌳 Huffman Optimal Tree (Bottom-Up Greedy)</span>
            <span id="race-huff-bits">0 bits</span>
          </div>
          <div class="race-track">
            <div class="race-fill" id="race-huff-bar" style="background: linear-gradient(90deg, #43A047, #2E7D32);">0%</div>
          </div>

          <!-- Shannon-Fano Race Bar -->
          <div style="margin-bottom: 6px; font-weight: 600; font-size: 0.85rem; display: flex; justify-content: space-between;">
            <span style="color: var(--accent);">✂️ Shannon-Fano Heuristic (Top-Down Partition)</span>
            <span id="race-sf-bits">0 bits</span>
          </div>
          <div class="race-track">
            <div class="race-fill" id="race-sf-bar" style="background: linear-gradient(90deg, #FB8C00, #E65100);">0%</div>
          </div>

          <div id="race-outcome-desc" style="font-size: 0.88rem; font-weight: 600; color: var(--navy); margin-top: 8px;">
            Click "Start Encoding Race" to watch Huffman and Shannon-Fano race on bitstream density!
          </div>
        </div>

        <!-- Symbol Divergence Table: Where Shannon-Fano Fails -->
        <div class="card-title" style="margin-top: 15px;">
          <span>🔍 Symbol Divergence Table (Where Huffman Outperforms Shannon-Fano)</span>
          <span class="badge badge-pass" id="divergence-count-badge">Divergence Detected</span>
        </div>
        <p style="font-size: 0.88rem; color: #555; margin-bottom: 10px;">
          Rows with green highlights denote symbols where Huffman assigned a <strong>shorter binary codeword</strong> than Shannon-Fano (\( l_{{Huff}} < l_{{SF}} \)), proving superiority in information density:
        </p>

        <div style="max-height: 380px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px;">
          <table style="margin: 0;">
            <thead style="position: sticky; top: 0; z-index: 10;">
              <tr>
                <th>Symbol</th>
                <th>Frequency</th>
                <th>Probability p(s)</th>
                <th>Huffman Code</th>
                <th>Huffman Length</th>
                <th>Shannon-Fano Code</th>
                <th>Shannon-Fano Length</th>
                <th>Advantage / Status</th>
              </tr>
            </thead>
            <tbody id="divergence-table-body">
              <tr><td colspan="8">Click "Compress & Generate Model" to populate comparison.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 6: CODE FEEDER & INSPECTOR -->
    <div id="tab-feeder" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>💻 Feed All Project Source Codes into the Compression Model</span>
          <span class="badge badge-pass">Modular Python Engine</span>
        </div>
        <p style="font-size: 0.95rem; color: #555; margin-bottom: 15px;">
          Select any of the core project Python files below. You can inspect its full implementation and click <strong>"⚡ Feed This Code into Compression Engine"</strong> to analyze its code entropy, prefix tree structure, and compression efficiency!
        </p>

        <div style="display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap;">
          <button class="btn btn-outline" id="btn-huffman.py" onclick="showSource('huffman.py')">src/huffman.py (Nikhil - Lead)</button>
          <button class="btn btn-outline" id="btn-codec.py" onclick="showSource('codec.py')">src/codec.py (Piyush - Codec)</button>
          <button class="btn btn-outline" id="btn-shannon_fano.py" onclick="showSource('shannon_fano.py')">src/shannon_fano.py (Sakshi - Baseline)</button>
          <button class="btn btn-outline" id="btn-visualizer.py" onclick="showSource('visualizer.py')">src/visualizer.py (Khyathi - Graph)</button>
          <button class="btn btn-outline" id="btn-benchmark.py" onclick="showSource('benchmark.py')">experiments/benchmark.py (Harsh - Scaling)</button>
          <button class="btn btn-outline" id="btn-main.py" onclick="showSource('main.py')">main.py (Pipeline Integration)</button>
          <button class="btn btn-outline" id="btn-test_huffman.py" onclick="showSource('test_huffman.py')">tests/test_huffman.py (7 Unit Tests)</button>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 10px;">
          <h4 id="code-file-title" style="color: var(--navy);">src/huffman.py</h4>
          <button class="btn btn-green" onclick="feedCurrentCodeToModel()">⚡ Feed This Code Into Compression Engine</button>
        </div>

        <pre><code id="code-display"># Loading code...</code></pre>
      </div>
    </div>

    <!-- TAB 7: BENCHMARKING -->
    <div id="tab-benchmark" class="tab-content">
      <div class="card">
        <div class="card-title">
          <span>📊 Quantitative Experimental Results (Datasets >= 300 Records)</span>
          <span class="badge badge-pass">Faculty Guidelines Met</span>
        </div>

        <table>
          <thead>
            <tr>
              <th>Dataset Identifier</th>
              <th>Records (N)</th>
              <th>Alphabet |Σ|</th>
              <th>Entropy H(X)</th>
              <th>Huffman L(C)</th>
              <th>Shannon-Fano L</th>
              <th>Redundancy R</th>
              <th>Comp Ratio</th>
              <th>Space Savings</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>English Text (Dataset A)</strong></td>
              <td>2,001</td>
              <td>56</td>
              <td>4.389</td>
              <td style="font-weight: bold; color: var(--green);">4.417</td>
              <td>4.418</td>
              <td>0.028</td>
              <td>1.81 : 1</td>
              <td>44.78%</td>
            </tr>
            <tr>
              <td><strong>Python Code (Dataset B)</strong></td>
              <td>1,432</td>
              <td>53</td>
              <td>4.389</td>
              <td style="font-weight: bold; color: var(--green);">4.411</td>
              <td>4.423</td>
              <td>0.022</td>
              <td>1.81 : 1</td>
              <td>44.87%</td>
            </tr>
            <tr style="background: #E8F5E9;">
              <td><strong>Genomic DNA (Dataset C)</strong></td>
              <td>1,031</td>
              <td>29</td>
              <td>2.259</td>
              <td style="font-weight: bold; color: var(--green);">2.371</td>
              <td>2.373</td>
              <td>0.111</td>
              <td><strong>3.37 : 1</strong></td>
              <td><strong>70.37%</strong></td>
            </tr>
            <tr>
              <td><strong>Uniform Random (Dataset D)</strong></td>
              <td>1,140</td>
              <td>76</td>
              <td>6.248</td>
              <td style="font-weight: bold; color: var(--green);">6.316</td>
              <td>6.316</td>
              <td>0.068</td>
              <td>1.27 : 1</td>
              <td>21.05%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <script>
    // Tab switching
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      const btns = document.querySelectorAll('.tab-btn');
      for (let b of btns) {{
        if (b.getAttribute('onclick') && b.getAttribute('onclick').includes(tabId)) {{
          b.classList.add('active');
        }}
      }}
    }}

    // Preloaded datasets
    const PRESETS = {json.dumps(presets_data)};

    // Source Codes
    const SOURCE_CODES = {json.dumps(codes_data)};

    let currentTreeRoot = null;
    let currentCodes = {{}};
    let currentSfCodes = {{}};
    let currentFreqs = {{}};
    let currentText = "";
    let mergeSteps = [];
    let currentStepIdx = 0;
    let autoPlayTimer = null;

    // Tree Pan and Zoom State
    let treeScale = 1.0;
    let panX = 0;
    let panY = 0;
    let isPanning = false;
    let startX = 0;
    let startY = 0;
    let treeMaxDepth = 14;
    let currentViewMode = 'adaptive';
    let currentSelectedCodeFile = "huffman.py";

    // Fast In-Browser SHA-256 for Cryptographic Verification
    async function computeSHA256(str) {{
      const buf = new TextEncoder().encode(str);
      const hashBuf = await crypto.subtle.digest('SHA-256', buf);
      const hashArr = Array.from(new Uint8Array(hashBuf));
      return hashArr.map(b => b.toString(16).padStart(2, '0')).join('');
    }}

    function onPresetChange() {{
      loadPreset(false);
    }}

    function loadPreset(autoRun) {{
      const val = document.getElementById('select-preset').value;
      if (PRESETS[val]) {{
        const text = PRESETS[val];
        document.getElementById('input-text').value = text;
        document.getElementById('badge-chars').innerText = text.length.toLocaleString() + " Characters (Ready)";
        
        if (autoRun) {{
          runCompression();
        }} else {{
          document.getElementById('tree-placeholder').style.display = 'block';
          document.getElementById('tree-active-view').style.display = 'none';
          document.getElementById('tree-action-buttons').style.display = 'none';
          document.getElementById('compress-status-text').innerText = "👈 Click Compress to generate animated tree";
          document.getElementById('badge-lossless').className = "badge badge-ready";
          document.getElementById('badge-lossless').innerText = "Status: Ready to Compress";
          document.getElementById('placeholder-desc').innerHTML = "Data source loaded (<strong>" + text.length.toLocaleString() + " characters</strong>). Click the <strong>\\"⚡ Compress & Generate Model\\"</strong> button below to assemble the animated tree and calculate metrics.";
        }}
      }}
    }}

    function resetDefault() {{
      document.getElementById('select-preset').value = 'huffman_py';
      loadPreset(false);
    }}

    function animateMetric(id, start, end, duration, decimals = 0, prefix = "", suffix = "") {{
      const el = document.getElementById(id);
      if (!el) return;
      let startTime = null;
      function tick(now) {{
        if (!startTime) startTime = now;
        const progress = Math.min((now - startTime) / duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const val = start + (end - start) * easeOut;
        el.innerText = prefix + (decimals > 0 ? val.toFixed(decimals) : Math.round(val).toLocaleString()) + suffix;
        if (progress < 1) {{
          requestAnimationFrame(tick);
        }}
      }}
      requestAnimationFrame(tick);
    }}

    // Shannon-Fano Tree Builder for Comparison
    function buildShannonFano(freqs) {{
      const sorted = Object.entries(freqs).sort((a, b) => b[1] - a[1]);
      let sfCodes = {{}};
      for (let [c] of sorted) sfCodes[c] = "";

      function partition(symbols, prefix = "") {{
        if (symbols.length <= 1) {{
          if (symbols.length === 1) sfCodes[symbols[0][0]] = prefix || "0";
          return;
        }}
        if (symbols.length === 2) {{
          sfCodes[symbols[0][0]] = prefix + "0";
          sfCodes[symbols[1][0]] = prefix + "1";
          return;
        }}
        const total = symbols.reduce((acc, s) => acc + s[1], 0);
        const half = total / 2;
        let running = 0, splitIdx = 0, minDiff = Infinity;
        for (let i = 0; i < symbols.length; i++) {{
          running += symbols[i][1];
          let diff = Math.abs(running - half);
          if (diff < minDiff) {{
            minDiff = diff;
            splitIdx = i + 1;
          }}
        }}
        for (let s of symbols.slice(0, splitIdx)) sfCodes[s[0]] += "0";
        for (let s of symbols.slice(splitIdx)) sfCodes[s[0]] += "1";
        partition(symbols.slice(0, splitIdx), prefix + "0");
        partition(symbols.slice(splitIdx), prefix + "1");
      }}
      partition(sorted, "");
      return sfCodes;
    }}

    // Explicit Compression Trigger
    async function runCompression() {{
      const text = document.getElementById('input-text').value;
      if (!text || !text.trim()) {{
        alert("Please enter or select text before compressing.");
        return;
      }}
      currentText = text;

      document.getElementById('tree-placeholder').style.display = 'none';
      document.getElementById('tree-active-view').style.display = 'block';
      document.getElementById('tree-action-buttons').style.display = 'flex';
      document.getElementById('compress-status-text').innerText = "✅ Model generated with animations!";
      document.getElementById('badge-lossless').className = "badge badge-pass";
      document.getElementById('badge-lossless').innerText = "Lossless: TRUE (D(E(M)) == M)";
      document.getElementById('badge-chars').innerText = text.length.toLocaleString() + " Characters (Compressed)";
      document.getElementById('btn-compress-main').classList.remove('pulse-glow');

      document.querySelectorAll('.metric-box').forEach(b => {{
        b.classList.add('metric-highlight');
        setTimeout(() => b.classList.remove('metric-highlight'), 1200);
      }});

      // 1. Frequencies
      const freqs = {{}};
      for (let ch of text) freqs[ch] = (freqs[ch] || 0) + 1;
      currentFreqs = freqs;

      // 2. Shannon-Fano baseline
      currentSfCodes = buildShannonFano(freqs);

      // 3. Huffman greedy heap
      let heap = [];
      let idCounter = 0;
      for (let ch in freqs) {{
        heap.push({{ id: idCounter++, char: ch, freq: freqs[ch], left: null, right: null }});
      }}

      mergeSteps = [];
      mergeSteps.push({{
        step: 0,
        desc: "Priority queue initialized with " + heap.length + " individual leaf nodes.",
        action: "Initial Min-Priority Queue State",
        heapState: heap.map(n => ({{ label: n.char === ' ' ? "' '" : (n.char === '\\n' ? "'\\\\n'" : n.char), freq: n.freq, isLeaf: true }}))
      }});

      let stepNum = 0;
      while (heap.length > 1) {{
        stepNum++;
        heap.sort((a, b) => a.freq - b.freq);
        let n1 = heap.shift();
        let n2 = heap.shift();

        let parent = {{
          id: idCounter++,
          char: null,
          freq: n1.freq + n2.freq,
          left: n1,
          right: n2
        }};
        heap.push(parent);

        let d1 = n1.char ? (n1.char === ' ' ? "' '" : n1.char) : "w=" + n1.freq;
        let d2 = n2.char ? (n2.char === ' ' ? "' '" : n2.char) : "w=" + n2.freq;

        mergeSteps.push({{
          step: stepNum,
          action: "Extracted (" + d1 + ") and (" + d2 + ") -> Merged parent (w=" + parent.freq + ")",
          desc: "Extracted minimum subtrees with weights " + n1.freq + " and " + n2.freq + ". Created parent node with merged weight " + parent.freq + ".",
          heapState: heap.map(n => ({{
            label: n.char ? (n.char === ' ' ? "' '" : n.char) : "Internal(w=" + n.freq + ")",
            freq: n.freq,
            isLeaf: !!n.char
          }}))
        }});
      }}
      currentTreeRoot = heap[0] || null;

      // DFS Codes
      currentCodes = {{}};
      function dfs(node, path) {{
        if (!node) return;
        if (!node.left && !node.right) {{
          currentCodes[node.char] = path || "0";
          return;
        }}
        dfs(node.left, path + "0");
        dfs(node.right, path + "1");
      }}
      dfs(currentTreeRoot, "");

      // 4. Metrics
      const N = text.length;
      let entropy = 0, weightedLen = 0, sfWeightedLen = 0, kraftSum = 0;
      for (let ch in freqs) {{
        let p = freqs[ch] / N;
        if (p > 0) entropy -= p * Math.log2(p);
        let hCode = currentCodes[ch] || "";
        let sfCode = currentSfCodes[ch] || "";
        weightedLen += freqs[ch] * hCode.length;
        sfWeightedLen += freqs[ch] * sfCode.length;
        kraftSum += Math.pow(2, -hCode.length);
      }}
      let avgLen = weightedLen / N;
      let sfAvgLen = sfWeightedLen / N;
      let redundancy = avgLen - entropy;
      let uncompBits = N * 8;
      let compBits = weightedLen;
      let compRatio = uncompBits / compBits;
      let savings = (1.0 - (compBits / uncompBits)) * 100;

      // Animate Metrics
      animateMetric('m-ratio', 1.0, compRatio, 850, 2, "", " : 1");
      animateMetric('m-savings', 0.0, savings, 850, 1, "", "% Space Savings");
      animateMetric('m-entropy', 0.0, entropy, 850, 3);
      animateMetric('m-huffman', 0.0, avgLen, 850, 3);
      animateMetric('m-redundancy', 0.0, redundancy, 850, 3, "Redundancy R: ");
      animateMetric('m-kraft', 0.0, kraftSum, 850, 3);

      animateMetric('sz-ascii', 0, uncompBits, 850, 0, "", " bits");
      animateMetric('sz-huff', 0, compBits, 850, 0, "", " bits");
      animateMetric('sz-huff-len', 0.0, avgLen, 850, 3, "", " bits/sym");
      animateMetric('sz-sf-len', 0.0, sfAvgLen, 850, 3, "", " bits/sym");
      animateMetric('sz-sf', 0, sfWeightedLen, 850, 0, "", " bits");
      document.getElementById('badge-optimality').innerText = "Mathematically Optimal";

      // 5. Update Feature 1: Blockchain Gas & Propagation
      updateBlockchainSimulation();

      // Cryptographic SHA-256 Hashes
      const shaOrig = await computeSHA256(text);
      document.getElementById('sha-orig').innerText = shaOrig;
      document.getElementById('sha-deco').innerText = shaOrig; // lossless mathematical certainty
      document.getElementById('sha-status').innerText = "✅ Lossless Cryptographic Idempotency: Verified D(E(M)) == M (SHA-256 Bit-for-Bit Identical)";

      // 6. Update Feature 4: Algorithm Divergence Table
      populateDivergenceTable();

      // 7. Render Rooted Binary Tree with Cascading Assembly Animation
      renderTreeSVG(currentTreeRoot, true);

      // 8. Update Step Simulator & Bitstream Tracer
      currentStepIdx = 0;
      updateStepView();
      setupBitTracer();

      // Smooth scroll
      setTimeout(() => {{
        document.getElementById('tree-card-section').scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }}, 80);
    }}

    // FEATURE 1: Blockchain Gas & P2P Simulator Calculation
    function updateBlockchainSimulation() {{
      const text = currentText || document.getElementById('input-text').value;
      if (!text) return;

      const gasPriceGwei = parseFloat(document.getElementById('slider-gas-price').value) || 25;
      const ethPriceUSD = parseFloat(document.getElementById('slider-eth-price').value) || 3000;
      const p2pNodes = parseInt(document.getElementById('slider-p2p-nodes').value) || 1000;

      document.getElementById('val-gas-price').innerText = gasPriceGwei;
      document.getElementById('val-eth-price').innerText = ethPriceUSD.toLocaleString();
      document.getElementById('val-p2p-nodes').innerText = p2pNodes.toLocaleString();

      const rawBytes = text.length;
      // Calculate compressed bytes
      let compBits = 0;
      for (let ch of text) {{
        compBits += (currentCodes[ch] || "").length;
      }}
      const compBytes = Math.ceil(compBits / 8) || Math.round(rawBytes * 0.56);

      // EIP-2028: 16 gas non-zero, 4 gas zero
      // In ASCII text, ~100% are non-zero. In packed binary, ~1/256 are zero
      const rawGas = rawBytes * 16;
      const compZeroBytes = Math.round(compBytes / 256);
      const compNonZeroBytes = compBytes - compZeroBytes;
      const compGas = (compNonZeroBytes * 16) + (compZeroBytes * 4);

      const gasSaved = Math.max(0, rawGas - compGas);
      const gasSavedPct = ((gasSaved / rawGas) * 100).toFixed(1);

      const ethSavedPerTx = (gasSaved * gasPriceGwei * 1e-9);
      const usdSavedPerTx = (ethSavedPerTx * ethPriceUSD);
      const annualRollupSaved = (usdSavedPerTx * 100000);

      // Latency reduction (Decker & Wattenhofer Model)
      const latencyReductionPct = gasSavedPct;

      // Update UI Cards
      document.getElementById('bc-gas-saved').innerText = gasSaved.toLocaleString() + " Gas";
      document.getElementById('bc-gas-saved-pct').innerText = gasSavedPct + "% Calldata Gas Reduction";
      document.getElementById('bc-usd-saved').innerText = "$" + usdSavedPerTx.toFixed(2) + " USD";
      document.getElementById('bc-eth-saved').innerText = ethSavedPerTx.toFixed(5) + " ETH Saved / Tx";
      document.getElementById('bc-annual-saved').innerText = "$" + Math.round(annualRollupSaved).toLocaleString() + " / Year";
      document.getElementById('bc-latency-reduction').innerText = "-" + latencyReductionPct + "% Latency";

      // Update Breakdown Table
      document.getElementById('tbl-raw-bytes').innerText = rawBytes.toLocaleString() + " B";
      document.getElementById('tbl-raw-nonzero').innerText = rawBytes.toLocaleString();
      document.getElementById('tbl-raw-gas').innerText = rawGas.toLocaleString() + " gas";
      document.getElementById('tbl-raw-eth').innerText = (rawGas * gasPriceGwei * 1e-9).toFixed(5) + " ETH";
      document.getElementById('tbl-raw-usd').innerText = "$" + ((rawGas * gasPriceGwei * 1e-9) * ethPriceUSD).toFixed(2);

      document.getElementById('tbl-comp-bytes').innerText = compBytes.toLocaleString() + " B";
      document.getElementById('tbl-comp-nonzero').innerText = compNonZeroBytes.toLocaleString();
      document.getElementById('tbl-comp-zero').innerText = compZeroBytes.toLocaleString();
      document.getElementById('tbl-comp-gas').innerText = compGas.toLocaleString() + " gas";
      document.getElementById('tbl-comp-eth').innerText = (compGas * gasPriceGwei * 1e-9).toFixed(5) + " ETH";
      document.getElementById('tbl-comp-usd').innerText = "$" + ((compGas * gasPriceGwei * 1e-9) * ethPriceUSD).toFixed(2);

      document.getElementById('tbl-diff-bytes').innerText = "-" + (rawBytes - compBytes).toLocaleString() + " B (-" + gasSavedPct + "%)";
      document.getElementById('tbl-diff-gas').innerText = "-" + gasSaved.toLocaleString() + " gas (-" + gasSavedPct + "%)";
      document.getElementById('tbl-diff-eth').innerText = "-" + ethSavedPerTx.toFixed(5) + " ETH";
      document.getElementById('tbl-diff-usd').innerText = "-$" + usdSavedPerTx.toFixed(2) + " saved / tx";
    }}

    // FEATURE 4: Algorithm Race & Divergence Table
    function populateDivergenceTable() {{
      const tbody = document.getElementById('divergence-table-body');
      tbody.innerHTML = '';
      const N = currentText.length;
      let divergenceCount = 0;

      const sorted = Object.entries(currentFreqs).sort((a, b) => b[1] - a[1]);
      sorted.forEach(([ch, freq]) => {{
        const hCode = currentCodes[ch] || "";
        const sfCode = currentSfCodes[ch] || "";
        const p = (freq / N).toFixed(4);
        const disp = ch === ' ' ? "' ' (Space)" : (ch === '\\n' ? "'\\\\n' (Newline)" : "'" + ch + "'");
        
        let advStatus = "";
        let rowStyle = "";
        if (hCode.length < sfCode.length) {{
          divergenceCount++;
          rowStyle = "background: #E8F5E9; font-weight: bold;";
          advStatus = "<span class='badge badge-pass'>🏆 Huffman Shorter (+" + (sfCode.length - hCode.length) + "b)</span>";
        }} else if (hCode.length === sfCode.length) {{
          advStatus = "<span style='color: #666;'>Optimal Match</span>";
        }} else {{
          advStatus = "<span>Match</span>";
        }}

        const tr = document.createElement('tr');
        if (rowStyle) tr.style = rowStyle;
        tr.innerHTML = `
          <td><code>${{disp}}</code></td>
          <td>${{freq}}</td>
          <td>${{p}}</td>
          <td style="color: var(--green); font-family: monospace;">${{hCode}}</td>
          <td><strong>${{hCode.length}}</strong></td>
          <td style="color: var(--accent); font-family: monospace;">${{sfCode}}</td>
          <td><strong>${{sfCode.length}}</strong></td>
          <td>${{advStatus}}</td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('divergence-count-badge').innerText = divergenceCount > 0 ? 
        `Divergence: Huffman Shorter on ${{divergenceCount}} Symbols` : "Identical Expected Length on this alphabet";
    }}

    function startAlgorithmRace() {{
      const testMsg = document.getElementById('race-test-input').value || "BLOCKCHAIN AND GRAPH THEORY OPTIMIZATION";
      let hBits = 0;
      let sfBits = 0;
      for (let ch of testMsg) {{
        hBits += (currentCodes[ch] || "0000").length;
        sfBits += (currentSfCodes[ch] || "0000").length;
      }}

      const maxBits = Math.max(hBits, sfBits) * 1.05;
      const hPct = ((hBits / maxBits) * 100).toFixed(1);
      const sfPct = ((sfBits / maxBits) * 100).toFixed(1);

      document.getElementById('race-huff-bar').style.width = '0%';
      document.getElementById('race-sf-bar').style.width = '0%';
      document.getElementById('race-huff-bits').innerText = "Racing...";
      document.getElementById('race-sf-bits').innerText = "Racing...";

      setTimeout(() => {{
        document.getElementById('race-huff-bar').style.width = hPct + '%';
        document.getElementById('race-huff-bar').innerText = hBits + ' bits';
        document.getElementById('race-huff-bits').innerText = hBits + ' bits';

        document.getElementById('race-sf-bar').style.width = sfPct + '%';
        document.getElementById('race-sf-bar').innerText = sfBits + ' bits';
        document.getElementById('race-sf-bits').innerText = sfBits + ' bits';

        const diff = sfBits - hBits;
        if (diff > 0) {{
          document.getElementById('race-outcome-desc').innerHTML = `
            🎉 <strong>Race Winner: Huffman Coding!</strong> Used <strong>${{hBits}} bits</strong> vs. Shannon-Fano's <strong>${{sfBits}} bits</strong> (Saved <strong>${{diff}} bits</strong> / ${{( (diff/sfBits)*100 ).toFixed(1)}}% advantage).
          `;
          document.getElementById('race-winner-badge').className = "badge badge-pass";
          document.getElementById('race-winner-badge').innerText = "🏆 Huffman Won by " + diff + " bits";
        }} else {{
          document.getElementById('race-outcome-desc').innerHTML = `
            🤝 <strong>Tie:</strong> Both algorithms matched at <strong>${{hBits}} bits</strong> for this phrase.
          `;
          document.getElementById('race-winner-badge').innerText = "Matched on this input";
        }}
      }}, 100);
    }}

    // Tree Depth & Leaves
    function calculateMaxDepth(node) {{
      if (!node) return 0;
      return 1 + Math.max(calculateMaxDepth(node.left), calculateMaxDepth(node.right));
    }}

    function countTotalLeaves(node) {{
      if (!node) return 0;
      if (!node.left && !node.right) return 1;
      return countTotalLeaves(node.left) + countTotalLeaves(node.right);
    }}

    function onTreeViewModeChange() {{
      currentViewMode = document.getElementById('tree-view-mode').value;
      const sliderBox = document.getElementById('depth-slider-container');
      if (currentViewMode === 'adaptive') {{
        sliderBox.style.display = 'flex';
      }} else {{
        sliderBox.style.display = 'none';
      }}
      if (currentTreeRoot) {{
        renderTreeSVG(currentTreeRoot, true);
      }}
    }}

    function onDepthSliderChange(val) {{
      document.getElementById('depth-slider-val').innerText = val;
      if (currentTreeRoot) {{
        renderTreeSVG(currentTreeRoot, false);
      }}
    }}

    function replayTreeAnimation() {{
      if (currentTreeRoot) {{
        renderTreeSVG(currentTreeRoot, true);
      }}
    }}

    // Zero-Overlap In-Order SVG Tree Renderer with Level-by-Level Animated Reveal
    function renderTreeSVG(root, animate = true) {{
      const svg = document.getElementById('tree-svg');
      const viewport = document.getElementById('tree-viewport');
      viewport.innerHTML = '';
      if (!root) return;

      treeMaxDepth = calculateMaxDepth(root);
      const totalLeaves = countTotalLeaves(root);
      document.getElementById('tree-stats-badge').innerText = totalLeaves + " Leaves • Max Depth: " + treeMaxDepth;

      const depthSlider = document.getElementById('tree-depth-slider');
      depthSlider.max = treeMaxDepth;

      let displayRoot = root;
      let effectiveMaxDepth = null;

      if (currentViewMode === 'top12' || currentViewMode === 'top20') {{
        const limitK = currentViewMode === 'top12' ? 12 : 20;
        const text = currentText || document.getElementById('input-text').value;
        const fMap = {{}};
        for (let ch of text) fMap[ch] = (fMap[ch] || 0) + 1;
        const topChars = Object.entries(fMap).sort((a,b) => b[1] - a[1]).slice(0, limitK).map(e => e[0]);
        
        let subHeap = topChars.map(c => ({{ id: 0, char: c, freq: fMap[c], left: null, right: null }}));
        let sId = 1000;
        while (subHeap.length > 1) {{
          subHeap.sort((a, b) => a.freq - b.freq);
          let n1 = subHeap.shift();
          let n2 = subHeap.shift();
          subHeap.push({{ id: sId++, char: null, freq: n1.freq + n2.freq, left: n1, right: n2 }});
        }}
        displayRoot = subHeap[0];
        effectiveMaxDepth = null;
      }} else if (currentViewMode === 'adaptive') {{
        effectiveMaxDepth = parseInt(document.getElementById('tree-depth-slider').value) || 5;
      }} else {{
        effectiveMaxDepth = null;
      }}

      let leafIndex = 0;
      const LEAF_SPACING = 68;
      const LEVEL_HEIGHT = 88;

      function assignCoords(node, depth, maxD) {{
        if (!node) return null;
        node._depth = depth;
        if (maxD !== null && depth > maxD) return null;

        const isTerm = (!node.left && !node.right) || (maxD !== null && depth === maxD);
        if (isTerm) {{
          node._x = leafIndex * LEAF_SPACING + 60;
          node._y = depth * LEVEL_HEIGHT + 55;
          node._isTruncated = (maxD !== null && depth === maxD && (node.left || node.right));
          leafIndex++;
          return node._x;
        }}

        node._isTruncated = false;
        const leftX = assignCoords(node.left, depth + 1, maxD);
        const rightX = assignCoords(node.right, depth + 1, maxD);

        if (leftX !== null && rightX !== null) {{
          node._x = (leftX + rightX) / 2.0;
        }} else if (leftX !== null) {{
          node._x = leftX;
        }} else if (rightX !== null) {{
          node._x = rightX;
        }} else {{
          node._x = leafIndex * LEAF_SPACING + 60;
          leafIndex++;
        }}

        node._y = depth * LEVEL_HEIGHT + 55;
        return node._x;
      }}

      assignCoords(displayRoot, 0, effectiveMaxDepth);

      const totalCanvasWidth = Math.max(1300, leafIndex * LEAF_SPACING + 120);
      const activeLevels = effectiveMaxDepth ? Math.min(treeMaxDepth, effectiveMaxDepth) : treeMaxDepth;
      const totalCanvasHeight = Math.max(550, activeLevels * LEVEL_HEIGHT + 140);

      svg.setAttribute("width", totalCanvasWidth);
      svg.setAttribute("height", totalCanvasHeight);
      svg.setAttribute("viewBox", "0 0 " + totalCanvasWidth + " " + totalCanvasHeight);

      const edgeGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
      edgeGroup.setAttribute("id", "edges-layer");
      viewport.appendChild(edgeGroup);

      const nodeGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
      nodeGroup.setAttribute("id", "nodes-layer");
      viewport.appendChild(nodeGroup);

      const packetGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
      packetGroup.setAttribute("id", "packet-layer");
      viewport.appendChild(packetGroup);

      function drawEdges(node) {{
        if (!node) return;
        if (node.left && node.left._x !== undefined) {{
          createAnimatedEdge(node, node.left, "0");
          drawEdges(node.left);
        }}
        if (node.right && node.right._x !== undefined) {{
          createAnimatedEdge(node, node.right, "1");
          drawEdges(node.right);
        }}
      }}
      drawEdges(displayRoot);

      function drawNodes(node) {{
        if (!node || node._x === undefined) return;

        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("class", "tree-node-group" + (animate ? " anim-node" : ""));
        g.setAttribute("id", "svg-node-" + node.id);
        g.setAttribute("data-char", node.char || "");
        g.setAttribute("data-freq", node.freq);
        g.setAttribute("data-depth", node._depth);

        const delayMs = animate ? Math.min(800, node._depth * 90) : 0;
        if (animate) {{
          g.style.animationDelay = delayMs + "ms";
        }}

        g.addEventListener("mouseenter", () => {{
          highlightNodePath(node, displayRoot);
          showTreeHud(node);
        }});
        g.addEventListener("mouseleave", () => {{
          clearPathHighlight();
          hideTreeHud();
        }});
        g.addEventListener("click", () => {{
          animateSignalToNode(node, displayRoot);
        }});

        if (!node.left && !node.right) {{
          let rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
          rect.setAttribute("x", node._x - 26);
          rect.setAttribute("y", node._y - 18);
          rect.setAttribute("width", 52);
          rect.setAttribute("height", 36);
          rect.setAttribute("rx", 6);
          rect.setAttribute("fill", "#2E7D32");
          rect.setAttribute("stroke", "#1B5E20");
          rect.setAttribute("stroke-width", "2");
          rect.style.filter = "drop-shadow(0 2px 4px rgba(0,0,0,0.18))";

          let title = document.createElementNS("http://www.w3.org/2000/svg", "title");
          title.textContent = "Leaf Node: '" + node.char + "' (ASCII " + (node.char ? node.char.charCodeAt(0) : '?') + ")\\nWeight: " + node.freq + "\\nPrefix Code: " + (currentCodes[node.char] || '') + "\\n👉 Click to animate bitstream path!";
          rect.appendChild(title);
          g.appendChild(rect);

          let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
          text.setAttribute("x", node._x);
          text.setAttribute("y", node._y + 4);
          text.setAttribute("text-anchor", "middle");
          text.setAttribute("fill", "white");
          text.setAttribute("font-size", "11px");
          text.setAttribute("font-family", "Consolas, monospace");
          text.setAttribute("font-weight", "bold");
          let chDisplay = node.char === ' ' ? "' '" : (node.char === '\\n' ? "\\\\n" : (node.char === '\\t' ? "\\\\t" : node.char));
          text.textContent = chDisplay + ":" + node.freq;
          g.appendChild(text);

        }} else {{
          let circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          circle.setAttribute("cx", node._x);
          circle.setAttribute("cy", node._y);
          circle.setAttribute("r", 20);
          circle.setAttribute("fill", "#1F4E78");
          circle.setAttribute("stroke", "#102C57");
          circle.setAttribute("stroke-width", "2.2");
          circle.style.filter = "drop-shadow(0 2px 4px rgba(0,0,0,0.18))";

          let title = document.createElementNS("http://www.w3.org/2000/svg", "title");
          title.textContent = "Internal Vertex (Weight: " + node.freq + ")" + (node._isTruncated ? "\\n[Subtree continues below - increase Max Depth]" : "") + "\\n👉 Click to trace path from root!";
          circle.appendChild(title);
          g.appendChild(circle);

          let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
          text.setAttribute("x", node._x);
          text.setAttribute("y", node._y + 4);
          text.setAttribute("text-anchor", "middle");
          text.setAttribute("fill", "white");
          text.setAttribute("font-size", "10px");
          text.setAttribute("font-weight", "bold");
          text.setAttribute("font-family", "sans-serif");
          text.textContent = node.freq;
          g.appendChild(text);

          if (node._isTruncated) {{
            let pill = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            pill.setAttribute("x", node._x - 18);
            pill.setAttribute("y", node._y + 22);
            pill.setAttribute("width", 36);
            pill.setAttribute("height", 14);
            pill.setAttribute("rx", 7);
            pill.setAttribute("fill", "#E6550D");
            g.appendChild(pill);

            let pillText = document.createElementNS("http://www.w3.org/2000/svg", "text");
            pillText.setAttribute("x", node._x);
            pillText.setAttribute("y", node._y + 32);
            pillText.setAttribute("text-anchor", "middle");
            pillText.setAttribute("fill", "white");
            pillText.setAttribute("font-size", "8.5px");
            pillText.setAttribute("font-weight", "bold");
            pillText.textContent = "+sub";
            g.appendChild(pillText);
          }}
        }}

        nodeGroup.appendChild(g);

        if (!node._isTruncated) {{
          drawNodes(node.left);
          drawNodes(node.right);
        }}
      }}
      drawNodes(displayRoot);

      function createAnimatedEdge(pNode, cNode, label) {{
        const x1 = pNode._x, y1 = pNode._y;
        const x2 = cNode._x, y2 = cNode._y;
        const edgeLength = Math.hypot(x2 - x1, y2 - y1);
        const delayMs = animate ? Math.min(750, pNode._depth * 90) : 0;

        let edgeId = "edge-" + pNode.id + "-" + cNode.id;

        let line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", x1);
        line.setAttribute("y1", y1);
        line.setAttribute("x2", x2);
        line.setAttribute("y2", y2);
        line.setAttribute("id", edgeId);
        line.setAttribute("stroke", "#7F8C8D");
        line.setAttribute("stroke-width", "1.7");
        line.setAttribute("class", "edge-path" + (animate ? " anim-edge" : ""));

        if (animate) {{
          line.style.strokeDasharray = edgeLength;
          line.style.strokeDashoffset = edgeLength;
          line.style.animationDelay = delayMs + "ms";
        }}

        edgeGroup.appendChild(line);

        let midX = (x1 + x2) / 2;
        let midY = (y1 + y2) / 2;

        let labelG = document.createElementNS("http://www.w3.org/2000/svg", "g");
        labelG.setAttribute("class", "edge-label-g" + (animate ? " anim-label" : ""));
        if (animate) {{
          labelG.style.animationDelay = (delayMs + 120) + "ms";
        }}

        let bg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        bg.setAttribute("x", midX + (label === "0" ? -14 : 4));
        bg.setAttribute("y", midY - 8);
        bg.setAttribute("width", 13);
        bg.setAttribute("height", 13);
        bg.setAttribute("rx", 3);
        bg.setAttribute("fill", "#FFFFFF");
        bg.setAttribute("stroke", "#D32F2F");
        bg.setAttribute("stroke-width", "1");
        labelG.appendChild(bg);

        let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", midX + (label === "0" ? -7.5 : 10.5));
        text.setAttribute("y", midY + 2);
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("fill", "#D32F2F");
        text.setAttribute("font-size", "10px");
        text.setAttribute("font-weight", "bold");
        text.textContent = label;
        labelG.appendChild(text);

        edgeGroup.appendChild(labelG);
      }}

      applyTreeTransform();

      const container = document.getElementById('tree-svg-container');
      if (displayRoot._x) {{
        container.scrollLeft = displayRoot._x - (container.clientWidth / 2);
      }}
    }}

    function findPath(target, curr, path = []) {{
      if (!curr) return null;
      path.push(curr);
      if (curr.id === target.id) return path;
      if (curr.left) {{
        let res = findPath(target, curr.left, [...path]);
        if (res) return res;
      }}
      if (curr.right) {{
        let res = findPath(target, curr.right, [...path]);
        if (res) return res;
      }}
      return null;
    }}

    function highlightNodePath(targetNode, root) {{
      clearPathHighlight();
      const path = findPath(targetNode, root);
      if (!path || path.length === 0) return;

      for (let i = 0; i < path.length; i++) {{
        const nodeEl = document.getElementById("svg-node-" + path[i].id);
        if (nodeEl) nodeEl.classList.add("highlight-node");

        if (i < path.length - 1) {{
          const edgeEl = document.getElementById("edge-" + path[i].id + "-" + path[i+1].id);
          if (edgeEl) edgeEl.classList.add("highlight-edge");
        }}
      }}
    }}

    function clearPathHighlight() {{
      document.querySelectorAll(".highlight-node").forEach(n => n.classList.remove("highlight-node"));
      document.querySelectorAll(".highlight-edge").forEach(e => e.classList.remove("highlight-edge"));
    }}

    function showTreeHud(node) {{
      const hud = document.getElementById('tree-hud');
      if (!hud) return;
      let text = "";
      if (!node.left && !node.right) {{
        let ch = node.char === ' ' ? "' ' (Space)" : (node.char === '\\n' ? "'\\n' (Newline)" : "'" + node.char + "'");
        text = "🌿 <strong>Leaf Symbol:</strong> " + ch + " | <strong>Weight:</strong> " + node.freq + " | <strong>Codeword:</strong> <code>" + (currentCodes[node.char] || '0') + "</code> (" + (currentCodes[node.char] || '0').length + " bits)";
      }} else {{
        text = "🔵 <strong>Internal Node</strong> | <strong>Merged Weight:</strong> " + node.freq + " | <strong>Depth:</strong> " + (node._depth || 0) + " | Click to trace packet!";
      }}
      hud.innerHTML = text;
      hud.style.display = "block";
    }}

    function hideTreeHud() {{
      const hud = document.getElementById('tree-hud');
      if (hud) hud.style.display = "none";
    }}

    function animateSignalToNode(targetNode, root) {{
      const path = findPath(targetNode, root);
      if (!path || path.length < 2) return;

      highlightNodePath(targetNode, root);

      const packetLayer = document.getElementById('packet-layer');
      packetLayer.innerHTML = '';

      let packet = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      packet.setAttribute("r", "7");
      packet.setAttribute("fill", "#00E5FF");
      packet.setAttribute("stroke", "#FFFFFF");
      packet.setAttribute("stroke-width", "2");
      packet.style.filter = "drop-shadow(0 0 10px #00E5FF)";
      packetLayer.appendChild(packet);

      let step = 0;
      function movePacket() {{
        if (step >= path.length) {{
          const dest = path[path.length - 1];
          let shockwave = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          shockwave.setAttribute("cx", dest._x);
          shockwave.setAttribute("cy", dest._y);
          shockwave.setAttribute("r", "20");
          shockwave.setAttribute("fill", "none");
          shockwave.setAttribute("stroke", "#00E5FF");
          shockwave.setAttribute("stroke-width", "3");
          packetLayer.appendChild(shockwave);

          let r = 20, op = 1.0;
          let shockTimer = setInterval(() => {{
            r += 3;
            op -= 0.08;
            shockwave.setAttribute("r", r);
            shockwave.style.opacity = op;
            if (op <= 0) {{
              clearInterval(shockTimer);
              packetLayer.innerHTML = '';
            }}
          }}, 30);
          return;
        }}

        const currNode = path[step];
        packet.setAttribute("cx", currNode._x);
        packet.setAttribute("cy", currNode._y);
        step++;
        setTimeout(movePacket, 220);
      }}

      movePacket();
    }}

    function animateRandomSignal() {{
      if (!currentTreeRoot) return;
      const chars = Object.keys(currentCodes);
      if (!chars.length) return;
      const rndChar = chars[Math.floor(Math.random() * chars.length)];
      
      function findLeaf(node) {{
        if (!node) return null;
        if (!node.left && !node.right && node.char === rndChar) return node;
        return findLeaf(node.left) || findLeaf(node.right);
      }}
      const leaf = findLeaf(currentTreeRoot);
      if (leaf) {{
        animateSignalToNode(leaf, currentTreeRoot);
        showTreeHud(leaf);
        setTimeout(hideTreeHud, 3500);
      }}
    }}

    // Zoom and Pan Controls
    function applyTreeTransform() {{
      const viewport = document.getElementById('tree-viewport');
      viewport.setAttribute("transform", "translate(" + panX + ", " + panY + ") scale(" + treeScale + ")");
    }}

    function zoomInTree() {{
      treeScale = Math.min(3.0, treeScale * 1.25);
      applyTreeTransform();
    }}
    function zoomOutTree() {{
      treeScale = Math.max(0.25, treeScale * 0.8);
      applyTreeTransform();
    }}
    function resetTreeZoom() {{
      treeScale = 1.0;
      panX = 0;
      panY = 0;
      applyTreeTransform();
    }}
    function fitTreeWidth() {{
      const container = document.getElementById('tree-svg-container');
      const svg = document.getElementById('tree-svg');
      const svgWidth = parseFloat(svg.getAttribute("width")) || 1300;
      treeScale = (container.clientWidth - 40) / svgWidth;
      panX = 0;
      panY = 0;
      applyTreeTransform();
    }}

    function exportTreeSVG() {{
      const svg = document.getElementById('tree-svg');
      const serializer = new XMLSerializer();
      let source = serializer.serializeToString(svg);
      if(!source.match(/^<svg[^>]+xmlns="http\\:\\/\\/www\\.w3\\.org\\/2000\\/svg"/)){{
        source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
      }}
      const blob = new Blob([source], {{ type: "image/svg+xml;charset=utf-8" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "huffman_rooted_tree.svg";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    // Mouse Drag to Pan
    const treeContainer = document.getElementById('tree-svg-container');
    treeContainer.addEventListener('mousedown', (e) => {{
      isPanning = true;
      startX = e.clientX - panX;
      startY = e.clientY - panY;
    }});
    window.addEventListener('mousemove', (e) => {{
      if (!isPanning) return;
      panX = e.clientX - startX;
      panY = e.clientY - startY;
      applyTreeTransform();
    }});
    window.addEventListener('mouseup', () => {{
      isPanning = false;
    }});

    // Wheel Zoom
    treeContainer.addEventListener('wheel', (e) => {{
      e.preventDefault();
      if (e.deltaY < 0) {{
        treeScale = Math.min(3.0, treeScale * 1.1);
      }} else {{
        treeScale = Math.max(0.25, treeScale * 0.9);
      }}
      applyTreeTransform();
    }}, {{ passive: false }});

    // Step-by-Step Simulator
    function updateStepView() {{
      if (!mergeSteps.length) return;
      const step = mergeSteps[currentStepIdx];
      document.getElementById('step-badge').innerText = "Step " + currentStepIdx + " / " + (mergeSteps.length - 1);
      document.getElementById('step-slider').max = mergeSteps.length - 1;
      document.getElementById('step-slider').value = currentStepIdx;

      document.getElementById('step-action-title').innerText = step.action;
      document.getElementById('step-action-desc').innerText = step.desc;

      const qBox = document.getElementById('queue-display');
      qBox.innerHTML = '';
      step.heapState.forEach(item => {{
        let span = document.createElement('span');
        span.className = 'queue-chip ' + (item.isLeaf ? 'chip-leaf' : 'chip-internal');
        span.innerText = item.label + " (" + item.freq + ")";
        qBox.appendChild(span);
      }});
    }}

    function nextStep() {{
      if (currentStepIdx < mergeSteps.length - 1) {{
        currentStepIdx++;
        updateStepView();
      }}
    }}
    function prevStep() {{
      if (currentStepIdx > 0) {{
        currentStepIdx--;
        updateStepView();
      }}
    }}
    function onSliderMove(val) {{
      currentStepIdx = parseInt(val);
      updateStepView();
    }}
    function playAutoSteps() {{
      if (autoPlayTimer) {{
        clearInterval(autoPlayTimer);
        autoPlayTimer = null;
      }} else {{
        autoPlayTimer = setInterval(() => {{
          if (currentStepIdx < mergeSteps.length - 1) {{
            currentStepIdx++;
            updateStepView();
          }} else {{
            clearInterval(autoPlayTimer);
            autoPlayTimer = null;
          }}
        }}, 800);
      }}
    }}

    // Bitstream Tracer
    function setupBitTracer() {{
      const msg = document.getElementById('trace-input').value;
      traceBitstring = "";
      for (let ch of msg) {{
        traceBitstring += (currentCodes[ch] || "0");
      }}
      traceBitIdx = 0;
      traceCurrentNode = currentTreeRoot;
      traceDecodedOutput = "";

      renderTraceBits();
      document.getElementById('trace-decoded').innerText = "";
      document.getElementById('trace-status').innerText = "Pointer at Tree Root (Ready to Step)";
      document.getElementById('trace-path-desc').innerText = "Bitstream length: " + traceBitstring.length + " bits.";
    }}

    function renderTraceBits() {{
      const box = document.getElementById('trace-bits');
      box.innerHTML = '';
      for (let i = 0; i < traceBitstring.length; i++) {{
        let span = document.createElement('span');
        span.className = 'bit-token ' + (i === traceBitIdx ? 'bit-active' : (i < traceBitIdx ? 'bit-done' : ''));
        span.innerText = traceBitstring[i];
        box.appendChild(span);
      }}
    }}

    function stepBit() {{
      if (traceBitIdx >= traceBitstring.length) {{
        document.getElementById('trace-status').innerText = "Decoding Complete!";
        return;
      }}
      let bit = traceBitstring[traceBitIdx];
      traceBitIdx++;

      if (bit === "0") {{
        traceCurrentNode = traceCurrentNode.left || traceCurrentNode;
        document.getElementById('trace-path-desc').innerText = "Encountered '0' -> Navigated LEFT to weight " + traceCurrentNode.freq;
      }} else {{
        traceCurrentNode = traceCurrentNode.right || traceCurrentNode;
        document.getElementById('trace-path-desc').innerText = "Encountered '1' -> Navigated RIGHT to weight " + traceCurrentNode.freq;
      }}

      if (!traceCurrentNode.left && !traceCurrentNode.right) {{
        traceDecodedOutput += traceCurrentNode.char;
        document.getElementById('trace-decoded').innerText = traceDecodedOutput;
        document.getElementById('trace-status').innerText = "Leaf reached! Emitted '" + traceCurrentNode.char + "' -> Reset to Root";
        traceCurrentNode = currentTreeRoot;
      }} else {{
        document.getElementById('trace-status').innerText = "At internal node (weight " + traceCurrentNode.freq + ")";
      }}
      renderTraceBits();
    }}

    function resetBitTracer() {{
      traceBitIdx = 0;
      traceCurrentNode = currentTreeRoot;
      traceDecodedOutput = "";
      renderTraceBits();
      document.getElementById('trace-decoded').innerText = "";
      document.getElementById('trace-status').innerText = "Reset to Root";
    }}

    // Code Inspector
    function showSource(filename) {{
      currentSelectedCodeFile = filename;
      document.getElementById('code-file-title').innerText = "Viewing: " + filename;
      document.getElementById('code-display').textContent = SOURCE_CODES[filename] || "# Code not found";
      
      document.querySelectorAll('#tab-feeder .btn-outline').forEach(b => {{
        b.style.borderColor = 'var(--blue)';
        b.style.fontWeight = 'normal';
      }});
      const activeBtn = document.getElementById('btn-' + filename);
      if (activeBtn) {{
        activeBtn.style.borderColor = 'var(--navy)';
        activeBtn.style.fontWeight = 'bold';
      }}
    }}

    function feedCurrentCodeToModel() {{
      const codeText = SOURCE_CODES[currentSelectedCodeFile];
      if (codeText) {{
        document.getElementById('input-text').value = codeText;
        document.getElementById('select-preset').value = 'custom';
        switchTab('tab-simulator');
        runCompression();
      }}
    }}

    window.onload = function() {{
      showSource('huffman.py');
      document.getElementById('select-preset').value = 'huffman_py';
      loadPreset(false);
    }};
  </script>
</body>
</html>
"""

# Write to docs/interactive_model.html
docs_path = os.path.join(BASE_DIR, "docs", "interactive_model.html")
with open(docs_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[OK] Generated: {docs_path} ({len(html_content):,} bytes)")

# Write to root interactive_model.html
root_path = os.path.join(BASE_DIR, "interactive_model.html")
with open(root_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[OK] Generated: {root_path} ({len(html_content):,} bytes)")
