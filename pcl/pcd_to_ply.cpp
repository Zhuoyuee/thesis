#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/point_types.h>

int main() {
    // Point Cloud Pointer
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>);

    // Load the PCD file
    if (pcl::io::loadPCDFile<pcl::PointXYZRGB>("/mnt/c/Users/wangz/thesis/pcl/aula_spc_test1.pcd", *cloud) == -1) {
        std::cerr << "Failed to load the PCD file!" << std::endl;
        return -1;
    }

    // Save to PLY
    if (pcl::io::savePLYFileBinary("/mnt/c/Users/wangz/thesis/pcl/aula_spc_test1.ply", *cloud) == -1) {
        std::cerr << "Failed to save the PLY file!" << std::endl;
        return -1;
    }

    std::cout << "Successfully converted " << cloud->points.size() << " points to PLY format." << std::endl;

    return 0;
}
