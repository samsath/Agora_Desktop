#include "fleet.h"
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>

using namespace std;

fleet::fleet()
{
}

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
                cout << "Create Ferry" << endl;
                cout << "Supply ship" << endl;
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

void readFleet(string loc){

        vector<string> logs;
        vector<string> myLines;
        string line;

        cout << "Testing loading of file." << endl;
        ifstream myfile (loc);
        if(myfile != NULL){
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
        }else{
            cout << "File didnt load" << endl;
        }
}

void writeFleet(){

}
