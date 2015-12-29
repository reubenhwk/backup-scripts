#!/usr/bin/env bash

DEV=/dev/sdd
FSTYPE=ext4
PART=${DEV}1
TMP=$(mktemp -d)
MNT=$TMP/mnt

die () {
	echo "$@"
	exit 1
}

prepare_device () {
	(echo o; echo n; echo p; echo 1; echo; echo; echo a; echo w) | fdisk $DEV
	partprobe
	mkfs.$FSTYPE -F -F $PART
}

mount_device () {
	mkdir -p $MNT || die "unable to mkdir $MNT"
	mount $PART $MNT || die "unable to mount $PART on $MNT"
}

clone_fs () {
	rsync -av /bin /boot /etc /lib /lib64 /opt /root /sbin /srv /usr /var $MNT/. || die "rsync failed"
	mkdir -p $MNT/{dev,home,proc,run,sys,tmp}
}

do_grub () {
	for d in dev proc run sys ; do
		mount --bind /$d $MNT/$d || die "failed to mount --bind /$d $MNT/$d"
	done

	grub-install $DEV || die "grub-install $DEV failed"

	sed -i 's/GRUB_TIMEOUT=.*$/GRUB_TIMEOUT=30/g' /etc/default/grub

cat << EOF > $MNT/tmp/grub.sh
#!/usr/bin/env bash
update-grub
EOF
	chmod +x $MNT/tmp/grub.sh
	(
		chroot $MNT /tmp/grub.sh
	)
	rm $MNT/tmp/grub.sh

	for d in dev proc run sys ; do
		umount $MNT/$d
	done
}

do_fstab () {
	local UUID=$(blkid $PART | cut -d\" -f2)

cat << EOF > $MNT/etc/fstab
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/sda1 during installation
UUID=$UUID /               $FSTYPE    errors=remount-ro 0       1
EOF

}

cleanup () {
	umount $MNT
	rm -rf $TMP
}

main () {
	#prepare_device
	mount_device
	clone_fs
	do_grub
	do_fstab
	cleanup
}

main
