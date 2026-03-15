#!/usr/bin/env python3
import subprocess
import os
import sys
import datetime
import argparse
import platform

VERSION = "2.0.0"
DEFAULT_HOSTS_URLS = [
    "https://raw.hellogithub.com/hosts",
    "https://fastly.jsdelivr.net/gh/AutismSuperman/github-dns/hosts",
    "https://ghp.ci/https://raw.hellogithub.com/hosts",
    "https://mirror.ghproxy.com/https://raw.hellogithub.com/hosts",
    "https://ghproxy.com/https://raw.hellogithub.com/hosts"
]

# 平台检测
SYSTEM = platform.system()
IS_WINDOWS = SYSTEM == "Windows"
IS_MACOS = SYSTEM == "Darwin"
IS_LINUX = SYSTEM == "Linux"

# 平台相关配置
if IS_WINDOWS:
    HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"
    BACKUP_DIR = os.path.expanduser("~/Documents/host_back")
elif IS_MACOS or IS_LINUX:
    HOSTS_FILE = "/etc/hosts"
    BACKUP_DIR = os.path.expanduser("~/Documents/host_back")
else:
    HOSTS_FILE = "/etc/hosts"
    BACKUP_DIR = os.path.expanduser("~/Documents/host_back")

MARKER_START = "# --- GitHub_START ---"
MARKER_END = "# --- GitHub_END ---"


