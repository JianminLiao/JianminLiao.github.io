# Jianmin Liao — Personal website

英文个人学术主页，使用原生 HTML/CSS 和 GitHub Pages。无构建工具、JavaScript、第三方字体、追踪服务或运行时依赖。

- 网址：https://jianminliao.github.io/
- 公开仓库：https://github.com/JianminLiao/JianminLiao.github.io
- 托管：GitHub Pages，main 分支的根目录；HTTPS。

## 本地预览

在本目录运行 `python -m http.server 4173 --bind 127.0.0.1`，打开 http://127.0.0.1:4173 。首页也可直接以本地文件打开。

## 更新网站

直接修改 index.html 中的个人简介、研究方向、教育经历、论文和项目。外观在 styles.css；简历在 assets/Jianmin-Liao-CV.pdf。编辑后提交并推送到 main，GitHub Pages 自动更新。

每篇论文使用 .publication，项目使用 .project；沿用已有条目的结构。只添加真实存在的 Paper、PDF、Code 或 Demo 链接。Google Scholar 主页已添加到侧栏与联系区域，使用公开链接 https://scholar.google.com/citations?user=6-htFRUAAAAJ&hl=en ，不携带账号或临时参数。

公开简历依据本人提供的版本生成，已去掉电话号码及电话超链接。更新 PDF 时同样移除手机号，检查提取文本和链接注释，并渲染检查排版。不要把原始私人简历、编辑分享链接、凭证或个人研究工作区上传到此仓库。

## Research Principles for the AI Era 栏目

`thoughts/index.html` 是 Research Principles for the AI Era 系列的目录，收录对 AI 时代科研选择、持续投入与评价的英文文章。首页的同名区域提供入口；文章使用 `thoughts/thoughts.css`，沿用主页的配色和字体。

Essay 01（首篇文章）为 `thoughts/research-principle-ai-era.html`，附同名主题的 `research-principle.pdf` 与 `research-principle.tex`。正文以 LaTeX 为源，网页中的数学公式已静态转换为原生 MathML，不需要浏览器加载脚本、字体或第三方服务。更新时同步核对网页、PDF 和源文件中的假设、定理与证明。

定理后展示一条固定线性函数的最优轨迹：所有 16 期均使用 `f(c)=c`、`g(c)=1.11c`、`h(e)=e`，初始 `c1=1`、`B0=0`，安全余额 `delta=0.1`，余额增长率 `rho=1.05`。定理给出 `K=13`，即前 3 期全部投入 external，后 13 期混合分配。`thoughts/simulation/solve.py` 使用 Python 标准库 Decimal 的 40 位精度按定理计算，`result.json` 保存全部数值；不需要数值优化、随机采样或多次模拟。

同一张图中，折线表示 intrinsic 投入比例，整根柱子表示累计 intrinsic，深色顶部表示当期新增部分。第 4 期和第 16 期的 intrinsic 比例分别为 8.70% 和 8.12%，当期增量分别为 0.1190 和 0.1348，最终累计值为 1.6403。所有期均满足固定安全余额和余额增长约束。`assets/research-simulation.svg` 和 `assets/research-simulation-mobile.svg` 分别用于桌面和手机。一般函数包夹模型与线性特例定理的区分保留；本例严格属于线性定理的范围。文章页面不显示 PDF 或 LaTeX 下载入口。

## 发布配置

Settings → Pages → Build and deployment：选择 Deploy from a branch，main，/ (root)。确认 Enforce HTTPS。.nojekyll 让 GitHub 直接发布静态文件。

自定义 404.html 使用根路径，因为这里是用户主页仓库。后续若迁往项目子目录，需要相应调整 404 页面中的根路径和首页 canonical / Open Graph URL。

## 验证

- 在桌面、390px 与 320px 手机宽度、200% 缩放下检查阅读和横向溢出。
- 检查页内导航、键盘焦点、站外链接和 CV 下载。
- 发布后检查首页、CSS、favicon、PDF 和自定义 404 的实际 HTTP 状态。
- 大陆访问体验需从当地网络实测，单一测试环境不能代表所有地区。

使用系统字体，所有呈现所需资源随网站一起托管。当前没有付费资源或独立域名。后续如需撤销修改，可 revert 对应提交后推送；不要强制覆盖历史。
