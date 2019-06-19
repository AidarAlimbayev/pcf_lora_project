#include <iostream>
#include <iomanip>

using namespace std;

int main()
{
    int n, m;
    cin >> n >> m;
    int a[n][m];
    //заполнение нулями
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            a[i][j] = 0;
        }
    }
    //заполнение
    int now0, now1;
    now0 = 0;
    now1 = 0;
    for(int x = 1; x < n * m; x++)
    {
        //n1
        while(a[now0][now1] == 0)
        {
            a[now0][now1] = x;
            x++;
            now1++;
        }
        now0++;
        //n2
        while(a[now0][now1] == 0)
        {
            a[now0][now1] = x;
            x++;
            now0++;
        }
        now1--;
        //n3
        while(a[now0][now1] == 0)
        {
            a[now0][now1] = x;
            x++;
            now1--;
        }
        now0--;

        while(a[now0][now1] == 0)
        {
            a[now0][now1] = x;
            x++;
            now0--;
        }
        now1++;
    }
    //вывод
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            cout << setw(4) << a[i][j] << " ";
        }
        cout << endl;
    }
    return 0;
}