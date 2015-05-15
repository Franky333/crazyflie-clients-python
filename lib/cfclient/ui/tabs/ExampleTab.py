#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2011-2013 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#  02110-1301, USA.

"""
An example template for a tab in the Crazyflie Client. It comes pre-configured
with the necessary QT Signals to wrap Crazyflie API callbacks and also
connects the connected/disconnected callbacks.
"""

__author__ = 'Bitcraze AB'
__all__ = ['ExampleTab']

import logging
import sys


# wmc status
WMC_STATUS_OK = 0
WMC_STATUS_BLOBCOUNT_LOW_ERROR = 1
WMC_STATUS_BLOBCOUNT_HIGH_ERROR = 2
WMC_STATUS_PATTERN_ERROR = 3
# posCtrl modes
POSCTRL_MODE_PATTERN = 0
POSCTRL_MODE_POINT = 1

logger = logging.getLogger(__name__)

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QThread, Qt
from PyQt4.QtGui import QMessageBox

from cfclient.ui.tab import Tab

from cflib.crazyflie.log import LogConfig, Log
from cflib.crazyflie.param import Param

from cfclient.ui.widgets.wmc import WMCBlobDisplay

example_tab_class = uic.loadUiType(sys.path[0] +
                                   "/cfclient/ui/tabs/exampleTab.ui")[0]


