# 课文讲读 & 知识点精讲 内容库 v2

## 四部分结构

每个单元固定 **4 页**：

| Part | 说明 |
|------|------|
| Part A | 核心对话 |
| Part B | 拓展语篇 |
| Part C | 语法发现 + 挑战 |
| Reading 阅读 | 阅读篇目（分句中英对照） |

## 从 PDF 生成课本 PNG（推荐）

1. 将 `2026秋pep人教版六上英语修订版(1).pdf` 放在项目根目录
2. 安装依赖：`python -m pip install pymupdf`
3. 运行：`python scripts/extract-textbook-pdf.py`  
   → 输出 `assets/images/textbook/pages/page-001.png` …
4. 编辑 `pdf-page-map.json` 映射单元与 PDF 页码
5. 运行：`python scripts/build-study-hub.py`

或直接双击 **`启动.bat`**（自动执行 3–5 步）。

## 网页功能

- **PPT 16:9 全屏**弹窗，左课本图右内容
- 讲读：**一句英文 + 一句中文**，附录词/短语 **黄色高亮**
- 精讲：特级教师指引模板 + 表格/LaTeX/链接
- **朗读（重要）**：仅点击工具栏 **「朗读」** 后，TTS 在本页内 **逐句向下** 播放；再点变为「停止」。**不会**自动翻 Part，也**不会**进入练习下一题
- **无自动朗读**：打开讲读/精讲不会自动读；练习区（单词/语法/选择题等）一律不自动朗读、不自动跳题
- **导出精讲 / 导入精讲** JSON（知识点精讲工具栏）
- **视频链接**可编辑保存（B站/YouTube 等）
- **交互笔记**本机保存

## 文件

| 文件 | 用途 |
|------|------|
| `reading-bank.json` | 讲读句子 `sentences: [{en, zh}]` |
| `knowledge-bank.json` | 精讲 `bodyHtml` + `videoUrl` |
| `glossary.json` | 高亮词表（自动生成） |
| `pdf-page-map.json` | PDF 页码映射 |

## AI 精讲提示词（用户原版）

```
你作为具有200年教学经验的资深特级小学六年级英语老师，请将这个图片翻译成中文(要求严格对应，准确翻译成中文，六年级孩子可以正确理解的），并一步步开展教育指导，识别图片中对六年级孩子全新的知识点，知识点重点在新知识点讲解并举一反三适当做拓展讲述，通过学习，能让六年级的孩子深刻的掌握和灵活使用英语，能听说读写练应用。同时也要让孩子学会有趣，印象深刻的单词和语法，短语的记忆，活学活用。要讲究适合孩子容易理解的教育教学方法。歌曲和记忆宫殿的方法以及抽象形象或者讲故事均可。现在开始完成任务，课本图片见左侧图片，按照一次一个部分比如part A, Part B来精讲
```

将 AI 输出 HTML 写入 `knowledge-bank.json` 的 `bodyHtml`，或导出 JSON 修改后 **导入精讲**。

## 导入精讲 JSON 格式

```json
{
  "version": 2,
  "title": "知识点精讲（自定义）",
  "units": [
    {
      "unit": 1,
      "pages": [
        {
          "id": "u1-k-part-a",
          "bodyHtml": "<h3>...</h3>",
          "videoUrl": "https://www.bilibili.com/video/BV..."
        }
      ]
    }
  ]
}
```

按 `id` 覆盖默认精讲页。
