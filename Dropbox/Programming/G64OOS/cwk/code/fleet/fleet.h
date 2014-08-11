#ifndef FLEET_H
#define FLEET_H
#include <iostream>
#include <string>
#include <fstream>
#include<vector>

using namespace std;


class Ship {
private:
    string Shiptype;
    int Cost;
    int Weight;
    int EnergyConsumption;

public:
    Ship(string type, int cost, int weight, int consump);
    ~Ship();
    int getEnergyConsumption();
    int getWeight();
    int getCost();
    string getName();
};

class ColonyShip : public Ship
{
private:
    int Capacity;
    int supplyNeeded;
    bool infection;
public:
    ColonyShip(string type, int cost, int weight, int consump, int cap);
    ~ColonyShip();
    int getColonistCount();
    void infect();
    bool isInfected();
    bool isDestroyed();

};

class SolarSailShip : public Ship
{
private:
    int energyGen;
public:
    SolarSailShip(int Energy);
    ~SolarSailShip();
    int getEnergyProduction();
};

class supplyShip : public Ship
{
public:
    supplyShip();
    ~supplyShip();
};

class Hospital{
public:
    Hospital();
    ~Hospital();
};

class Regeneration{
public:
    Regeneration();
    ~Regeneration();
};

class Medic : public Ship
{
private:
    Hospital* partHospital;
    Regeneration* partRegeneration;
public:
    Medic();
    ~Medic();
    void addHospital(Hospital* h);
    void addRegeneration(Regeneration* r);
    void removeHospital();
    void removeRegerneration();
};

class fleet
{
private:
    // may need to change this so the fleet itereates the ship list
    // and return the values.
    int Money;
    string CorpName;

public:
    fleet();
    int getWight();
    int getEnergyConsumption();
    int getColonistCount();
    int getCost();
    int getEnergyProduction();
    bool hasMedic();
    string getCorporationName();
    vector<Ship> colonyShip();
    vector<Ship> shipList();
    void Arrived();
};

class UI {
public:
    void fleetgen(string type, string amount);
    void userInterfaceCreateFleet();
    void saveFleet();
    void readFleet();
    void writeFleet();
};

#endif // FLEET_H
