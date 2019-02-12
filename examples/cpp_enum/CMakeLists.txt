cmake_minimum_required(VERSION 3.0)
project(cpp_enums CXX)

include(Pycodegen.cmake)

# Generate code using the cpp frontend
# Put the names of the generated files in the GENERATED_SRC variable
codegen(
    OUTPUT_VAR GENERATED_SRC
    FRONTEND cpp
    DRIVER enum_reflection.py
    INPUT_FILES
        my_enums.h
)

add_executable(cpp_enums
    cpp_enums.cpp
    ${GENERATED_SRC}
)

target_include_directories(cpp_enums PRIVATE ${CMAKE_BINARY_DIR})

# Hopefully most people should be able to compile C++11 by now
set_target_properties(cpp_enums PROPERTIES CXX_STANDARD 11)
