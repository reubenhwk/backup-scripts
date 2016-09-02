
To make a clone of your system...

 $ sudo lrc clone backup.fstab

...where backup.fstab is in the format of EXAMPLE.spec.  It's similar to
/etc/fstab, but does away with the options, the filesystem type is optional,
and it adds an extra line telling 'lrc clone' on which device to install the
boot loader.  An example...

 /dev/sdc  boot-loader
 /dev/sdc1 /boot
 /dev/sdc2 /

At this point, you must partition the device yourself and create the
filesystems.  I plan to add tools to help you through this process at some
point, but for now you have to do that.
