#include<iostream>
using namespace std;
int main ()
{
    int num, temp, i = 1, j, r;
    char hex[50];
    cout << " Enter a decimal number : ";
    cin >> num;
    temp = num;
    while (temp != 0)
    {
        r = temp % 16;
        if (r < 10)
            hex[i++] = r + 48;
        else
            hex[i++] = r + 55;
        temp = temp / 16;
    }
    cout << "\nHexadecimal equivalent of " << num << " is : ";
    for (j = i; j > 0; j--)
        cout << hex[j] << "\n" ;
    return 0;
}