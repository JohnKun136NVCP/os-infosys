TARGET = osinfosys
CC = gcc
CFLAGS = -O2 -Wall

SRC = main.c $(wildcard src/*.c)
OBJ = $(SRC:.c=.o)

$(TARGET): $(OBJ)
    $(CC) $(CFLAGS) -o $(TARGET) $(OBJ)

%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@


clean:
    rm -f $(OBJ) $(TARGET)
