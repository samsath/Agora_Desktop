/*
 * Fleet.cpp
 *
 *  Created on: 7 Apr 2014
 *      Author: sam
 */
#include "fleet.h"
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>




enum string_code{
    Ferry,
    Liner,
    Cloud,
    Radiant,
    Ebulient,
    Medica
};

string_code hashit (string const& inString){
    if(inString == "Ferry") return Ferry;
    if(inString == "Liner") return Liner;
    if(inString == "Cloud") return Cloud;
    if(inString == "Radiant") return Radiant;
    if(inString == "Ebulient") return Ebulient;
    if(inString == "Medic") return Medica;
};


Fleet::Fleet() {
    Money = 10000;

}

Fleet::~Fleet() {

}

int Fleet::getWeight(){
    int weight = 0;
    for (unsigned i = 0; i < FleetList.size();i++){
        weight = FleetList.at(i)->getWeight() + weight;
    }
    return weight;
}

int Fleet::getEnergyConsumption(){
    int consump = 0;
    for (unsigned i =0; i < FleetList.size();i++){
        consump = FleetList.at(i)->getEnergyConsumption() + consump;
    }
    return consump;
}

int Fleet::getColonistCount()
{
    int pop = 0;
    for (unsigned i =0; i < colonyList.size();i++){
        pop = colonyList.at(i)->getColonistCount() + pop;
    }
    return pop;
}

int Fleet::getCost(){
    int cost = 0;
    for(unsigned i = 0; i<FleetList.size(); i++){
        cost = FleetList.at(i)->getCost() + cost;
    }
    return cost;
}

int Fleet::getEnergyProduction(){
    int epro = 0;

    for(unsigned i = 0; i<FleetList.size(); i++){
        if(FleetList.at(i)->getTypeName() == "Radiant" || FleetList.at(i)->getTypeName() == "Ebulient"){
            SolarSailShip* solar = dynamic_cast<SolarSailShip*>(FleetList.at(i));
            if(solar){
                epro = solar->getEnergyProd() + epro;
            }
        }
    }
    return epro;
}

bool Fleet::hasMedic(){
     for (unsigned i = 0; i < FleetList.size(); i++){
         if(FleetList.at(i)->getTypeName() == "Medic"){
             return true;
         }
     }
     return false;
}

string Fleet::getCorporationName(){
    return CorpName;
}

vector<ColonyShip*> Fleet::colonyShip(){
    return colonyList;
}

vector<Ship*> Fleet::shipList(){
    return FleetList;
}

void Fleet::addcolonyShip(ColonyShip *shp){
    colonyList.push_back(shp);
}

void Fleet::addship(Ship *shp){
    FleetList.push_back(shp);
}

void Fleet::setCorpName(string name)
{
    CorpName = name;
}

bool Fleet::canBuy(int amount){
    int newAmount = Money - amount;
    if(newAmount >= Money){
        Money = newAmount;
        return true;
    }else{
        return false;
    }
}

Ship::Ship(){
}

Ship::~Ship(){

}

int Ship::getEnergyConsumption(){
    return EnergyConsumption;
}

int Ship::getCost(){
    return Cost;
}

string Ship::getTypeName(){
    return Shiptype;
}

int Ship::getWeight(){
    return Weight;
}

ColonyShip::ColonyShip(string type, int cost, int weight, int consump, int cap, int supShip){
    Shiptype = type;
    Cost = cost;
    Weight = weight;
    EnergyConsumption = consump;
    Capacity = cap;
    supplyNeeded = supShip;
    infection = false;
    destroyed = false;

}

ColonyShip::~ColonyShip(){

}

int ColonyShip::getColonistCount()
{
    return Capacity;
}

void ColonyShip::infect(){
    int check =0;
    Fleet Fleets;
    vector<ColonyShip*> colList = Fleets.colonyShip();
    for(unsigned i =0; i < colList.size(); i++){
        if(colList.at(i)->getTypeName() == "Medic"){
            check=1;
        }
    }
    if(check==1){
        infection = false;
    }else{
        infection = true;
    }
}

bool ColonyShip::isInfected(){
    return infection;
}

bool ColonyShip::isDestroyed(){
    return destroyed;
}

void ColonyShip::addSupplyShip(supplyShip shp){
    thesupply.push_back(shp);
}

supplyShip::supplyShip(string type, int cost, int weight, int consump){
    Shiptype = type;
    Cost = cost;
    Weight = weight;
    EnergyConsumption = consump;
}

supplyShip::~supplyShip(){

}

SolarSailShip::SolarSailShip(string type, int cost, int weight, int consump, int energy){
    Shiptype = type;
    Cost = cost;
    Weight = weight;
    EnergyConsumption = consump;
    energygen = energy;
}

int SolarSailShip::getEnergyProd()
{
    return energygen;
}


Hospital::Hospital(){

}

Hospital::~Hospital(){

}

Regeneration::Regeneration(){

}
Regeneration::~Regeneration(){

}


Medic::Medic(string type, int cost, int weight, int consump){
    Shiptype = type;
    Cost = cost;
    Weight = weight;
    EnergyConsumption = consump;
    parthospital = new Hospital();
    partregeneration = new Regeneration();
}

