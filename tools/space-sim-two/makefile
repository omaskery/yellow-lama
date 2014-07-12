
CC=clang++

TARGET=space-sim-two

SOURCES=\
	src/main.cpp\
	src/spacesim/networking/system_message.cpp\
	src/spacesim/networking/client_connection.cpp\
	src/spacesim/networking/sim_server.cpp\
	src/spacesim/sim/simulation.cpp\
	src/spacesim/sim/entity.cpp

LIBS=\
	-lboost_system

FLAGS=\
	--std=c++11\
	-Iinclude

R_FLAGS=\
	-O3

D_FLAGS=\
	-g

R_PATH=bin/release/

D_PATH=bin/debug/

all: build-debug build-release

make-dirs:
	@mkdir -p bin/debug/
	@mkdir -p bin/release/

build-debug bd: make-dirs
	$(CC) $(SOURCES) -o $(D_PATH)$(TARGET) $(FLAGS) $(D_FLAGS) $(LIBS)

build-release br: make-dirs
	$(CC) $(SOURCES) -o $(R_PATH)$(TARGET) $(FLAGS) $(R_FLAGS) $(LIBS)

run-debug rd: make-dirs
	gdb --se=$(D_PATH)$(TARGET)

run-release rr: make-dirs
	./$(R_PATH)$(TARGET)

clean: make-dirs
