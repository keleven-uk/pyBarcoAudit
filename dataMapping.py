###############################################################################################################
#    dataMapping.py    Copyright (C) <2020>  <Kevin Scott>                                                    #
#                                                                                                             #
#    Defines some constants used in pyBarcoAudit.                                                             #
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

#  Edges of the data table .
MIN_ROW = 4
MAX_ROW = 1179
MIN_COL = 2
MAX_COL = 28

#  Header columns
#  These are row positions, tuples start at zero.
#  Not spreadsheet column numbers.
MONITOR_TYPE      = 0
SERIAL_NUMBER     = 2
CE_ID             = 4
PC_ASSET_NO       = 6
SITE              = 8
LOCATION          = 9
DISPLAY_TIME      = 11
BACKLIGHT_TIME    = 12
INSTALLED_DATE    = 14
ACCEPTANCE_DATE   = 15
FIRST_PPM_DATE    = 16
SECOND_PPM_DATE   = 17
THIRD_PPM_DATE    = 18
FOURTH_PPM_DATE   = 19
PPM_DUE_DATE      = 21
STATUS            = 23
COMMENT_ONE       = 24
COMMENT_TWO       = 25
