# Author: Riley Raschke
# © 2016 rrappsdev.com
# DWTFYW Licensce - Just mention me

.DEFAULT_GOAL := build

TARGET=gemini-data-feed
CC=g++
CFLAGS=-std=c++0x #-ggdb -Wall
SRC_INCLUDE=src
BEAST_INCLUDE=/var/git/beast/include
INC=include
DEST=bin
OBJ_DIR=obj
mkd=@mkdir

#build: clean-all BigInt.o PBnumbers.o PBgenerator.o exec
build: clean-all exec

exec:
	$(mkd) -p $(DEST)
	$(CC) $(CFLAGS) -I $(SRC_INCLUDE) -I $(BEAST_INCLUDE) \
		-o $(DEST)/$(TARGET) $(SRC_INCLUDE)/main.cpp

#		$(OBJ_DIR)/PBnumbers.o $(OBJ_DIR)/PBgenerator.o $(OBJ_DIR)/BigInt.o \
#		-l boost_program_options -l pthread -l boost_system -l boost_thread -l boost_timer

#PBnumbers.o:
#	$(CC) $(CFLAGS) -I $(SRC_INCLUDE) -o $(OBJ_DIR)/PBnumbers.o \
#		-c $(SRC_INCLUDE)/PBnumbers.cpp

#PBgenerator.o:
#	$(CC) $(CFLAGS) -I $(SRC_INCLUDE) -o $(OBJ_DIR)/PBgenerator.o \
#		-c $(SRC_INCLUDE)/PBgenerator.cpp \
#		-l boost_thread -l boost_system

#BigInt.o:
#	$(mkd) -p $(OBJ_DIR)
#	$(CC) $(CFLAGS) -I $(SRC_INCLUDE) -o $(OBJ_DIR)/BigInt.o -c $(SRC_INCLUDE)/BigInt.cpp

clean-all: clean
	$(RM) $(DEST)/$(TARGET)

clean:
	ulimit -c unlimited ;
	$(RM) core $(OBJ_DIR)/*.o

