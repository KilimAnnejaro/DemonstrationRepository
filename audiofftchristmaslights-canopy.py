""" The purpose of this program is to convert audio data into
light/visual data using the pyaudio module and Fast Fourier Transform machinery.
The project was inspired by Mahesh Venkitachalam's book Python Playground as
well as a Christmas lights display in Appleton.
In particular, most of the audio readin data coding came from the book. 
I made the GUI and the graphics printouts.

Primary author: Anne E. Ulrich
Additional contributors: (none yet)
    
Citation from GitHub (username electronut):
laser.py
Description: Analyze audio input using FFT and send motor speed/direction 
              information via serial port. This is used to create 
              Lissajous-like figures using 2 motors with mirrors, 
              a laser pointer, and an Arduino microcontroller.
Author: Mahesh Venkitachalam
Website: electronut.in
Sample Run: 
$python laser.py --port /dev/tty.usbserial-A7006Yqb
opening  /dev/tty.usbserial-A7006Yqb
opening stream...
^Cstopping...
cleaning up

improvements: color changes (to match vocals?) 

"""

import pyaudio
import numpy
import math
import time
import turtle

#This method draws a circle and fills it with the desired color.
def drawCircleTurtle(r,c):
    turtle.up()
    x = 0
    y = 0
    turtle.setpos(x+r,y)
    turtle.color(c,c)
    turtle.down()
    turtle.begin_fill()
    turtle.circle(r)
    turtle.end_fill()
    #I wanted to make sure the viewer saw the circle rather than having it just 
    #disappear.
    time.sleep(0.1)    
    turtle.clear()
   
# get pyaudio input device
# Code from Python Playground
def getInputDevice(p):
    index = None
    nDevices = p.get_device_count()
    print('Found %d devices. Select input device:' % nDevices)
    
    # print all devices found
    for i in range(nDevices):
        deviceInfo = p.get_device_info_by_index(i)
        devName = deviceInfo['name']
        print("%d: %s" % (i, devName))
    # get user selection
    try:
        # get user selection and convert to integer
        index = int(input())
    except:
        pass

    # print out chosen device
    if index is not None:
        devName = p.get_device_info_by_index(index)["name"]
        print("Input device chosen: %s" % devName)
    return index
    
# fft of live audio
#Code mostly from Python Playground with my turtle method call
#at the end.
def fftLive():
  # initialize pyaudio
  p = pyaudio.PyAudio()

  # get pyAudio input device index
  inputIndex = getInputDevice(p)

  # set FFT sample length
  fftLen = 2**11
  # set sample rate
  sampleRate = 44100

  print('opening stream...')
  stream = p.open(format = pyaudio.paInt16,
                  channels = 1,
                  rate = sampleRate,
                  input = True,
                  frames_per_buffer = fftLen,
                  input_device_index = inputIndex)
  
  try:
      while True:
          # read a chunk of data
          data  = stream.read(fftLen)
          # convert to numpy array
          dataArray = numpy.frombuffer(data, dtype=numpy.int16)

          # get FFT of data
          fftVals = numpy.fft.rfft(dataArray)*2.0/fftLen
          # get absolute values of complex numbers
          fftVals = numpy.abs(fftVals)
          # get average of 3 frequency bands
          # 0-100 Hz, 100-1000 Hz and 1000-2500 Hz
          levels = [numpy.sum(fftVals[0:100])/100,
                    numpy.sum(fftVals[100:1000])/900,
                    numpy.sum(fftVals[1000:2500])/1500]

          #Defining the radius based on the music's beat.
          r=levels[0]%50
          
          #This code is intended to change the circle's color with the 
          #harmonics of the music. We are assigning a color to the circle
          #based on the music's melody frequency range.
          if levels[1]<10:
              drawCircleTurtle(r,"white")
          elif levels[1]<20:
              drawCircleTurtle(r,"blue")
          elif levels[1]<30:
              drawCircleTurtle(r,"green")
          elif levels[1]<40:
              drawCircleTurtle(r,"yellow")
          elif levels[1]<50:
              drawCircleTurtle(r,"orange")
          elif levels[1]<60:
              drawCircleTurtle(r,"red")
          else:
              drawCircleTurtle(r,"purple")

  except KeyboardInterrupt:
      print('stopping...')
  finally:
      print('cleaning up')
      stream.close()
      p.terminate()

# main method
def main():
    fftLive()
    #Originally Python Playground had more things being called from
    #the main method. I left it (rather than moving in the FFT Live code) 
    #because I had in mind the future possibility of defining more function 
    #calls than just fftlive().
    
# call main function
if __name__ == '__main__':
    main()