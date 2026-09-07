# 精讲截图存档目录

老师分配的学习任务与学生作业截图，由 Study Hub「知识点精讲」工具栏保存。

## 目录结构

```
snip/
  unit1/
    task/       # 老师分配的学习任务
    homework/   # 学生作业记录
  unit2/
    ...
```

## 命名规则

`Unit{N}-{Part}_{task|homework}_{YYYY-MM-DD}_{HH-MM-SS}.png`

索引文件：`data/study-hub/snip-index.json`

需通过 `启动.bat` 启动本地服务后，截图才会写入本目录。
