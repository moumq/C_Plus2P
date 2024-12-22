#include<iostream>
#include<string>
#include<algorithm>
using namespace std;
int main(){
	string a;
	cin>>a;
	string b=a;
	int l=0,r=b.length()-1;
    while(l<r){
        swap(b[l],b[r]);
        l++;r--;
    }
    if (a == b) cout << "True" << endl;
    else cout <<  "False" << endl;
	return 0;
}
