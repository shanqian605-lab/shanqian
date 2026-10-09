# install.ps1 - 安装 video-transcript skill 到 Codex
# 用法：右键使用 PowerShell 运行，或在终端执行：powershell -ExecutionPolicy Bypass -File install.ps1
$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot "video-transcript"
$destRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $HOME ".codex\skills" }
$dest = Join-Path $destRoot "video-transcript"
if (Test-Path $dest) {
    Write-Host "已存在: $dest"
    $ans = Read-Host "覆盖安装? (y/N)"
    if ($ans -ne "y") { Write-Host "已取消"; exit 0 }
    Remove-Item -Recurse -Force $dest
}
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
Copy-Item -Recurse -Force $src $dest
Write-Host "安装完成 -> $dest"
Write-Host "重启 Codex 或开启新对话后，直接说「帮我转写这个视频」即可使用。"
