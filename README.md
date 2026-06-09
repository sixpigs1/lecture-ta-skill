# lecture-ta Codex Skill

`lecture-ta` 是一个用于阅读课程 slides PDF 并生成中文 HTML 学习笔记的 Codex Skill。它的目标不是简单总结 slides，而是像助教一样把一节课讲清楚：先整理知识结构，再按主题解释概念、公式、图表、定理和核心 takeaway。

## 适合的课程类型

- 硬件类课程：嵌入式系统、计算机组成、数字系统、电子电路等
- AI / ML / RL / 算法类课程：机器学习、强化学习、人工智能、算法分析等
- 数学类课程：线性代数、概率论、优化、信号与系统、数学基础课程等

输出默认使用中文讲解，同时保留关键英文术语，例如 `memory-mapped I/O`、`policy gradient`、`eigenvalue`、`KCL`。

## 功能特点

- 读取课程 slides PDF，生成结构化 HTML 学习笔记
- 自动将 PDF 页面渲染为图片资产，保存到 `outputs/<lecture_name>/assets/`
- 对硬件类课程强调图文绑定讲解，把结构图、电路图、时序图放在对应解释旁边
- 对数学、AI、算法类课程使用 LaTeX 公式，并通过 MathJax 在网页中渲染
- 支持知识地图、核心概念速查、分主题讲解、公式/定理解释、理论证明和核心 takeaway
- 不依赖复杂前端框架，生成的 HTML 可以直接用浏览器打开

## 目录结构

```text
lecture-ta/
├── SKILL.md
├── README.md
├── requirements.txt
├── templates/
│   └── lecture_note_template.html
├── scripts/
│   ├── extract_pdf_assets.py
│   └── build_html.py
└── examples/
    └── example_output.html
```

## 安装到 Codex

将本仓库克隆到你的 Codex skills 目录：

```powershell
git clone git@github.com:sixpigs1/lecture-ta-skill.git "$env:USERPROFILE\.codex\skills\lecture-ta"
```

如果你使用 HTTPS：

```powershell
git clone https://github.com/sixpigs1/lecture-ta-skill.git "$env:USERPROFILE\.codex\skills\lecture-ta"
```

安装完成后，重新打开 Codex 或开启一个新的 Codex 线程，让 Skill 被重新发现。

## Python 环境

建议为这个 Skill 建立独立 venv，避免依赖系统 Python 或 Anaconda 环境。

```powershell
cd "$env:USERPROFILE\.codex\skills\lecture-ta"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

如果你的电脑上 `python` 命令不可用，可以换成你本机可用的 Python 路径，例如：

```powershell
& "D:\Program Files\anaconda\python.exe" -m venv .venv
```

如果下载依赖时网络不通，可以先设置代理：

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

依赖安装完成后，可以检查 PyMuPDF 是否可用：

```powershell
.\.venv\Scripts\python.exe -c "import fitz; print(fitz.__doc__.splitlines()[0])"
```

## 使用方式

在任意课程文件夹中启动 Codex，然后输入类似请求：

```text
Use the lecture-ta skill to read ./slides/lecture03.pdf and generate an HTML teaching note under ./outputs/lecture03/.
```

如果 Codex 没有自动识别 Skill，可以写得更明确：

```text
Use the lecture-ta skill from C:\Users\<your-user>\.codex\skills\lecture-ta to read ./slides/lecture03.pdf and generate an HTML teaching note under ./outputs/lecture03/.
```

生成结果通常包括：

```text
outputs/lecture03/
├── index.html
└── assets/
    ├── page_001.png
    ├── page_002.png
    └── ...
```

打开 `index.html` 即可阅读笔记。

## 手动运行工具

渲染 PDF 页面为图片：

```powershell
& "$env:USERPROFILE\.codex\skills\lecture-ta\.venv\Scripts\python.exe" `
  "$env:USERPROFILE\.codex\skills\lecture-ta\scripts\extract_pdf_assets.py" `
  ".\slides\lecture03.pdf" `
  --lecture-name lecture03 `
  --output-root ".\outputs"
```

使用结构化 JSON 生成 HTML：

```powershell
& "$env:USERPROFILE\.codex\skills\lecture-ta\.venv\Scripts\python.exe" `
  "$env:USERPROFILE\.codex\skills\lecture-ta\scripts\build_html.py" `
  ".\note.json" `
  --template "$env:USERPROFILE\.codex\skills\lecture-ta\templates\lecture_note_template.html" `
  --output ".\outputs\lecture03\index.html"
```

## 公式渲染

生成的 HTML 模板使用 MathJax 渲染 LaTeX：

- 行内公式：`\(V^\pi(s)\)`
- 独立公式：

```latex
\[
V^\pi(s)=\mathbb{E}_\pi\left[R_{t+1}+\gamma V^\pi(S_{t+1})\mid S_t=s\right]
\]
```

注意：MathJax 默认从 CDN 加载。如果离线打开 HTML，公式可能无法渲染。

## 常见问题

### Codex 没有识别这个 Skill

确认仓库路径是：

```text
C:\Users\<your-user>\.codex\skills\lecture-ta
```

然后重新打开 Codex 或新建线程。

### `fitz` 找不到

说明当前 Python 环境没有安装 PyMuPDF。进入 Skill 目录并重新安装依赖：

```powershell
cd "$env:USERPROFILE\.codex\skills\lecture-ta"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### HTML 中公式不渲染

检查网络是否可以访问 MathJax CDN，或者确认公式是否使用了 `\( ... \)` / `\[ ... \]` 语法。

### 图片太多或太少

这个 Skill 会优先保留对讲解有帮助的图片。硬件课程通常需要更多结构图、示意图和时序图；数学课程通常更适合转写公式和证明，而不是大量截图。

