#include <iostream>
#include <vector>
#include <fstream>

#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/filters/filter.h>
#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <pcl/filters/filter_indices.h>
#include <pcl/segmentation/region_growing_rgb.h>

bool segmentRegionGrowingRGB(
    const std::string& input_pcd,
    const std::string& output_ply,
    const std::string& output_csv,
    int distance_threshold = 10,
    int point_color_threshold = 6,
    int region_color_threshold = 5,
    int min_cluster_size = 600)
{
    pcl::search::Search<pcl::PointXYZRGB>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZRGB>);
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>);

    if (pcl::io::loadPCDFile<pcl::PointXYZRGB>(input_pcd, *cloud) == -1) {
        std::cerr << "Failed to load input file: " << input_pcd << std::endl;
        return false;
    }
    std::cout << "Loaded " << cloud->points.size() << " points.\n";

    pcl::IndicesPtr indices(new std::vector<int>);
    pcl::removeNaNFromPointCloud(*cloud, *indices);
    std::cout << "After removing NaNs: " << indices->size() << " points.\n";

    pcl::RegionGrowingRGB<pcl::PointXYZRGB> reg;
    reg.setInputCloud(cloud);
    reg.setIndices(indices);
    reg.setSearchMethod(tree);
    reg.setDistanceThreshold(distance_threshold);
    reg.setPointColorThreshold(point_color_threshold);
    reg.setRegionColorThreshold(region_color_threshold);
    reg.setMinClusterSize(min_cluster_size);

    std::vector<pcl::PointIndices> clusters;
    reg.extract(clusters);
    std::cout << "Found " << clusters.size() << " clusters.\n";

    std::vector<int> cluster_ids(cloud->size(), -1);
    srand(static_cast<unsigned int>(time(nullptr)));

    for (size_t i = 0; i < clusters.size(); ++i) {
        uint8_t r = static_cast<uint8_t>((rand() % 256));
        uint8_t g = static_cast<uint8_t>((rand() % 256));
        uint8_t b = static_cast<uint8_t>((rand() % 256));
        for (int idx : clusters[i].indices) {
            cloud->points[idx].r = r;
            cloud->points[idx].g = g;
            cloud->points[idx].b = b;
            cluster_ids[idx] = static_cast<int>(i);
        }
    }

    // Save CSV with cluster mapping
    std::ofstream csv(output_csv);
    if (!csv.is_open()) {
        std::cerr << "Could not open CSV file: " << output_csv << std::endl;
        return false;
    }

    csv << "point_index,x,y,z,r,g,b,cluster_id\n";
    for (size_t i = 0; i < cloud->points.size(); ++i) {
        const auto& pt = cloud->points[i];
        csv << i << "," << pt.x << "," << pt.y << "," << pt.z << ","
            << static_cast<int>(pt.r) << "," << static_cast<int>(pt.g) << "," << static_cast<int>(pt.b) << ","
            << cluster_ids[i] << "\n";
    }
    csv.close();
    std::cout << "Saved cluster mapping to: " << output_csv << std::endl;

    // Save colored PLY
    if (pcl::io::savePLYFileBinary(output_ply, *cloud) == -1) {
        std::cerr << "Failed to save PLY: " << output_ply << std::endl;
        return false;
    }
    std::cout << "Segmented colored PLY saved to: " << output_ply << std::endl;

    return true;
}

int main() {
    std::string input_pcd  = "/mnt/c/Users/wangz/monastery/phone_scan/HK_pc_phone.pcd";
    std::string output_ply = "/mnt/c/Users/wangz/monastery/phone_scan/HK_phone_color_rg_seg.ply";
    std::string output_csv = "/mnt/c/Users/wangz/monastery/phone_scan/HK_phone_color_rg_seg.csv";

    if (!segmentRegionGrowingRGB(input_pcd, output_ply, output_csv,
                                 4, 10, 8, 2000)) {
        return -1;
                                 }

    return 0;
}
// std::string input_pcd  = "/mnt/c/Users/wangz/monastery/HK_temp.pcd";
// std::string output_ply = "/mnt/c/Users/wangz/monastery/HK_color_rg_seg.ply";
// std::string output_csv = "/mnt/c/Users/wangz/monastery/HK_color_rg_seg.csv";