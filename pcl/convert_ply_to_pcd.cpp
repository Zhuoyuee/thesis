#include <iostream>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/io/ply_io.h>
#include <pcl/io/pcd_io.h>

// Define the conversion function
void convertPLYtoPCD(const char* inputFilename, const char* outputFilename) {
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>);

    if (pcl::io::loadPLYFile<pcl::PointXYZRGB>(inputFilename, *cloud) == -1) {
        PCL_ERROR("Couldn't read file\n");
        return;
    }

    pcl::io::savePCDFile(outputFilename, *cloud);
    std::cout << "Converted " << inputFilename << " to " << outputFilename << std::endl;
}

// Main function that calls the conversion function with hardcoded paths
int main() {
    //const char* inputPath = "/mnt/c/Users/wangz/thesis/AULA_merge/AULA_sep.ply";  // Specify the full path to the input file
    //const char* outputPath = "/mnt/c/Users/wangz/thesis/pcl/aula_sep.pcd";  // Specify the full path to the output file
    const char* inputPath = "/mnt/c/Users/wangz/monastery/HK_clipped1.ply";
    const char* outputPath = "/mnt/c/Users/wangz/monastery/HK.pcd";

    convertPLYtoPCD(inputPath, outputPath);
    return 0;
}

