#include <iostream>
#include <vector>
#include <fstream>
#include <ctime>

#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/point_types.h>
#include <pcl/filters/filter.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/segmentation/sac_segmentation.h>

bool segmentPlanesRANSAC(
    const std::string& input_pcd,
    const std::string& output_ply,
    const std::string& output_csv,
    float distance_threshold = 0.01f,   // in meters
    int max_planes = 10,
    int min_plane_size = 500)
{
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr full_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    if (pcl::io::loadPCDFile(input_pcd, *full_cloud) == -1) {
        std::cerr << "Failed to load input file: " << input_pcd << std::endl;
        return false;
    }

    std::cout << "Loaded " << full_cloud->size() << " points.\n";

    pcl::PointCloud<pcl::PointXYZRGB>::Ptr working_cloud(new pcl::PointCloud<pcl::PointXYZRGB>(*full_cloud));
    pcl::SACSegmentation<pcl::PointXYZRGB> seg;
    seg.setOptimizeCoefficients(true);
    seg.setModelType(pcl::SACMODEL_PLANE);
    seg.setMethodType(pcl::SAC_RANSAC);
    seg.setMaxIterations(1000);
    seg.setDistanceThreshold(distance_threshold);

    pcl::ExtractIndices<pcl::PointXYZRGB> extract;

    std::vector<int> plane_ids(full_cloud->size(), -1);  // default: unassigned
    int current_plane_id = 0;

    while (working_cloud->size() > min_plane_size && current_plane_id < max_planes) {
        pcl::PointIndices::Ptr inliers(new pcl::PointIndices);
        pcl::ModelCoefficients::Ptr coefficients(new pcl::ModelCoefficients);

        seg.setInputCloud(working_cloud);
        seg.segment(*inliers, *coefficients);

        if (inliers->indices.size() < min_plane_size) {
            std::cout << "Plane too small (" << inliers->indices.size() << " points). Stopping.\n";
            break;
        }

        std::cout << "Plane " << current_plane_id << ": " << inliers->indices.size() << " points.\n";

        // Assign plane_id and color to inlier points in full cloud
        uint8_t r = static_cast<uint8_t>(rand() % 256);
        uint8_t g = static_cast<uint8_t>(rand() % 256);
        uint8_t b = static_cast<uint8_t>(rand() % 256);

        for (int idx : inliers->indices) {
            const auto& pt = working_cloud->points[idx];
            for (size_t i = 0; i < full_cloud->size(); ++i) {
                if (pt.x == full_cloud->points[i].x &&
                    pt.y == full_cloud->points[i].y &&
                    pt.z == full_cloud->points[i].z) {
                    plane_ids[i] = current_plane_id;
                    full_cloud->points[i].r = r;
                    full_cloud->points[i].g = g;
                    full_cloud->points[i].b = b;
                    break;
                }
            }
        }

        // Remove inliers from working cloud
        extract.setInputCloud(working_cloud);
        extract.setIndices(inliers);
        extract.setNegative(true); // remove inliers
        pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_f(new pcl::PointCloud<pcl::PointXYZRGB>);
        extract.filter(*cloud_f);
        working_cloud.swap(cloud_f);

        ++current_plane_id;
    }

    // Save CSV
    std::ofstream csv(output_csv);
    csv << "point_index,x,y,z,r,g,b,plane_id\n";
    for (size_t i = 0; i < full_cloud->size(); ++i) {
        const auto& pt = full_cloud->points[i];
        csv << i << "," << pt.x << "," << pt.y << "," << pt.z << ","
            << static_cast<int>(pt.r) << "," << static_cast<int>(pt.g) << "," << static_cast<int>(pt.b) << ","
            << plane_ids[i] << "\n";
    }
    csv.close();
    std::cout << "CSV saved to: " << output_csv << std::endl;

    // Save colored PLY
    if (pcl::io::savePLYFileBinary(output_ply, *full_cloud) == -1) {
        std::cerr << "Failed to save output PLY.\n";
        return false;
    }

    std::cout << "Segmented PLY saved to: " << output_ply << std::endl;
    return true;
}

int main() {
    std::string input_pcd  = "/mnt/c/Users/wangz/monastery/HK_temp.pcd";
    std::string output_ply = "/mnt/c/Users/wangz/monastery/HK_ransac_seg.ply";
    std::string output_csv = "/mnt/c/Users/wangz/monastery/HK_ransac_seg.csv";

    if (!segmentPlanesRANSAC(input_pcd, output_ply, output_csv,
                             0.01f,  // 1 cm tolerance
                             8,     // Max planes
                             500)) { // Min inliers per plane
        return -1;
                             }

    return 0;
}
