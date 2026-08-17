# Windows 11 使用说明

LeoDock是仅面向 Windows 11 的本地网页应用。后端只绑定 `127.0.0.1`，运行时无需第三方 Python 包，也不会安装 Windows 服务、计划任务或开机启动项。

## 系统要求

- Windows 11 22H2 或更高版本。
- Python 3.12 或更高版本，并安装 Python Launcher（`py.exe`/`pyw.exe`）。
- Windows PowerShell 5.1 或 PowerShell 7。
- Edge、Chrome 或 Firefox 等现代浏览器。

## 启动

日常使用双击 `start-leodock.cmd`。它会在后台启动并打开浏览器；重复双击会识别已有实例。

排查启动错误时双击 `start-leodock-debug.cmd`，或运行：

```powershell
cd D:\Projects\leo-dock
py -3 leodock.py
```

只启动后台服务、不打开浏览器：

```powershell
py -3 leodock.py --no-browser
```

默认地址为 <http://127.0.0.1:9600/>，端口占用时自动尝试到 9609。

## 数据与日志

```text
%LOCALAPPDATA%\LeoDock
```

- `config.json`：应用、任务、端口和界面设置。
- `config.json.bak`：上一份良好配置。
- `icons\`：用户上传图标和站点图标。
- `logs\`：应用与中枢日志。

旧版“总控台”的数据位于 `%LOCALAPPDATA%\总控台`。首次启动LeoDock时，
如果新目录还不存在，程序会将旧配置、图标和日志复制到新目录；不会覆盖新数据，
也不会删除旧目录。

可覆盖为专用绝对路径：

```powershell
$env:LEODOCK_DATA_DIR = 'D:\LeoDockData'
$env:LEODOCK_LOG_DIR = 'D:\LeoDockLogs'
py -3 leodock.py
```

## 服务与任务

- 服务适用于长期运行命令，并可填写监听端口。
- 任务适用于会自然结束的命令，不配置端口。
- 原生脚本选择支持 `.py`、`.ps1`、`.cmd`、`.bat`、`.js`。
- Shell 脚本需要用户自行安装并明确调用 Git Bash 或 WSL。

停止服务时，LeoDock先通过随机运行令牌、根 PID、父子进程链和当前用户 SID 验证身份，再使用 `taskkill /T /F` 回收受控进程树。它不会按端口结束未知进程。

Windows 不可靠地公开任意外部进程的当前工作目录，因此外部监听进程的“认领”仅在能够可靠推断目录时可用。中枢自己启动的应用不受影响，因为工作目录已经保存在配置中。

## 卸载

1. 在页面中停止不再需要的受控服务和任务。
2. 停止LeoDock。
3. 删除项目文件夹。
4. 确认不再需要配置后，删除 `%LOCALAPPDATA%\LeoDock`。
