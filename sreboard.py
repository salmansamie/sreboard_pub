#!/usr/bin/env python

import argparse
import json
import os
import subprocess
import time
import factors

__author__ = 'Salman_M_Rahman'


class PrcInitiator:
    def __init__(self, prc_com=None, instance=None, keystone=None, wait_io=None):
        print("[INFO]  PrcInitiator class instantiated")
        self.prc_com = prc_com
        self.instance = instance
        self.keystone = keystone
        self.wait_io = wait_io

    # Timer interrupts between instance triggers
    def sys_interrupt(self):
        print("[INFO]  Partial interrupt triggered")
        return time.sleep(self.wait_io)

    # Application instance spin up trigger
    def call_sys_stack(self):
        print("[INFO]  Spun up instance of: " + self.instance)
        return subprocess.call(self.prc_com + self.instance, shell=True)

    # Window relocation osascript trigger
    def sys_core(self):
        print("[INFO]  osascript triggered for: " + self.instance)
        fp = open('cord_attr.json')
        filejs = fp.read()
        loadjson = json.loads(filejs)
        osascript = "osascript<<END " + \
                    "\nset theApp to \"" + loadjson[self.keystone]['Application'] + '\"' + \
                    "\nset appHeight to " + loadjson[self.keystone]['appHeight'] + \
                    "\nset appWidth to " + loadjson[self.keystone]['appWidth'] + \
                    '\ntell application "Finder"' + \
                    "\n\tset screenResolution to bounds of window of desktop" + \
                    "\nend tell" + \
                    "\n\tset screenWidth to item 3 of screenResolution" + \
                    "\n\tset screenHeight to item 4 of screenResolution" + \
                    "\n\ttell application theApp" + \
                    "\n\t\tactivate" + \
                    "\n\t\treopen" + \
                    "\n\t\tset yAxis to " + loadjson[self.keystone]['Y-ordinate'] + " as integer" + \
                    "\n\t\tset xAxis to " + loadjson[self.keystone]['X-ordinate'] + " as integer" + \
                    "\n\t\tset the bounds of the first window to {xAxis, yAxis, appWidth + xAxis, appHeight + yAxis}" + \
                    "\nend tell"

        osa_call_sc = os.system(osascript)
        return osa_call_sc


# Reusable class-object function
def sys_consol(prc_com, instance, keystone, wait_io):
    print("[INFO]  Initializing class object for PrcInitiator...")
    initiator = PrcInitiator(prc_com, instance, keystone, wait_io)
    sys_call = initiator.call_sys_stack()
    sys_intr = initiator.sys_interrupt()
    sys_core = initiator.sys_core()
    return sys_call, sys_intr, sys_core


# MAIN
def main():

    print("[INIT]\n  |")

    # Mute system at init
    print("[INFO]  System set on mute\n  |")
    os.system("osascript<<END -e 'set Volume 0'")

    print("[INFO]  Setting up SRE-board\n  |")

    # Function call for VPN connection**
    print("[INFO]  Triggering VPN function")
    factors.__auth_core__()
    time.sleep(2)

    def default():
        print("[INFO]  Default configurations set >>>")
        factors.default()

    def bin_switch():
        print("[INFO]  Flag set >>> SWITCH")
        factors.alter_swc()
        pass

    def kill_switch():
        print("[WARN]  Flag set >>> SIGKILL\n\tTriggered process termination (SIGKILL)")
        factors.kill_pcs()
        pass

    parser = argparse.ArgumentParser(prog='sreboard\n\n')

    parser.add_argument(
        "-d", "--default",
        action="append_const",
        const=default,
        help="Activate default host application configurations")

    parser.add_argument(
        "-s", "--switch",
        action="append_const",
        const=bin_switch,
        help="Switch to auxiliary monitor configurations")

    parser.add_argument(
        "-q", "--quit",
        action="append_const",
        const=kill_switch,
        help="Quit ALL running Chrome AND/OR Adium processes only")

    args = parser.parse_args()

    if args.switch:
        bin_switch()

    elif args.quit:
        kill_switch()

    else:
        default()


if __name__ == '__main__':
    print("\n\nEmail issues to:\nsalman.rahman@servicenow.com\n(2016-17)\n")
    main()
    print("[RC-0]\n\n")
