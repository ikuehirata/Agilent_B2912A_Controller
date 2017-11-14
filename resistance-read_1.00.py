# -*- coding: utf-8 -*-

import visa
import numpy as np
import sys
from datetime import datetime as dt
import pytz
import glob
import traceback

voltstar = 0 # source start 0
voltstop = 0.1 # source stop 0.1
voltpoin = 101 # steps

def checkSaveFileName(basefname):
    fname = "%s.csv"%(basefname)
    i = 2
    while len(glob.glob(fname)) > 0:
        fname = "%s-%g.csv"%(basefname, i)
        i = i + 1
    if i != 2:
        print "saved file %s"%fname
    return fname

def main():
    if len(sys.argv) < 2:
        print 'input device name'
        return 0
    else:
        basefname = sys.argv[1]

    # check output file duplicate
    fname = checkSaveFileName(basefname)

    # open instrument
    rm = visa.ResourceManager("C:/Windows/System32/visa64.dll")
    pia = rm.open_resource('USB0::0x0957::0x8E18::MY51140120::0::INSTR')

    # misc
    pia.write(":SYST:BEEP:STAT ON") # enable beep
    pia.write(":OUTP:ON:AUTO ON") # eanble automatic output on
    pia.write(":OUTP:OFF:AUTO ON") # enable automatic output off

    # setup measurement parameters
    pia.write(":sour:func:mode volt") # source mode volt
    pia.write(":sour:volt:mode swe") # source mode sweep
    pia.write(":sour:volt:star %g"%voltstar)
    pia.write(":sour:volt:stop %g"%voltstop)
    pia.write(":sour:volt:poin %g"%voltpoin)

    # compliance current 1 uA
    pia.write(":SENS:CURR:PROT 0.001")

    # setup measure mode to resistance
    pia.write(":SENS:FUNC ""RES""")

    # internal triggers
    pia.write(":TRIG:SOUR AINT")
    pia.write(":TRIG:COUN %g"%voltpoin)

    # turn on output switch
    pia.write(":OUTP ON")

    # initiate transition and acquire
    pia.write(":INIT (@1)")

    # fetch input voltage
    listvol = np.linspace(voltstar, voltstop, num=voltpoin)
    # fetch result (resistance)
    listres = np.array(pia.query_ascii_values(':FETC:ARR:RES? (@1)'))
    alldat = np.column_stack((listvol, listres))

    # display result as graph
    pia.write(":DISP:VIEW GRAP")

    # save data
    head = """data file made from Agilent B2912A Precision Source/Measure Unit by resistance-read.py
URL: https://github.com/ikuehirata/Agilent_B2912A_Controller

Data file created at %s UTC
Connection type %s (0 for 2-wire, 1 for 4-wire)
Trigger transition delay %s
Trigger acquisition delay %s
Voltage\tRegistance""" %\
    (dt.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S"),
     pia.query(':SENS:REM?').strip('\n'),
     pia.query(':TRIG:TRAN:DEL?').strip('\n'),
     pia.query(':TRIG:ACQ:DEL?').strip('\n'))
    np.savetxt(fname, alldat, delimiter='\t', header=head)

    # end of session beep
    pia.write(":SYST:BEEP 1760,0.2")

    # turn off output
    pia.write(":OUTP OFF")

try:
        main()
except:
        traceback.print_exc()
