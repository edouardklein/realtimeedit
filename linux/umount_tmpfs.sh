#!/bin/sh

# This program has two features.
#
# 1. Unmount a disk image.
# 2. Detach the disk image from RAM.
#
# Usage:
#   $0 <dir>
#
#   dir:
#     The `dir' is a directory, the dir is mounting a disk image.
#

if [ $# -lt 1 ]; then
    echo "Usage: $0 <mount point>" >&2
    exit 1
fi

mount_point=$1
if [ ! -d "${mount_point}" ]; then
    echo "The mount point isn't available." >&2
    exit 1
fi
mount_point=$(cd $mount_point && pwd)

sudo umount "${mount_point}"
if [ $? -ne 0 ]; then
    echo "Could not unmount." >&2
    exit $?
fi

