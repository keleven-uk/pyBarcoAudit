###############################################################################################################
#   model_utils.py    Copyright (C) <2020-22>  <Kevin Scott>                                                  #
#                                                                                                             #
#    Utility functions to gather and print information regarding the monitors by model.                       #
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

############################################################################################ parseModel ###############
def parseModel(monitors, modelResults):
    """  Loops through the directory monitors collating the Model results.
    """
    for monitor in monitors:
        modelResults.addModel(monitor.monitorType, monitor.Status, monitor.PPMDueDate)

############################################################################################ printModelResults ########
def printModelResults(modelResults):
    """  Prints the Model results
    """
    model_total    = 0
    model_scrapped = 0
    model_faulty   = 0
    model_live     = 0
    model_indate   = 0
    model_percent  = 0

    print("-" + " Model Information " + "-"*61)
    print("Model             Total      Scrapped   Faulty      live     In Date")
    print("")
    for model in modelResults.models:
        total    = modelResults.models[model][0]
        scrapped = modelResults.models[model][1]
        faulty   = modelResults.models[model][2]
        indate   = modelResults.models[model][3]
        live     = total - scrapped - faulty
        percent  = (indate/total) * 100
        print(f"{model:14} {total:10} {scrapped:10} {faulty:10} {live:10} {indate:10} {percent:10.2f}")
        model_total    += total
        model_scrapped += scrapped
        model_faulty   += faulty
        model_indate   += indate

    print("="*80)
    model_live = model_total - model_scrapped - model_faulty
    model_percent  = (model_indate/model_total) * 100
    print(f"{model_total:25} {model_scrapped:10} {model_faulty:10} {model_live:10} {model_indate:10} {model_percent:10.2f}")
    print()


