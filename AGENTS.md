# LeoDock开发说明

本项目是 Windows 11 专用的本地服务与批处理任务控制台：Python 3.12+ 标准库后端，原生 HTML/CSS/ES Modules 前端，无运行时第三方依赖。

## 核心结构

- `leodock.py`：HTTP API、配置、Windows 进程/端口扫描、任务生命周期和安全校验。
- `static/`：无构建前端；`app.js` 为入口，`static/js/` 为功能模块。
- `static/themes/leodock-glass.css`：唯一内置的“LeoDock Glass”主题；界面需要兼容浅色、深色和窄屏。
- `tests/`：后端、Windows、前端契约、加固和发行测试。
- `tools/check_project.py`：权威项目检查。
- `tools/build_release.py`：可复现发行 ZIP 和发布边界审计。
- `start-leodock.cmd` / `start-leodock-debug.cmd`：Windows 启动入口。

## 平台约束

- 仅支持 Windows 11；新代码不得加入其他操作系统安装、启动或运行分支。
- 端口扫描使用 PowerShell `Get-NetTCPConnection`。
- 进程快照使用 CIM `Win32_Process`，所有权使用访问令牌 SID 验证。
- 受控进程身份由随机运行令牌、根 PID、父子关系和当前用户 SID 联合确定。
- 不得按端口直接结束进程；停止前必须确认受控身份。
- Windows 隐藏进程无法可靠接收优雅终止信号，验证后使用 `taskkill /T /F` 回收进程树。
- 任意外部进程的工作目录可能不可得；不可因目录未知而猜测认领。

## 运行与数据

```powershell
py -3 leodock.py
```

HTTP 只绑定 `127.0.0.1`，从 9600 到 9609 选择端口。默认数据位于 `%LOCALAPPDATA%\LeoDock`，日志在其 `logs` 子目录。`LEODOCK_DATA_DIR` 和 `LEODOCK_LOG_DIR` 可覆盖为专用绝对路径。

## 修改要求

- 后端保持 Python 标准库；前端保持无 CDN、无构建。
- 写接口必须保留 Host、Origin、Cookie 与大小/类型校验。
- 配置变更必须增加或迁移 `schemaVersion`，并补充测试。
- 危险操作必须保留确认流程。
- 修改 UI 文案或接口字段时同步更新前后端契约测试。
- 修改素材时同步更新 `ASSET_PROVENANCE.md` 与 SHA-256。
- 不提交运行数据、日志、绝对个人路径、凭据或未脱敏截图。

## 验证

```powershell
py -3 tools/check_project.py
py -3 tools/build_release.py --check-only
```

任何用户可见变化都应更新 `CHANGELOG.md`。发布前还应完成 `RELEASE_CHECKLIST.md` 中的 Windows 11 手工验收。
