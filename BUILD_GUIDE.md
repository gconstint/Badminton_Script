# 自动构建指南

本项目包含了两个GitHub Actions工作流，用于自动将Python脚本打包为Windows可执行文件。

## 工作流说明

### 1. 主构建工作流 (`build-exe.yml`)

**触发条件:**
- 推送到 `main` 或 `master` 分支
- 创建新的标签 (如 `v3.0.1`)
- 手动触发

**功能:**
- 自动安装Python依赖
- 下载最新的ChromeDriver
- 使用PyInstaller打包为单个exe文件
- 创建完整的发布包
- 自动创建GitHub Release (当推送标签时)

### 2. 手动构建工作流 (`manual-build.yml`)

**触发条件:**
- 仅手动触发

**功能:**
- 可选择构建类型 (release/debug/both)
- 可选择是否包含ChromeDriver
- 提供更多自定义选项

## 使用方法

### 自动构建 (推荐)

1. **创建新版本:**
   ```bash
   git tag v3.0.1
   git push origin v3.0.1
   ```

2. **查看构建状态:**
   - 访问 GitHub 仓库的 "Actions" 标签页
   - 查看工作流运行状态

3. **下载构建结果:**
   - 构建完成后，在 "Releases" 页面下载
   - 或在 "Actions" 页面的 "Artifacts" 中下载

### 手动构建

1. **触发构建:**
   - 访问 GitHub 仓库的 "Actions" 标签页
   - 选择 "Manual Build EXE" 工作流
   - 点击 "Run workflow"
   - 选择构建选项并运行

2. **下载结果:**
   - 在工作流完成后，从 "Artifacts" 部分下载

## 构建配置

### PyInstaller 配置 (`badminton.spec`)

自定义的PyInstaller配置文件，包含:
- 数据文件打包 (UI文件、图标、配置等)
- 隐藏导入模块
- 图标设置
- 优化选项

### 依赖管理 (`requirements.txt`)

项目依赖列表:
```
PyQt5==5.15.10
selenium==4.15.2
requests==2.31.0
pyinstaller==6.1.0
```

## 构建产物

### Release 版本
- `BadmintonScript.exe` - 主程序 (无控制台窗口)
- `chromedriver.exe` - Chrome浏览器驱动
- `使用说明.txt` - 用户指南
- 必要的资源文件 (图标、图片等)

### Debug 版本
- `BadmintonScript-Debug.exe` - 调试版本 (带控制台窗口)
- 便于查看错误信息和调试

## 故障排除

### 常见问题

1. **构建失败 - 依赖问题**
   - 检查 `requirements.txt` 中的版本号
   - 确保所有依赖都兼容

2. **ChromeDriver 下载失败**
   - 工作流会尝试自动下载
   - 如果失败，可以手动添加到仓库

3. **打包后运行错误**
   - 使用Debug版本查看详细错误信息
   - 检查是否缺少必要的数据文件

### 本地测试

在提交前，可以本地测试打包:

```bash
# 安装依赖
pip install -r requirements.txt

# 使用spec文件打包
pyinstaller badminton.spec

# 或使用简单命令
pyinstaller --onefile --windowed --icon=icons/badminton_ico.ico script_final_beta.py
```

## 版本发布流程

1. **更新版本号**
   - 在代码中更新版本信息
   - 更新 `CHANGELOG.md` (如果有)

2. **创建标签**
   ```bash
   git tag -a v3.0.1 -m "Release version 3.0.1"
   git push origin v3.0.1
   ```

3. **自动构建**
   - GitHub Actions 自动触发构建
   - 自动创建 Release 并上传文件

4. **发布说明**
   - 在 GitHub Releases 页面编辑发布说明
   - 添加更新内容和使用说明

## 注意事项

- 确保仓库中包含所有必要的资源文件
- 工作流需要 `GITHUB_TOKEN` 权限来创建 Release
- 构建时间约 5-10 分钟，取决于依赖下载速度
- 生成的exe文件大小约 50-100MB (包含所有依赖)
