###############################################################################################################
#    dataClasses.py    Copyright (C) <2020>  <Kevin Scott>                                                    #
#                                                                                                             #
#    Defines some classes used in pyBarcoAudit.                                                             #
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

import datetime
from dataclasses import dataclass


@dataclass
class Monitor:
    """  A dataclass to hold the information about one monitor,
         this is populated from each row in the spreadsheet.
    """
    monitorType   : str
    serialNumber  : str
    CliEng_ID     : str
    PCAssetNumber : str
    Site          : str
    Location      : str
    DisplayTime   : str
    BacklightTime : str
    InstalledDate : datetime.datetime
    AcceptanceDate: datetime.datetime
    FirstPPMDate  : datetime.datetime
    SecondPPMDate : datetime.datetime
    ThirdPPMDate  : datetime.datetime
    FourthPPMDate : datetime.datetime
    PPMDueDate    : datetime.datetime
    Status        : str
    CommentOne    : str
    CommentTwo    : str


class MonitorResults():
    """  A results class for Monitor Information
         Uses dataclass, so fewer lines of code i.e. no __init__
    """
    totalMonitors   : int = 0
    ScrappedMonitors: int = 0
    FailedMonitors  : int = 0
    inDateMonitors  : int = 0
    outDateMonitors : int = 0
    errDateMonitors : int = 0


class ModelResults():
    """  A results class for Model Information
    """
    def __init__(self):
        self.models = {}

    def models(self):
        """  Returns the model dictionary.
        """
        return self.models

    def addModel(self, model):
        """  If the model already exists in the dictionary add to the count else add the model.
        """
        if model in self.models:
            self.models[model][0] = self.models[model][0] + 1
        else:
            self.models[model] = [0]


class SiteResults():
    """  A results class for Site Information
    """
    def __init__(self):
        self.sites = {}

    def sites(self):
        """  Returns the sites dictionary.
        """
        return self.sites

    def addSite(self, site):
        """  If the site already exists in the dictionary add to the count else add the site.
        """
        if site in self.sites:
            self.sites[site][0] = self.sites[site][0] + 1
        else:
            self.sites[site] = [0]


