
.PHONY: clean

CFLAGS = -std=gnu99 -D_GNU_SOURCE

TARGETS = hdm csort disk-id

all: $(TARGETS)

disk-id: disk-id.c
	$(CC) -o $@ $^

csort: csort.o
	$(CC) -o $@ $^

hdm: hdm.o
	$(CC) -o $@ $^ -lparted

%.o: %.c
	$(CC) -c -o $@ $^ $(CFLAGS)

clean:
	rm -f $(TARGETS)

