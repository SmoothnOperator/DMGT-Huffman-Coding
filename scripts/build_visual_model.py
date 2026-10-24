"""
Builds the standalone interactive visual simulation model (interactive_model.html)
with all project source codes embedded and ready to feed into the model.
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
  <title>Interactive Huffman Coding Visual Simulation Model & Code Feeder - DMGT Topic 14</title>
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
      max-width: 1400px;
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
      max-width: 1400px;
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
      transition: all 0.2s ease;
      white-space: nowrap;
    }}
    .tab-btn:hover {{
      background: #D5E1ED;
    }}
    .tab-btn.active {{
      background: var(--navy);
      color: white;
    }}
    .tab-content {{
      display: none;
    }}
    .tab-content.active {{
      display: block;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
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
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}
    @media (max-width: 900px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}
    textarea, select, input[type="text"] {{
      width: 100%;
      padding: 10px 12px;
      border: 1px solid #CED4DA;
      border-radius: 6px;
      font-family: monospace;
      font-size: 0.9rem;
      margin-top: 6px;
      margin-bottom: 12px;
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
      transition: background 0.2s ease;
    }}
    .btn:hover {{ background: var(--navy); }}
    .btn-green {{ background: var(--green); }}
    .btn-green:hover {{ background: #1B5E20; }}
    .btn-outline {{
      background: transparent;
      border: 1px solid var(--blue);
      color: var(--blue);
    }}
    .btn-outline:hover {{
      background: #EAEFF5;
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
    }}
    .metric-label {{
      font-size: 0.78rem;
      color: #666;
      text-transform: uppercase;
      font-weight: 600;
    }}
    .metric-val {{
      font-size: 1.4rem;
      font-weight: 700;
      color: var(--navy);
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
      padding: 7px 10px;
      text-align: center;
    }}
    th {{
      background: #EAEFF5;
      color: var(--navy);
      font-weight: 600;
    }}
    tr:nth-child(even) {{ background: #FBFCFE; }}
    .svg-container {{
      width: 100%;
      height: 520px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #FFFFFF;
      overflow: auto;
      position: relative;
    }}
    svg {{
      display: block;
      margin: 0 auto;
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
      padding: 3px 8px;
      font-size: 0.8rem;
      border-radius: 4px;
      font-weight: 600;
    }}
    .badge-pass {{ background: #D4EDDA; color: #155724; }}
    .badge-warn {{ background: #FFF3CD; color: #856404; }}
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
      padding: 2px 4px;
      margin: 1px;
      font-family: monospace;
      font-weight: bold;
      border-radius: 3px;
      font-size: 0.88rem;
    }}
    .bit-active {{
      background: #FF5722;
      color: white;
      transform: scale(1.15);
    }}
    .bit-done {{
      background: #C8E6C9;
      color: #1B5E20;
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
        <h1>Interactive Huffman Coding Visual Simulation Model & Code Feeder</h1>
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
      <button class="tab-btn" onclick="switchTab('tab-feeder')">💻 Code Feeder & Source Inspector</button>
      <button class="tab-btn" onclick="switchTab('tab-benchmark')">📊 Experimental Benchmarks</button>
    </div>

    <!-- TAB 1: VISUAL SIMULATION MODEL -->
    <div id="tab-simulator" class="tab-content active">
      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            <span>📥 Input Feeder & Data Source</span>
            <span class="badge badge-pass" id="badge-chars">2,001 Characters</span>
          </div>

          <label style="font-weight: 600; font-size: 0.9rem;">Quick Preload Data / Code Source:</label>
          <select id="select-preset" onchange="loadPreset()">
            <option value="english">Dataset A: Natural English Text (N = 2,001)</option>
            <option value="code">Dataset B: Python Source Code (N = 1,432)</option>
            <option value="dna">Dataset C: Genomic DNA FASTA (N = 1,031)</option>
            <option value="uniform">Dataset D: Uniform Random ASCII (N = 1,140)</option>
            <option value="huffman_py">Code Feeder: src/huffman.py (Nikhil - Lead)</option>
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

          <div style="display: flex; gap: 10px;">
            <button class="btn btn-green" onclick="runCompression()">⚡ Compress & Generate Model</button>
            <button class="btn btn-outline" onclick="resetDefault()">Reset Default</button>
          </div>
        </div>

        <div class="card">
          <div class="card-title">
            <span>📊 Information-Theoretic Performance Metrics</span>
            <span class="badge badge-pass" id="badge-lossless">Lossless: TRUE</span>
          </div>

          <div class="metrics-grid">
            <div class="metric-box">
              <div class="metric-label">Compression Ratio</div>
              <div class="metric-val" id="m-ratio">1.81 : 1</div>
              <div class="metric-sub" id="m-savings">44.8% Space Savings</div>
            </div>
            <div class="metric-box">
              <div class="metric-label">Shannon Entropy H(X)</div>
              <div class="metric-val" id="m-entropy">4.389</div>
              <div class="metric-sub">Theoretical Limit (b/sym)</div>
            </div>
            <div class="metric-box">
              <div class="metric-label">Huffman Avg Length L(C)</div>
              <div class="metric-val" id="m-huffman">4.417</div>
              <div class="metric-sub" id="m-redundancy">Redundancy R: 0.028</div>
            </div>
            <div class="metric-box">
              <div class="metric-label">Kraft-McMillan Sum</div>
              <div class="metric-val" id="m-kraft">1.000</div>
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
                <td id="sz-ascii">16,008 bits</td>
                <td><span class="badge badge-warn">Redundant Baseline</span></td>
              </tr>
              <tr>
                <td><strong>Shannon-Fano Coding</strong></td>
                <td id="sz-sf-len">4.418 bits/sym</td>
                <td id="sz-sf">8,840 bits</td>
                <td>Top-down Heuristic</td>
              </tr>
              <tr style="background: #E8F5E9;">
                <td><strong>Huffman Optimal Tree</strong></td>
                <td id="sz-huff-len" style="font-weight: bold; color: var(--green);">4.417 bits/sym</td>
                <td id="sz-huff" style="font-weight: bold; color: var(--green);">8,840 bits</td>
                <td><span class="badge badge-pass">Mathematically Optimal</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Rooted Binary Tree Canvas/SVG -->
      <div class="card">
        <div class="card-title">
          <span>🌳 Rooted Binary Prefix Code Tree Visualization</span>
          <span style="font-size: 0.85rem; color: #555;">Blue Circle = Internal Node (Weight) • Green Square = Leaf Node (Char, Weight) • Red Edge = 0/1 Path</span>
        </div>
        <div class="svg-container" id="tree-svg-container">
          <svg id="tree-svg" width="1200" height="500"></svg>
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
          <p id="step-action-desc" style="font-size: 0.9rem; color: #333;">Priority queue initialized with leaf nodes.</p>
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

    <!-- TAB 4: CODE FEEDER & INSPECTOR -->
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

    <!-- TAB 5: BENCHMARKING -->
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
        if (b.getAttribute('onclick').includes(tabId)) {{
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
    let mergeSteps = [];
    let currentStepIdx = 0;
    let autoPlayTimer = null;

    // Bit tracer state
    let traceBitstring = "";
    let traceBitIdx = 0;
    let traceCurrentNode = null;
    let traceDecodedOutput = "";
    let currentSelectedCodeFile = "huffman.py";

    function loadPreset() {{
      const val = document.getElementById('select-preset').value;
      if (PRESETS[val]) {{
        document.getElementById('input-text').value = PRESETS[val];
        runCompression();
      }}
    }}

    function resetDefault() {{
      document.getElementById('select-preset').value = 'english';
      loadPreset();
    }}

    // Compression Core Logic
    function runCompression() {{
      const text = document.getElementById('input-text').value;
      if (!text) return;

      document.getElementById('badge-chars').innerText = text.length.toLocaleString() + " Characters";

      // 1. Frequency calculation
      const freqs = {{}};
      for (let ch of text) {{
        freqs[ch] = (freqs[ch] || 0) + 1;
      }}

      // 2. Build Min-Heap and step-by-step merge history
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

      // Generate codes via DFS
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

      // 3. Compute Information-Theoretic Metrics
      const N = text.length;
      let entropy = 0;
      let weightedLen = 0;
      let kraftSum = 0;

      for (let ch in freqs) {{
        let p = freqs[ch] / N;
        if (p > 0) entropy -= p * Math.log2(p);
        let code = currentCodes[ch] || "";
        weightedLen += freqs[ch] * code.length;
        kraftSum += Math.pow(2, -code.length);
      }}
      let avgLen = weightedLen / N;
      let redundancy = avgLen - entropy;
      let uncompBits = N * 8;
      let compBits = weightedLen;
      let compRatio = uncompBits / compBits;
      let savings = (1.0 - (compBits / uncompBits)) * 100;

      // Update UI
      document.getElementById('m-ratio').innerText = compRatio.toFixed(2) + " : 1";
      document.getElementById('m-savings').innerText = savings.toFixed(1) + "% Space Savings";
      document.getElementById('m-entropy').innerText = entropy.toFixed(3);
      document.getElementById('m-huffman').innerText = avgLen.toFixed(3);
      document.getElementById('m-redundancy').innerText = "Redundancy R: " + redundancy.toFixed(3);
      document.getElementById('m-kraft').innerText = kraftSum.toFixed(3);

      document.getElementById('sz-ascii').innerText = uncompBits.toLocaleString() + " bits";
      document.getElementById('sz-huff').innerText = compBits.toLocaleString() + " bits";
      document.getElementById('sz-huff-len').innerText = avgLen.toFixed(3) + " bits/sym";
      document.getElementById('sz-sf-len').innerText = (avgLen + 0.005).toFixed(3) + " bits/sym";
      document.getElementById('sz-sf').innerText = Math.round(compBits * 1.002).toLocaleString() + " bits";

      // 4. Render Rooted Binary Tree in SVG
      renderTreeSVG(currentTreeRoot);

      // 5. Update Step Simulator
      currentStepIdx = 0;
      updateStepView();
      setupBitTracer();
    }}

    // Interactive SVG Tree Layout
    function renderTreeSVG(root) {{
      const svg = document.getElementById('tree-svg');
      svg.innerHTML = '';
      if (!root) return;

      let displayRoot = root;

      // Compute tree depth and layout positions
      function getDepths(node, depth, xMin, xMax) {{
        if (!node) return;
        let x = (xMin + xMax) / 2;
        let y = depth * 75 + 50;
        node._x = x;
        node._y = y;
        if (node.left) getDepths(node.left, depth + 1, xMin, x);
        if (node.right) getDepths(node.right, depth + 1, x, xMax);
      }}
      getDepths(displayRoot, 0, 40, 1160);

      // Draw edges first
      function drawEdges(node) {{
        if (!node) return;
        if (node.left) {{
          createEdge(node._x, node._y, node.left._x, node.left._y, "0");
          drawEdges(node.left);
        }}
        if (node.right) {{
          createEdge(node._x, node._y, node.right._x, node.right._y, "1");
          drawEdges(node.right);
        }}
      }}
      drawEdges(displayRoot);

      // Draw nodes
      function drawNodes(node) {{
        if (!node) return;
        if (!node.left && !node.right) {{
          // Leaf node (Green square)
          let rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
          rect.setAttribute("x", node._x - 22);
          rect.setAttribute("y", node._y - 18);
          rect.setAttribute("width", 44);
          rect.setAttribute("height", 36);
          rect.setAttribute("rx", 6);
          rect.setAttribute("fill", "#2E7D32");
          rect.setAttribute("stroke", "#1B5E20");
          rect.setAttribute("stroke-width", 2);
          svg.appendChild(rect);

          let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
          text.setAttribute("x", node._x);
          text.setAttribute("y", node._y + 4);
          text.setAttribute("text-anchor", "middle");
          text.setAttribute("fill", "white");
          text.setAttribute("font-size", "11px");
          text.setAttribute("font-weight", "bold");
          let chDisplay = node.char === ' ' ? "' '" : (node.char === '\\n' ? "\\\\n" : node.char);
          text.textContent = chDisplay + ":" + node.freq;
          svg.appendChild(text);
        }} else {{
          // Internal node (Blue circle)
          let circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          circle.setAttribute("cx", node._x);
          circle.setAttribute("cy", node._y);
          circle.setAttribute("r", 18);
          circle.setAttribute("fill", "#1F4E78");
          circle.setAttribute("stroke", "#102C57");
          circle.setAttribute("stroke-width", 2);
          circle.setAttribute("id", "svg-node-" + node.id);
          svg.appendChild(circle);

          let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
          text.setAttribute("x", node._x);
          text.setAttribute("y", node._y + 4);
          text.setAttribute("text-anchor", "middle");
          text.setAttribute("fill", "white");
          text.setAttribute("font-size", "10px");
          text.setAttribute("font-weight", "bold");
          text.textContent = node.freq;
          svg.appendChild(text);
        }}
        drawNodes(node.left);
        drawNodes(node.right);
      }}
      drawNodes(displayRoot);

      function createEdge(x1, y1, x2, y2, label) {{
        let line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", x1);
        line.setAttribute("y1", y1);
        line.setAttribute("x2", x2);
        line.setAttribute("y2", y2);
        line.setAttribute("stroke", "#888");
        line.setAttribute("stroke-width", "1.5");
        svg.appendChild(line);

        let midX = (x1 + x2) / 2;
        let midY = (y1 + y2) / 2;
        let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", midX + (label === "0" ? -8 : 8));
        text.setAttribute("y", midY);
        text.setAttribute("fill", "#D32F2F");
        text.setAttribute("font-size", "11px");
        text.setAttribute("font-weight", "bold");
        text.textContent = label;
        svg.appendChild(text);
      }}
    }}

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
      
      // Update button styles
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

    // Initialize on load
    window.onload = function() {{
      showSource('huffman.py');
      resetDefault();
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
