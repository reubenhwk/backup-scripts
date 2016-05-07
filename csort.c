
#include <stdlib.h>
#include <stdio.h>

#define LINES 128
#define LINE_MAX 1024

int main(int argc, char * argv[])
{
	char lines[LINES][LINE_MAX];
	int line_count = 0;
	while (line_count < LINES, fgets(lines[line_count++], LINE_MAX, stdin));

	for (int i = 0; i < line_count; ++i) {
		printf("%s", lines[i]);
	}

	return 0;
}