def parse_args():
    parser = argparse.ArgumentParser(
        description='GitHub DNS 修复工具 - 自动修复 GitHub 访问问题',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python3 fix_github_dns.py              # 自动修复
  python3 fix_github_dns.py -u URL       # 使用自定义 hosts 源
  python3 fix_github_dns.py --check      # 仅检查连接状态
        '''
    )
    parser.add_argument('-u', '--urls', nargs='+', help='自定义 hosts URL 地址列表')
    parser.add_argument('--check', action='store_true', help='仅检查 GitHub 连接状态，不进行修复')
    parser.add_argument('-v', '--version', action='version', version=f'GitHub DNS Helper v{VERSION}')
    return parser.parse_args()


def get_hosts_urls(args=None):
    if args is None:
        args = parse_args()
    if args.urls:
        return args.urls
    return DEFAULT_HOSTS_URLS


def run_command(cmd, sudo=False):
    if sudo:
        cmd = f"sudo {cmd}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def print_status(msg, success=True):
    prefix = "✅" if success else "❌"
    print(f"{prefix} {msg}")


def extract_github_hosts(content):
    start_markers = ["# --- SWITCHHOSTS_CONTENT_START ---", "# GitHub hosts start", "# GitHub520 Host Start"]
    end_marker = "# GitHub520 Host End"

    for start_marker in start_markers:
        start_idx = content.find(start_marker)
        if start_idx != -1:
            end_idx = content.find(end_marker, start_idx)
            if end_idx != -1:
                section = content[start_idx:end_idx]
                lines = []
                for line in section.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 2:
                            lines.append(line)
                return '\n'.join(lines)
    return None


def fetch_hosts(args=None):
    hosts_urls = get_hosts_urls(args)
    for i, url in enumerate(hosts_urls, 1):
        print(f"  尝试 ({i}/{len(hosts_urls)}): {url}")
        returncode, stdout, stderr = run_command(f"curl -s --max-time 10 {url}")
        if returncode == 0 and stdout:
            github_hosts = extract_github_hosts(stdout)
            if github_hosts:
                print_status(f"成功从 {url} 获取 hosts")
                return github_hosts
        print_status(f"从 {url} 获取失败，尝试下一个...", False)
    return None


def check_github_connectivity():
    print("\n🔍 步骤 0: 检查 GitHub 连接状态...")
    domains = [
        "github.com",
        "api.github.com",
        "githubusercontent.com",
        "github.global.ssl.fastly.net",
        "raw.githubusercontent.com",
        "gist.github.com"
    ]
    
    all_success = True
    for domain in domains:
        if IS_WINDOWS:
            ping_cmd = f"ping -n 1 -w 2000 {domain}"
        else:
            ping_cmd = f"ping -c 1 -W 2 {domain}"
        
        returncode, stdout, stderr = run_command(ping_cmd)
        if returncode == 0:
            print_status(f"{domain} - 连接正常")
        else:
            print_status(f"{domain} - 连接失败", False)
            all_success = False
    
    return all_success


def main():
    args = parse_args()
    
    print("=" * 50)
    print("🔧 GitHub DNS 修复工具")
    print("=" * 50)

    is_connected = check_github_connectivity()
    
    if args.check:
        if is_connected:
            print("\n✅ GitHub 连接正常")
        else:
            print("\n❌ GitHub 连接异常")
        print("=" * 50)
        sys.exit(0 if is_connected else 1)
    
    if is_connected:
        print("\n✅ GitHub 连接正常，无需修复")
        print("=" * 50)
        sys.exit(0)
    
    print("\n⚠️  检测到 GitHub 连接异常，开始修复...")

    print("\n📥 步骤 1: 获取最新 hosts...")
    github_hosts = fetch_hosts(args)
    if not github_hosts:
        print_status("所有 hosts 源都获取失败", False)
        sys.exit(1)

    print(f"找到 GitHub hosts ({len(github_hosts.splitlines())} 条记录)")

    print("\n💾 步骤 2: 备份当前 hosts...")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"hosts_{timestamp}")

    returncode, stdout, stderr = run_command(f"cp {HOSTS_FILE} {backup_file}", sudo=False)
    if returncode == 0:
        print_status(f"已备份到 {backup_file}")
        
        # 清理旧备份，只保留最新的5个
        try:
            backup_files = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("hosts_")])
            if len(backup_files) > 5:
                files_to_delete = backup_files[:-5]
                for old_file in files_to_delete:
                    old_backup_path = os.path.join(BACKUP_DIR, old_file)
                    try:
                        os.remove(old_backup_path)
                        print(f"  🗑️  已删除旧备份: {old_file}")
                    except PermissionError:
                        print(f"  ⚠️  删除备份失败 {old_file}: 权限不足")
                    except Exception as e:
                        print(f"  ⚠️  删除备份失败 {old_file}: {e}")
        except Exception as e:
            print(f"  ⚠️  清理备份失败: {e}")
    else:
        print_status(f"备份失败: {stderr}", False)

    print("\n🗑️ 步骤 3: 清理旧的 GitHub hosts...")
    with open(HOSTS_FILE, "r") as f:
        current_hosts = f.read()

    old_section_start = current_hosts.find(MARKER_START)
    old_section_end = current_hosts.find(MARKER_END)

    if old_section_start != -1 and old_section_end != -1:
        cleaned_hosts = current_hosts[:old_section_start] + current_hosts[old_section_end + len(MARKER_END):]
    else:
        cleaned_hosts = current_hosts

    cleaned_hosts = cleaned_hosts.rstrip() + "\n"
    print_status("已清理旧的 GitHub hosts")

    print("\n✍️ 步骤 4: 写入新的 hosts...")
    hosts_urls = get_hosts_urls(args)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    final_hosts = cleaned_hosts + "\n" + MARKER_START + "\n"
    final_hosts += github_hosts + "\n"
    final_hosts += f"# Update time: {timestamp}\n"
    final_hosts += f"# Update url: {hosts_urls[0]}\n"
    final_hosts += MARKER_END + "\n"

    with open(HOSTS_FILE, "w") as f:
        f.write(final_hosts)

    print_status("已写入 hosts 文件")

    print("\n🔄 步骤 5: 刷新 DNS 缓存...")
    success = False
    
    if IS_WINDOWS:
        returncode, stdout, stderr = run_command("ipconfig /flushdns", sudo=False)
        success = returncode == 0
    elif IS_MACOS:
        returncode, stdout, stderr = run_command("dscacheutil -flushcache", sudo=False)
        returncode2, stdout2, stderr2 = run_command("killall -HUP mDNSResponder", sudo=False)
        success = returncode == 0 or returncode2 == 0
    elif IS_LINUX:
        returncode, stdout, stderr = run_command("sudo systemd-resolve --flush-caches", sudo=False)
        success = returncode == 0
    else:
        print("⚠️  未知平台，跳过 DNS 缓存刷新")

    if success:
        print_status("DNS 缓存已刷新")
    else:
        print_status(f"刷新 DNS 失败", False)

    print("\n🏓 步骤 6: 验证连接...")
    domains = ["github.com", "api.github.com", "raw.githubusercontent.com", "gist.github.com"]

    success_count = 0
    for domain in domains:
        print(f"\n  正在 ping {domain}...")
        if IS_WINDOWS:
            ping_cmd = f"ping -n 3 {domain}"
        else:
            ping_cmd = f"ping -c 3 {domain}"
        
        returncode, stdout, stderr = run_command(ping_cmd)

        if returncode == 0:
            lines = stdout.strip().split("\n")
            if lines:
                avg_time = ""
                for line in lines:
                    if "avg" in line or "rtt" in line:
                        avg_time = line
                        break
                print_status(f"{domain} - 连接成功 {avg_time if avg_time else ''}")
                success_count += 1
        else:
            print_status(f"{domain} - 连接失败", False)

    print("\n" + "=" * 50)
    if success_count == len(domains):
        print("✨ 修复完成！所有域名连接正常")
    elif success_count > 0:
        print(f"✨ 修复完成！{success_count}/{len(domains)} 个域名连接正常")
    else:
        print("⚠️  修复完成，但连接仍有问题，请检查网络设置")
    print("=" * 50)


if __name__ == "__main__":
    main()
