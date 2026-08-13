# Windows 11 发布检查表

## 自动检查

- [ ] `py -3 tools/check_project.py` 全部通过。
- [ ] `py -3 tools/build_release.py --check-only` 通过。
- [ ] 构建两次发行 ZIP，SHA-256 完全一致。
- [ ] GitHub Actions Windows CI 通过。

## 全新环境

- [ ] 在 Windows 11 22H2 或更高版本上测试。
- [ ] 使用 Python 3.12 测试 `start-windows.cmd`。
- [ ] 使用 `start-windows-debug.cmd` 验证错误输出。
- [ ] 默认数据目录不存在时能创建 `%LOCALAPPDATA%\北辰本地中枢`。
- [ ] 9600 被占用时能回退到 9601–9609。

## 功能验收

- [ ] 创建、编辑、排序和删除服务卡片。
- [ ] 启动服务并识别监听端口与进程树。
- [ ] 停止和重启只影响经过身份验证的受控进程树。
- [ ] 创建成功、失败、取消和中止的批处理任务。
- [ ] 检查日志中心、命令面板、浅色、深色和窄屏布局。
- [ ] 检查 Windows 原生目录/脚本选择器。
- [ ] 验证项目识别不会安装依赖或执行项目代码。

## 安全与隐私

- [ ] 服务仍只绑定 `127.0.0.1`。
- [ ] Host、Origin、会话 Cookie 和请求大小限制有效。
- [ ] 不能结束其他 Windows 用户的进程。
- [ ] 不按端口结束未知进程。
- [ ] ZIP 不包含配置、日志、凭据、token、个人绝对路径或 Git 元数据。
- [ ] 截图、日志和 Issue 示例已经脱敏。

## 开源与发行

- [ ] `VERSION`、`CHANGELOG.md`、Git 标签和发行名称一致。
- [ ] LICENSE 保留上游 MIT 版权声明。
- [ ] 第三方许可和素材来源记录完整。
- [ ] README 中的仓库占位符 `OWNER` 已替换为实际 GitHub 用户名或组织名。
- [ ] GitHub Private Vulnerability Reporting 已启用。
- [ ] Release 附上 ZIP 和对应 `.sha256`。
