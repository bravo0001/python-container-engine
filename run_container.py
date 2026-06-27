import os
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Bravo Engine: Custom Linux Container Runtime")
    parser.add_argument("command", nargs="+", help="Command to execute inside the container (e.g., /bin/bash)")
    return parser.parse_args()

def contain_process(args):
    print(f"[!] Initializing container containment layers (PID: {os.getpid()})...")
    
    # 1. Isolate Hostname (UTS Namespace)
    try:
        os.sethostname(b"bravo-isolated-node")
    except PermissionError:
        print("[-] Execution halted: Root privileges (sudo) required.")
        sys.exit(1)

    # 2. Isolate File System (Chroot Jail over rootfs)
    rootfs_dir = os.path.abspath("./rootfs")
    if not os.path.exists(rootfs_dir):
        print(f"[-] Missing file layer target: {rootfs_dir}. Downloading fallback layer...")
        os.system("wget -q https://github.com/ericchiang/containers-from-scratch/raw/master/rootfs.tar.gz")
        os.system("mkdir -p rootfs && tar -xzf rootfs.tar.gz -C ./rootfs")
        
    os.chroot(rootfs_dir)
    os.chdir("/")

    # 3. Mount Isolated Process tracking layer
    if not os.path.exists("/proc"):
        os.makedirs("/proc")
    os.system("mount -t proc proc /proc")

    # 4. Hand off execution to target isolated shell binary
    print("[+] Shifting environment matrix context. Entering container space...")
    try:
        os.execvp(args.command[0], args.command)
    except Exception as e:
        print(f"[-] Operational runtime failure: {e}")
        sys.exit(1)

def main():
    args = parse_arguments()
    
    # Linux kernel primitive constants for system namespace unsharing
    CLONE_NEWPID = 0x20000000  
    CLONE_NEWUTS = 0x04000000  
    CLONE_NEWNS  = 0x00020000  

    import ctypes
    libc = ctypes.CDLL('libc.so.6', use_errno=True)
    
    if libc.unshare(CLONE_NEWPID | CLONE_NEWUTS | CLONE_NEWNS) != 0:
        print("[-] Namespace structural extraction failure. Run using sudo.")
        sys.exit(1)

    child_pid = os.fork()
    if child_pid == 0:
        contain_process(args)
    else:
        _, status = os.waitpid(child_pid, 0)
        print(f"\n[!] Container session terminated securely (Exit status: {status}).")

if __name__ == "__main__":
    main()