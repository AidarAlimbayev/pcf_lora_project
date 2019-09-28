#include <iostream>
#include <iomanip>
#include <stdio.h>

using namespace std;

int main()
{
	//setlocale(LC_ALL, "");
	int n, m;
	int counter = 0;
    int counter2 = 0;
	cin >> n >> m;

	// ввод
	int array_fill[30][30];
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			array_fill[i][j] = 0;
		}
	}

	// заполнение
    int d, s, a, w;
    d = s = a = w = 0;

    for (int t = m * n; t != 0; t++)
    {
        if (d == 1){
            for(int i = 0; i < n; i++){
                d = 0;
                for (int j = 0; j < m; j++) {
		            counter++;
				    array_fill[i][j] = counter; 
                    


        }
        
        }            

    }
    




	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
		        counter++;
				array_fill[i][j] = counter;

                if (j == m){
                    
                }
        }
	}
	
	// вывод
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			//std::cout.width(2); std::cout << array_fill[i][j];
			cout << setw(3) << array_fill[i][j] << " ";
			//printf(" %4d", array_fill[i][j]);
			//printf(" %4d", array_fill[i][j]);
		}
		cout << endl;
	}
	return 0;
}