#include <iostream>
#include <vector>

#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <pcl/filters/filter_indices.h> // for pcl::removeNaNFromPointCloud
#include <pcl/segmentation/region_growing_rgb.h>

int main ()
{
    pcl::search::Search<pcl::PointXYZRGB>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZRGB>);
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZRGB>);
    if (pcl::io::loadPCDFile<pcl::PointXYZRGB>("/mnt/c/Users/wangz/monastery/HK.pcd", *cloud) == -1)
    {
        std::cout << "Cloud reading failed." << std::endl;
        return -1;
    }
    std::cout << "Loaded " << cloud->points.size() << " points." << std::endl;

    pcl::IndicesPtr indices (new std::vector<int>);
    pcl::removeNaNFromPointCloud(*cloud, *indices);
    std::cout << "Removed NaNs, remaining " << indices->size() << " valid points." << std::endl;

    pcl::RegionGrowingRGB<pcl::PointXYZRGB> reg;
    reg.setInputCloud(cloud);
    reg.setIndices(indices);
    reg.setSearchMethod(tree);
    reg.setDistanceThreshold(10);
    reg.setPointColorThreshold(6);
    reg.setRegionColorThreshold(5);
    reg.setMinClusterSize(600);

    std::vector<pcl::PointIndices> clusters;
    reg.extract(clusters);
    std::cout << "Found " << clusters.size() << " clusters." << std::endl;

    // Manually coloring the clusters
    for (size_t i = 0; i < clusters.size(); ++i) {
        uint8_t r = static_cast<uint8_t>((rand() % 256));
        uint8_t g = static_cast<uint8_t>((rand() % 256));
        uint8_t b = static_cast<uint8_t>((rand() % 256));
        for (size_t j = 0; j < clusters[i].indices.size(); ++j) {
            int idx = clusters[i].indices[j];
            cloud->points[idx].r = r;
            cloud->points[idx].g = g;
            cloud->points[idx].b = b;
        }
    }

    // Save the modified cloud to a PLY file
    if (pcl::io::savePLYFileBinary("/mnt/c/Users/wangz/monastery/HK_color_rg_seg.ply", *cloud) == -1) {
        std::cerr << "Failed to save the PLY file!" << std::endl;
        return -1;
    }
    std::cout << "Segmented colored cloud saved to 'aula_region_growth_rgb.ply'." << std::endl;

    return 0;
}