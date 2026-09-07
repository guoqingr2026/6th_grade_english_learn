# 课本配图目录

## 方式一：从 PDF 提取（推荐，与教材一致）

1. 将 PEP 六年级上册 PDF 放在项目根目录（文件名含 `pep` 或 `六上`）
2. 运行：`python scripts/extract-textbook-pdf.py`
3. 运行：`python scripts/build-study-hub.py`

输出目录：`assets/images/textbook/pages/page-XXX.png`

## 方式二：手机/扫描 JPG 批量转 PNG（Unit 1）

将课本拍照文件放入 `pages/` 目录，命名规则：
- `page-009.png.JPG`、`page-010.png.JPG` … 或
- 按拍摄顺序 `IMG_3386.PNG.JPG` … 自动映射为 `page-011.png` 起

运行：

```bat
python scripts/convert_u1_page_images.py
```

脚本会：JPG→PNG、按页码重命名、备份旧图、同步到 `release/assets/.../pages/`。

## 配置

在 `data/study-hub/reading-bank.json` 中：

```json
"image": "assets/images/textbook/pages/page-011.png",
"fallbackImage": "assets/images/unit1-travel.svg"
```

若 `image` 文件不存在，自动显示 `fallbackImage`。
