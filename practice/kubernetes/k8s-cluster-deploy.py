#!/usr/bin/env python3
import os
import subprocess
import re
import shutil

server = [
    {"type": "harbor", "name": "harbor.labworlds.cc", "ip": "192.168.110.164"},
    {"type": "master", "name": "k8s-master1-175", "ip": "192.168.110.175"},
    {"type": "master", "name": "k8s-master2-176", "ip": "192.168.110.176"},
    {"type": "master", "name": "k8s-master3-177", "ip": "192.168.110.177"},
    {"type": "node", "name": "k8s-node-yy-137", "ip": "192.168.110.137"},
    {"type": "node", "name": "k8s-node-yqn-171", "ip": "192.168.110.171"},
    {"type": "node", "name": "k8s-node-yqn-172", "ip": "192.168.110.172"},
    {"type": "node", "name": "k8s-node-shiqi-8", "ip": "192.168.110.8"},
    {"type": "node", "name": "k8s-node-ll-93", "ip": "192.168.110.93"},
    {"type": "node", "name": "k8s-node-xtx-117", "ip": "192.168.110.117"},
    {"type": "node", "name": "k8s-node-wyf-88", "ip": "192.168.110.88"},
    {"type": "node", "name": "k8s-node-zry-112", "ip": "192.168.110.112"},
    {"type": "node", "name": "k8s-node-xy-155", "ip": "192.168.110.155"},
    {"type": "node", "name": "k8s-node-yyq-32", "ip": "192.168.110.32"},
    {"type": "node", "name": "k8s-node-syy-38", "ip": "192.168.110.38"},
    {"type": "node", "name": "k8s-node-myh-77", "ip": "192.168.110.77"},
    {"type": "node", "name": "k8s-node-zgz-96", "ip": "192.168.110.96"},
    {"type": "node", "name": "k8s-node-zrq-126", "ip": "192.168.110.126"},
    {"type": "node", "name": "k8s-node-zrq-127", "ip": "192.168.110.127"},
    {"type": "node", "name": "k8s-node-zwj-71", "ip": "192.168.110.71"},
    {"type": "node", "name": "k8s-node-zyz-178", "ip": "192.168.110.178"},
    {"type": "node", "name": "k8s-node-lbw-56", "ip": "192.168.110.56"},
    {"type": "node", "name": "k8s-node-lby-12", "ip": "192.168.110.12"},
    {"type": "node", "name": "k8s-node-lyy-122", "ip": "192.168.110.122"},
    {"type": "node", "name": "k8s-node-lp-132", "ip": "192.168.110.132"},
    {"type": "node", "name": "k8s-node-yf-52", "ip": "192.168.110.52"},
    {"type": "node", "name": "k8s-node-lyf-148", "ip": "192.168.110.148"},
    {"type": "node", "name": "k8s-node-wyt-140", "ip": "192.168.110.140"},
    {"type": "node", "name": "k8s-node-wy-61", "ip": "192.168.110.61"},
    {"type": "node", "name": "k8s-node-pfl-83", "ip": "192.168.110.83"},
    {"type": "node", "name": "k8s-node-wky-28", "ip": "192.168.110.28"},
    {"type": "node", "name": "k8s-node-wze-102", "ip": "192.168.110.102"},
    {"type": "node", "name": "k8s-node-gh-107", "ip": "192.168.110.107"},
    {"type": "node", "name": "k8s-node-gh-108", "ip": "192.168.110.108"},
    {"type": "node", "name": "k8s-node-zx-17", "ip": "192.168.110.17"},
    {"type": "node", "name": "k8s-node-slq-42", "ip": "192.168.110.42"},
    {"type": "node", "name": "k8s-node-fbl-46", "ip": "192.168.110.46"},
    {"type": "node", "name": "k8s-node-wxy-23", "ip": "192.168.110.23"},
    {"type": "node", "name": "k8s-node-hjc-68", "ip": "192.168.110.68"},
    {"type": "node", "name": "k8s-node-hfg-153", "ip": "192.168.110.153"}
]

def run_command(command, shell=False):
    try:
        print(f"运行命令: {command}")
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[错误] 命令执行失败: {e}")
        
