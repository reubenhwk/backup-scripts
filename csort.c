
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define LINES 128
#define LINE_MAX 1024

struct csort_opt {
	int k;
	int r:1;
} _opt;

static char const * col(char const * a, int n)
{
	if (n <= 1) {
		return a;
	}

	int i = 0;

	while (a[i] && isspace(a[i])) ++i;

	++n;
	while (a[i] && --n > 1) {
		while (a[i] && !isspace(a[i])) ++i;
		while (a[i] && isspace(a[i])) ++i;
	}

	return &a[i];
}

static 
int compar(const void * _a, const void * _b)
{
	char const * a = (char const*)_a;
	char const * b = (char const*)_b;

	char const * c0 = col(a, _opt.k);
	char const * c1 = col(b, _opt.k);

	if (_opt.r)
		return strcmp(c1, c0);
	return strcmp(c0, c1);
}

static void
usage(FILE * out, char const * binary)
{
	fprintf(out,
		"usage: %s [options]\n"
		"   -h      this help message\n"
		"   -k N    sort on column N\n"
		"   -r      reverse sort\n"
		, binary
	);
}

int main(int argc, char * argv[])
{
	int c;
	while (c = getopt(argc, argv, "hk:r"), c != -1) {
		switch (c) {
			case 'h':
				usage(stdout, basename(argv[0]));
				exit(0);

			case 'k':
				_opt.k = atoi(optarg);
			break;

			case 'r':
				_opt.r = 1;
			break;

			default:
				usage(stderr, basename(argv[0]));
				exit(-1);
		}
	}

	char lines[LINES][LINE_MAX];
	int line_count = 0;
	while (line_count < LINES, fgets(lines[line_count++], LINE_MAX, stdin));

	qsort(lines, line_count, LINE_MAX, compar);

	for (int i = 0; i < line_count; ++i) {
		printf("%s", lines[i]);
	}

	return 0;
}

