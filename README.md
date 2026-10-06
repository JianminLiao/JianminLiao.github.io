# Jianmin Liao — Personal website

英文个人学术主页，使用原生 HTML/CSS 和 GitHub Pages。无构建工具、JavaScript、第三方字体、追踪服务或运行时依赖。

- 网址：https://jianminliao.github.io/
- 公开仓库：https://github.com/JianminLiao/JianminLiao.github.io
- 托管：GitHub Pages；main 经安全检查后，通过 GitHub Actions 发布白名单内的文件；HTTPS。

## 本地预览

在本目录运行 `python -m http.server 4173 --bind 127.0.0.1`，打开 http://127.0.0.1:4173 。首页也可直接以本地文件打开。

## 更新网站

直接修改 index.html 中的个人简介、研究方向、教育经历、论文和项目。外观在 styles.css；简历在 assets/Jianmin-Liao-CV.pdf。在工作分支编辑后，先运行下面的检查，再通过 PR 合并到 main。安全检查成功后，GitHub Pages 自动更新；检查失败时保留上一版本。单人维护无需第二位审批者。

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/check_site.py
```

新增网页或资源时同步更新 `site-files.txt`。检查器只检查 Git 已跟踪的文件，首次添加文件后请再次运行。发布流程只上传名单内的文件，不上传整个仓库。安全约定及恢复方法见 `SECURITY.md`。

每篇论文使用 .publication，项目使用 .project；沿用已有条目的结构。只添加真实存在的 Paper、PDF、Code 或 Demo 链接。Google Scholar 主页已添加到侧栏与联系区域，使用公开链接 https://scholar.google.com/citations?user=6-htFRUAAAAJ&hl=en ，不携带账号或临时参数。

公开简历依据本人提供的版本生成，已去掉电话号码及电话超链接。更新 PDF 时同样移除手机号，检查提取文本和链接注释，并渲染检查排版。不要把原始私人简历、编辑分享链接、凭证或个人研究工作区上传到此仓库。

## Research Principles for the AI Era 栏目

`thoughts/index.html` 是 Research Principles for the AI Era 系列的目录，收录对 AI 时代科研选择、持续投入与评价的英文文章。首页的同名区域提供入口；文章使用 `thoughts/thoughts.css`，沿用主页的配色和字体。

Essay 01（首篇文章）为 `thoughts/research-principle-ai-era.html`，附同名主题的 `research-principle.pdf` 与 `research-principle.tex`。正文以 LaTeX 为源，网页中的数学公式已静态转换为原生 MathML，不需要浏览器加载脚本、字体或第三方服务。更新时同步核对网页、PDF 和源文件中的假设、定理与证明。

正文只围绕一个结论：即使唯一目标是最大化 intrinsic value，足够长的研究期限仍要求最优策略在初期全部投入 external value。保留 iid 随机线性回报、`d_i >= 1` 和增长余额约束 `B_i >= rho B_{i-1}`、`1 < rho < b`。共同分布可以未知，只需知道 `b = ess inf b_i`、`E[b_i]`、`E[b_i d_i]`；当前预算和余额可观测，策略不使用历史系数实现值。正文按假设、单一结论的定理、例图、证明组织。

定理给出与总期限无关的有限 `K`：当 `n > K` 时，所有最优策略的前 `n-K` 期均全部投入 external。例子使用固定线性函数、`n=13`、`a=1`、`b=1.11`、`d=rho=1.05`，得到 `K=10`，即前 3 期全 external。图中只画 intrinsic 分配比例折线和累计 intrinsic 柱子，深色柱段表示当期增量。

`thoughts/simulation/solve.py` 使用标准库 Decimal 的 40 位精度计算；运行 `python3 thoughts/simulation/solve.py` 可重建同目录 `result.json`。`assets/research-simulation.svg` 和 `assets/research-simulation-mobile.svg` 分别用于桌面和手机。文章页面不显示 PDF 或 LaTeX 下载入口。

## 发布配置

Settings → Pages → Build and deployment：使用 GitHub Actions，保持 Enforce HTTPS。工作流 `.github/workflows/pages.yml` 先运行测试和安全检查，再生成 `_site/` 并部署；部署环境只接受 main。不要改回从仓库根目录直接发布，否则会绕过文件白名单和发布检查。

自定义 404.html 使用根路径，因为这里是用户主页仓库。后续若迁往项目子目录，需要相应调整 404 页面中的根路径和首页 canonical / Open Graph URL。

## 验证

- 在桌面、390px 与 320px 手机宽度、200% 缩放下检查阅读和横向溢出。
- 检查页内导航、键盘焦点、站外链接和 CV 下载。
- 发布后检查首页、CSS、favicon、PDF 和自定义 404 的实际 HTTP 状态。
- 大陆访问体验需从当地网络实测，单一测试环境不能代表所有地区。

使用系统字体，所有呈现所需资源随网站一起托管。当前没有付费资源或独立域名。后续如需撤销修改，可 revert 对应提交后推送；不要强制覆盖历史。
