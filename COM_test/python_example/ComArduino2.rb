# 19 July 2014

# this is designed to work with ... ArduinoPC2.ino ...

# this receives data prefixed by < and terminated by >

# this version uses JSSC - Java Simple Serial Connector - rather than RxTx 
#     RXTX seems to have disappeared from the web
#   apparently all the necessary binaries are included in the Jar
#   note that JSSC returns a signed java byte -  hence & 0xFF to convert to an unsigned value
#   also note the use of .to_java_bytes to convert the JRuby string into a Java byte array

#============================

def waitForArduino

    # wait until the Arduino sends something - allows time for Arduino reset
   msg = ""
   while msg.include?("Arduino is ready") != true

      while $sp.getInputBufferBytesCount == 0
      end
      
      msg = recvFromArduino
      
   end
   puts msg
   puts "========="
    
end

#=====================================

def sendToArduino(sendStr)

	$sp.writeBytes(sendStr.to_java_bytes)
	
end

#======================================

def recvFromArduino

	ck = ""
  x = 32 # any value that is not an end- or $startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many

    # wait for the start character
  while  x != $startMarker 
    x = $sp.readBytes(1)[0] & 0xFF
  end
    
    # save data until the end marker is found
  while x != $endMarker
    if x != $startMarker
      ck = ck + x.chr
      byteCount += 1
    end
    x = $sp.readBytes(1)[0] & 0xFF
  end
    
  return ck

end


#=====================================

def setupStuff

    $LOAD_PATH << Dir.pwd

    require 'java'
    require 'lib/jssc.jar' 
    java_import('jssc.SerialPort')
    java_import('jssc.SerialPortException')

end

#==================

def openSerial

    baudRate = 9600
    serialPort = "/dev/ttyS80"

    $sp = SerialPort.new(serialPort)
    $sp.openPort
    $sp.setParams(baudRate, 8, 1, 0)
    
    at_exit{ $sp.closePort if $sp.isOpened }

    puts "Serial port #{serialPort} opened"
    puts "Baud Rate #{baudRate}"
    
end

#=================

def runTest(td)

    numLoops = td.size
    waitingForReply = false
    
    n = 0
    while n < numLoops

	    teststr = td[n]

	    if waitingForReply == false
	      sendToArduino(teststr)
	      puts "Sent from PC -- LOOP NUM #{n} TEST STR #{teststr}"
        waitingForReply = true
	    end

      if waitingForReply == true

          while $sp.getInputBufferBytesCount == 0
          end
	
          dataRecvd = recvFromArduino
          puts "Reply Received  #{dataRecvd}"
          n += 1
          waitingForReply = false

          puts "==========="
      end
      
      sleep 5

    end # while n < numLoops
end

#======================================

# the program starts here

puts
puts

setupStuff

openSerial

$startMarker = 60
$endMarker = 62

waitForArduino

testData = []
testData[0] = "<LED1,200,0.2>"
testData[1] = "<LED1,800,0.7>"
testData[2] = "<LED2,800,0.5>"
testData[3] = "<LED2,200,0.2>"
testData[4] = "<LED1,200,0.7>"

runTest(testData)

