using System;
using ReaderB;
using System.IO.Ports;
namespace test_rfid_2
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			string[] a = SerialPort.GetPortNames ();
			foreach (var item in a) {
				Console.WriteLine (item.ToString());
			}
			int port = 0;
			byte addrport =  Convert.ToByte(0x03f8);
			int PortHandle = 0;
			StaticClassReaderB.OpenComPort (0,ref addrport, 5,ref PortHandle);
			Console.Read();
			//Console.WriteLine ("Hello World!");
		}
	}
}
