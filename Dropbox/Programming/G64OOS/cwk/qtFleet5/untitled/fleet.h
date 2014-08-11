/*
 * Fleet.h
 *
 *  Created on: 7 Apr 2014
 *      Author: sam
 */

#ifndef FLEET_H_
#define FLEET_H_
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
using namespace std;


class Ship {
public:
    Ship();
    virtual ~Ship();

    virtual int getEnergyConsumption();
    virtual int getCost();
    virtual string getTypeName();
    virtual int getWeight();

protected:
    int Cost;
    int Weight;
    int EnergyConsumption;
    string Shiptype;
private:
};

class SolarSailShip : public Ship{
public:
    SolarSailShip(string type, int cost, int weight, int consump, int energy);
    virtual ~SolarSailShip();

    virtual int getEnergyProd();

protected:
    int energygen;
private:
};


class supplyShip :public Ship {
public:
    supplyShip(string type, int cost, int weight, int consump);
    virtual ~supplyShip();

protected:
private:
};

class ColonyShip : public Ship {
public:
    ColonyShip(string type, int cost, int weight, int consump, int cap, int supShip);
    virtual ~ColonyShip();

    virtual int getColonistCount();
    virtual void infect();
    virtual bool isInfected();
    virtual bool isDestroyed();
    virtual void addSupplyShip(supplyShip shp);

protected:
    int Capacity;
    int supplyNeeded;
    bool infection;
    bool destroyed;
    vector<supplyShip> thesupply;
private:
};





class Hospital {
public:
    Hospital();
    virtual ~Hospital();
protected:
private:
};

class Regeneration {
public:
    Regeneration();
    virtual ~Regeneration();
protected:
private:
};

class Medic : public Ship {
public:
    Medic(string type, int cost, int weight, int consump);
    virtual ~Medic();
protected:
private:
    Hospital* parthospital;
    Regeneration* partregeneration;
};



class Fleet {
public:
    Fleet();
    virtual ~Fleet();
    virtual int getWeight();
    virtual int getEnergyConsumption();
    virtual int getColonistCount();
    virtual int getCost();
    virtual int getEnergyProduction();
    virtual bool hasMedic();
    virtual string getCorporationName();
    virtual vector<ColonyShip*> colonyShip();
    virtual vector<Ship*> shipList();
    virtual void addcolonyShip(ColonyShip *shp);
    virtual void addship(Ship *shp);
    virtual void setCorpName(string name);
    virtual bool canBuy(int amount);

protected:

private:
    string CorpName;
    int Money;
    vector<Ship*> FleetList;  //was vector<Ship> *FleetList;
    vector<ColonyShip*> colonyList; // was vector<ColonyShip> *colonyList
};

void userInterfaceCreateFleet();
void saveFleet();
Fleet readFleet(string filename);
void writeFleet();

#endif /* Fleet_H_ */
