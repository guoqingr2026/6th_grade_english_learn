# 题库维护说明

> 完整说明见根目录 `FINAL_PRODUCT_MANUAL.md` 第四节。  
> 日常加题用网页右侧 **「题库导入 CSV」**；加题后记得点 **「同步数据」** 分享到手机。

## 傻瓜三步（推荐）

1. 网页点 **「下载模板 CSV」**（或复制本目录 `import-template.csv`）
2. Excel 填写，另存为 **UTF-8 CSV**
3. 网页点 **「选择文件并导入」** → 其他设备点 **「同步数据」**

## 表头（勿改列名）

```
type,id,unit,part,itemType,prompt,answer,clue,options,badge,explain,title,en,zh,fillPrompt
```

| type | 说明 |
|------|------|
| `quiz` | 选择题 |
| `fillblank` | 综合填空 |
| `writing` | 作文范文 |

- `options`：用 `|` 分隔四个选项
- 同一 `id` 再次导入会 **覆盖** 旧题
- `id` 建议：`u3-custom-01` 格式，全库唯一
- **`unit` 必填**：1–6 或 0（附录/综合）；便于筛选与错题本

## 附录补充包（OR 合并）

`data/practice/supplement.json` 在网页启动时与默认题库 **按 id 合并**，不替换整库。  
生成：`python scripts/build_practice_supplement.py`（附录2词汇、附录4表达、语法点等）。  
不规则动词固定 47 个：`data/practice/irregular-verbs.json`（不走 supplement 覆盖）。

## 默认题库

`quiz-bank.json` / `fillblank-bank.json` / `writing-bank.json` 为出厂默认题，随 `启动.bat` 加载。

## 高级方式

| 方式 | 步骤 |
|------|------|
| 题卡 JSON | 放入 `import-cards/` → 运行 `启动.bat` |
| 改 JSON | 直接编辑 `*-bank.json` |
| 改 Markdown | 编辑 `.md` 文末 `bank-json` 块 → `启动.bat` |

## AI 生成 CSV（复制给 AI）

```
你是 PEP 六年级英语上册命题老师。按下列 CSV 表头输出，每行一题，只输出 CSV（含表头），不要 Markdown：

type,id,unit,part,itemType,prompt,answer,clue,options,badge,explain,title,en,zh,fillPrompt

要求：Unit {1-6}；选择题/填空/作文各 {数量}；主题 {主题}。
id 格式 u{单元}-custom-01 递增。选择题 options 用|分隔4项，answer 与 options 之一完全一致。
填空 prompt 含___，answer 英文，clue 中文与 prompt 一致。作文需 en/zh/fillPrompt/fillAnswer。
```

## AI 生成题卡 JSON（复制给 AI）

```
生成 PEP 六年级英语题卡 JSON，结构：
{"cardType":"quiz|fillblank|writing","action":"append","source":"...","items":[...]}
参考：import-cards/_templates/ 下示例。Unit {单元}，{题量}题，{主题}。items 每题 id 唯一。只输出合法 JSON。
```

## 审核 checklist

- [ ] 每题 `id` 唯一
- [ ] 填空：`___` ↔ `answer`，`clue` 语义一致
- [ ] 选择题：`answer` ∈ `options`
- [ ] 导入后标签数字增加
- [ ] 多设备已点「同步数据」
