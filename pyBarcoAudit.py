###############################################################################################################
#    pyBarcoAudit   Copyright (C) <2020>  <Kevin Scott>                                                       #                                                                                                             #
#    The program will scan a Excel spreadsheet of calibration dates and produce a usage report.               #
#                                                                                                             #
# usage: pyBarcoAudit.py [-h] [-s SOURCE]                                                                     #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2020>  <Kevin Scott>                                                                      #
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

import textwrap
import argparse
import datetime
from pathlib import Path
import colorama
import myTimer
import myConfig
import myLogger
from openpyxl import load_workbook
from tqdm import tqdm
from dataClasses import Monitor, Results
from myLicense import printLongLicense, printShortLicense
from dataMapping import *

############################################################################################ printResults ######
def printResults(results):
    """  Prints the results
    """
    inDate  = results.inDateMonitors  / results.totalMonitors * 100
    outDate = results.outDateMonitors / results.totalMonitors * 100

    print("-"*85)
    print(f" Total Monitors    : {results.totalMonitors:4}             Monitors in date          : {results.inDateMonitors}  {inDate:.2f}%")
    print(f" Scrapped Monitors : {results.ScrappedMonitors:4}             Monitors out of date      : {results.outDateMonitors}  {outDate:.2f}%")
    print(f" Failed Monitors   : {results.FailedMonitors:4}             Monitors with no due date : {results.errDateMonitors}")
    print("="*75)
    print(f" Live Monitors     : {results.totalMonitors-results.ScrappedMonitors-results.FailedMonitors:4} \
                                        {results.inDateMonitors+results.outDateMonitors-results.errDateMonitors}")


############################################################################################ parseMonitors ######
def parseMonitors(monitors, results):
    """  Loops through the directory monitors collating the results.
    """
    results.totalMonitors = len(monitors)

    for monitor in monitors:
        if monitor.Status == "Scrapped":
            results.ScrappedMonitors = results.ScrappedMonitors + 1
        elif monitor.Status == "Faulty":
            results.FailedMonitors = results.FailedMonitors + 1
        else:
            #  Only process live monitors.
            if monitor.PPMDueDate == None:                                      #  In case of error.
                logger.error(f"{monitor.serialNumber} has no PPM date set.")
                results.errDateMonitors = results.errDateMonitors + 1

            if monitor.PPMDueDate > datetime.datetime.now():
                results.inDateMonitors = results.inDateMonitors + 1
            else:
                results.outDateMonitors = results.outDateMonitors + 1

############################################################################################ scanWorkBook ######
def scanWorkBook(source, monitors):
    """  Loads the spreadsheet, already been validated.
         Populates the directory monitors with the contents of the spreadsheet.
    """
    #  Load the spreadsheet in read only [don't want to accidentally amend]
    #  and only load data and not formulas.
    workBook = load_workbook(filename=source, read_only=True, data_only=True)

    #  Grab the active worksheet
    workSheet = workBook.active
    logger.info(f"Scanning {workSheet.title} in {source}")

    for row in tqdm(workSheet.iter_rows(min_row = MIN_ROW,
                                        max_row = MAX_ROW,
                                        min_col = MIN_COL,
                                        max_col = MAX_COL,
                                        values_only=True), unit=" rows", ncols=myConfig.NCOLS):

        monitor = Monitor(monitorType    = row[MONITOR_TYPE],
                          serialNumber   = row[SERIAL_NUMBER],
                          CliEng_ID      = row[CE_ID],
                          PCAssetNumber  = row[PC_ASSET_NO],
                          Site           = row[SITE],
                          Location       = row[LOCATION],
                          DisplayTime    = row[DISPLAY_TIME],
                          BacklightTime  = row[BACKLIGHT_TIME],
                          InstalledDate  = row[INSTALLED_DATE],
                          AcceptanceDate = row[ACCEPTANCE_DATE],
                          FirstPPMDate   = row[FIRST_PPM_DATE],
                          SecondPPMDate  = row[SECOND_PPM_DATE],
                          ThirdPPMDate   = row[THIRD_PPM_DATE],
                          FourthPPMDate  = row[FOURTH_PPM_DATE],
                          PPMDueDate     = row[PPM_DUE_DATE],
                          Status         = row[STATUS],
                          CommentOne     = row[COMMENT_ONE],
                          CommentTwo     = row[COMMENT_TWO])

        monitors.append(monitor)

############################################################################################## parseArgs ######
def main(source):
    """  Main function, calls each separate stage.
            scanWorkBook(source)                -   scans the spreadsheet and populates the directory monitors.
            parseMonitors(monitors, results)    -   collates the results.
            printResults(results)               -   prints the results.
    """
    results = Results()     #  Used to hold the results.
    monitors = []           #  Used to hold the monitor data.

    scanWorkBook(source, monitors)
    parseMonitors(monitors, results)
    printResults(results)

############################################################################################## parseArgs ######
def parseArgs():
    """  Process the command line arguments.

         Checks the arguments and will exit if not valid.

         Exit Code 0 - program has exited normally, after print version, licence or help.
         Exit Code 1 - No source supplied.
         Exit Code 2 - Source does not exist.
    """
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        The program will scan a Excel spreadsheet of calibration dates and produce a usage report.
        -----------------------
        """),
        epilog = f" Kevin Scott (C) 2020 :: {myConfig.NAME} {myConfig.VERSION}")

    parser.add_argument("-s",  "--source",
        type=Path, action="store", default=False, help="Source file.")
    parser.add_argument("-l",  "--license",        action="store_true" , help="Print the Software License.")
    parser.add_argument("-v",  "--version",        action="store_true" , help="Print the version of the application.")

    args = parser.parse_args()


    if args.version:
        printShortLicense(myConfig.NAME, myConfig.VERSION)
        logger.info(f"End of {myConfig.NAME} V{myConfig.VERSION}: version")
        print("Goodbye.")
        exit(0)

    if args.license:
        printLongLicense(myConfig.NAME, myConfig.VERSION)
        logger.info(f"End of {myConfig.NAME} V{myConfig.VERSION} : Printed Licence")
        print("Goodbye.")
        exit(0)

    if not args.source:
        logger.error("No Source Supplied.")
        print(f"{colorama.Fore.RED}No Source Supplied. {colorama.Fore.RESET}")
        parser.print_help()
        print("Goodbye.")
        exit(1)

    if not args.source.exists():
        logger.error("Source does not exist.")
        print(f"{colorama.Fore.RED}Source does not exist. {colorama.Fore.RESET}")
        parser.print_help()
        print("Goodbye.")
        exit(2)

    return (args.source)

############################################################################################### __main__ ######

if __name__ == "__main__":

    myConfig    = myConfig.Config()                                                # Need to do this first.
    logger      = myLogger.get_logger(myConfig.NAME + ".log")                      # Create the logger.
    timer       = myTimer.Timer()

    timer.Start

    logger.info("-"*100)
    logger.info(f"Start of {myConfig.NAME} {myConfig.VERSION}")

    source = parseArgs()

    main(source)

    timeStop = timer.Stop

    print()
    print(f"{colorama.Fore.CYAN}Completed :: {timeStop} {colorama.Fore.RESET}")
    logger.info(f"Completed :: {timeStop}")
    logger.info(f"End of {myConfig.NAME} {myConfig.VERSION}")

    exit(0)
