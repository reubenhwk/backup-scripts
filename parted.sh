#!/bin/bash

set -e -u

# Use /dev/disk/by-id
device=$1

if [[ ! $device =~ /dev/disk/by-id/* ]] ; then
	echo "usage: $0 /dev/disk/by-id/<disk>" >&2
	exit 1
fi

# Make this storage device GPT
parted --script $device mklabel gpt

# Create a 510 Mib partition for EFI and set the ESP flag on it.
parted --script -a optimal -- $device mkpart primary fat32 1Mib 300Mib
parted --script $device set 1 esp on

# Create a big partition ending 2048 sectors before the last sector
parted --script -a optimal -- $device mkpart primary ext4 300Mib -2048s

# Wait for devfs to see the new partitions...
sleep 1

# This is why the usage mandates /dev/disk/by-id/*   ...because the partition
# names are so predictable.
mkfs.vfat -F32 ${device}-part1
mkfs.ext4 ${device}-part2
