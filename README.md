# pcdquery

The function pcd_finding is in findPCD_allin.h. 

Include findPCD_allin.h, then call std::vector<double> pcd_finder(double lon, double lat, int query_size). 

Input is longitude, latitude, the radius of searching field in terms of num of blocks(1 indicates only 1 block, 2 indicates nearby 9 blocks, 3 indicates nearby 25 blocks. Each block is of 20*20 m^2. 

findPCD_allin.cpp is a demo to call pcd_finding function. 
