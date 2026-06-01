# 贡献指南

感谢你对 **围棋 · Claude vs OpenCLAW** 的关注！

## 如何贡献

### 报告 Bug
1. 在 [Issues](../../issues) 中描述问题
2. 附上截图、浏览器版本和操作系统
3. 说明复现步骤

### 提出功能
1. 在 [Issues](../../issues) 中说明想法
2. 描述使用场景和预期效果

### 提交代码
1. Fork 本项目
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交改动：`git commit -m '✨ Add your feature'`
4. 推送：`git push origin feature/your-feature`
5. 提交 Pull Request

### Commit 规范

| emoji | 类型 | 说明 |
|-------|------|------|
| ✨ | feat | 新功能 |
| 🐛 | fix | Bug 修复 |
| 🎨 | style | 样式调整 |
| ♻️ | refactor | 重构 |
| 📝 | docs | 文档 |
| ⚡ | perf | 性能优化 |
| 🧪 | test | 测试 |
| 🤖 | ai | AI 策略改进 |

### AI 策略开发

改进 AI 的方法：

1. **调参**：修改 `GoAI.evaluateMove()` 中的权重
2. **新策略**：在 `GoAI` 中添加新的评估方法
3. **搜索算法**：实现蒙特卡洛树搜索（MCTS）
4. **神经网络**：集成 ONNX 或 TensorFlow.js 模型

测试 AI 改进：运行 `index.html`，观察对局质量。

### 项目结构
```
go-claude-vs-openclaw/
├── index.html          # 主程序（单文件）
├── README.md           # 项目说明
├── CONTRIBUTING.md     # 贡献指南（本文件）
├── VM-SETUP-GUIDE.md   # 虚拟机安装教程
└── LICENSE             # MIT 协议
```

### 行为准则
- 尊重每一位贡献者
- 建设性的代码评审
- 帮助新手

欢迎任何形式的贡献！
