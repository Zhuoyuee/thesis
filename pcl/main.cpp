#include <iostream>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/io/ply_io.h>

int main() {
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
    cloud->width = 5;
    cloud->height = 1;
    cloud->is_dense = false;
    cloud->points.resize(cloud->width * cloud->height);

    for (size_t i = 0; i < cloud->points.size(); ++i) {
        cloud->points[i].x = 1024 * rand() / (RAND_MAX + 1.0f);
        cloud->points[i].y = 1024 * rand() / (RAND_MAX + 1.0f);
        cloud->points[i].z = 1024 * rand() / (RAND_MAX + 1.0f);
    }

    std::cout << "Saved " << cloud->points.size() << " data points to test_pcl:" << std::endl;
    for (size_t i = 0; i < cloud->points.size(); ++i) {
        std::cout << "    " <<
        cloud->points[i].x << " " << cloud->points[i].y << " " << cloud->points[i].z << std::endl;
    }

    return 0;
}
