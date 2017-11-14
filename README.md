# Agilent_B2912A_Controller
Agilent B2912A Precision Source/Measure Unit controller by PyVISA.  

### Requirement ###
+ Python 2.x
+ NumPy
+ PyVISA

### Usage ###
Run the program with output file name as an argument
    ``python resistance-read.py output``
and you get tab-separated output.csv.
Customize setups accordingly. Details can be found at 
[User's Guide](http://literature.cdn.keysight.com/litweb/pdf/B2910-90010.pdf?id=1357946),
[Programming Guide](http://literature.cdn.keysight.com/litweb/pdf/B2910-90020.pdf?id=1240149), and 
[SCPI Command Reference](http://literature.cdn.keysight.com/litweb/pdf/B2910-90030.pdf?id=1240049).


### What this does ###
1. Sets connection to B2912A at USB port USB0::0x0957::0x8E18::MY51140120::0::INSTR (check the USB address by Keysight Connection Expert).
2. Sets voltage sweep paramter.
3. Performs sweep.
4. Saves voltage and resistance data.
5. Displays graph on the display.

-----
# Updates  
2017 Nov 14 Version 1.00 uploaded
