#!/usr/bin/env bash
# install.sh - 安装 video-transcript skill 到 Codex
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/video-transcript"
DEST_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
DEST="$DEST_ROOT/video-transcript"
if [ -d "$DEST" ]; then
  read -r -p "已存在 $DEST，覆盖安装? (y/N) " ans
  [ "$ans" = "y" ] || { echo "已取消"; exit 0; }
  rm -rf "$DEST"
fi
mkdir -p "$DEST_ROOT"
cp -R "$SRC" "$DEST"
echo "安装完成 -> $DEST"
echo "重启 Codex 或开启新对话后，直接说「帮我转写这个视频」即可使用。"
