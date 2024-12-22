#include <iostream>
using namespace std;

class Complex {
private:
    double real, imag;

public:
    Complex(double r, double i) : real(r), imag(i) {}

    Complex operator+(const Complex &other) {
        return Complex(real + other.real, imag + other.imag);
    }

    void print() {
        cout << real << " + " << imag << "i" << endl;
    }
};

int main() {
    Complex c1(5, 3), c2(2, 4);
    Complex c3 = c1 + c2;
    c3.print();
    return 0;
}
