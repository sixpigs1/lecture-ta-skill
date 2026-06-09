---
name: lecture-ta
description: Create clear Chinese teaching-oriented HTML study notes from course slide PDFs while preserving important English concepts and technical terms. Use when the user provides lecture slides, class PDFs, or slide decks from electronics, computer engineering, hardware, circuits, embedded systems, computer architecture, machine learning, reinforcement learning, artificial intelligence, algorithms, mathematics, or related courses and asks Codex to read them, explain the lecture like a teaching assistant, extract important visual assets, and generate an .html learning note under an output directory.
---

# Lecture TA

Use this skill when a user provides a course slides PDF and asks for an HTML teaching note. The goal is not to summarize slides mechanically. The goal is to teach the lecture clearly, like a TA preparing a readable study note for a student who wants to understand the class.

Write the teaching note in Chinese by default. Keep important concepts, algorithms, methods, formulas, theorem names, hardware components, signals, and discipline-specific terms in English, optionally followed by a short Chinese explanation. For example: `memory-mapped I/O（内存映射输入输出）`, `policy gradient（策略梯度）`, `eigenvalue（特征值）`, `Kirchhoff's Current Law (KCL)`.

## Output Contract

Generate a `.html` file, usually `outputs/<lecture_name>/index.html`.

If the slides contain important charts, diagrams, flowcharts, circuit figures, architecture drawings, timing diagrams, tables, or formula screenshots, extract or render them into:

```text
outputs/<lecture_name>/assets/
```

The final HTML must reference necessary images with relative paths such as `assets/page_003.png` and include helpful captions.

## Teaching Principles

Follow these principles:

1. Identify the lecture topic first.
2. Build a concise knowledge map that explains relationships between concepts, not just a list of topics.
3. Organize the note by concepts and themes, not by slide number.
4. Put each key image directly next to the explanation that uses it.
5. Explain complex ideas with intuition before formal details.
6. For formulas, explain each variable, the meaning of the formula, and when the formula is used.
7. For theorems or formal claims, explain assumptions, conclusion, significance, and at least one concrete example.
8. Add a compact concept glossary for important ports, signals, components, algorithms, theorem names, and terms appearing in the slides.
9. Use slide page references only when useful for traceability.
10. Avoid page-by-page retelling and avoid bullet-point-only summaries.
11. Do not generate homework or after-class exercises unless the user explicitly asks.

## Required HTML Structure

Use Chinese section titles by default. Include:

- 课程标题
- 主题概览
- 知识地图
- 核心概念速查
- 分主题讲解
- 复杂概念详解
- 关键公式 / 定理解释
- 理论证明（only when useful for math, AI, algorithms, or theoretical slides）
- 必要图片与图注, placed beside the relevant explanation rather than isolated at the end
- 本节课核心 takeaway

## Image and Formula Placement

Choose image usage by course type:

The default rule is 图文绑定讲解: place a figure immediately before or after the paragraph that explains it, then explain what the reader should observe in that figure.

- Hardware, circuits, embedded systems, and computer architecture: images are often central. Place block diagrams, circuit diagrams, timing diagrams, datapaths, register maps, pin diagrams, and interface diagrams inside the exact subsection that explains them. After each image, explain the visible components, signal flow, interfaces, assumptions, and why the diagram matters.
- Mathematics: use images only when the slide has an essential geometric diagram, graph, or visual proof. Prefer direct transcription and explanation of definitions, formulas, theorem statements, and proof steps.
- Machine learning, reinforcement learning, AI, and algorithms: use images when they clarify an architecture, pipeline, algorithm flow, state transition, graph, or experimental result. For theorem-heavy material, put formulas and proof ideas in text instead of screenshotting every formula slide.

Do not create a detached image gallery. If an image is included, the surrounding text must tell the reader what to look at.

## Formula and LaTeX Rendering Rules

All formulas, theorem statements with mathematical symbols, and formula-like expressions must be written in LaTeX so the HTML can render them with MathJax.

- Use inline math delimiters for short symbols and expressions: `\(x\)`, `\(V^\pi(s)\)`, `\(\gamma\)`, `\(O(n \log n)\)`.
- Use display math delimiters for standalone formulas:

```latex
\[
V^\pi(s)=\mathbb{E}_\pi\left[R_{t+1}+\gamma V^\pi(S_{t+1})\mid S_t=s\right]
\]
```

