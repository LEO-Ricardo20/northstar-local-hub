# 北辰本地中枢

[![Windows CI](https://github.com/LEO-Ricardo20/northstar-local-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/LEO-Ricardo20/northstar-local-hub/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Windows 11](https://img.shields.io/badge/Windows-11-0078D4.svg)](WINDOWS.md)

Northstar Local Hub 是一个面向 Windows 11 的本地服务与批处理任务启动、监测和诊断面板。它把常用开发服务、项目启动命令和一次性脚本集中到浏览器界面中，并使用仅绑定回环地址的 Python 标准库后端。

> 当前版本是 Preview。项目会执行你保存的本地命令，请只添加已经检查并信任的工作目录与命令。

## 主要能力

- 集中管理长期服务和一次性批处理任务。
- 启动、停止、重启、查看日志并进行启动前诊断。
- 监测当前 Windows 用户的本地监听端口、CPU、内存和运行时长。
- 从项目目录识别 Node.js、Python、Go、Rust、静态站点等常见启动方式。
- 原生选择 `.py`、`.ps1`、`.cmd`、`.bat` 和 `.js` 脚本。
- 使用随机运行令牌、根 PID、父子进程关系与当前用户 SID 识别受控进程树。
- “北辰光幕”界面采用深黑蓝空间、雾白玻璃、北辰蓝折射光与分级透明材质，支持浅色、深色、系统主题、命令面板和键盘排序。
- 后端只使用 Python 标准库；前端使用原生 HTML、CSS 和 ES Modules，不依赖 CDN。

## 界面预览

| 启动台 | 服务监控 |
| --- | --- |
| ![北辰本地中枢启动台](docs/screenshots/ops-launchpad.jpg) | ![北辰本地中枢服务监控](docs/screenshots/ops-services.jpg) |

## 系统要求

- Windows 11 22H2 或更高版本。
- Python 3.12 或更高版本，并保留 Python Launcher（`py.exe`）。
- Windows PowerShell 5.1 或 PowerShell 7。
- Edge、Chrome、Firefox 等支持 ES Modules 的现代浏览器。

## 快速开始

```powershell
git clone https://github.com/LEO-Ricardo20/northstar-local-hub.git
cd northstar-local-hub
py -3 --version
```

日常使用直接双击：

```text
start-windows.cmd
```

需要查看启动输出时双击：

```text
start-windows-debug.cmd
```

也可以在 PowerShell 中启动：

```powershell
py -3 server.py
py -3 server.py --no-browser
py -3 server.py --preferred-port 9603 --no-browser
```

默认地址为 <http://127.0.0.1:9600/>。如果端口被占用，程序会依次尝试 9601–9609。

## 使用说明

### 启动台

- 添加服务：选择项目目录，使用自动识别候选命令或手工填写命令与端口。
- 添加任务：保存会自然结束的命令；退出码 `0` 表示成功，`130` 表示任务主动取消。
- 卡片操作：支持启动、停止、重启、编辑、删除、日志、诊断和拖拽排序。
- 批量停止：只停止经过运行身份验证的受控进程树，不按端口结束未知进程。

### 服务监控

- 每两秒刷新一次当前用户的本地监听服务。
- 展示 PID、端口、命令、负载、时长和来源信息。
- 新出现的端口可加入启动台、忽略或临时关闭提示。
- Windows 无法可靠读取任意外部进程的当前工作目录，因此外部服务的“认领”只有在能可靠推断目录时才可用；由北辰本地中枢启动的服务不受影响。

### 快捷键

- `Ctrl+K`：打开命令面板。
- `Ctrl+J`：打开日志中心。
- 卡片聚焦后按空格：进入键盘排序模式。

## 数据与日志

默认运行目录：

```text
%LOCALAPPDATA%\北辰本地中枢
```

| 路径 | 内容 |
| --- | --- |
| `%LOCALAPPDATA%\北辰本地中枢\config.json` | 服务、任务、端口和界面配置 |
| `%LOCALAPPDATA%\北辰本地中枢\config.json.bak` | 上一份良好配置 |
| `%LOCALAPPDATA%\北辰本地中枢\icons\` | 用户上传图标和站点图标 |
| `%LOCALAPPDATA%\北辰本地中枢\logs\` | 应用与中枢日志 |

从旧版“总控台”首次启动时，如果新目录尚不存在，程序会从
`%LOCALAPPDATA%\总控台` 复制配置、图标和日志；旧目录会完整保留，且不会覆盖
已经存在的新目录。

可使用专用环境变量覆盖路径：

```powershell
$env:CONSOLE_DATA_DIR = 'D:\NorthstarData'
$env:CONSOLE_LOG_DIR = 'D:\NorthstarLogs'
py -3 server.py
```

环境变量必须指向专用绝对路径，不能直接使用盘符根目录、用户主目录或项目根目录。

## 安全边界

- HTTP 服务只绑定 `127.0.0.1`，项目不是远程管理面板或多用户权限系统。
- 不要通过端口映射、反向代理或其他方式把控制面板暴露到局域网或公网。
- 写操作会校验 Host、Origin、会话 Cookie、当前用户 SID 和受控进程身份。
- Windows 停止受控服务时会在验证身份后使用 `taskkill /T /F` 回收进程树。
- 配置和日志可能包含绝对路径与完整命令，不应提交到 Git 或未经脱敏上传。

详细安全报告流程见 [SECURITY.md](SECURITY.md)。

## 开发与验证

运行完整检查：

```powershell
py -3 tools/check_project.py
```

运行后端测试：

```powershell
py -3 -m unittest discover -s tests -p 'test_*.py' -v
```

检查发行内容并生成可复现 ZIP：

```powershell
py -3 tools/build_release.py --check-only
py -3 tools/build_release.py --dist dist
py -3 tools/build_release.py --dist dist --verify-only
```

重新生成品牌 favicon 需要开发依赖：

```powershell
py -3 -m pip install -r requirements-dev.txt
py -3 tools/gen_brand_assets.py
```

## 项目结构

```text
server.py                  Python 标准库后端
static/                    原生前端、北辰光幕主题、字体与图标
tests/                     后端、前端契约和发行测试
tools/check_project.py     完整项目检查
tools/build_release.py     可复现发行包生成与审计
start-windows.cmd          Windows 后台启动入口
start-windows-debug.cmd    Windows 调试启动入口
```

## 参与贡献

- 贡献说明：[CONTRIBUTING.md](CONTRIBUTING.md)
- 行为准则：[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
- 第三方素材：[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- 素材来源：[ASSET_PROVENANCE.md](ASSET_PROVENANCE.md)

## 版权与许可

本仓库由 [LEO-Ricardo20](https://github.com/LEO-Ricardo20) 维护。项目代码依据 [MIT License](LICENSE) 开放使用；既有代码的原版权声明与本项目修改部分的版权声明均保留在许可证中。字体、Lucide 图标和品牌素材适用各自许可与来源说明，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 [ASSET_PROVENANCE.md](ASSET_PROVENANCE.md)。
