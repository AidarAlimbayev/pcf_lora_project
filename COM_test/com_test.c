#include <stdio.h>

int main()
{
	int data[] = {10, 5, 13};
	FILE *file;
	file = fopen("/dev/ttyACM0", "w");
	int i = 0;
	for(i = 0 ; i < 3; i++){
		fprintf(file, "%d", data[i]);
		fprintf(file, "%c", ',');
		//sleep(1);
	}
	fclose(file);
}