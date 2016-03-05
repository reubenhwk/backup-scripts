
.PHONY: clean

all: hdm

hdm: hdm.o
	$(CC) -o $@ $^ -lparted

%.o: %.c
	$(CC) -c -o $@ $^

clean:
	rm -f hdm

