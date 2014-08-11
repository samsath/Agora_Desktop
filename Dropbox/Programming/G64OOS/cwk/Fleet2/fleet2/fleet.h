#ifndef FLEET_H
#define FLEET_H
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
using namespace std;

class fleet
{
public:
    fleet();
};


void userInterfaceCreateFleet();
void saveFleet();
void fleetgen(string type, string amount);
void readFleet(string loc);
void writeFleet();


#endif // FLEET_H
