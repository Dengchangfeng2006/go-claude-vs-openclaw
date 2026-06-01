# 围棋 · Claude vs OpenCLAW

> 两个 AI 在 19×19 棋盘上的对决 —— Claude（黑棋）vs OpenCLAW（白棋）

纯浏览器端围棋对弈。点击"开始对局"，观看两个不同策略的 AI 在精美木质棋盘上对弈。完整围棋规则、实时棋谱、领地估算。

## 快速开始

```bash
# 方式 1：直接打开
# 用浏览器打开 index.html

# 方式 2：本地服务器
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080
```

## 操作

| 操作 | 方式 |
|------|------|
| 开始对局 | 点击按钮 或 按空格键 |
| 暂停/继续 | 点击按钮 或 按空格键 |
| 重新开始 | 按 R 键 |

## 功能

- 19×19 Canvas 渲染棋盘，木纹纹理，渐变棋子
- 完整围棋规则：提子、打劫、禁手、双 Pass 终局、贴目 6.5
- 两个不同风格 AI：Claude（均衡型）vs OpenCLAW（进攻型）
- 实时棋谱、提子计数、领地可视化
- AI 评估因子：提子价值、影响力、敌我距离、连接性、开局星位

## 技术架构

```
index.html          # 单文件应用
├── GoGame          # 围棋引擎 (board, captures, ko, territory)
├── GoAI            # AI 策略 (influence + capture + proximity)
├── BoardRenderer   # Canvas 渲染 (wood, stones, territory shading)
└── GameController  # 对局控制 (turn management, pause/resume)
```

## 部署到虚拟机

参见 [VM-SETUP-GUIDE.md](VM-SETUP-GUIDE.md)，完整教程带你从零安装 VirtualBox + Ubuntu + OpenCLAW。

游戏在 VM 上的部署：

```bash
# SSH 连接到 VM
ssh openclaw-vm

# 启动 HTTP 服务
cd ~/go-game && python3 -m http.server 8080 &

# 在宿主机浏览器访问
# http://localhost:8080
```

## 如何贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。欢迎提交：
- AI 策略改进（蒙特卡洛树搜索、神经网络）
- 新功能（SGF 导出、人机对战、在线对战）
- UI 优化（移动端适配、暗色/亮色主题）
- 文档翻译

## 许可证

MIT License

---

由 Claude 和 OpenCLAW 共同开发 🦞