def backup_file(filepath):
    if os.path.exists(filepath):
        backup_path = filepath + ".bak"
        if not os.path.exists(backup_path):
            shutil.copy(filepath, backup_path)
            print(f"[备份] {filepath} -> {backup_path}")
        else:
            print(f"[跳过备份] {backup_path} 已存在")

def set_hostname(ip):
    for s in server:
        if s["ip"] == ip:
            hostname = s["name"]
            run_command(["hostnamectl", "set-hostname", hostname])
            return hostname
    return None

def update_hosts(ip):
    backup_file("/etc/hosts")
    lines = [
        "127.0.0.1       localhost\n",
        f"127.0.1.1       {set_hostname(ip)}\n",
        "::1     ip6-localhost ip6-loopback\n",
        "fe00::0 ip6-localnet\n",
        "ff00::0 ip6-mcastprefix\n",
        "ff02::1 ip6-allnodes\n",
        "ff02::2 ip6-allrouters\n",
    ]
    with open("/etc/hosts", "w") as f:
        f.writelines(lines)
        for s in server:
            f.write(f"{s['ip']} {s['name']}\n")

def replace_apt_sources():
    backup_file("/etc/apt/sources.list")
    apt_source = """deb https://mirrors.aliyun.com/ubuntu/ noble main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ noble main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ noble-security main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ noble-security main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ noble-updates main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ noble-updates main restricted universe multiverse
deb https://mirrors.aliyun.com/ubuntu/ noble-backports main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ noble-backports main restricted universe multiverse
"""
    with open("/etc/apt/sources.list", "w") as f:
        f.write(apt_source)
    run_command(["apt", "update"])
    run_command(["apt", "list", "--upgradable"])

def disable_firewall():
    run_command(["systemctl", "stop", "ufw"])
    run_command(["systemctl", "disable", "ufw"])

def configure_kernel():
    backup_file("/etc/fstab")
    backup_file("/etc/modules-load.d/k8s.conf")
    run_command(["swapoff", "-a"])
    run_command(["sed", "-i", "/ swap / s/^\\(.*\\)$/#\\1/g", "/etc/fstab"])

    with open("/etc/modules-load.d/k8s.conf", "w") as f:
        f.write("overlay\nbr_netfilter\n")

    run_command(["modprobe", "overlay"])
    run_command(["modprobe", "br_netfilter"])

    with open("/etc/sysctl.d/k8s.conf", "w") as f:
        f.write("""net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
""")
    run_command(["sysctl", "--system"])

def install_dependencies():
    run_command([
        "apt", "install", "-y", "apt-transport-https", "ca-certificates", "curl",
        "software-properties-common", "gnupg", "lsb-release", "net-tools",
        "ntpdate", "chrony"
    ])

def configure_chrony():
    chrony_conf = "/etc/chrony/chrony.conf"
    backup_file(chrony_conf)
    if os.path.exists(chrony_conf):
        with open(chrony_conf, "r") as f:
            lines = f.readlines()

        new_servers = [
            "server ntp.aliyun.com iburst\n",
            "server cn.pool.ntp.org iburst\n",
            "server ntp1.aliyun.com iburst\n",
            "server ntp2.aliyun.com iburst\n",
            "server ntp.tencent.com iburst\n"
        ]

        with open(chrony_conf, "w") as f:
            for line in lines:
                if line.strip().startswith("pool") or line.strip().startswith("server"):
                    f.write("# " + line if not line.startswith("#") else line)
                else:
                    f.write(line)
            for s in new_servers:
                f.write(s)

    run_command(["systemctl", "restart", "chrony"])
    run_command(["systemctl", "enable", "chrony"])
    run_command(["chronyc", "sources"])

def install_containerd():
    backup_file("/etc/apt/sources.list.d/docker.list")
    run_command(["curl", "-fsSL", "http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg", "|", "apt-key", "add", "-"], shell=True)
    run_command(
        "echo 'deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable' > /etc/apt/sources.list.d/docker.list",
        shell=True
    )
    run_command(["apt-get", "update"])
    run_command(["dpkg", "--configure", "-a"])
    run_command([
        "apt-get", "install", "-y",
        "docker-ce", "docker-ce-cli", "containerd.io",
        "docker-buildx-plugin", "docker-compose-plugin"
    ])
    backup_file("/etc/crictl.yaml")
    with open("/etc/crictl.yaml", "w") as f:
        f.write("""runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 10
debug: false
""")

    run_command("containerd config default > /etc/containerd/config.toml", shell=True)
    patch_containerd_config()

