# GitHub Pages · 方案 B（私有仓库 + 协作者）

仓库：**https://github.com/guoqingr2026/6th_grade_english_learn**

网页地址（配置完成后）：

**https://guoqingr2026.github.io/6th_grade_english_learn/**

> 仅**已登录 GitHub** 且被你**邀请为协作者**的账号才能打开（私有 Pages）。

---

## 前提条件（必看）

| 条件 | 说明 |
|------|------|
| **GitHub Pro** | 个人账号需 [升级 Pro](https://github.com/settings/billing/plans)（约 $4/月），否则**私有仓库无法发布 Pages** |
| 或 **组织账号** | 学校/单位 GitHub Team 也可 |
| 访客要有 **GitHub 账号** | 家长/老师需注册 GitHub，你邀请后才能看网页 |
| 学生无账号 | 可继续用 **`启动.bat` 局域网**（教室），不依赖 GitHub 登录 |

---

## 操作清单（按顺序做）

### 第 1 步：确认已部署

1. 打开 https://github.com/guoqingr2026/6th_grade_english_learn/actions  
2. 找到 **Deploy to GitHub Pages**，状态为绿色 ✓  
3. 若失败（红色）：点进去看日志；常见原因：
   - **Pages 未选 GitHub Actions**：Settings → Pages → Source 改为 **GitHub Actions**
   - **私有仓库未开 Pro**：无法发布私有 Pages
   - **Actions 权限**：Settings → Actions → General → Workflow permissions 选 **Read and write**
4. 可手动重跑：Actions → Deploy to GitHub Pages → **Run workflow**

### 第 2 步：仓库改为私有

1. 打开 https://github.com/guoqingr2026/6th_grade_english_learn/settings  
2. 拉到最下 **Danger Zone**  
3. **Change repository visibility** → **Change visibility**  
4. 选 **Private** → 按提示输入仓库名确认  

代码只有你和协作者能看，外人搜不到仓库。

### 第 3 步：开启 GitHub Pages（重要：选 GitHub Actions）

1. 左侧 **Pages**（或 https://github.com/guoqingr2026/6th_grade_english_learn/settings/pages ）
2. **Build and deployment**
   - **Source**：**GitHub Actions**（不要选「Deploy from a branch」里的旧 gh-pages，除非 Actions 不可用）
3. 保存后，打开 **Actions** 标签，点 **Deploy to GitHub Pages** → **Run workflow** 手动跑一次
4. 等绿色 ✓ 后，回到 **Settings → Pages**，复制站点 URL

### 第 4 步：限制网页仅协作者可访问（方案 B 核心）

在同一 **Settings → Pages** 页面：

1. 找到 **Visibility**（可见性）  
2. 选择：**Only people with access to this repository**  
   （中文界面类似：「仅对此仓库有访问权限的用户」）  
3. **Save**

> 若没有此选项：说明账号还不是 Pro，或 Pages 尚未从 `gh-pages` 部署成功，先完成第 1～3 步并升级 Pro。

### 第 5 步：邀请谁能看（你决定名单）

1. **Settings → Collaborators**（或 **Manage access**）  
2. **Add people**  
3. 输入对方的 **GitHub 用户名或邮箱**  
4. 权限建议：**Read**（只读即可看网页，不能改代码）  
5. 对方邮箱会收到邀请 → 接受后登录 GitHub，再打开 Pages 链接  

**移除访问：** 在 Collaborators 里 **Remove** 即可，对方立刻无法再看私有 Pages。

### 第 6 步：把链接发给已邀请的人

发送内容示例：

```
六年级英语训练营（需登录 GitHub）：
https://guoqingr2026.github.io/6th_grade_english_learn/

请先接受我发的 GitHub 协作邀请，用浏览器登录 GitHub 后再打开。
```

---

## 协作者（家长/老师）怎么做

1. 注册 GitHub：https://github.com/signup  
2. 邮箱里接受 **Collaborator invitation**  
3. 浏览器登录 GitHub（同一账号）  
4. 打开上面的 Pages 链接  

未登录或未接受邀请时，会显示 **404** 或要求登录——这是正常的权限保护。

---

## 你本地更新网站后

```bash
cd "C:\Users\guoqren\.cursor\englishi learn"
git add .
git commit -m "更新说明"
git push origin main
```

约 2～5 分钟后 Actions 自动更新 `gh-pages`，协作者刷新网页即可。

---

## 方案 B 与局域网怎么配合

| 场景 | 建议 |
|------|------|
| 家里复习、已邀请的家长 | 私有 Pages 链接 |
| 教室上课、要同步/作业截图 | `启动.bat` 局域网 |
| 学生没有 GitHub 账号 | 只用局域网，不要强求 Pages |

---

## 常见问题

**Q：必须是 GitHub Pro 吗？**  
A：私有仓库的 **受限 Pages** 需要 Pro（或 Team）。免费版只能「公开仓库 + 公开网页」。

**Q：能设网页密码而不是 GitHub 账号吗？**  
A：GitHub 官方不支持。方案 B 用「GitHub 登录 + 协作者名单」代替密码。

**Q：公网版有同步吗？**  
A：没有。多端同步请用 `启动.bat`。

**Q：`PARENT_GUIDE.md` 会上传吗？**  
A：自动部署**不包含**该文件，请私下发给家长。

---

## 维护者链接速查

| 项目 | 链接 |
|------|------|
| 仓库 | https://github.com/guoqingr2026/6th_grade_english_learn |
| Actions | https://github.com/guoqingr2026/6th_grade_english_learn/actions |
| Pages 设置 | https://github.com/guoqingr2026/6th_grade_english_learn/settings/pages |
| 协作者 | https://github.com/guoqingr2026/6th_grade_english_learn/settings/access |
| 升级 Pro | https://github.com/settings/billing/plans |
