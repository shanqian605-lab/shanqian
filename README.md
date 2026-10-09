# video-transcript — Codex 视频/音频逐字转写 Skill

把本地视频或音频文件转写成**带时间轴的逐字稿**，支持任意语言自动识别，可输出原文 + 中文对照的翻译文档。基于 faster-whisper，**全部本地处理，媒体文件不会上传**。

## 团队成员如何安装（三选一）

### 方式 A：对 Codex 说一句话（推荐，需 skill 在 GitHub 上）
如果团队已把本仓库推到 GitHub（例如 `your-team/codex-skills`），直接对 Codex 说：

> 帮我安装 your-team/codex-skills 仓库里的 video-transcript skill

Codex 会通过内置的 skill-installer 自动下载安装。

### 方式 B：本地一键脚本
拿到本文件夹后：
- **Windows**：在文件夹内运行 `powershell -ExecutionPolicy Bypass -File install.ps1`
- **macOS/Linux**：运行 `bash install.sh`

### 方式 C：手动复制
把 `video-transcript/` 整个文件夹复制到 `~/.codex/skills/` 目录下。

安装后**重启 Codex 或开新对话**生效。

## 安装后怎么用

直接对 Codex 说，例如：
- 「帮我总结这个视频的逐字脚本」
- 「把这个采访录音转成文字稿并翻译成中文」

## 首次使用说明

- 首次运行会自动安装 `faster-whisper` 并下载 Whisper 模型（约几百 MB，需联网，仅需一次）。
- 默认使用 small 模型（CPU 可跑）；要更高精度可让 Codex 改用 medium / large-v3。
- 支持 .mov / .mp4 / .mp3 / .wav / .m4a 等常见格式。

## 目录结构

```
video-transcript-skill/
├── install.ps1            # Windows 一键安装
├── install.sh             # macOS/Linux 一键安装
└── video-transcript/      # skill 本体（复制此文件夹即完成手动安装）
    ├── SKILL.md           # 触发条件 + 流程 + 已知坑
    ├── agents/openai.yaml
    └── scripts/transcribe.py
```
