# Release 发布包说明

本目录为**可直接分发**的运行包（ZIP 压缩整个文件夹即可）。

## 必含文件

```
release/
├── index.html / app.js / styles.css
├── 启动.bat                    # 含题库同步 + 局域网数据同步
├── 使用说明.txt
├── FINAL_PRODUCT_MANUAL.md     # 完整产品说明书
├── PARENT_GUIDE.md             # 家长指南
├── data/question-banks/        # 默认题库 + 导入模板
├── scripts/
│   ├── lan_server.py           # 局域网同步服务 ★
│   ├── import-question-cards.py
│   └── sync-question-banks.py
└── assets/images/
```

运行时自动生成：`lan-sync/`（同步数据，按昵称存储）

## 维护者：同步最新代码

在项目根目录双击：

```
sync-release.bat
```

## 发布前检查

- [ ] `启动.bat` 可打开 localhost:8080
- [ ] 手机同 WiFi 可访问
- [ ] 昵称 +「同步数据」可 PC/手机对齐
- [ ] 题库标签数字正常
- [ ] 动词专项显示 **附录5 不规则动词 47/47**
- [ ] 讲读/精讲仅「朗读」链式 TTS；练习区无自动朗读/跳题

详见 `FINAL_PRODUCT_MANUAL.md` 第六节「发布检查清单」。

## 公网部署

静态托管见根目录 `DEPLOY.md`。**注意：公网版无局域网同步 API**，多设备需各自练习或仅用局域网包。
