#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""
import os
import sys


QEMU_EXEC = "qemu-system-arm"
PI_OS_IMAGE_LITE = "pios/2023-10-10-raspios-bookworm-armhf-lite-autologin-ssh-expanded-rm-copy.img"
PI_OS_IMAGE_DESKTOP = "pios/2023-12-05-raspios-bookworm-armhf.img"
KERNEL_IMAGE = "kernel/zImage"


def qemu_executable():
    # Add .exe if running on Windows
    return f"{QEMU_EXEC}{'.exe' if os.name == 'nt' else ''}"


def launch_qemu(args):
    qemu_cmd = f"{qemu_executable()} {' '.join(args)}"
    print(f"Running:\n{qemu_cmd}")
    return os.system(qemu_cmd)


def get_os_image():
    return os.path.abspath(PI_OS_IMAGE_LITE)


def get_kernel_image():
    return os.path.abspath(KERNEL_IMAGE)


def get_qemu_args():
    return [
        '-machine', 'virt',
        '-cpu', 'cortex-a7',
        '-smp', '3', 
        '-m', '1024m',
        '-drive', f'"format=raw,file={get_os_image()},if=none,id=hd0"',
        '-device', '"virtio-blk-device,drive=hd0,bootindex=0"',
        '-netdev', '"user,id=mynet,hostfwd=tcp::5022-:22"',
        '-device', '"virtio-net-device,netdev=mynet"',
        '-kernel', f'"{get_kernel_image()}"',
        '-append', '"rw earlyprintk loglevel=8 console=ttyAMA0,115200 dwc_otg.lpm_enable=0 root=/dev/vda2 rootwait panic=1"',
        '-no-reboot',
        '-display', 'none',
        '-serial', 'mon:stdio',
    ]


def main():
    qemu_cmd = get_qemu_args()
    return launch_qemu(get_qemu_args())


if __name__ == "__main__":
    sys.exit(main())
