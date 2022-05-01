###############################################################################################################
#   site_utils.py    Copyright (C) <2020-22>  <Kevin Scott>                                                   #
#                                                                                                             #
#    Utility functions to gather and print information regarding the monitors at each site.                   #
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

############################################################################################ parseSite ################
def parseSite(monitors, siteResults):
    """  Loops through the directory monitors collating the Site results.
    """
    for monitor in monitors:
        siteResults.addSite(monitor.Site, monitor.Status, monitor.PPMDueDate)

############################################################################################ printSiteResults #########
def printSiteResults(siteResults):
    """  Prints the Site results
    """
    site_total    = 0
    site_scrapped = 0
    site_faulty   = 0
    site_live     = 0
    site_indate   = 0
    site_percent  = 0

    print("-" + " Site Information " + "-"*61)
    print("Site             Total      Scrapped   Faulty      live     In Date")
    print("")
    for site in siteResults.sites:
        total    = siteResults.sites[site][0]
        scrapped = siteResults.sites[site][1]
        faulty   = siteResults.sites[site][2]
        indate   = siteResults.sites[site][3]
        live     = total - scrapped - faulty
        percent  = (indate/total) * 100
        print(f"{site:10} {total:10} {scrapped:10} {faulty:10} {live:10} {indate:10} {percent:10.2f}")
        site_total    += total
        site_scrapped += scrapped
        site_faulty   += faulty
        site_indate   += indate

    print("="*80)
    site_live = site_total - site_scrapped - site_faulty
    site_percent  = (site_indate/site_total) * 100
    print(f"{site_total:21} {site_scrapped:10} {site_faulty:10} {site_live:10} {site_indate:10} {site_percent:10.2f}")
    print()

