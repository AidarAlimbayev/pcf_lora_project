#include <iostream>

using namespace std;

int main() {
 	double a, b, c, d, e, f, x, y, x_delta, y_delta, delta;
 	x = 0; 
  	y = 0;
  	x_delta = 0;
  	y_delta = 0;
  	delta = 0;
  	cin >> a >> b >> c >> d >> e >> f;
  	delta = (a * d) - (b * c);
	x_delta = (e * d) - (b * f);
	y_delta = (a * f) - (e * c);

	if (delta != 0) {
		x = x_delta/delta;
		y = y_delta/delta;
		cout << x << " " << y;
	} else {
		cout << 0;
	}

  return 0;
}