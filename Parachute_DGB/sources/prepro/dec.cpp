#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <set>
#include <algorithm>

int main() {
  // step 1. read surface topology file and construct node_to_sub connectivity
  // decomposition: 1st 80 subdomains coincide with contact surface pairs:
  // 0 -> 80, 1
  // 1 -> 2, 3 
  // ...
  // 39 -> 78, 79
  // 40 -> 160, 81
  // 41 -> 82, 83
  // ...
  // 79 -> 158, 159

  std::ifstream in1("mesh_Structural.surfacetop.tria");
  std::string s, dummy;
  std::vector<std::set<int>> node_to_sub(182554);
  int surface_id, face_id, face_type, node1, node2, node3;
  do {
    std::getline(in1, s);
    if(in1.eof()) break;
    if(s[0] == '*') continue;
    if(s.compare(0, 11, "SURFACETOPO") == 0) {
      std::stringstream ss(s);
      ss >> dummy >> surface_id;
      {
        int sub_id;
        if(surface_id == 80) sub_id = 0;
        else if(surface_id == 160) sub_id = 40;
        else sub_id = surface_id/2;
        std::cerr << "surface_id = " << surface_id << ", sub_id = " << sub_id << std::endl;
        int surface_id, face_id, face_type, node1, node2, node3;
        do {
          std::getline(in1, s);
          if(s[0] == '*') break;
          std::stringstream ss(s);
          ss >> face_id >> face_type >> node1 >> node2 >> node3;
          node_to_sub[node1-1].insert(sub_id);
          node_to_sub[node2-1].insert(sub_id);
          node_to_sub[node3-1].insert(sub_id);
        } while(true);
      }
    }
  } while(true);
  in1.close();

  // step 2. read mesh file and form decomposition
  // 1st 80 subdomains coincide with contact surface pairs:
  // 1 -> 6, 8
  // 2 -> 10, 12
  // ...
  // 80 -> 322, 324
  std::ifstream in2("mesh_Structural.top.tria");
  std::vector<int> lines; // gap, suspension and vent line elements
  std::vector<std::vector<int>> dec(80); // decomposition of disk and band elements
  do {
    std::getline(in2, s);
    if(in2.eof()) break;
    if(s.compare(0, 8, "TOPOLOGY") == 0) {
      int elem_id, elem_type, node1, node2, node3;
      do {
        std::getline(in2, s);
        if(s.compare(0, 10, "ATTRIBUTES") == 0) break;
        std::stringstream ss(s);
        ss >> elem_id >> elem_type >> node1 >> node2;
        std::set<int>& s1 = node_to_sub[node1-1];
        std::set<int>& s2 = node_to_sub[node2-1];
        std::vector<int> v1;
        std::set_intersection(s1.begin(), s1.end(),
                              s2.begin(), s2.end(),
                              std::back_inserter(v1));
        if(elem_type == 6) { // beam
          if(v1.empty()) lines.push_back(elem_id);
          else {
            int sub_id = v1.front();
            dec[sub_id].push_back(elem_id);
          }
        }
        else { // shell
          ss >> node3;
          //std::cerr << ", node3 = " << node3 << std::endl;
          std::set<int>& s3 = node_to_sub[node3-1];
          std::vector<int> v2;
          std::set_intersection(v1.begin(), v1.end(),
                                s3.begin(), s3.end(),
                                std::back_inserter(v2));
          if(v2.empty()) {
            std::cerr << "ERROR: could not find subdomain for shell element #" << elem_id << std::endl;
            exit(-1);
          }
          else {
            int sub_id = v2.front();
            dec[sub_id].push_back(elem_id);
          }
        }
      } while(true);
    }
  } while(true);
  in2.close();

  for(int i=0; i<80; ++i) {
    std::cerr << "subdomain #" << i+1 << " has " << dec[i].size() << " elements\n";
  }
  std::cerr << "number of line elements = " << lines.size() << std::endl;

  // step 3: write decomposition file
  const int nl = 16; // number of subdomains for lines
  std::ofstream fout("DGB.cusDec."+std::to_string(80+nl));
  fout << "Decomposition dec for elemset\n"
       << " " << 80 + nl << std::endl;
  for(int i = 0; i < 80; ++i) {
    fout << " " << dec[i].size() << std::endl;
    for(int elem_id : dec[i]) fout << elem_id << std::endl;
  }
  for(int i = 0, k = 0; i < nl; ++i) {
    int size = lines.size()/nl + ((i < lines.size()%nl) ? 1 : 0);
    fout << " " << size << std::endl;
    for(int j = 0; j < size; j++, k++) fout << lines[k] << std::endl;
  }
  fout.close();
}
