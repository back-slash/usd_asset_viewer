#################################################################################################################
#################################################################################################################
cmake_minimum_required(VERSION 3.10)
project(c_base C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
#################################################################################################################
#################################################################################################################

# External Dependencies
set(OPENUSD_PATH "P:/DATA/CODE/OpenUSD")
set(GLAD_PATH "${CMAKE_SOURCE_DIR}/external/GLAD")
set(PYBIND11_PATH "${CMAKE_SOURCE_DIR}/external/pybind11")
#################################################################################################################
#################################################################################################################

# SETUP PYTHON
find_package(Python COMPONENTS Interpreter Development)

# SETUP USD
link_directories(
    ${OPENUSD_PATH}/lib
)
include_directories(${OPENUSD_PATH}/include)

# SETUP GLAD
include_directories(${GLAD_PATH})
add_library(glad ${GLAD_PATH}/src/glad.c)
target_include_directories(glad PUBLIC ${GLAD_PATH}/include)

# SETUP PYBIND11
add_subdirectory(${PYBIND11_PATH} ${CMAKE_BINARY_DIR}/pybind11_build)
pybind11_add_module(c_base src/c_base.cpp)

# CREATE
set_target_properties(c_base PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/../core
    LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/../core
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../core   
)

target_link_libraries(c_base
    PRIVATE
        usd_gf
        usd_tf
        usd_sdf
        usd_usd
        usd_usdGeom
        usd_usdLux
        usd_usdShade
        usd_usdSkel
        usd_usdRender
        usd_usdUtils
        usd_trace
        usd_python
        usd_usdImagingGL
        glad
)

#################################################################################################################
#################################################################################################################
