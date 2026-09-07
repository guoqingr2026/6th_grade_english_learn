# 课本扫描图目录

将 PEP 六年级上册课本页面图片放在此目录，例如：

- unit1-part-a.jpg
- unit1-part-b.jpg
- unit2-part-a.jpg

在 `data/study-hub/reading-bank.json` 或 `knowledge-bank.json` 中设置：

```json
"image": "assets/images/textbook/unit1-part-a.jpg",
"fallbackImage": "assets/images/unit1-travel.svg"
```

若 `image` 不存在，自动显示 `fallbackImage`。
