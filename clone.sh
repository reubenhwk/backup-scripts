#!/usr/bin/env bash

DEV=$1
PART=${DEV}1
TMNT=
MNT=

die () {
	echo "error: $@, exiting"
	exit 1
}

second_guess () {
	local DEVICE_INFO=$(fdisk -l $DEV | head -n 1)
	if [ "$DEVICE_INFO" = "" ] ; then
		die "failed to get disk info on $DEV"
	fi

	echo -n "Use $DEVICE_INFO? (y/n) [n]: "
	read yesno
	if [ "$yesno" != "y" ] ; then
		exit
	fi
}

mount_device () {
	MNT=$(cat /proc/mounts | grep $PART | cut -d\  -f2)
	if (( $? == 0 )) ; then
		TMNT=$(mktemp -d)
		MNT=$TMNT
		mkdir -p $MNT || die "unable to mkdir $MNT"
		mount $PART $MNT || die "unable to mount $PART on $MNT"
	fi
}

clone_fs () {
	rsync -av /home /bin /boot /etc /lib /lib64 /opt /root /sbin /srv /usr /var $MNT/. || die "rsync failed"
	mkdir -p $MNT/{dev,proc,run,sys,tmp}
}

rewrite_grub () {
	for d in dev proc run sys ; do
		mount --bind /$d $MNT/$d || die "failed to mount --bind /$d $MNT/$d"
	done

cat << EOF > $MNT/etc/default/grub
GRUB_DEFAULT=0
GRUB_TIMEOUT=20
#GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo "Reuben Reboot Lunux Backup"`
GRUB_DISTRIBUTOR="Reuben Reboot Lunux Backup"
#GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""
EOF

cat << EOF > $MNT/tmp/grub.sh
#!/usr/bin/env bash
sed -i 's/GRUB_TIMEOUT=.*$/GRUB_TIMEOUT=30/g' /etc/default/grub
echo GRUB_DISABLE_OS_PROBER=true >> /etc/default/grub
grub-install $DEV
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

rewrite_fstab () {
	local UUID=$(blkid $PART | cut -d\" -f2)

cat << EOF > $MNT/etc/fstab
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
UUID=$UUID / auto    errors=remount-ro 0       1
EOF

}

cleanup () {
	if [ "$TMNT" != "" ] ; then
		umount $TMNT && rmdir $TMNT
	fi
}

main () {
	#prepare_device
	second_guess
	mount_device
	clone_fs
	rewrite_fstab
	rewrite_grub
	cleanup
}

main