- Do not write mathematical formulas as plain text such as `V^pi(s) = E[...]` when LaTeX is possible.
- Transcribe formulas from slides into LaTeX whenever possible. Use formula screenshots only when the visual layout itself is important or the formula cannot be reliably transcribed.
- Explain every important symbol after the formula in Chinese, while preserving English names for standard terms.
- Use LaTeX for hardware and circuit formulas too, such as `\(V=IR\)`, `\(P=VI\)`, `\(f_{clk}=1/T\)`, and `\(\tau=RC\)`.
- Use code formatting only for actual code identifiers, register names, bit names, or literal programming expressions. If the expression is mathematical, use LaTeX.

The bundled HTML template loads MathJax, so `\( ... \)` and `\[ ... \]` should render normally in the browser.

## Knowledge Map Requirements

The knowledge map should be short, clear, and relational. It should answer:

- What is the main object studied in this lecture?
- Which prerequisites feed into it?
- Which subtopics depend on which earlier concepts?
- What is the input-output or cause-effect relationship?
- What is the final goal of the lecture?

Use a compact bullet chain, a small table, or a simple Mermaid diagram when it clarifies the structure. Do not make this section long.

Example:

```mermaid
flowchart LR
  A["Register / Memory Map"] --> B["Bit Mask Operations"]
  B --> C["Peripheral Configuration"]
  C --> D["Interrupt-Driven I/O"]
```

## Concept Glossary

Create a short "核心概念速查" section when the slides introduce many named items. Keep entries brief:

- Hardware: ports, pins, buses, registers, flags, peripherals, modules, clock domains, interfaces.
- Circuits: nodes, branches, operating regions, equivalent models, gain, impedance, poles/zeros.
- AI/ML/RL/Algorithms: objective, loss, state, action, policy, value, gradient, complexity, approximation, convergence.
- Math: definitions, theorem names, assumptions, standard symbols, spaces, mappings, operators.

Each entry should include the English term and a concise Chinese explanation.

## Subject-Specific Templates

Adapt the note structure to the course domain.

### Hardware, Embedded Systems, Computer Architecture, and Circuits

Prefer this structure:

1. 主题概览
2. 知识地图
3. 核心概念速查
4. 结构图 / 电路图 / 时序图讲解
5. 分主题硬件分析
6. 关键公式、寄存器、接口或 timing 解释
7. 设计取舍与常见误区
8. 本节课核心 takeaway

Emphasize hardware behavior and analysis:

- Explain the physical or architectural object first: circuit block, register, bus, memory hierarchy, processor datapath, peripheral, timing path, or I/O interface.
- For each key figure, explain components, ports, interfaces, signal direction, data/control flow, and what changes over time.
- For circuits, analyze current, voltage, impedance, operating region, small-signal behavior, timing, power, noise margin, and assumptions behind equivalent models.
- For digital hardware and computer architecture, explain datapath, control path, instruction flow, pipeline hazards, memory access, timing constraints, and tradeoffs.
- For embedded systems, connect code-level operations to hardware effects: registers, interrupts, timers, GPIO, ADC/DAC, communication buses, scheduling, latency, and resource limits.

### Machine Learning, Reinforcement Learning, AI, and Algorithms

Prefer this structure:

1. 主题概览
2. 知识地图
3. 核心概念速查
4. 方法主线
5. 数学基础与关键定理
6. Algorithm / model / training procedure
7. 理论证明或推导（separate from the main line when long）
8. 适用场景、限制和 takeaway

Emphasize theory, mathematical foundations, and methods:

- Identify the learning or algorithmic problem: supervised learning, unsupervised learning, reinforcement learning, planning, inference, optimization, graph algorithm, dynamic programming, or representation learning.
- Explain objectives, loss functions, assumptions, training or algorithm procedure, evaluation metrics, and complexity where relevant.
- For reinforcement learning, clarify state, action, reward, policy, value function, Bellman equation, exploration-exploitation, Markov Decision Process (MDP), and convergence assumptions.
- Put long proofs, derivations, or convergence arguments in a separate "理论证明 / 推导" section so the main explanation remains readable.

### Mathematics

Prefer this structure:

1. 主题概览
2. 知识地图
3. 核心概念速查
4. Definitions and intuition
5. Theorems
6. Proof ideas and proof details
7. Examples and counterexamples
8. 本节课核心 takeaway

Emphasize concepts, definitions, theorems, proof ideas, and examples:

