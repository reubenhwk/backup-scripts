
.PHONY: clean

CFLAGS = -std=gnu99 -D_GNU_SOURCE

TARGETS = csort

all: $(TARGETS)

csort: csort.o
	$(CC) -o $@ $^

%.o: %.c
	$(CC) -c -o $@ $^ $(CFLAGS)

install:
	install -D csort      /usr/local/bin/csort
	install -D lrc        /usr/local/bin/lrc
	install -D lrc-clone  /usr/local/bin/lrc-clone
	install -D lrc-busycd /usr/local/bin/lrc-busycd

uninstall:
	rm -f /usr/local/bin/csort
	rm -f /usr/local/bin/lrc
	rm -f /usr/local/bin/lrc-clone
	rm -f /usr/local/bin/lrc-busycd

clean:
	rm -f $(TARGETS) *.o

