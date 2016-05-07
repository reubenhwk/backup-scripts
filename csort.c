
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINES 128
#define LINE_MAX 1024

static char const * col(char const * a, int n)
{
	int i = 0;

	while (a[i] && isspace(a[i])) ++i;

	while (a[i] && n-- > 0) {
		while (a[i] && !isspace(a[i])) ++i;
		while (a[i] && isspace(a[i])) ++i;
	}

	return &a[i];
}

static 
int compar(const void * _a, const void * _b, void * _n)
{
	char const * a = (char const*)_a;
	char const * b = (char const*)_b;
	int n = *(int*)_n;

	char const * c0 = col(a, n);
	char const * c1 = col(b, n);

	return strcmp(c0, c1);
}

int main(int argc, char * argv[])
{
	char lines[LINES][LINE_MAX];
	int line_count = 0;
	while (line_count < LINES, fgets(lines[line_count++], LINE_MAX, stdin));

	qsort_r(lines, line_count, LINE_MAX, compar, (int[]){1});

	for (int i = 0; i < line_count; ++i) {
		printf("%s", lines[i]);
	}

	return 0;
}