- Start from definitions and explain why each condition exists.
- For theorems, state assumptions, conclusion, meaning, and a simple example or counterexample when useful.
- For proofs, explain the proof strategy before technical steps.
- For formulas, explain symbols, domains, dimensions, and the situation where the formula applies.
- Preserve precise English names for standard concepts, such as `linear independence`, `eigenvalue`, `gradient`, `convexity`, `Fourier transform`, and `Bayes' theorem`.

## Workflow

1. Inspect the PDF title, filename, slide headings, repeated terms, diagrams, formulas, theorem statements, and examples.
2. Determine the lecture title, domain type, and main conceptual goal.
3. Extract useful visual assets:
   - Prefer the skill-local venv Python to run `scripts/extract_pdf_assets.py`.
   - On Windows, the expected path is `%USERPROFILE%\.codex\skills\lecture-ta\.venv\Scripts\python.exe` after setup.
   - If only a region of a page is important, crop or screenshot that region when tools permit.
   - Keep images that support explanation; do not render every slide into the note unless the user asks.
4. Read the slide content and infer:
   - Main theme
   - Prerequisites and background
   - Subtopics and dependencies
   - Cause-effect, input-output, or proof relationships
   - Equations, definitions, theorems, algorithms, diagrams, and examples
5. Write the HTML note:
   - Use `templates/lecture_note_template.html` as the style and layout baseline.
   - Use `scripts/build_html.py` when a structured generation helper is useful.
   - Include a left-side table of contents with anchor links to major sections.
   - Keep a clean academic style with readable Chinese prose and English technical terms.
6. Verify that:
   - `index.html` exists.
   - Referenced images exist under `assets/`.
   - Each key image appears next to the explanation that depends on it.
   - Links in the table of contents point to section ids.
   - The knowledge map explains relationships rather than merely listing topics.
   - The note teaches concepts rather than merely listing slides.

## Language and Terminology Rules

- Use Chinese prose for explanations, transitions, captions, and takeaways.
- Preserve English for key technical nouns and method names.
- When a term first appears, prefer `English term（中文解释）`.
- Do not translate code identifiers, register names, signal names, theorem names, or standard acronyms.
- Keep formulas exactly readable; do not rewrite mathematical notation into vague prose.
- Avoid English-only notes unless the user explicitly requests English.

## Bundled Resources

- `templates/lecture_note_template.html`: standalone academic HTML template with responsive layout and a left-side table of contents.
- `scripts/extract_pdf_assets.py`: render PDF pages to PNG images with PyMuPDF (`fitz`) when available.
- `scripts/build_html.py`: reusable HTML builder for creating `index.html` from structured sections, images, formulas, proofs, concept glossaries, and prose.
- `examples/example_output.html`: examples for hardware, AI/algorithm, and mathematics lecture-note styles.
- `.venv/`: optional local Python virtual environment for running bundled scripts reliably. Do not commit this directory; recreate it from `requirements.txt`.

## Practical Notes

Use relative paths from `index.html` to assets. For example, if the generated note is at `outputs/lecture03/index.html`, reference an image as:

```html
<img src="assets/page_004.png" alt="Diagram from lecture slide 4">
```

Use the skill-local Python environment when running the bundled tools:

```powershell
& "$env:USERPROFILE\.codex\skills\lecture-ta\.venv\Scripts\python.exe" "$env:USERPROFILE\.codex\skills\lecture-ta\scripts\extract_pdf_assets.py" ".\slides\lecture03.pdf" --lecture-name lecture03 --output-root ".\outputs"
```

The skill-local venv currently uses Python 3.12 and includes:

- `pymupdf` / `fitz` for PDF rendering
- Python standard library modules used by `build_html.py`

If the venv is missing or broken, recreate it with:

```powershell
cd "$env:USERPROFILE\.codex\skills\lecture-ta"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If package download fails because of networking, retry with the user's local proxy:

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

When PyMuPDF is unavailable, tell the user that asset rendering needs the skill-local venv to be repaired, then proceed with text-only HTML if enough slide text is available.

## Calling This Skill From Other Folders

This skill has been designed for global installation. Put or keep the folder at:

```text
C:\Users\<your-user>\.codex\skills\lecture-ta
```

After it is available globally, start Codex in any course folder and ask:

```text
Use the lecture-ta skill to read ./slides/lecture03.pdf and generate an HTML teaching note under ./outputs/lecture03/.
```
