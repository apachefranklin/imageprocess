#include <iostream>
#include <vector>
using namespace std;

std::vector<std::string> split_string(std::string chaine,std::string sep){
    std::vector<std::string> splitElts;
    std:string tempchaine=chaine;
    size_t pos = 0;
    std::string token;
    while ((pos = tempchaine.find(sep)) != std::string::npos)
    {
        token = tempchaine.substr(0, pos);
        splitElts.push_back(token);
        tempchaine.erase(0, pos + sep.length());
    }
    splitElts.push_back(tempchaine);
    return splitElts;

}

int main(int argc, char **argv)
{

    std::string s = "scott>=tiger>=mushroom";
    std::string delimiter = ">=";
    
    /* size_t pos = 0;
    std::string token;
    while ((pos = s.find(delimiter)) != std::string::npos)
    {
        token = s.substr(0, pos);
        std::cout << token << std::endl;
        s.erase(0, pos + delimiter.length());
    }
    std::cout << s << " "<<"apache"<< std::endl; */

    std::vector<string> splits=split_string(s,delimiter);

    for(std::string x:splits){
        cout<<x<<std::endl;
    }
    return 45;
}