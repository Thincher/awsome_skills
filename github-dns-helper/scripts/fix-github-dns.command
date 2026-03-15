#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/fix_github_dns.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    osascript -e 'display dialog "错误: 找不到脚本文件" buttons {"确定"} default button 1'
    exit 1
fi

echo "=================================================="
echo "🔧 GitHub DNS 修复工具 - macOS 启动器"
echo "=================================================="
echo "系统: $(uname -s)"
echo "Python 版本: $(python3 --version 2>&1 | awk '{print $2}')"
echo "脚本路径: $PYTHON_SCRIPT"
echo "=================================================="
echo ""

python3 "$PYTHON_SCRIPT" "$@"

if [ $? -eq 0 ]; then
    osascript -e 'display dialog "✅ GitHub DNS 修复完成！" buttons {"确定"} default button 1'
else
    osascript -e 'display dialog "❌ GitHub DNS 修复失败！" buttons {"确定"} default button 1'
fi