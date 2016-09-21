
This software makes a bootable close of your system to another storage device,
or set of storage devices.  Currently, only BIOS is supported.  There is no
GPT/EFI support.

To make this bootable clone, follow these steps...

1) Partition the destination device(s) and create filesystem(s).

You must partition the device and create the filesystems yourself.  It is very
important to leave enough room on the target device for the boot loader.
Modern versions of fdisk do this by default, leaving two megabytes of empty
space before the first partition.

I plan to add tools to help you through this process at some point, but for now
you have to do it manually.  Example...

 $ sudo fdisk /dev/sdc
 $ sudo mkfs.ext4 /dev/sdc1
 $ sudo mkfs.ext4 /dev/sdc2


2) Create an fstab of your target device(s) and filesystems.

You have to tell this software how to mount the destination device filesystems.
To do this, you make an fstab.  This fstab is similar, but not identical to,
/etc/fstab.  In this file, you specify on each line a device followed by that
device's mount point.  You can also follow the mount point with a filesystem
type, but this is optional if your version of mount is smart enough to
automatically detect the filesystem type for you.  Finally, but in no
particular order, you need to specify the device on which the boot loader is to
be installed.  Example...

 $ cat ~/backup.fstab
 /dev/sdc  boot-loader
 /dev/sdc1 /boot
 /dev/sdc2 /


3) Do the clone.

Now that you have a device partitioned, filesystems created, and a backup.fstab,
you're ready to make the clone.  Just invoke lrc clone and pass the backup.fstab
on the command line as the first argument.  This will bind mount all the filesystems
in /etc/fstab somewhere in /tmp, then mount all the filesystems in your backup.fstab
somewhere in /tmp, then rsync the roots making a complete close.  The boot loader
will also be installed on the destination device specified in backup.fstab.

 $ sudo lrc clone backup.fstab

