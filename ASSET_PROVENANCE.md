# 素材来源与发布状态

本文件是发行门禁的一部分，登记会进入源码仓库或发行包的字体、图标、Logo、App Icon、插画和生成纹理。根目录 MIT 许可证只覆盖项目有权许可的代码和文档，不会自动改变第三方素材的许可，也不能替代 AI 生成平台或素材提供方的条款核验。

状态含义：

- `CLEARED`：来源、许可和再分发条件已在仓库中形成可核验记录；
- `REVIEW_REQUIRED`：有初步来源，但仍需补齐原文、校验值或授权判断；
- `BLOCKED`：不得进入公开发行包，必须补证或替换；
- `TO_REPLACE`：已决定替换，替换完成前不得公开发行。

公开发行前，`RELEASE_CHECKLIST.md` 要求发行范围内不存在 `BLOCKED` 或 `TO_REPLACE` 项。自动检查会核对正式素材路径与当前 SHA-256 是否在本文件中登记，但不能替代人工权利核验。

## 每项记录必须包含

新增或替换素材时，至少记录：

1. 仓库路径和用途；
2. 原始文件名、来源 URL 或生成工具/模型；
3. 作者、版权方或生成操作人；
4. 获取/生成日期与上游版本；
5. 对原始素材执行的裁切、压缩、描摹、子集化等修改；
6. 适用许可和允许捆绑再分发的依据；
7. 当前文件 SHA-256；
8. 原始文件、许可快照、订单或授权邮件等凭证的归档位置；
9. 状态、复核人和复核日期。

凭证可能包含个人信息时，只在本文件记录受控归档位置，不要把私人邮件、订单或账户信息提交到仓库。

## 当前素材登记

### Lucide 图标

- 路径：`static/icons/*.svg`、生成文件 `static/icons.js`
- 用途：界面功能图标
- 来源/版本：Lucide Static 0.544.0；SVG 文件头带版本与许可标记
- 修改：`tools/gen_icons.py` 清理注释并生成 JavaScript 注册表；不改变图标路径语义
- 许可：ISC；部分 Feather 来源图标同时保留 MIT 条款
- 凭证：`licenses/Lucide-LICENSE.txt`、`THIRD_PARTY_NOTICES.md`
- 状态：`CLEARED`
- 复核：发布负责人仍需在每次上游升级后重新核对版本与许可

### Geist Mono

- 路径：`static/fonts/GeistMono-Variable.woff2`
- 用途：数据与代码字体
- 来源/版本：Vercel Geist Mono；仓库当前未单独记录上游 release/tag
- 修改：未记录
- 许可：SIL Open Font License 1.1
- SHA-256：`fba8f577f38a2bbcbe818efa6348dd58f36303a10b8737c42fefad275be563ab`
- 凭证：`licenses/Geist-OFL-1.1.txt`、`THIRD_PARTY_NOTICES.md`
- 状态：`REVIEW_REQUIRED`
- 待办：补齐准确上游版本、下载 URL 和原始文件校验值

### 统一品牌标识与图标导出

- 路径与 SHA-256：
  - `static/assets/leodock-app-icon.png`：`49c9af98f3480ace498bdb3992835515c000a5990a7c687e16ef5b9310398f9b`
  - `static/assets/leodock-brand-mark.png`：`60b29836b3e790dda4015621efa2c8bfc02e404a8549f6df7a694c0594613fc2`
  - `static/assets/favicon-32.png`：`c5d3c4011928827c0e752cdbcaf4916a373fef7285d3bdca16d391f457b90baa`
  - `static/assets/favicon.ico`：`88d276e465a25f163b8b74e08751ffdf24b2af9c77c99fac3a94d52dee331173`
- 用途：Windows/Web 应用主图、浏览器 favicon 与网页顶栏品牌标识
- 设计：冷白色 `L`、LEO 蓝 `D` 与暖金色定位点组成 `LD` 字母标识，应用图标使用深色玻璃底板与蓝金光影
- 来源：项目维护者于 2026-08-17 在 Codex 中设计参数，并由仓库内 `tools/gen_brand_assets.py` 使用 Pillow 确定性绘制；未使用外部图片、AI 图像输出或第三方品牌素材
- 修改：同一脚本直接生成透明品牌标识、应用图标、32px favicon 与多尺寸 Windows ICO；缩放使用 Pillow Lanczos
- 凭证：`tools/gen_brand_assets.py`、本文件校验值和 Git 历史；任意环境可由锁定的 Pillow 版本复现
- 许可：作为 LeoDock 项目自有程序化品牌素材，随项目依据根目录 MIT License 分发
- 状态：`CLEARED`
- 复核：Codex，2026-08-17

### 文档界面截图

- 路径与 SHA-256：
  - `docs/screenshots/leodock-launchpad.jpg`：`7abe6bc1bd82b3fd57e67aef2bbb7f812177fd8d797f39695c794bfce8928a75`
  - `docs/screenshots/leodock-services.jpg`：`e054bc8ed29551d550e7f1fa9fe1e61f40770bfbb2c80f640aa33f07dba5228d`
- 用途：README 展示“LeoDock Glass”主题下的启动台与服务监控浅色玻璃界面
- 来源/生成：项目维护者于 2026-08-17 在本地启动LeoDock，使用 Microsoft Edge 与 Playwright 以 `1920x1080` 视口捕获；画面完全由仓库内前端、品牌素材和本地合成演示数据生成
- 数据清洗：截图捕获前在浏览器 DOM 中将端口、负载、进程、服务计数和工作目录替换为合成演示值，仅保留 `C:\LeoDock\workspace\...` 等虚构路径；多余本机进程行被隐藏，不包含真实用户项目路径、账户、密钥、私人日志或可识别的本机运行记录
- 修改：浏览器原始 PNG 截图经 Pillow 转换为 RGB JPEG，质量 93、4:4:4 色度采样、渐进编码；未裁切、拼接或加入仓库外视觉素材
- 凭证：本文件校验值、Git 历史及可由项目本地界面复现的截图流程；一次性浏览器捕获文件不进入发行包
- 许可：截图中的项目自有界面与文档内容按根目录许可证发布；其中 Lucide 图标、Geist Mono 字体和品牌图片仍分别受本文件及 `THIRD_PARTY_NOTICES.md` 中对应条款约束
- 状态：`CLEARED`
- 复核：Codex，2026-08-17

## 更新规则

- 文件内容变化后必须更新 SHA-256 和修改说明。
- 上游素材升级后必须重新核对许可原文、版本和版权声明。
- AI 生成素材不能只记录“AI 生成”；必须能说明生成主体、平台/模型、生成日期、适用条款和原始输出凭证。
- 发行负责人必须对最终解压产物重新计算校验值，而不是只核对开发工作区。
