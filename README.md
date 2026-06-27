# Custom Linux Container Virtualization Engine (Python & C)

A systems-level engineering project executing OS-level virtualization from scratch. This repository serves as a progressive development sandbox used to build a lightweight container runtime by directly interfacing with low-level Linux kernel primitives.

The project transitions from basic process spawning to an isolated, resource-constrained execution bubble, mimicking core functionalities found in modern container runtimes like Docker and runC.

---

## 🏗️ Core Architectural Mechanics Implemented

The architecture is developed sequentially across isolated verification targets, culminating in a monolithic runtime:

* **Process Lifecycles (`00_fork_exec`):** Managing deterministic process isolation using bare-metal POSIX fork/exec pipelines.
* **Storage Isolation & Jails (`01_chroot_image` to `04_overlay`):** Constructing secure root directory sandboxes via `os.chroot` and advanced multi-layered storage compilation patterns using Union/Overlay filesystems.
* **Kernel Namespace Desegregation (`05_uts_namespace` to `07_net_namespace`):** Programmatically unsharing system kernels using `CLONE_NEWPID`, `CLONE_NEWUTS`, `CLONE_NEWNS`, and `CLONE_NEWNET` to fully decouple process trees, network routing tables, and host contexts.
* **Resource Constraint Boundaries (`08_cpu_cgroup` & `09_memory_cgroup`):** Interfacing directly with the Linux kernel `/sys/fs/cgroup` controller pathway to throttle maximum CPU allocation slices and force memory exhaustion walls.
* **Privilege De-escalation (`10_setuid`):** Dropping structural kernel capabilities and lowering user permissions inside the execution environment to enforce secure, non-root sandbox execution boundaries.

---

## 🚀 Production Entrypoint: `run_container.py`

While the subdirectory branches contain granular educational step-logs exploring specific primitives, a compiled, production-ready monolithic runtime script has been engineered directly in the root folder:

```bash
# Bootstrapping an isolated, secure shell sandbox via the runtime engine
sudo python3 run_container.py /bin/bash
