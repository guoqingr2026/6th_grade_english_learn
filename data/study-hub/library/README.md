# Study Hub HTML 文档库



讲读与精讲内容以 HTML 文件存储，一次编辑永久生效。



## 目录



- `reading/u{N}-p{NNN}.html` — 讲读，按图册页码（如 `u3-p037.html` = page-037.png）

- `knowledge/{pageId}.html` — 精讲（如 `u1-k-part-a.html`）



## 显示页码



界面显示 **Page 30**（课本印刷页）= 图册页码 − `printPageOffset`（默认 7）。  

例：`page-037.png` → **Page 30**



## 数据来源优先级



1. 本目录 HTML 文件（已编辑 / CSV 导入）

2. `reading-bank.json` / `knowledge-bank.json` 内置默认内容



## CSV 导入



`page` 列填**课本印刷页码**（全局），如 `30` 对应 `page-037.png`。  

通过讲读页 **导入 CSV** 或 `scripts/import-csv-to-library.py` 写入本目录。



### Emoji 与特殊符号（✅ 支持）



CSV、HTML、JSON 全程 **UTF-8**，以下字符可正常使用，**不会**破坏生成结果：



| 类型 | 示例 |

|------|------|

| Emoji | 😢 😂 ✅ 🎧 📌 ⭐ ✉️ |

| 中文标点/方框 | 【】※ ├─ └─ │ ➜ ✗ ✓ |



**原理**：写入 HTML 时仅转义 `<` `>` `&` `"` 四个字符；Emoji 与【】等原样保留。JSON 使用 `ensure_ascii=False`，不转成 `\uXXXX`。



**CSV 注意**：

- 用 **UTF-8** 保存（Excel 选「CSV UTF-8」）

- 含逗号的单元格用双引号包住：`30,"A, B, C",选项`

- 双引号本身写成两个：`30,"He said ""Hi""",他说「嗨」`



**示例行**：



```csv

page,en,zh

32,😢 Liu Jia was crying.,刘佳在哭泣。

32,【Mind Map】,【思维导图】

32,├─ Eat healthy food,├─ 吃健康的食物

32,⭐ Jump rope every day.,⭐ 每天跳绳。

```


