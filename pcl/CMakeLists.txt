cmake_minimum_required(VERSION 3.28)
project(pcl)

set(CMAKE_CXX_STANDARD 20)

# Find PCL package
find_package(PCL 1.10 REQUIRED COMPONENTS common io filters segmentation visualization search kdtree)

# Include PCL headers
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

# Create an executable
add_executable(main main.cpp)
target_link_libraries(main ${PCL_LIBRARIES})

# Create an executable
add_executable(convert_ply_to_pcd convert_ply_to_pcd.cpp)
target_link_libraries(convert_ply_to_pcd ${PCL_LIBRARIES})

add_executable(region_rgb_segmentation region_rgb_segmentation.cpp)
target_link_libraries(region_rgb_segmentation ${PCL_LIBRARIES})

add_executable(pcd_to_ply pcd_to_ply.cpp)
target_link_libraries(pcd_to_ply ${PCL_LIBRARIES})

add_executable(downsampling downsampling.cpp)
target_link_libraries(downsampling ${PCL_LIBRARIES})
