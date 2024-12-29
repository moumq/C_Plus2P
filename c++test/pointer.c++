#include <iostream>
using namespace std;

void modifyValue(int &ref) {
    ref = 100;
}

int main() {
    int a = 10;
    int *ptr = &a;
    modifyValue(a);
    cout << "a: " << a << endl;
    cout << "*ptr: " << *ptr << endl;
    return 0;
}
