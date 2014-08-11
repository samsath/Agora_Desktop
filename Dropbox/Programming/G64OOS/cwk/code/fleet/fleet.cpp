#include "fleet.h"
#include <iostream>
#include <string>
#include <fstream>
#include<vector>

using namespace std;

enum string_code{
    Ferry,
    Liner,
    Cloud,
    Radiant,
    Ebulient,
    Medic
};

string_code hashit (string const& inString){
    if(inString == "Ferry") return Ferry;
    if(inString == "Liner") return Liner;
    if(inString == "Cloud") return Cloud;
    if(inString == "Radiant") return Radiant;
    if(inString == "Ebulient") return Ebulient;
    if(inString == "Medic") return Medic;
}


fleet::fleet()
{
// may need to change this so the FLEET itereates the ship list and return the values.
    vector<Ship> *colonyList = new vector<Ship>;
    vector<Ship> *shipList = new vector<Ship>;
}

fleet::~fleet(){
    //dtor
    delete colonyList;
    delete shipList;
}

int fleet::getWight(){
   //Returns the weight of the fleet
   int weight = 0;
   for (int i : *shipList){
       weight = i.getWeight() + weight;
   }
   return weight;
}

int fleet::getEnergyConsumption(){
    // Returns the fleets energy use
    int consump = 0;
    for(int i : *shipList){
        consump = i.getEnergyConsumption() + consump;
    }
    return consump;
}

int fleet::getColonistCount(){
    //Returns how many colonist there area in the fleet
    int pop =0;
    for(int i : *colonyList){
        pop = i.getColonistCount() + pop;
    }
    return pop;
}

int fleet::getCost(){
    //Returns the complete fleet cost
    int cost =0;
    for(int i : *shipList){
        cost = i.getCost() + cost;
    }
    return cost;
}

int fleet::getEnergyProduction(){
    //Return the complete energy production of the fleet
    int epro =0;
    for(int i: *shipList){
        if(i.getTypeName =="Radiant" || i.getTypeName() == "Ebulient" ){
            epro = i.getEnergyProduction() + epro;
        }
    }

    return epro;
}

bool fleet::hasMedic(){
    //Returns true if the fleet has a medic ship, false otherwise

    for(int i : *shipList){
        if(i.getTypeName() == "Medic" ){
            return true;
        }
    }
    return false;
}

string fleet::getCorporationName()const{
    //return what the name of the corporation is
    return CorpName;
}

vector<Ship> fleet::colonyShip(){
    //Returns a vector with ship pointers of all ships that are a colony ship
    return colonyList;
}

vector<Ship> fleet::shipList(){
    //Returns a vector with all ships in the fleet
    return shipList;
}

Ship::Ship(string type, int cost, int weight, int consump){
    Shiptype = type;
    Cost = cost;
    Weight = weight;
    EnergyConsumption = consump;
}

Ship::~Ship(){

}

int Ship::getEnergyConsumption()const{
    //Returns energy consumption of a ship
    return EnergyConsumption;
}

int Ship::getWeight()const{
    //Returns weight of a ship
    return Weight;
}

int Ship::getCost()const{
    //Returns cost of a ship
    return Cost;
}

string Ship::getTypeName()const{
    //Returns the ship type (e.g. Ferry or Radiant); make sure you use the correct spelling!

    return Shiptype;
}

ColonyShip::ColonyShip(string type, int cost, int weight, int consump, int cap){
    Shiptype = type;
    Cost = cost;
    Weight = weight;
    EnergyConsumption = consump;
    Capacity = cap;

}

ColonyShip::~ColonyShip(){

}

int ColonyShip::getColonistCount(){
    //Returns number of colonists of a ship
    return Capacity;
}

void ColonyShip::infect(){
    // Infects a colony ship
    int check = 0;
    for(int i : fleet::shipList){
        if(i.getTypeName() == "Medic"){
            check = 1;
        }
    }
    if (check == 1){
        infection = false;
    } else {
        infection = true;
    }

}

bool ColonyShip::isInfected(){
    //Returns "true" if the ship is infected with a disease, "false" otherwise

    return isInfected;
}

bool ColonyShip::isDestroyed() const{
    return destroyed;
}

SolarSailShip::SolarSailShip(int Energy){
    energyGen = Energy;
}

SolarSailShip::~SolarSailShip(){

}

int SolarSailShip::getEnergyProduction(){
    //Returns energy production of Solar Sail Ship

    return energyGen;
}

supplyShip::supplyShip(){

}

supplyShip::~supplyShip(){

}



Hospital::Hospital(){

}

Hospital::~Hospital(){

}

Regeneration::Regeneration(){

}

Regeneration::~Regeneration(){

}

Medic::Medic(){

}

Medic::~Medic(){

}

void Medic::addHospital(Hospital* h){
    partHospital = h;

}
void Medic::addRegeneration(Regeneration* r){
    partRegeneration = r;

}
void Medic::removeHospital(){
    partHospital = NULL;
}

void Medic::removeRegerneration(){
    partRegeneration = NULL;
}




void userInterfaceCreateFleet(){

}

void saveFleet(){

}

void fleetgen(string type, string amount){
    //cout << type << " is at point" << amount << endl;
    int c  = atoi(amount.c_str());
    int clocked =0;
    while(clocked <= c){
        switch(hashit(type)){
            // this has all the ship types here
            // colony ships
            //supply ship cost 100, weight 2, energy con 3
            case Ferry:
                // colonist 100 cost 500 weight 10 energycon 5
                // requires 1 supply ship
                ColonyShip *Ferry = new ColonyShip("Ferry",500,10,5,100);
                cout << "Create Ferry" << endl;
                supplyShip *Supply = new supplyShip();
                cout << "Supply ship" << endl;
                fleet::colonyList.pop_back(*Ferry);
                fleet::shipList.pop_back(*Supply);
                clocked++;
                break;
            case Liner:
                // colonist 250 cost 1000 weight 20 energy 7
                // requires 2 supply ships
                cout << "Create Liner" << endl;
                cout << "Create Supply" << endl;
                cout << "Create Supply" << endl;
                clocked++;
                break;
            case Cloud:
                // colonist 750 cost 2000 weight 40 energy 10
                // requires 4 supply ships
                cout << "Create Cloud" << endl;
                cout << "Create Supply" << endl;
                cout << "Create Supply" << endl;
                cout << "Create Supply" << endl;
                cout << "Create Supply" << endl;
                clocked++;
                break;
            //Solar sail ship
            case Radiant:
                // energy gen 50 cost 50 weight 3 energycon 5
                cout << "Create Radiant" << endl;
                clocked++;
                break;
            case Ebulient:
                //energygen 500 cost 350 weight 50 energycon 5
                cout << "Create Ebulient" << endl;
                clocked++;
                break;
            //Medic
            case Medic:
                // cost 1000 weight 1 energy 1
                //will auto create the composed of a hospital and a regeneration
                cout << "Create Medic" << endl;
                clocked++;
                break;
            }


    }
}

void readFleet(){
    fleet* fleets = new fleet();

    vector<string> logs;
    vector<string> myLines;
    string line;

    cout << "Testing loading of file." << endl;
    ifstream myfile ("sxh33m_fleet.dat");
    while(getline(myfile,line)){
            stringstream s(line);
            while(!s.eof()){
                string tmp;
                s >>tmp;
                myLines.push_back(tmp);
            }
    }
    for(int i =0; i < myLines.size(); i++){
        if(i%2 == 0 ){
            fleetgen(myLines.at(i),myLines.at(i+1));

        }

    }
    return fleets;
}

void writeFleet(){

}
