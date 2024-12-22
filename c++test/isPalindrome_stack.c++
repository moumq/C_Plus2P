#include<iostream>
#include<string>
#include<algorithm>
#include<stack>

using namespace std;
int main() {
	stack<char> p;
	string a;
	cin >> a;
	for (int i = 0; i < a.length(); i++) p.push(a[i]); 
	string b;
	while (!p.empty()) {
		 b += p.top();  
		 p.pop();       
	}
	if (a == b) cout <<  "True" << endl;
	else cout <<  "False" << endl;
	return 0;
}
