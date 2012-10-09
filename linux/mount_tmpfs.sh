#!/bin/sh

# This program has two feature.
#
# 1. Create a disk image on RAM.
# 2. Mount that disk image.
#
# Usage:
#   $0 <dir> <size>
#
#   size:
#     The `size' is a size of disk image (MB).
#
#   dir:
#     The `dir' is a directory, the dir is used to mount the disk image.
#

if [ $# -lt 1 ]; then
    cat <<EOF >&2
Usage: $0 <dir> [size]
Creates a disk image of the given size in megabyte (default: 64) and mounts it at the given directory.
EOF
    exit 1
fi

mount_point=${1}
size=${2:-64}

mkdir -p $mount_point
if [ $? -ne 0 ]; then
    echo "The mount point isn't available." >&2
    exit $?
fi


sudo mount -t tmpfs -o size=${size}M tmpfs ${mount_point}
if [ $? -ne 0 ]; then
    echo "Could not mount disk image." >&2
    exit $?
fi
