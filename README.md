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

定理后是一条确定性的非线性轨迹。三个函数每期均采用 `F_i(x)=a_i*x*(1+q_i*x/(1+x))`：f、g、h 的 a 范围分别为 `[0.9,1.1]`、`[1.25,1.65]`、`[0.85,0.95]`，q 范围均为 `[0.05,0.15]`。所有函数严格递增，并具有统一的正斜率线性上下界。使用 NumPy `default_rng(20260928)`，依次生成三个长度为 16 的 a 数组，再生成形状 `(3,16)` 的 q 数组。余额参数为 `rho=1.05`、`delta=0.1`。

`thoughts/simulation/solve.py` 和 `result.json` 保存可复现实验及完整数值记录。SLSQP 使用解析梯度、17 个初始分配方案优化同一条已知函数序列；16 次报告收敛，收敛结果的目标值一致。一次未报告收敛的尝试保留在记录中，不用于数值结果声明。解析梯度与中心差分核对，最大绝对误差小于 4e-10。数值解满足所有余额约束至浮点误差，数值求解不提供全局最优证书。正文严格区分一般非线性模型、线性特例的精确定理和非线性数值例子。

同一张图中，折线表示 intrinsic 投入比例，整根柱子表示累计 intrinsic，深色顶部表示当期新增部分；没有均值或 external 数值。`assets/research-simulation.svg` 和 `assets/research-simulation-mobile.svg` 分别服务于桌面和手机。文章页面不显示 PDF 或 LaTeX 下载入口。

## 发布配置

Settings → Pages → Build and deployment：选择 Deploy from a branch，main，/ (root)。确认 Enforce HTTPS。.nojekyll 让 GitHub 直接发布静态文件。

自定义 404.html 使用根路径，因为这里是用户主页仓库。后续若迁往项目子目录，需要相应调整 404 页面中的根路径和首页 canonical / Open Graph URL。

## 验证

- 在桌面、390px 与 320px 手机宽度、200% 缩放下检查阅读和横向溢出。
- 检查页内导航、键盘焦点、站外链接和 CV 下载。
- 发布后检查首页、CSS、favicon、PDF 和自定义 404 的实际 HTTP 状态。
- 大陆访问体验需从当地网络实测，单一测试环境不能代表所有地区。

使用系统字体，所有呈现所需资源随网站一起托管。当前没有付费资源或独立域名。后续如需撤销修改，可 revert 对应提交后推送；不要强制覆盖历史。
