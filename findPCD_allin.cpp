#include "findPCD_allin.h"
//Query surrounding into vector result as [x1, z1, y1, i1, x2, z2, y2, i2, ... , xn, zn, yn, in]
std::vector<double> pcd_finder(double lon, double lat, int query_size){
    // query_size is "block_radius" of query
    std::vector<double> result;
    double x_m = lon2x_m(lon) - x_m0;
    double z_m = lat2y_m(lat) - z_m0;
    std::cout << x_m <<" and " << z_m << std::endl;
    int block_size = 20;
    int x_block = int(round(x_m/block_size)) * block_size;
    int z_block = int(round(z_m/block_size)) * block_size;
    std::cout << x_block <<" and " << z_block << std::endl;
    char filename[128];
    sprintf(filename, "/mnt/truenas/scratch/genmao/one_map_files/map1492801000.06.txt");
    char indexname[128];
    sprintf(indexname, "/mnt/truenas/scratch/genmao/one_map_files/idx1492801000.06.txt");
    

    std::vector<double> index;
    std::ifstream infile, infile1;
    infile.open(indexname, std::ios::binary | std::ios::in);
    infile1.open(filename, std::ios::binary | std::ios::in);

    if(infile.is_open()){
        int begin = infile.tellg();
        infile.seekg(0, std::ios::end);
        int fileSize = infile.tellg();
        infile.seekg(begin, std::ios::beg);
        std::vector<double> buffer(fileSize/sizeof(double));
        infile.read(reinterpret_cast<char*>(&buffer[0]), fileSize); // or &buf[0] for C++98
        infile.close();
        //append buffer at the end of result;
        index.insert(index.end(), buffer.begin(), buffer.end());
        std::cout << "Index loaded." << std::endl;
    }
    else{
        std::cout << "Index not found!" << std::endl;
    }

    int radius = query_size - 1;
    for (int i = x_block - radius*block_size; i <= x_block + radius*block_size; i += block_size){
        for (int j = z_block - radius*block_size; j <= z_block + radius*block_size; j += block_size){
            int start = 0, end = -1;
	    for (int k = 0; k < index.size(); k += 4){
		if (round(index[k]) == i && round(index[k+1]) == j){
                    start = index[k+2];
		    end = index[k+3];
		    break;
		}
	    }
            if (end == -1) {
                std::cout << "Current block exceeds measured area!" << std::endl;
                continue;
            }

	    if(infile1.is_open()){
		//int begin = infile.tellg();
		//infile1.seekg(0, ios::end);
		//int fileSize = infile1.tellg();
		infile1.seekg(start*4*sizeof(double), std::ios::beg);
		std::vector<double> buffer((end-start)*4);
		infile1.read(reinterpret_cast<char*>(&buffer[0]), (end-start)*4*sizeof(double)); // or &buf[0] for C++98
		//append buffer at the end of result;
		result.insert(result.end(), buffer.begin(), buffer.end());
	    }
	    else{
		std::cout << "datafile closed!" << std::endl;
	    }
        }
    }
    infile1.close(); 
       
    return result;
}
