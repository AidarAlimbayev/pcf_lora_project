#include <iostream>
#include <fstream>

int main (int argc, char* argv[])
{
	//open arduino device file
	std::ofstream arduino;
	arduino.open("/dev/ttyACM0");

	//write to it
	arduino << ;
	arduino.close();

	return 0;
}
