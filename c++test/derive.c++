#include <iostream>
using namespace std;

class Base1 {
public:
    void printBase1() {
        cout << "Base1" << endl;
    }
};

class Base2 {
public:
    void printBase2() {
        cout << "Base2" << endl;
    }
};

class Derived : public Base1, public Base2 {
};

int main() {
    Derived d;
    d.printBase1();
    d.printBase2();
    return 0;
}