Medic::~Medic(){

}

void userInterfaceCreateFleet(){

}

void saveFleet(){

}


Fleet readFleet(string filename){
    Fleet* Fleets = new Fleet();


    vector<string> myLines;
    string line;

    cout << "Testing loading of file." << endl;
    ifstream myfile (filename);
    while(getline(myfile,line)){
            stringstream s(line);
            while(!s.eof()){
                string tmp;
                s >>tmp;
                myLines.push_back(tmp);
            }
    }
    Fleets->setCorpName(myLines.at(0));
    cout << Fleets->getCorporationName() << endl;
    for(int i =1; i < myLines.size(); i++){
        if(i%2 == 1 ){
            //Fleetgen(*Fleets, myLines.at(i),myLines.at(i+1));
            istringstream buffer(myLines.at(i+1));
            int c;
            buffer >> c;
            int clocked =0;
            while(clocked <= c){
                switch(hashit(myLines.at(i))){
                    // this has all the ship types here
                    // colony ships
                    //supply ship cost 100, weight 2, energy con 3
                    case Ferry:
                        {
                        // colonist 100 cost 500 weight 10 energycon 5
                        // requires 1 supply ship
                        //if(f.canBuy(600)){
                            ColonyShip* ferry = new ColonyShip("Ferry",500,10,5,100,1);
                            supplyShip* Suplly = new supplyShip("Supplier",100,2,3);

                            ferry->addSupplyShip(*Suplly);
                            //cout << "got here" << endl;
                            Fleets->addcolonyShip(ferry);
                            cout << "Create Ferry" << endl;
                            Fleets->addship(ferry);
                            Fleets->addship(Suplly);
                            cout << "Supply ship" << endl;
                            clocked++;

                        }
                        break;
                    case Liner:
                        {
                            // colonist 250 cost 1000 weight 20 energy 7
                            // requires 2 supply ships
                            ColonyShip* liner = new ColonyShip("Liner",1000,20,7,250,2);
                            cout << "Create Liner" << endl;
                            supplyShip* Suplly1 = new supplyShip("Supplier",100,2,3);
                            cout << "Create Supply" << endl;
                            supplyShip* Suplly2 = new supplyShip("Supplier",100,2,3);
                            cout << "Create Supply" << endl;
                            Fleets->addcolonyShip(liner);
                            Fleets->addship(liner);
                            Fleets->addship(Suplly1);
                            Fleets->addship(Suplly2);
                            liner->addSupplyShip(*Suplly1);
                            liner->addSupplyShip(*Suplly2);
                            clocked++;
                        }
                        break;
                    case Cloud:
                        {
                            // colonist 750 cost 2000 weight 40 energy 10
                            // requires 4 supply ships
                            ColonyShip* cloud = new ColonyShip("Cloud",2000,40,10,750,4);
                            cout << "Create Cloud" << endl;
                            supplyShip* Suplly1 = new supplyShip("Supplier",100,2,3);
                            cout << "Create Supply" << endl;
                            supplyShip* Suplly2 = new supplyShip("Supplier",100,2,3);
                            cout << "Create Supply" << endl;
                            supplyShip* Suplly3 = new supplyShip("Supplier",100,2,3);
                            cout << "Create Supply" << endl;
                            supplyShip* Suplly4 = new supplyShip("Supplier",100,2,3);
                            cout << "Create Supply" << endl;
                            Fleets->addcolonyShip(cloud);
                            Fleets->addship(cloud);

                            Fleets->addship(Suplly1);
                            Fleets->addship(Suplly2);
                            Fleets->addship(Suplly3);
                            Fleets->addship(Suplly4);

                            cloud->addSupplyShip(*Suplly1);
                            cloud->addSupplyShip(*Suplly2);
                            cloud->addSupplyShip(*Suplly3);
                            cloud->addSupplyShip(*Suplly4);

                            clocked++;
                        }
                        break;
                    //Solar sail ship
                    case Radiant:
                        {
                            // energy gen 50 cost 50 weight 3 energycon 5
                            SolarSailShip* radiant = new SolarSailShip("Radiant",50,3,5,50);
                            Fleets->addship(radiant);
                            cout << "Create Radiant" << endl;
                            clocked++;
                        }
                        break;
                    case Ebulient:
                        {
                            //energygen 500 cost 350 weight 50 energycon 5
                            SolarSailShip* ebulient = new SolarSailShip("Ebulient",350,50,5,500);
                            Fleets->addship(ebulient);
                            cout << "Create Ebulient" << endl;
                            clocked++;
                        }
                        break;
                    //Medic
                    case Medica:
                        {
                            // cost 1000 weight 1 energy 1
                            //will auto create the composed of a hospital and a regeneration
                            Medic* medic = new Medic("Medic",1000,1,1);
                            Fleets->addship(medic);
                            cout << "Create Medic" << endl;
                            clocked++;
                        }
                        break;
                    }


            }

        }

    }
    cout << Fleets->getCorporationName() << endl;
    return *Fleets;
}


void writeFleet(){

}
