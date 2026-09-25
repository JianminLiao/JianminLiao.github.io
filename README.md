# Jianmin Liao — Personal website

英文个人学术主页，使用原生 HTML/CSS 和 GitHub Pages。无构建工具、JavaScript、第三方字体、追踪服务或运行时依赖。

- 网址：https://jianminliao.github.io/
- 公开仓库：https://github.com/JianminLiao/JianminLiao.github.io
- 托管：GitHub Pages，main 分支的根目录；HTTPS。

## 本地预览

在本目录运行 `python -m http.server 4173 --bind 127.0.0.1`，打开 http://127.0.0.1:4173 。首页也可直接以本地文件打开。

## 更新网站

直接修改 index.html 中的个人简介、研究方向、教育经历、论文和项目。外观在 styles.css；简历在 assets/Jianmin-Liao-CV.pdf。编辑后提交并推送到 main，GitHub Pages 自动更新。

每篇论文使用 .publication，项目使用 .project；沿用已有条目的结构。只添加真实存在的 Paper、PDF、Code 或 Demo 链接。Google Scholar 主页尚未提供，因此不显示该入口。

公开简历依据本人提供的版本生成，已去掉电话号码及电话超链接。更新 PDF 时同样移除手机号，检查提取文本和链接注释，并渲染检查排版。不要把原始私人简历、编辑分享链接、凭证或个人研究工作区上传到此仓库。

## 发布配置

Settings → Pages → Build and deployment：选择 Deploy from a branch，main，/ (root)。确认 Enforce HTTPS。.nojekyll 让 GitHub 直接发布静态文件。

自定义 404.html 使用根路径，因为这里是用户主页仓库。后续若迁往项目子目录，需要相应调整 404 页面中的根路径和首页 canonical / Open Graph URL。

## 验证

- 在桌面、390px 与 320px 手机宽度、200% 缩放下检查阅读和横向溢出。
- 检查页内导航、键盘焦点、站外链接和 CV 下载。
- 发布后检查首页、CSS、favicon、PDF 和自定义 404 的实际 HTTP 状态。
- 大陆访问体验需从当地网络实测，单一测试环境不能代表所有地区。

使用系统字体，所有呈现所需资源随网站一起托管。当前没有付费资源或独立域名。后续如需撤销修改，可 revert 对应提交后推送；不要强制覆盖历史。
