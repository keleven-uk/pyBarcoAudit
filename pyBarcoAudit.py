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
import colorama
import myTimer
import myConfig
import myLogger
from openpyxl import load_workbook
from tqdm import tqdm
from pathlib import Path
from myLicense import printLongLicense, printShortLicense

############################################################################################ scanWorkBook ######
def scanWorkBook(source):

    wb = load_workbook(filename=source)

    #  Grab the active worksheet
    ws = wb.active
    logger.info(f"Scanning {ws} in {source}")

    for row in tqdm(ws.rows, unit="rows", ncols=160, position=0):
        pass
        #print(row)

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

    scanWorkBook(source)

    timeStop = timer.Stop

    logger.info(f"Completed :: {timeStop}")
    logger.info(f"End of {myConfig.NAME} {myConfig.VERSION}")

    exit(0)
