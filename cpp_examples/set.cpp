#include <iostream>
#include <set>

using namespace std;
int main() {
    set <int> s;
    int n;
    cin << n;
    for (int i = 0; i < n; i++){
        int type, x;
        cin >> type >> x;
        if (type == 1) { // add
            s.insert(x);
        }
        else if (type == 2){ //
            if (s.find(x) == s.end()){
                cout << "NO\n";
            }
            else {
                cout << "YES\n";
            }
        }
        else { // substract
            s.erase(x);

        }
    }
    return 0;
}