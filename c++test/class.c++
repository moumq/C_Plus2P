#include <iostream>
using namespace std;

class Rectangle {
private:
    int width, height;

public:
    Rectangle(int w, int h) : width(w), height(h) {}

    int area() {
        return width * height;
    }
};

int main() {
    Rectangle rect(5, 10);
    cout << "Area: " << rect.area() << endl;
    return 0;
}
