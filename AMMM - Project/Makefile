# Compiler settings
CXX = g++
CXXFLAGS = -std=c++11 -Wall

# Output executable names
EXEC1 = project
EXEC2 = multiple_instance_generator

# Source files
SRC1 = project.cc
SRC2 = multiple_instance_generator.cc

# Object files
OBJ1 = $(SRC1:.cc=.o)
OBJ2 = $(SRC2:.cc=.o)

# Default target: Compile both executables
all: $(EXEC1) $(EXEC2)

# Compile solve_with_greedy
$(EXEC1): $(SRC1)
	$(CXX) $(CXXFLAGS) -o $(EXEC1) $(SRC1)

# Compile multiple_instance_generator
$(EXEC2): $(SRC2)
	$(CXX) $(CXXFLAGS) -o $(EXEC2) $(SRC2)

# Clean up object files and executables
clean:
	rm -f $(OBJ1) $(OBJ2) $(EXEC1) $(EXEC2)

# Phony targets
.PHONY: all clean
