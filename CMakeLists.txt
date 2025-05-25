#################################################################################################################
#################################################################################################################
cmake_minimum_required(VERSION 3.10)
project(c_base C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
#################################################################################################################
#################################################################################################################

if(WIN32)
    set(IS_WINDOWS TRUE)
    set(IS_LINUX FALSE)
elseif(UNIX AND NOT APPLE)
    set(IS_WINDOWS FALSE)
    set(IS_LINUX TRUE)
else()
    set(IS_WINDOWS FALSE)
    set(IS_LINUX FALSE)
    message(FATAL_ERROR "Unsupported platform: Only Windows and Linux are supported.")
endif()

# WINDOWS
if(IS_WINDOWS)
    set(PYTHON_PATH "~/AppData/Local/Programs/Python/Python311")
    set(OPENUSD_PATH "P:/DATA/CODE/OpenUSD")
    set(GLAD_PATH "P:/DATA/CODE/_SRC/glad")
    set(PYBIND11_PATH "P:/DATA/CODE/_SRC/pybind11")
# LINUX
elseif(IS_LINUX)
    set(PYTHON_PATH "/usr/include/python3.12")
    set(OPENUSD_PATH "~/DATA/CODE/OpenUSD")
    set(GLAD_PATH "~/DATA/CODE/_SRC/glad")
    set(PYBIND11_PATH "/home/nikolas/DATA/CODE/_SRC/pybind11")
endif()
#################################################################################################################
#################################################################################################################

# SETUP PYTHON (WINDOIWS)
if (IS_WINDOWS)
    find_package(Python COMPONENTS Interpreter Development)
    if(Python_FOUND)
        include_directories(${Python_INCLUDE_DIRS})
        link_libraries(${Python_LIBRARIES})
        link_directories(${PYTHON_PATH}/libs)
    endif()
endif()
# SET PYTHON (LINUX)
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
        usd_kind
        usd_ar
        usd_js
        usd_plug
        usd_work
        usd_arch
        usd_pcp
        usd_vt
        usd_trace
        usd_python
        usd_usdImagingGL
        glad
)


#################################################################################################################
#################################################################################################################
