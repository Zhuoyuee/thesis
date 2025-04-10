#include <iostream>
#include <vector>
#include <fstream>
#include <ctime>

#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/point_types.h>
#include <pcl/search/kdtree.h>
#include <pcl/filters/filter.h>
#include <pcl/features/normal_3d_omp.h>
#include <pcl/segmentation/region_growing.h>

bool segmentRegionGrowingGeometry(
    const std::string& input_pcd,
    const std::string& output_ply,
    const std::string& output_csv,
    int k_neighbors = 30,
    float smoothness_deg = 3.0,
    float curvature_threshold = 1.0,
    int min_cluster_size = 100)
{
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    if (pcl::io::loadPCDFile<pcl::PointXYZ>(input_pcd, *cloud) == -1) {
        std::cerr << "❌ Failed to load: " << input_pcd << std::endl;
        return false;
    }
    std::cout << "📥 Loaded " << cloud->size() << " points.\n";

    // Remove NaNs
    std::vector<int> nan_indices;
    pcl::removeNaNFromPointCloud(*cloud, *cloud, nan_indices);
    std::cout << "Cleaned cloud, removed " << nan_indices.size() << " NaN points. Remaining: " << cloud->size() << "\n";

    // Compute normals
    pcl::search::Search<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>);
    pcl::PointCloud<pcl::Normal>::Ptr normals(new pcl::PointCloud<pcl::Normal>);

    pcl::NormalEstimationOMP<pcl::PointXYZ, pcl::Normal> norm_est;
    norm_est.setInputCloud(cloud);
    norm_est.setSearchMethod(tree);
    norm_est.setKSearch(k_neighbors);
    norm_est.compute(*normals);
    std::cout << "📐 Normals computed.\n";

    // Region Growing on normals
    pcl::RegionGrowing<pcl::PointXYZ, pcl::Normal> reg;
    reg.setMinClusterSize(min_cluster_size);
    reg.setSearchMethod(tree);
    reg.setNumberOfNeighbours(k_neighbors);
    reg.setInputCloud(cloud);
    reg.setInputNormals(normals);
    reg.setSmoothnessThreshold(smoothness_deg / 180.0 * M_PI);
    reg.setCurvatureThreshold(curvature_threshold);

    std::vector<pcl::PointIndices> clusters;
    reg.extract(clusters);
    std::cout << "🔍 Found " << clusters.size() << " clusters.\n";

    // Create RGB output cloud with cluster colors
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr colored_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    colored_cloud->resize(cloud->size());
    std::vector<int> cluster_ids(cloud->size(), -1);
    srand(static_cast<unsigned int>(time(nullptr)));

    for (size_t i = 0; i < cloud->size(); ++i) {
        colored_cloud->points[i].x = cloud->points[i].x;
        colored_cloud->points[i].y = cloud->points[i].y;
        colored_cloud->points[i].z = cloud->points[i].z;
        colored_cloud->points[i].r = 128;
        colored_cloud->points[i].g = 128;
        colored_cloud->points[i].b = 128;
    }

    for (size_t i = 0; i < clusters.size(); ++i) {
        uint8_t r = static_cast<uint8_t>((rand() % 256));
        uint8_t g = static_cast<uint8_t>((rand() % 256));
        uint8_t b = static_cast<uint8_t>((rand() % 256));
        for (int idx : clusters[i].indices) {
            colored_cloud->points[idx].r = r;
            colored_cloud->points[idx].g = g;
            colored_cloud->points[idx].b = b;
            cluster_ids[idx] = static_cast<int>(i);
        }
    }

    // Save colored cloud
    if (pcl::io::savePLYFileBinary(output_ply, *colored_cloud) == -1) {
        std::cerr << "❌ Failed to save output PLY.\n";
        return false;
    }
    std::cout << "✅ Saved segmented PLY to: " << output_ply << std::endl;

    // Save CSV
    std::ofstream csv(output_csv);
    csv << "point_index,x,y,z,r,g,b,cluster_id\n";
    for (size_t i = 0; i < colored_cloud->size(); ++i) {
        const auto& pt = colored_cloud->points[i];
        csv << i << "," << pt.x << "," << pt.y << "," << pt.z << ","
            << static_cast<int>(pt.r) << "," << static_cast<int>(pt.g) << "," << static_cast<int>(pt.b) << ","
            << cluster_ids[i] << "\n";
    }
    csv.close();
    std::cout << "📄 Cluster CSV saved to: " << output_csv << std::endl;

    return true;
}

int main() {
    std::string input_pcd  = "/mnt/c/Users/wangz/monastery/phone_scan/HK_pc_phone.pcd";
    std::string output_ply = "/mnt/c/Users/wangz/monastery/phone_scan/HK_rgn_seg1.ply";
    std::string output_csv = "/mnt/c/Users/wangz/monastery/phone_scan/HK_rgn_seg1.csv";

    if (!segmentRegionGrowingGeometry(input_pcd, output_ply, output_csv,
                                      40,      // k_neighbors
                                      3.0f,    // smoothness_deg
                                      0.05f,    // curvature_threshold
                                      1000)) {  // min_cluster_size
        return -1;
    }

    return 0;
}
