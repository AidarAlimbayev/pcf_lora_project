#include <iostream>

using namespace std;

int main() {
 	
 	double k, n, a, b, c, d, e, f, x, y, x_delta, y_delta, delta;
 	x = 0; 
  	y = 0;

  	x_delta = 0;
  	y_delta = 0;
  	delta = 0;
  	cin >> a >> b >> c >> d >> e >> f;
  	delta = (a * d) - (b * c);
	x_delta = (e * d) - (b * f);
	y_delta = (a * f) - (c * e);

	if (delta != 0) {
		x = x_delta/delta;
		y = y_delta/delta;
		cout << 2 << " " << x << " " << y;
	} else {
		if (x_delta == 0 && y_delta == 0){
			if (a == 0 && b == 0 && c == 0 && d == 0){
				if (e != 0 || f != 0) {
					cout << 0;
				} else {
					cout << 5;
				}
			} else {
				if (a == 0 && c == 0){
					if(b != 0){
						y = e/b;
						cout << 4 << " " << y;
					} else {
						y = f/d;
						cout << 4 << " " << y;
					}
				} else {
					if (b == 0 && d == 0){
						if (a != 0) {
							x = e/a;
							cout << 3 << " " << x;
						} else {
							x = f/c;
							cout << 3 << " " << x;
						}
					} else {
						if (b != 0){
							n = e/b;
							k = -a/b;
							cout << 1 << " " << k << " " << n;
						} else {
							n = f/d;
							k = -c/d;
							cout << 1 << " " << k << " " << n;
						}
					}
				}
			}
		} else {
			cout << 0;
		}
	}
  return 0;
}
// #include <iostream>

// using namespace std;

// int main() {
//  	double a, b, c, d, e, f, x, y, x_delta, y_delta, delta;
//  	x = 0; 
//   	y = 0;
//   	x_delta = 0;
//   	y_delta = 0;
//   	delta = 0;
//   	cin >> a >> b >> c >> d >> e >> f;
//   	delta = (a * d) - (b * c);
// 	x_delta = (e * d) - (b * f);
// 	y_delta = (a * f) - (e * c);

// 	if (delta != 0) {
// 		x = x_delta/delta;
// 		y = y_delta/delta;
// 		cout << x << " " << y;
// 	} else {
// 		cout << 0;
// 	}

//   return 0;
// }