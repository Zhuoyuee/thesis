#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/voxel_grid.h>
#include <iostream>

int main() {
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>());
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_filtered(new pcl::PointCloud<pcl::PointXYZRGB>());

    // Load the original point cloud
    if (pcl::io::loadPCDFile<pcl::PointXYZRGB>("/mnt/c/Users/www/Documents/thesis/aula_sep.pcd", *cloud) != -1) {
        std::cout << "Original cloud points: " << cloud->points.size() << std::endl;

        // Set up the voxel grid filter
        pcl::VoxelGrid<pcl::PointXYZRGB> sor;
        sor.setInputCloud(cloud);
        float base_leaf_size = 0.08f; // Start with a base leaf size
        sor.setLeafSize(base_leaf_size, base_leaf_size, base_leaf_size);
        sor.filter(*cloud_filtered);

        std::cout << "Filtered cloud points: " << cloud_filtered->points.size() << std::endl;

        // Save the reduced cloud
        pcl::io::savePCDFile("/mnt/c/Users/www/Documents/thesis/aula_downsampled_005 .pcd", *cloud_filtered);
    } else {
        std::cerr << "Failed to load the point cloud file!" << std::endl;
        return -1;
    }

    return 0;
}
