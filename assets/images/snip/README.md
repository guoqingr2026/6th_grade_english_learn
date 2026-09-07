# 精讲截图存档目录

老师分配的学习任务与学生作业截图，由 Study Hub「知识点精讲」工具栏保存。

## 目录结构

```
snip/
  unit1/
    part-a/
      task/       # 本 Part 作业布置（最多 4 张）
      homework/   # 本 Part 作业提交（最多 4 张）
    part-b/
      ...
```

## 命名规则

`Unit{N}-{part}_{task|homework}_{YYYY-MM-DD}_{HH-MM-SS}.png`

例如：`Unit1-part-a_homework_2026-09-07_20-15-30.png`

每条记录绑定 `pageId`（如 `u1-k-part-a`），切换 Part 后显示对应空白格。

索引文件：`data/study-hub/snip-index.json`

需通过 `启动.bat` 启动本地服务后，截图才会写入本目录。
