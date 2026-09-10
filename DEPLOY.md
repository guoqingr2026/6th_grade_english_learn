# 部署与发布指南

## 公网免费发布（推荐：GitHub Pages）

本项目是纯静态网页（HTML + JS + JSON），**不需要服务器、不需要域名、不需要付费**，适合用免费静态托管。

### 你能得到什么

- 一个公网网址，例如：`https://你的用户名.github.io/english-learn/`
- 手机、平板、任何地方的浏览器都能打开
- 学习数据仍在各自浏览器 `localStorage` 里（不会混用）
- **公网版没有「同步数据」功能**；PC/手机对齐请用 `启动.bat` 局域网模式（见 `FINAL_PRODUCT_MANUAL.md` 第三节）

### 一步步操作（约 10 分钟）

#### 1. 注册 GitHub（免费）

打开 [https://github.com](https://github.com) 注册账号。

#### 2. 新建仓库

- 点 **New repository**
- 名称示例：`english-learn`（英文、无空格）
- 选 **Public**（公开仓库 Pages 完全免费）
- 创建仓库

#### 3. 上传项目代码

在项目文件夹打开终端（PowerShell），执行：

```bash
cd "C:\Users\guoqren\.cursor\englishi learn"
git init
git add .
git commit -m "Initial commit: PEP Grade 6 English Trainer"
git branch -M main
git remote add origin https://github.com/你的用户名/english-learn.git
git push -u origin main
```

（若未安装 Git，可先安装 [Git for Windows](https://git-scm.com/download/win)）

#### 4. 开启 GitHub Pages

1. 打开仓库 → **Settings** → **Pages**
2. **Build and deployment**：
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** → **/ (root)** → Save

> 首次 push 到 `main` 后，Actions 会自动创建 `gh-pages` 分支。若还没有，等 1～2 分钟再选。

#### 5. 等待自动部署

- 打开仓库 **Actions** 标签
- 看到 **Deploy to GitHub Pages** 绿色勾即成功
- 访问：`https://你的用户名.github.io/english-learn/`

也可手动触发：**Actions** → **Deploy to GitHub Pages** → **Run workflow**

#### 6. 以后更新

改完代码后：

```bash
git add .
git commit -m "更新说明"
git push
```

几分钟内公网站点自动更新。

---

## 其他免费公网方案（可选）

| 平台 | 费用 | 特点 |
|------|------|------|
| [GitHub Pages](https://pages.github.com) | 免费 | 本项目已配置，最推荐 |
| [Cloudflare Pages](https://pages.cloudflare.com) | 免费 | 国内外访问较快，需注册 Cloudflare |
| [Netlify](https://www.netlify.com) | 免费额度 | 拖拽 `release` 文件夹即可部署 |
| [Vercel](https://vercel.com) | 免费额度 | 适合静态站，连接 GitHub 自动部署 |

**国内访问提示：** GitHub Pages 在国内有时较慢或不稳定；**面向中国学生，更推荐阿里云 OSS 或腾讯云 COS 静态网站托管**（见下文），或教室继续用 **局域网 `启动.bat`**（零费用）。

---

## 国内公网发布（推荐：阿里云 / 腾讯云）

### 能不能实现和 GitHub Pages 类似的效果？

**可以。** 本项目是纯静态站，上传到对象存储并开启「静态网站托管」后：

- 得到一个 **公网链接**，学生手机/电脑都能打开  
- 功能与本地一致：做题、积分、错题本、CSV 导入题库  
- 学习数据仍在 **各自浏览器** 里，不上传云端  

与 GitHub Pages 的区别主要是：**国内访问更快、更稳定**，但通常不是「永久 0 元」，而是 **按量极低费用**（流量很小时往往每月几元钱以内；新用户常有免费试用额度）。

### 费用大致概念（供参考）

| 方式 | 典型费用 | 国内访问 |
|------|----------|----------|
| 教室 `启动.bat` 局域网 | **0 元** | 仅同一 WiFi |
| GitHub Pages | **0 元** | 可能慢 |
| 阿里云 OSS 静态托管 | 存储+流量，低访问量很便宜 | **快** |
| 腾讯云 COS 静态托管 | 同上 | **快** |
| 买云服务器 ECS 常开 | 几十元/月起 | 快（对本项目 **不必**） |

> 不需要买 ECS 服务器跑 Python；只需 **对象存储 + 静态网站**，把 `release/` 里的文件传上去即可。

### 发布前要准备的文件

1. 在项目根目录运行 **`sync-release.bat`**（生成最新 `release/`）
2. 上传 **`release/` 整个目录** 的内容（含 `index.html`、`app.js`、`data/`、`assets/` 等）

---

### 方案 A：阿里云 OSS 静态网站托管

#### 1. 注册与开通

1. 打开 [阿里云](https://www.aliyun.com) 注册（可领新用户试用券）
2. 控制台搜索 **对象存储 OSS** → 开通
3. **创建 Bucket**：
   - 地域：选离学生近的（如「华东1-杭州」）
   - 读写权限：**公共读**（静态网站需要）
   - 版本控制：关即可

#### 2. 开启静态网站

1. 进入该 Bucket → **基础设置** → **静态页面**
2. 默认首页：`index.html`
3. 默认 404 页：可填 `index.html`（单页应用友好）
4. 记下 **静态网站访问地址**（形如 `http://xxx.oss-cn-hangzhou.aliyuncs.com`）

#### 3. 上传文件

控制台 → Bucket → **文件管理** → **上传文件**：

- 上传 `release/` 下所有文件和文件夹（保持目录结构）
- 尤其要有：`data/question-banks/*.json`、`assets/images/*`

或使用 [ossbrowser](https://help.aliyun.com/zh/oss/developer-reference/ossbrowser-2-0-overview/) 图形工具批量上传。

#### 4. 发给学生

把 **静态网站访问地址** 发到班级群即可。  
若需 **自己的域名**（如 `english.school.com`），要在阿里云绑定域名，且 **在中国大陆通常需 ICP 备案**；仅用 OSS 默认域名做班级链接，一般 **无需备案**。

#### 5. 更新题库/程序

改代码 → 运行 `sync-release.bat` → 在 OSS 控制台 **覆盖上传** 变更的文件。

---

### 方案 B：腾讯云 COS 静态网站托管

#### 1. 注册与开通

1. 打开 [腾讯云](https://cloud.tencent.com) 注册
2. 控制台 → **对象存储 COS** → 创建存储桶
3. 访问权限：**公有读私有写**
4. 地域：选就近（如「广州」）

#### 2. 开启静态网站

1. 存储桶 → **基础配置** → **静态网站**
2. 索引文档：`index.html`
3. 错误文档：可填 `index.html`
4. 复制 **静态网站访问节点**（形如 `https://bucket-xx.cos-website.ap-guangzhou.myqcloud.com`）

#### 3. 上传与分发

- 控制台 **文件列表** 上传 `release/` 全部内容  
- 或使用 [COSBrowser](https://cloud.tencent.com/document/product/436/11366)  

#### 4. 更新

同阿里云：本地 `sync-release.bat` 后重新上传变更文件。

---

### 方案 C：腾讯云 CloudBase 静态托管（有免费额度）

适合想 **连 Git 自动部署** 的用户：

1. 控制台 → **云开发 CloudBase** → 开通环境  
2. **静态网站托管** → 上传 `release/` 或关联代码仓库  
3. 获得 `xxx.tcloudbaseapp.com` 类域名  

新用户常有免费套餐，具体以控制台为准。

---

### 国内部署注意事项

| 项目 | 说明 |
|------|------|
| **备案** | 用 **自定义域名** 在国内访问，通常要 ICP 备案；用云厂商提供的 **默认测试域名** 一般不用备案 |
| **HTTPS** | 默认 OSS/COS 域名多为 HTTP；要 HTTPS 可绑自定义域名并配置证书 |
| **隐私** | 积分、昵称、错题本在浏览器本地，不会进你的云存储 |
| **题库 CSV 导入** | 在网页操作，导入内容存在用户本机，与 GitHub 方案相同 |
| **教室上课** | 仍建议用 `启动.bat` 局域网，最快、0 元 |

### 国内方案怎么选（简表）

| 你的情况 | 建议 |
|----------|------|
| 只要班里用、有 WiFi | `启动.bat` 局域网 |
| 学生回家也要用、在国内 | **腾讯云 COS** 或 **阿里云 OSS** |
| 完全不想花钱、能忍受偶尔慢 | GitHub Pages |
| 想要自动发布 | GitHub Actions 或 CloudBase |

---

## 公网 vs 局域网 怎么选

| 场景 | 推荐方式 |
|------|----------|
| 全班在教室同一 WiFi | `启动.bat` 局域网 |
| 学生回家练习（国内） | **阿里云 OSS / 腾讯云 COS** |
| 学生回家练习（可访问 GitHub） | GitHub Pages |
| 无网络时 | 拷贝 `release` 文件夹 + `启动.bat` |

---

## 一、本地 Windows 一键启动

双击根目录或 `release/` 目录下的：

```
启动.bat
```

浏览器访问：`http://localhost:8080`

---

## 二、打包给其他电脑

### 方式 A：直接拷贝 release 文件夹

1. 先运行根目录 `sync-release.bat`（确保 release 为最新）
2. 将 `release/` 整个文件夹复制到 U 盘或网盘
3. 对方解压后双击 `启动.bat`

### 方式 B：ZIP 压缩包

压缩 `release/` 为 `PEP六年级英语训练营_v1.0.zip` 分发。

---

## 三、GitHub Pages 技术说明

已配置工作流：`.github/workflows/deploy-gh-pages.yml`

push 到 `main` / `master` 时会自动：

1. 打包 `index.html`、`app.js`、`styles.css`、`data/` 题库、`assets/` 等到 `release/`
2. 发布到 `gh-pages` 分支

### 访问地址

```
https://<GitHub用户名>.github.io/<仓库名>/
```

### 公网使用注意

- **不需要** 再运行 `启动.bat`（那是本地用的）
- 题库导入 CSV：在网页右侧操作，数据存在访客自己的浏览器里
- 家长密码、积分、错题本：每人本机独立，不会上传到 GitHub

---

## 四、手机访问

### 局域网（同一 WiFi）

1. 电脑运行 `启动.bat`
2. 查电脑 IP：`ipconfig`（IPv4 地址）
3. 手机浏览器打开：`http://<电脑IP>:8080`

### 公网（GitHub Pages / 阿里云 / 腾讯云）

部署完成后，手机直接打开对应公网网址即可（国内建议用 OSS/COS 链接）。

---

## 五、维护 release 目录

每次修改 `index.html / app.js / styles.css` 后，运行：

```
sync-release.bat
```

再提交 Git 或重新打包 ZIP。

---

## 六、阿里云 ECS（多用户 + 授权码 + 加密同步）

若需要 **多设备云端同步**、**授权码登录**、**服务器端加密存储**，请使用 ECS（而非纯 OSS 静态托管）。

### 功能说明

| 功能 | 说明 |
|------|------|
| License 授权码 | 格式 `PEP6-XXXX-XXXX-XXXX`，带到期时间 |
| 登录鉴权 | 同步 API 需 Bearer Token；网页弹出授权框 |
| 数据加密 | `lan-sync/*.json` 在服务器上以 Fernet 加密存储 |
| 多用户 | 每位学生用昵称作为 `syncId`，数据独立合并 |

### 一键部署（Ubuntu ECS）

```bash
sudo bash deploy/ecs/deploy.sh
```

脚本会：安装 Python/nginx → 拉取代码到 `/opt/pep6-english` → 启用 `PEP6_AUTH_REQUIRED=1` → 启动 systemd 服务。

### 生成授权码

在 ECS 上执行：

```bash
cd /opt/pep6-english
python3 scripts/gen_license.py --days 365 --label "六(1)班"
```

或在网页 **远程密码控制 → 学习授权码** 面板生成（需管理员密码）。

### 环境变量（`/etc/pep6-english/env`）

| 变量 | 说明 |
|------|------|
| `PEP6_AUTH_REQUIRED=1` | 开启授权（ECS 建议开启） |
| `PEP6_AUTH_ALLOW_LOCAL=0` | 云端建议关闭本机绕过 |
| `PEP6_TOKEN_TTL` | 会话有效期（秒），默认 7 天 |

### 安全组

阿里云控制台 → ECS → 安全组 → 入方向放行 **TCP 80**（及 443 若配置 HTTPS）。

### 更新代码

```bash
cd /opt/pep6-english && git pull && sudo systemctl restart pep6-english
```

---

## 七、注意事项

- 学习数据保存在浏览器 `localStorage`，不会随文件夹自动迁移
- 建议使用 Chrome / Edge 浏览器
- 直接双击 `index.html` 可用，但本地服务器方式更稳定
