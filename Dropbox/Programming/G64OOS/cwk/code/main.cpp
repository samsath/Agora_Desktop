#include<iostream>
#include<string>
#include<fstream>
#include<vector>
using namespace std;

int main(){
    string line;
    vector<string> list;
    ifstream fleetFile;
    fleetFile.open("sxh33m_fleet.dat");
    int v =0;
    string chr;
    while(!fleetFile.eof){
        if(ifleetFile.get(ch) != " "){
            chr = string(chr) + ch;
        }else{
            list.at(v) = chr;
            v++;
        }
    }
    for(vector<string>::iterator it = list.begin(); it != list.end(); ++list){
        cout << list << endl;

    }

    return 0;
}

