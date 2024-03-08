#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <sstream>
#include <iomanip>

int main() {
  // NOTE: the outer surfaces are modified (and combined)
  std::ifstream in("mesh_Structural.surfacetop.tria");
  std::ofstream out1("MasterSurfaceTopology.include");
  out1 << "SURFACETOPO 161\n";
  std::ofstream out2("SlaveSurfaceTopology.include");
  out2 << "SURFACETOPO 162\n";
  std::string s, dummy;
  std::set<int> surface_nodes;
  int surface_id, face_id, face_type, node_A, node_B, node_C;
  do {
    std::getline(in, s);
    if(in.eof()) break;
    if(s[0] == '*') { continue; }
    if(s.compare(0, 11, "SURFACETOPO") == 0) {
      std::stringstream line(s);
      line >> dummy >> surface_id;
      if((surface_id)%2 == 0) surface_nodes.clear();
    }
    else {
      //if(surface_id < 5 || surface_id%2 == 1) { continue; } // only need to process the even-numbered gores
      std::stringstream line(s);
      line >> face_id >> face_type >> node_A >> node_B >> node_C;
      if(surface_id%2 == 0) { // master surface
        surface_nodes.insert(node_A);
        surface_nodes.insert(node_B);
        surface_nodes.insert(node_C);
        out1 << s << std::endl;
      }
      else {
        if(surface_nodes.find(node_A) == surface_nodes.end() &&
           surface_nodes.find(node_B) == surface_nodes.end() &&
           surface_nodes.find(node_C) == surface_nodes.end()) { // none of the slave nodes are on the master surface
          out2 << std::setw(6) << face_id << " " << std::setw(2) << face_type << " " << std::setw(6) << node_A
               << " " << std::setw(6) << node_B << " " << std::setw(6) << node_C << " " << std::endl;
        }
      }
    }
  } while(true);
}
