/*
 * This program reads the disk id value
 * from the MBR and prints it.  The value
 * can be verified with fdisk like so...
 *
 * sudo fdisk -l /dev/sda | grep "Disk identifier"
 */

#include <stdint.h>
#include <stdio.h>

int main(int argc, char * argv[])
{
	char * dev = argv[1];
	FILE * f = fopen(dev, "rb");
	fseek(f, 440, SEEK_SET);
	uint32_t id = 0;
	fread(&id, sizeof(id), 1, f);
	fclose(f);
	printf("0x%08x\n", id);
	return 0;
}

