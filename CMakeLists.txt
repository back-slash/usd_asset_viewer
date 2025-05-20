#################################################################################################################
#################################################################################################################
cmake_minimum_required(VERSION 3.10)
project(c_draw C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
#################################################################################################################
#################################################################################################################

# WINDOWS
set(PYTHON_PATH "~/AppData/Local/Programs/Python/Python311")
set(OPENUSD_PATH "P:/DATA/CODE/OpenUSD")
set(GLAD_PATH "P:/DATA/CODE/_SRC/glad")
set(PYBIND11_PATH "P:/DATA/CODE/_SRC/pybind11")

# LINUX
#set(OPENUSD_PATH "~/DATA/CODE/OpenUSD")
#set(GLAD_PATH "~/DATA/CODE/_SRC/glad")
#set(PYTHON_PATH "/usr/include/python3.12")
#set(PYBIND11_PATH "/home/nikolas/DATA/CODE/_SRC/pybind11")

#################################################################################################################
#################################################################################################################

# SETUP PYTHON (WINDOIWS)
find_package(Python COMPONENTS Interpreter Development)
if(Python_FOUND)
    include_directories(${Python_INCLUDE_DIRS})
    link_libraries(${Python_LIBRARIES})
    link_directories(${PYTHON_PATH}/libs)
endif()


# SETUP PYTHON (LINUX)
# NOTHING


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
pybind11_add_module(c_draw_opengl src/c_draw_opengl.cpp)


# CREATE
set_target_properties(c_draw_opengl PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/../core
    LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/../core
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../core   
)
target_link_libraries(c_draw_opengl PRIVATE usd_gf glad)


#################################################################################################################
#################################################################################################################
