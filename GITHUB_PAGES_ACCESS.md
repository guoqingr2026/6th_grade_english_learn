# GitHub Pages 部署与访问权限说明

你的仓库：**https://github.com/guoqingr2026/6th_grade_english_learn**

部署成功后，网页地址一般为：

**https://guoqingr2026.github.io/6th_grade_english_learn/**

（以 GitHub → Settings → Pages 里显示的为准。）

---

## 一、如何发布网页（首次）

1. 把代码 **push 到 `main` 分支**（已配置自动部署工作流）。
2. 打开仓库 → **Settings** → **Pages**。
3. **Build and deployment**：
   - Source：**Deploy from a branch**
   - Branch：**gh-pages** → **/ (root)** → **Save**
4. 打开 **Actions**，等待 **Deploy to GitHub Pages** 显示绿色勾（约 2～5 分钟）。
5. 刷新 **Settings → Pages**，复制站点链接发给需要的人。

以后每次 `git push` 到 `main`，几分钟内网站会自动更新。

---

## 二、谁能看？由你决定（三种方案）

### 方案 A：公开网页（免费，最简单）

| 项目 | 说明 |
|------|------|
| 仓库可见性 | **Public（公开）** |
| 谁能打开网页 | **互联网上任何人**（知道链接即可） |
| 费用 | 免费 |
| 适合 | 不介意公开、希望学生在家直接打开链接 |

**操作：** 仓库 **Settings → General → Danger Zone** 确认为 Public；开启 Pages 即可。

> 家长密码、学生积分等仍在**访客各自浏览器**里，不会上传到 GitHub；但练习页面本身可被任何人访问。

---

### 方案 B：仅授权的人能看（推荐：要控制访问时）

| 项目 | 说明 |
|------|------|
| 需要 | **GitHub Pro**（个人付费）或 **团队/学校 GitHub 组织** |
| 仓库可见性 | **Private（私有）** |
| 谁能看网页 | 仅你**邀请的协作者**（Settings → Collaborators） |
| Pages 设置 | Settings → Pages → **Restrict visibility**（限制为仅有仓库权限的人） |

**操作步骤：**

1. 升级到 [GitHub Pro](https://github.com/pricing)（或使用学校/单位组织账号）。
2. 仓库改为 **Private**。
3. **Settings → Collaborators** → **Add people**，添加允许查看的家长/老师 GitHub 账号。
4. **Settings → Pages** → 开启 **Restrict access to people with access to this repository**。
5. 被邀请的人登录 GitHub 后，才能打开 Pages 链接。

这样**由你决定名单**：加协作者 = 能看；移除 = 不能看。

---

### 方案 C：不放到公网，只在班里用（最私密）

| 项目 | 说明 |
|------|------|
| 方式 | 电脑运行 **`启动.bat`**，手机同一 WiFi 访问局域网地址 |
| 谁能用 | 仅连同一 WiFi 的设备 |
| 费用 | 免费 |
| 同步/精讲审核 | 完整功能（公网 Pages **没有**局域网同步 API） |

适合：教室上课、不想把链接发到网上。

---

## 三、公网版与局域网版的区别

| 功能 | GitHub Pages 公网 | 启动.bat 局域网 |
|------|-------------------|-----------------|
| 单词/语法/选择题等练习 | ✅ | ✅ |
| 课文讲读 / 知识点精讲 | ✅（只读为主） | ✅ 完整 |
| 多端同步数据 | ❌ | ✅ |
| 作业截图上传 | ❌ | ✅ |
| 主机管理员审核 | ❌ | ✅ |

---

## 四、常见问题

**Q：免费公开仓库，能设密码让别人输入才能进吗？**  
A：GitHub Pages 本身**不支持**访问密码。要么用方案 B（私有仓库 + 协作者），要么继续用局域网。

**Q：不想把 `PARENT_GUIDE.md` 放到网上？**  
A：公网部署包已**不包含**该文件；家长指南请只在本地或私下发给家长。

**Q：国内打开很慢？**  
A：见 [DEPLOY.md](./DEPLOY.md) 阿里云 OSS / 腾讯云 COS 方案；或学生在家用 GitHub 链接、学校用局域网。

---

## 五、维护者快速命令

```bash
cd "C:\Users\guoqren\.cursor\englishi learn"
git add .
git commit -m "更新说明"
git push origin main
```

推送后 Actions 自动部署，无需手动上传文件。
