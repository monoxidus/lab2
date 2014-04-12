TARGET = dictionary
SOURCES = dict_helpers.c helpers.c index.c data.c pair.c list.c dict.c
HEADERS = $(wildcard *.h)
OBJECTS = $(SOURCES:.c=.o)

# Uncomment EACH library that you want to re-use. Remove the .o when providing
# your own .c implementation
LIBS = # dict.o list.o main.o pair.o

.PHONY : clean

CC = gcc
CFLAGS = -Wall -Werror -Wextra -pedantic -std=c99 -g

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(LIBS) -o $@ $(OBJECTS) main.c

clean:
	rm -f $(TARGET) $(OBJECTS)
