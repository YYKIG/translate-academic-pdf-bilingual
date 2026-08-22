# Academic PDF Bilingual Translation Skill

一个面向 Codex 的英文学术论文 PDF 翻译 Skill。它要求生成完整、经过学术润色的简体中文译文，并交付逐页对齐的中英对照 PDF：左侧为排版后的中文，右侧为视觉上保持不变的英文原页。

## 主要能力

- 翻译完整论文，而不是只生成摘要或节选。
- 中文译文经过忠实性复核和学术语言润色。
- 中英逐页左右并列：左中文、右英文。
- 右侧直接保留原始英文页面的版式、公式、图表和页码。
- 专业术语统一；存在英文缩写时，每次按 `中文术语（ABBR）` 呈现。
- 精确识别公式并从英文原页裁切，将公式原貌插入中文对应位置。
- 保留引用、图、表、标题、脚注、参考文献和附录。
- 检查 PDF 文本层、Unicode 复制顺序和英文连字，避免复制时出现字符粘连。
- 输出术语表、公式清单和质量检查报告，便于审计。

## 默认交付物

对于输入文件 `paper.pdf`，默认生成：

```text
paper-bilingual.pdf
paper-bilingual.html
paper-terminology.csv
paper-formula-manifest.json
paper-qa.json
```

原始 PDF 不会被覆盖。

## 安装

### 让 Codex 安装

在任意 Codex 对话中提出：

```text
请从 https://github.com/YYKIG/translate-academic-pdf-bilingual 安装这个 Skill，并设为全局/项目 Skill。
```

### 手动安装

将仓库复制到全局 Codex Skills 目录：

```text
$CODEX_HOME/skills/translate-academic-pdf-bilingual
```

Windows 默认通常对应：

```text
C:\Users\<用户名>\.codex\skills\translate-academic-pdf-bilingual
```

安装后重新打开 Codex 对话，确保 Skill 已被发现。

## 使用示例

把英文论文 PDF 提供给 Codex，然后提出：

```text
请使用 translate-academic-pdf-bilingual 翻译这篇论文。输出完整的左右并列中英对照 PDF：左侧中文、右侧英文原页；中文进行学术润色；专业术语保留英文缩写；公式使用原文精准截图。
```

## 工作流程

1. 检查 PDF 页数、页面尺寸、文本层、扫描页和多栏结构。
2. 重建正文阅读顺序，并建立段落、图表和公式的来源锚点。
3. 建立统一术语表，确定中文术语和英文缩写。
4. 按段落翻译、逐项忠实性复核，再进行学术中文润色。
5. 从原页精确裁切公式并插入中文对应位置。
6. 排版中文左栏，并将原始英文页面完整放入右栏。
7. 导出 PDF，检查完整性、页面配对、公式、文本复制和视觉排版。

具体约束和验收标准请参阅 [`SKILL.md`](SKILL.md) 以及 [`references/`](references/) 中的规范。

## 目录结构

```text
translate-academic-pdf-bilingual/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── bilingual-paper.css
├── references/
│   ├── chinese-typesetting.md
│   ├── formula-capture.md
│   ├── output-spec.md
│   ├── text-layer.md
│   └── translation-standard.md
└── scripts/
    └── validate_bilingual.py
```

## 重要说明

- 这是 Codex 工作流 Skill，不是独立桌面翻译软件。
- 翻译质量由所用 Codex 模型、原 PDF 质量、OCR 结果和可用 PDF 工具共同决定。
- 复杂公式的可见内容以原页裁切图像为准；只有在可靠时才叠加可搜索文本层。
- 对加密、损坏或无法可靠识别的论文，Skill 会报告问题，不会伪造缺失内容。

## License

[MIT](LICENSE)

