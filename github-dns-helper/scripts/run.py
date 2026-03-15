#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    python_script = os.path.join(script_dir, "fix_github_dns.py")
    
    if not os.path.exists(python_script):
        print(f"错误: 找不到脚本文件: {python_script}")
        sys.exit(1)
    
    print("=" * 50)
    print("🔧 GitHub DNS 修复工具 - 启动器")
    print("=" * 50)
    print(f"系统: {platform.system()}")
    print(f"Python 版本: {sys.version.split()[0]}")
    print(f"脚本路径: {python_script}")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, python_script] + sys.argv[1:], check=True)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 执行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()