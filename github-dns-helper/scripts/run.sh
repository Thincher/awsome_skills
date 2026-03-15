#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/fix_github_dns.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ 错误: 找不到脚本文件: $PYTHON_SCRIPT"
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
exit $?