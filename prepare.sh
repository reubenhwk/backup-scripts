#!/usr/bin/env bash

prepare_device () {
	local FSTYPE=$2
	(echo o; echo n; echo p; echo 1; echo; echo; echo a; echo w) | fdisk $1
	mkfs.$FSTYPE -F -F $PART
	partprobe
}


