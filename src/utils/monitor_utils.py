###############################################################################################################
#   monitor_utils.py    Copyright (C) <2020-22>  <Kevin Scott>                                                #
#                                                                                                             #
#    Utility functions to gather and print information regarding the monitors .                               #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <22020-22>  <Kevin Scott>                                                                  #
#                                                                                                             #
#    This program is free software: you can redistribute it and/or modify it under the terms of the           #
#    GNU General Public License as published by the Free Software Foundation, either Version 3 of the         #
#    License, or (at your option) any later Version.                                                          #
#                                                                                                             #
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without        #
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#    GNU General Public License for more details.                                                             #
#                                                                                                             #
#    You should have received a copy of the GNU General Public License along with this program.               #
#    If not, see <http://www.gnu.org/licenses/>.                                                              #
#                                                                                                             #
###############################################################################################################

import datetime

############################################################################################ printMonitorResults ######
def printMonitorResults(monitorResults):
    """  Prints the Monitor results
    """
    inDate  = monitorResults.inDateMonitors  / monitorResults.totalMonitors * 100
    outDate = monitorResults.outDateMonitors / monitorResults.totalMonitors * 100

    print("-" + " Monitor Information " + "-"*58)
    print()
    print(f" Total Monitors    : {monitorResults.totalMonitors:4}             Monitors in date       : {monitorResults.inDateMonitors}  {inDate:.2f}%")
    print(f" Scrapped Monitors : {monitorResults.ScrappedMonitors:4}             Monitors out of date   : {monitorResults.outDateMonitors}  {outDate:.2f}%")
    print(f" Failed Monitors   : {monitorResults.FailedMonitors:4}             Monitors with errors   : {monitorResults.errDateMonitors}")
    print("="*80)
    print(f" Live Monitors     : {monitorResults.totalMonitors-monitorResults.ScrappedMonitors-monitorResults.FailedMonitors:4} \
                                        {monitorResults.inDateMonitors+monitorResults.outDateMonitors-monitorResults.errDateMonitors}")
    print()

############################################################################################ parseMonitors ############
def parseMonitors(monitors, monitorResults, logger):
    """  Loops through the directory monitors collating the Monitor results.
    """
    monitorResults.totalMonitors = len(monitors)

    for monitor in monitors:
        if monitor.Status == "Scrapped":
            monitorResults.ScrappedMonitors = monitorResults.ScrappedMonitors + 1
        elif monitor.Status == "Faulty":
            monitorResults.FailedMonitors = monitorResults.FailedMonitors + 1
        else:
            #  Only process live monitors.
            checkForErrors(monitor, monitorResults, logger)

            if monitor.PPMDueDate > datetime.datetime.now():
                monitorResults.inDateMonitors = monitorResults.inDateMonitors + 1
            else:
                monitorResults.outDateMonitors = monitorResults.outDateMonitors + 1


######################################################################################### checkForErrors ######
def checkForErrors(monitor, monitorResults, logger):
    """  Check for some common errors with the data.
    """
    future_date = datetime.datetime.now() + datetime.timedelta(days=365)

    if monitor.PPMDueDate == None:                                      #  In case of error.
        logger.error(f"{monitor.serialNumber} has no PPM date set.")
        monitorResults.errDateMonitors = monitorResults.errDateMonitors + 1
    if monitor.monitorType == "":
        logger.error(f"Monitor has no monitor type {monitor.serialNumber}.")
        monitorResults.errDateMonitors = monitorResults.errDateMonitors + 1
    if monitor.Site == "":
        logger.error(f"Monitor has no Site {monitor.serialNumber}.")
        monitorResults.errDateMonitors = monitorResults.errDateMonitors + 1
    if monitor.Status not in ("Scrapped", "Faulty", None):
        logger.error(f"Monitor has unknown status {monitor.serialNumber} of {monitor.Status}.")
        monitorResults.errDateMonitors = monitorResults.errDateMonitors + 1
    if monitor.PPMDueDate > future_date:
        logger.error(f"Monitor has a future date {monitor.serialNumber} of {monitor.PPMDueDate}.")
        monitorResults.errDateMonitors = monitorResults.errDateMonitors + 1




