
.PHONY: clean

CFLAGS = -std=gnu99

all: hdm csort

csort: csort.o
	$(CC) -o $@ $^

hdm: hdm.o
	$(CC) -o $@ $^ -lparted

%.o: %.c
	$(CC) -c -o $@ $^ $(CFLAGS)

clean:
	rm -f hdm

