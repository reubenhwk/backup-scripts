
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define LINES 128
#define LINE_MAX 1024

static char const * col(char const * a, int n)
{
	if (n <= 0) {
		return a;
	}

	int i = 0;

	while (a[i] && isspace(a[i])) ++i;

	while (a[i] && --n > 0) {
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

static void
usage(FILE * out, char const * binary)
{
	fprintf(out,
		"usage: %s [options]\n"
		"   -h      this help message\n"
		"   -k N    sort on column N\n"
		, binary
	);
}

int main(int argc, char * argv[])
{
	int col = 0;
	int c;

	while (c = getopt(argc, argv, "hk:"), c != -1) {
		switch (c) {
			case 'h':
				usage(stdout, basename(argv[0]));
				exit(0);

			case 'k':
				col = atoi(optarg);
			break;

			default:
				usage(stderr, basename(argv[0]));
				exit(-1);
		}
	}

	char lines[LINES][LINE_MAX];
	int line_count = 0;
	while (line_count < LINES, fgets(lines[line_count++], LINE_MAX, stdin));

	qsort_r(lines, line_count, LINE_MAX, compar, &col);

	for (int i = 0; i < line_count; ++i) {
		printf("%s", lines[i]);
	}

	return 0;
}