def patch_containerd_config():
    config_file = "/etc/containerd/config.toml"
    backup_file(config_file)
    print("[INFO] 正在修改 containerd config.toml 中的 sandbox_image 和 config_path")
    if not os.path.exists(config_file):
        print(f"[ERROR] 配置文件 {config_file} 不存在")
        return

    with open(config_file, "r") as f:
        content = f.read()

    content = re.sub(r'sandbox_image\s*=\s*".*?"',
                     'sandbox_image = "registry.aliyuncs.com/google_containers/pause:3.8"', content)
    content = re.sub(r'SystemdCgroup\s*=\s*(?:"[^"]*"|\w+)',
                    'SystemdCgroup = true', content)
    content = re.sub(r'config_path\s*=\s*".*?"',
                     'config_path = "/etc/containerd/certs.d"', content)

    with open(config_file, "w") as f:
        f.write(content)

    print("[INFO] config.toml 修改完成")

def configure_registry():
    registries = {
        "harbor.labworlds.cc": """server = "http://harbor.labworlds.cc"
[host."http://harbor.labworlds.cc"]
  capabilities = ["pull", "resolve", "push"]
  skip_verify = true
""",
        "docker.io": """server = "https://docker.io"
  [host."https://docker.mirrors.ustc.edu.cn"]
    capabilities = ["pull", "resolve"]
  [host."https://hub-mirror.c.163.com"]
    capabilities = ["pull", "resolve"]
  [host."https://docker.io"]
    capabilities = ["pull", "resolve"]
""",
        "registry.k8s.io": """server = "https://registry.k8s.io"
  [host."https://registry.aliyuncs.com/google_containers"]
    capabilities = ["pull", "resolve"]
  [host."https://registry.k8s.io"]
    capabilities = ["pull", "resolve"]
""",
        "quay.io": """server = "https://quay.io"
  [host."https://quay.mirrors.ustc.edu.cn"]
    capabilities = ["pull", "resolve"]
  [host."https://quay.io"]
    capabilities = ["pull", "resolve"]
"""
    }

    for domain, content in registries.items():
        dir_path = f"/etc/containerd/certs.d/{domain}"
        backup_file(dir_path + "/hosts.toml")
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "hosts.toml")
        with open(file_path, "w") as f:
            f.write(content)
        os.chmod(file_path, 0o600)

    run_command(["systemctl", "daemon-reexec"])
    run_command(["systemctl", "daemon-reload"])
    run_command(["systemctl", "restart", "containerd"])
    run_command(["systemctl", "enable", "containerd"])

def pull_pause_image():
    result = subprocess.run(["ctr", "-n", "k8s.io", "images", "list"], capture_output=True, text=True)
    if "registry.k8s.io/pause:3.8" in result.stdout:
        print("[INFO] 镜像 registry.k8s.io/pause:3.8 已存在，跳过拉取")
        return
    run_command(["ctr", "-n", "k8s.io", "images", "pull", "registry.aliyuncs.com/google_containers/pause:3.8"])
    run_command([
        "ctr", "-n", "k8s.io", "images", "tag",
        "registry.aliyuncs.com/google_containers/pause:3.8",
        "registry.k8s.io/pause:3.8"
    ])

def install_kubernetes():
    run_command(["curl", "-s", "https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg", "|", "apt-key", "add", "-"], shell=True)
    with open("/etc/apt/sources.list.d/kubernetes.list", "w") as f:
        f.write("deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main\n")
    run_command(["apt-get", "update"])
    run_command(["apt-get", "install", "-y", "kubelet", "kubeadm", "kubectl"])
    run_command(["apt-mark", "hold", "kubelet", "kubeadm", "kubectl"])

if __name__ == "__main__":
    local_ip = subprocess.getoutput("hostname -I").strip().split()[0]
    set_hostname(local_ip)
    update_hosts(local_ip)
    replace_apt_sources()
    disable_firewall()
    configure_kernel()
    install_dependencies()
    configure_chrony()
    install_containerd()
    configure_registry()
    pull_pause_image()
    install_kubernetes()
