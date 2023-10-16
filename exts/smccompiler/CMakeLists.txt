cmake_minimum_required(VERSION 3.10)
project(smcc)

set(CMAKE_SHARED_LIBRARY_PREFIX "")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
add_library(_emulator SHARED mq8b_solution/MQ8B/src/emulator.cpp)

