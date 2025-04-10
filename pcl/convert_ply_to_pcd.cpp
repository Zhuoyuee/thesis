#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/io/ply_io.h>
#include <pcl/io/pcd_io.h>
#include <pcl/PCLPointCloud2.h>
#include <pcl/conversions.h>
#include <iostream>

// Function to convert PLY (float64 or float32) to PCD
void convertPLYtoPCD(const std::string& inputFilename, const std::string& outputFilename) {
    pcl::PCLPointCloud2 cloud2;
    if (pcl::io::loadPLYFile(inputFilename, cloud2) == -1) {
        PCL_ERROR("Couldn't read file\n");
        return;
    }

    bool needsConversion = false;
    for (const auto& field : cloud2.fields) {
        if ((field.name == "x" || field.name == "y" || field.name == "z") &&
            field.datatype == pcl::PCLPointField::FLOAT64) {
            needsConversion = true;
            break;
            }
    }

    if (needsConversion) {
        std::cout << "Detected float64, converting to float32...\n";
        pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
        pcl::fromPCLPointCloud2(cloud2, *cloud);

        for (auto& pt : cloud->points) {
            pt.x = static_cast<float>(pt.x);
            pt.y = static_cast<float>(pt.y);
            pt.z = static_cast<float>(pt.z);
        }

        pcl::io::savePCDFile(outputFilename, *cloud);
    } else {
        std::cout << "Data is already float32, saving directly.\n";
        pcl::io::savePCDFile(outputFilename, cloud2);
    }

    std::cout << "✅ Successfully converted to: " << outputFilename << std::endl;
}

int main() {
    // 🔧 Set your input/output file paths here
    std::string inputPath = "/mnt/c/Users/wangz/monastery/phone_scan/HK_pc_phone.ply";
    std::string outputPath = "/mnt/c/Users/wangz/monastery/converted/HK_pc_phone.pcd";

    convertPLYtoPCD(inputPath, outputPath);
    return 0;
}


    //const char* inputPath = "/mnt/c/Users/wangz/thesis/AULA_merge/AULA_sep.ply";  // Specify the full path to the input file
    //const char* outputPath = "/mnt/c/Users/wangz/thesis/pcl/aula_sep.pcd";  // Specify the full path to the output file
    // const char* inputPath = "/mnt/c/Users/wangz/monastery/HK_clipped1.ply";
    // const char* outputPath = "/mnt/c/Users/wangz/monastery/HK.pcd";
    // const char* inputPath = "/mnt/c/Users/wangz/monastery/phone_scan/HK_pc_phone.ply";
    // const char* outputPath = "/mnt/c/Users/wangz/monastery/phone_scan/HK_pc.pcd";