class ExampleTab(Tab, example_tab_class):
    """Tab for plotting logging data"""

    _connected_signal = pyqtSignal(str)
    _disconnected_signal = pyqtSignal(str)
    _log_data_signal = pyqtSignal(int, object, object)
    _log_error_signal = pyqtSignal(object, str)
    _param_updated_signal = pyqtSignal(str, str)

    def __init__(self, tabWidget, helper, *args):
        super(ExampleTab, self).__init__(*args)
        self.setupUi(self)

        self.tabName = "Example"
        self.menuName = "Example Tab"
        self.tabWidget = tabWidget

        self._helper = helper

        # Always wrap callbacks from Crazyflie API though QT Signal/Slots
        # to avoid manipulating the UI when rendering it
        self._connected_signal.connect(self._connected)
        self._disconnected_signal.connect(self._disconnected)
        self._log_data_signal.connect(self._log_data_received)
        self._param_updated_signal.connect(self._param_updated)

        # Connect the Crazyflie API callbacks to the signals
        self._helper.cf.connected.add_callback(
            self._connected_signal.emit)

        self._helper.cf.disconnected.add_callback(
            self._disconnected_signal.emit)

        self.displayWidget = WMCBlobDisplay()
        self.horizontalLayout.addWidget(self.displayWidget)
        self.displayWidget.setBlob(0, 100, 200)
        self.displayWidget.setBlob(1, 200, 200)
        self.displayWidget.setBlob(2, 300, 200)
        self.displayWidget.setBlob(3, 200, 100)
        self.displayWidget.setTPattern(0, 2, 1, 3)

        self._pushButton_posCtrlMode.clicked.connect(self._pushbutton_posctrlmode_clicked)

        self._helper.cf.param.add_update_callback(group="posCtrl", name="mode", cb=self._param_updated_signal.emit)

    def _pushbutton_posctrlmode_clicked(self):
        if self._label_mode.text() == "posCtrl-Mode: Point":
            self._label_mode.setText("posCtrl-Mode: Pattern")
            self._helper.cf.param.set_value("posCtrl.mode", str(POSCTRL_MODE_PATTERN))
        else:
            self._label_mode.setText("posCtrl-Mode: Point")
            self._helper.cf.param.set_value("posCtrl.mode", str(POSCTRL_MODE_POINT))

    def _connected(self, link_uri):
        """Callback when the Crazyflie has been connected"""
        logger.debug("Crazyflie connected to {}".format(link_uri))

        wmc_conf = LogConfig("WiiMoteCam", 50)
        wmc_conf.add_variable("wmc.blobsValid")
        wmc_conf.add_variable("wmc.blob_0_x")
        wmc_conf.add_variable("wmc.blob_0_y")
        wmc_conf.add_variable("wmc.blob_1_x")
        wmc_conf.add_variable("wmc.blob_1_y")
        wmc_conf.add_variable("wmc.blob_2_x")
        wmc_conf.add_variable("wmc.blob_2_y")
        wmc_conf.add_variable("wmc.blob_3_x")
        wmc_conf.add_variable("wmc.blob_3_y")
        wmc_conf.add_variable("wmc.pattern_f")
        wmc_conf.add_variable("wmc.pattern_l")
        wmc_conf.add_variable("wmc.pattern_m")
        wmc_conf.add_variable("wmc.pattern_r")
        wmc_conf.add_variable("pos.wmcStatus")

        self._helper.cf.log.add_config(wmc_conf)
        if wmc_conf.valid:
            wmc_conf.data_received_cb.add_callback(self._log_data_signal.emit)
            wmc_conf.start()

        pos_conf = LogConfig("Position", 50)
        pos_conf.add_variable("pos.alt")
        pos_conf.add_variable("pos.yaw")
        pos_conf.add_variable("pos.x")
        pos_conf.add_variable("pos.y")

        self._helper.cf.log.add_config(pos_conf)
        if pos_conf.valid:
            pos_conf.data_received_cb.add_callback(self._log_data_signal.emit)
            pos_conf.start()


    def _disconnected(self, link_uri):
        """Callback for when the Crazyflie has been disconnected"""
        logger.debug("Crazyflie disconnected from {}".format(link_uri))

        self._label_value_status.setText("Not Connected")
        self._pushButton_posCtrlMode.setEnabled(False)


    def _param_updated(self, name, value):
        """Callback when the registered parameter get's updated"""
        logger.debug("Updated {0} to {1}".format(name, value))

        if not self._pushButton_posCtrlMode.isEnabled():
            self._pushButton_posCtrlMode.setEnabled(True)

        if eval(str(value)) == POSCTRL_MODE_PATTERN:
            self._label_mode.setText("posCtrl-Mode: Pattern")
        elif eval(str(value)) == POSCTRL_MODE_POINT:
            self._label_mode.setText("posCtrl-Mode: Point")
        else:
            self._label_mode.setText("posCtrl-Mode: unknown")


    def _log_data_received(self, timestamp, data, log_conf):
        """Callback when the log layer receives new data"""
        logger.debug("{0}:{1}:{2}".format(timestamp, log_conf.name, data))

        if log_conf.name == "WiiMoteCam":

            if data["wmc.blobsValid"] & (1 << 0):
                self.displayWidget.setBlob(0, data["wmc.blob_0_x"], data["wmc.blob_0_y"])
            else:
                self.displayWidget.clearBlob(0)
            if data["wmc.blobsValid"] & (1 << 1):
                self.displayWidget.setBlob(1, data["wmc.blob_1_x"], data["wmc.blob_1_y"])
            else:
                self.displayWidget.clearBlob(1)
            if data["wmc.blobsValid"] & (1 << 2):
                self.displayWidget.setBlob(2, data["wmc.blob_2_x"], data["wmc.blob_2_y"])
            else:
                self.displayWidget.clearBlob(2)
            if data["wmc.blobsValid"] & (1 << 3):
                self.displayWidget.setBlob(3, data["wmc.blob_3_x"], data["wmc.blob_3_y"])
            else:
                self.displayWidget.clearBlob(3)

            if data["pos.wmcStatus"] == WMC_STATUS_OK or data["pos.wmcStatus"] == WMC_STATUS_PATTERN_ERROR:  # TODO: also check if param posCtrl.mode==POSCTRL_MODE_PATTERN
                self.displayWidget.setTPattern(data["wmc.pattern_l"],
                                               data["wmc.pattern_r"],
                                               data["wmc.pattern_m"],
                                               data["wmc.pattern_f"])
            else:
                self.displayWidget.clearTPattern()

            if data["pos.wmcStatus"] == WMC_STATUS_OK:
                self._label_value_status.setText("OK")
                self._label_value_status.setStyleSheet('color: green')
            elif data["pos.wmcStatus"] == WMC_STATUS_BLOBCOUNT_LOW_ERROR:
                self._label_value_status.setText("Error: blobcount too low")
                self._label_value_status.setStyleSheet('color: red')
            elif data["pos.wmcStatus"] == WMC_STATUS_BLOBCOUNT_HIGH_ERROR:
                self._label_value_status.setText("Error: blobcount too high")
                self._label_value_status.setStyleSheet('color: red')
            elif data["pos.wmcStatus"] == WMC_STATUS_PATTERN_ERROR:
                self._label_value_status.setText("Error: pattern recognition fail")
                self._label_value_status.setStyleSheet('color: red')
            else:
                self._label_value_status.setText("Unknown Status")
                self._label_value_status.setStyleSheet('color: red')

        elif log_conf.name == "Position":
            self._label_value_altitude.setText("{0:.02f}".format(data["pos.alt"]))
            self._label_value_yaw.setText("{0:.02f}".format(data["pos.yaw"]))
            self._label_value_x.setText("{0:.02f}".format(data["pos.x"]))
            self._label_value_y.setText("{0:.02f}".format(data["pos.y"]))


    def _logging_error(self, log_conf, msg):
        """Callback from the log layer when an error occurs"""

        QMessageBox.about(self, "Example error",
                          "Error when using log config"
                          " [{0}]: {1}".format(log_conf.name, msg))