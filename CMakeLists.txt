cmake_minimum_required(VERSION 3.10)

project(SkyGeo VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(
    test
    experiments/test/main.cpp
)

target_include_directories(
    test
    PRIVATE
    ${PROJECT_SOURCE_DIR}/include
)