# 🐧 从零开始：VirtualBox + Ubuntu + OpenCLAW 完整教程

> 面向新手小白的保姆级指南。零基础也能跟着完成。

## 📋 目录

1. [准备清单](#准备清单)
2. [下载文件](#第-1-步下载文件)
3. [安装 VirtualBox](#第-2-步安装-virtualbox)
4. [创建虚拟机](#第-3-步创建虚拟机)
5. [安装 Ubuntu Server](#第-4-步安装-ubuntu-server)
6. [配置 SSH](#第-5-步配置-ssh-连接)
7. [安装 OpenCLAW](#第-6-步安装-openclaw)
8. [初始化与使用](#第-7-步初始化-openclaw)
9. [部署围棋游戏](#第-8-步部署围棋游戏)
10. [常见问题](#常见问题)
11. [命令速查](#命令速查)

---

## 准备清单

| 需求 | 说明 |
|------|------|
| Windows 10/11 | 64 位 |
| 内存 | ≥ 8GB（VM 占 4GB） |
| 磁盘 | ≥ 35GB 剩余空间 |
| 时间 | 约 40 分钟 |
| 不需要 | Linux 经验、编程知识 |

---

## 第 1 步：下载文件

### Ubuntu Server 24.04 ISO
- 官方：https://ubuntu.com/download/server
- 国内清华镜像：https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/24.04/
- 保存到 E 盘，约 3.4GB

### VirtualBox
- 下载：https://www.virtualbox.org/wiki/Downloads
- 选 "Windows hosts"

### SSH 密钥（推荐）
打开 PowerShell：
```powershell
ssh-keygen -t ed25519 -f E:\openclaw_key -N '""'
```
生成 `E:\openclaw_key`（私钥）和 `E:\openclaw_key.pub`（公钥）。

---

## 第 2 步：安装 VirtualBox

双击安装程序 → 一路 Next → 完成。

---

## 第 3 步：创建虚拟机

### 新建 VM
1. VirtualBox → **新建**
2. 名称：`Ubuntu-OpenCLAW`，文件夹：`E:\VirtualBox_VMs`
3. ISO：选择 `E:\ubuntu-server-2404.iso`
4. 类型：Linux / Ubuntu (64-bit)
5. 下一步

### 硬件
- 内存：**4096 MB**
- CPU：**2**

### 硬盘
- 大小：**30 GB**
- 类型：VDI，动态分配

### 网络（重要！）
在 VM 设置 → 网络：
- 连接方式：**NAT**
- 高级 → 端口转发 → 添加：

| 名称 | 协议 | 主机端口 | 子系统端口 |
|------|------|----------|------------|
| ssh | TCP | 2222 | 22 |
| dashboard | TCP | 18789 | 18789 |
| gogame | TCP | 8080 | 8080 |

---

## 第 4 步：安装 Ubuntu Server

双击 VM 启动，按以下步骤操作：

| 步骤 | 屏幕 | 你的选择 |
|------|------|----------|
| Language | 选语言 | **English** |
| Keyboard | 键盘 | **English (US)** |
| Type | 安装类型 | **Ubuntu Server** |
| Network | 网络 | 直接 Done |
| Proxy | 代理 | 留空 Done |
| Mirror | 镜像 | 默认 Done |
| Storage | 磁盘 | **Use entire disk** → Done → Continue |
| ⚠️ LVM | 是否用 LVM | **不要勾选**（按空格取消） |
| Profile | 用户信息 | 见下表 |
| ⚠️ SSH | SSH 服务 | **✅ 必须勾选 Install OpenSSH server** |
| Snaps | 附加软件 | 跳过 Done |

**Profile 填写：**

| 字段 | 值 |
|------|-----|
| Your name | `openclaw` |
| Server name | `openclaw-vm` |
| Username | `openclaw` |
| Password | `openclaw123` |

> ⚠️ SSH 那步不勾选，后面无法远程连接！

安装约 5-10 分钟。完成后 **Reboot Now**。

---

## 第 5 步：配置 SSH 连接

### 测试密码登录
```powershell
ssh openclaw@localhost -p 2222
# 密码：openclaw123
```

### 注入 SSH 密钥
```powershell
type E:\openclaw_key.pub | ssh openclaw@localhost -p 2222 "cat >> ~/.ssh/authorized_keys"
```

### 创建 SSH 别名
在 PowerShell 中运行：
```powershell
notepad $env:USERPROFILE\.ssh\config
```

粘贴：
```
Host openclaw-vm
  HostName localhost
  Port 2222
  User openclaw
  IdentityFile E:/openclaw_key
  StrictHostKeyChecking no
  LocalForward 18789 127.0.0.1:18789
  LocalForward 8080 127.0.0.1:8080
```

之后只需 `ssh openclaw-vm`。

---

## 第 6 步：安装 OpenCLAW

SSH 连接到 VM：
```bash
ssh openclaw-vm
```

### 配置免密码 sudo
```bash
echo "openclaw123" | sudo -S bash -c 'echo "openclaw ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/openclaw'
```

### 安装
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### 配置 PATH
```bash
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 第 7 步：初始化 OpenCLAW

```bash
# 初始化向导
openclaw onboard
# 安全声明页面 → 选 Yes

# 安装网关为系统服务（开机自启）
openclaw gateway install --force
openclaw gateway start

# 检查状态
openclaw status
# 看到 "Runtime: running" = 成功
```

浏览器访问 `http://localhost:18789`（需要 SSH 隧道连通）。

---

## 第 8 步：部署围棋游戏

### 复制游戏文件到 VM
```bash
# 在 VM 上
mkdir -p ~/go-game

# 从宿主机复制（PowerShell）
type index.html | ssh openclaw-vm "cat > ~/go-game/index.html"
```

### 启动 HTTP 服务器
```bash
# 在 VM 上
cd ~/go-game
python3 -m http.server 8080 &
```

### 访问
浏览器打开 `http://localhost:8080`

---

## 常见问题

### SSH 连不上
```bash
# 在 VM 里检查
systemctl status ssh
# 开启密码认证
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

### curl 下载中断
```bash
curl -C - --retry 5 -fsSL https://openclaw.ai/install.sh | bash
```

### 虚拟机启动黑屏
确保 VirtualBox 驱动完整安装（C 盘）。

### 磁盘空间不足
建议分配 ≥ 30GB。Ubuntu 最小安装约需 4GB。

---

## 命令速查

### VirtualBox
```powershell
VBoxManage list vms                     # 列出所有 VM
VBoxManage list runningvms              # 运行中的 VM
VBoxManage startvm "Ubuntu-OpenCLAW" --type headless  # 无界面启动
VBoxManage controlvm "Ubuntu-OpenCLAW" acpipowerbutton  # 正常关机
VBoxManage controlvm "Ubuntu-OpenCLAW" poweroff         # 强制关机
VBoxManage unregistervm "Ubuntu-OpenCLAW" --delete      # 删除 VM
```

### SSH
```bash
ssh -p 2222 openclaw@localhost          # 密码登录
ssh -i E:/openclaw_key -p 2222 openclaw@localhost  # 密钥登录
ssh openclaw-vm                         # 使用别名
```

### OpenCLAW
```bash
openclaw status           # 查看状态
openclaw gateway start    # 启动网关
openclaw gateway stop     # 停止网关
openclaw tui              # 终端 UI
openclaw --help           # 帮助
```

---

## 总结

```
✅ 下载文件          → 15 分钟（等下载）
✅ 安装 VirtualBox   → 5 分钟
✅ 创建 VM          → 3 分钟
✅ 安装 Ubuntu      → 10 分钟
✅ 配置 SSH         → 5 分钟
✅ 安装 OpenCLAW    → 10 分钟
✅ 初始化           → 5 分钟
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   实际操作时间     → 约 40 分钟
```

🎉 完成！你现在有了一个运行 OpenCLAW 的 Ubuntu 虚拟机。

---

> 本教程是 [围棋 · Claude vs OpenCLAW](https://github.com) 项目的一部分。
> 欢迎提交 Issue 或 PR 改进本文档。
