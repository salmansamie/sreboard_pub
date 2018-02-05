#!/usr/bin/env python

from data import *
import sreboard
import configparser
import getpass
import os
import socket
import subprocess
import time


__author__ = 'Salman_M_Rahman'


# Trigger configuration set: 01
def app_config01():
    conf_exp(config[0])

    sreboard.sys_consol(cmd_utils['goog_command'], blocks['datacenter_ins'], 'datacenter_ins', 0.7)
    print('  |\n  |----\tStarted====> Datacenter\n  |')

    sreboard.sys_consol(cmd_utils['goog_command'], blocks['bigdata_stats'], 'bigdata_stats', 0.7)
    print('  |\n  |----\tStarted====> Big Data\n  |')


# Trigger configuration set: 02
def app_config02():
    conf_exp(config[1])

    sreboard.sys_consol(cmd_utils['goog_command'], blocks['skynews_live'], 'sky_live', 0.7)
    print("  |\n  |----\tStarted====> Sky News\n  |")

    sreboard.sys_consol(cmd_utils['goog_command'], blocks['thousand_eyes'], 'thousand_eyes', 0.7)
    print('  |\n  |----\tStarted====> Thousand Eyes\n  |')

    sreboard.sys_consol(cmd_utils['goog_command'], blocks['xymond_board'], 'xymon_hi', 0.7)
    print('  |\n  |----\tStarted====> Xymon : HI instance\n  |')

    os.popen(cmd_utils['adium_client'], 'r')
    print('  |----\tStarted====> Adium IRC\n  |')

    sreboard.sys_consol(cmd_utils['goog_command'], blocks['schedule_board'], 'sre_schedule', 0.7)
    print('  |\n  |----\tStarted====> SRE Schedule Board\n  |')


# Default configuration based on network hostname
def default():
    hostname = socket.gethostname()
    print("[INFO]  Triggering application configurations for " + hostname + "\n")
    try:
        if hostname in hostnames:
            app_config01()
        else:
            app_config02()

    except TypeError:
        print("[WARN]  Fix by importing correct data type(s)")

    except KeyboardInterrupt:
        print("[WARN]  Sreboard terminated externally")


# > Temp. storage for last configuration set record
def conf_exp(args):
    conf = configparser.ConfigParser()
    confile = open('board.cnf', 'w')
    conf.add_section('prior_set')
    conf.set('prior_set', 'value', args)
    conf.write(confile)


# < Scan from the last stored configurations set
def conf_scan():
    conf = configparser.ConfigParser()
    conf.read('board.cnf')
    store_import = conf.get('prior_set', 'value')
    return store_import


# Switch [-s] flag as the command-line argument invokes alter_swc()
def alter_swc():
    try:
        if conf_scan() == config[0]:
            conf_exp(config[1])
            app_config02()

        elif conf_scan() == config[1]:
            conf_exp(config[0])
            app_config01()

    except TypeError:
        print("[WARN]  Error while reading the configuration file.")


# Quit [-q] flag as the command-line argument invokes kill_pcs()
def kill_pcs():
    for fn in killproc:
        os.popen("pkill -9 " + fn, 'r')
        print("Quiting process: " + fn)


# Generate RSA token
def get_stoken():
    try:
        str_tokencode = os.popen('stoken tokencode').read()
        str_tokencode = (str(str_tokencode)).strip()
        return str_tokencode

    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print('[FATAL]  Stoken not installed. VPN connection will fail')


# Kill any desired single process only
def kill_single_prcs(prcs):
    os.popen("pkill -9 " + prcs, 'r')


# VPN function call trigger
def __auth_core__():
    print("[INFO]  Contacting EMEA VPN...\n  |")
    kill_single_prcs(killproc[1])
    kill_single_prcs(killproc[2])
    kill_single_prcs(killproc[3])

    if __auth_pass__(v_domain['emea_vpn']):
        print("[INFO]  Verifying credentials for primary domain: EMEA UK SecureVPN")
        print("[INFO]  VPN connection return status is TRUE\n  |")
        return True
    else:
        print("[INFO]  Primary domain connection ABORTED. Trying Secondary domain..")
        kill_single_prcs(killproc[1])
        kill_single_prcs(killproc[2])
        kill_single_prcs(killproc[3])
        time.sleep(1)
        if __auth_pass__(v_domain['usa_east']):
            print("[INFO]  Verifying credentials for secondary domain: US EAST SecureVPN")
            return True
        else:
            print("[INFO]  Secondary domain connection ABORTED. Trying Tertiary domain..")
            kill_single_prcs(killproc[1])
            kill_single_prcs(killproc[2])
            kill_single_prcs(killproc[3])
            time.sleep(1)
            if __auth_pass__(v_domain['usa_west']):
                print("[INFO]  Verifying credentials for tertiary domain: US WEST SecureVPN")
                return True
            else:
                kill_single_prcs(killproc[1])
                kill_single_prcs(killproc[2])
                kill_single_prcs(killproc[3])
                print("[WARN]  VPN connection failed. Check host network connection.")
                exit(1)
                return False


# VPN pin from the network hostname
def __auth_pass__(vpn_domain):
    hostname = socket.gethostname()
    username = getpass.getuser()
    if hostname in hosts_vpn_group:
        print("  |\n[INFO]  Matching <====> HOST-PIN-DOMAIN:")
        __auth_cisco_vpn__(username, sn_pin[1], vpn_domain)
        return True
    else:
        print("  |\n[INFO]  Matching <====> HOST-PIN-DOMAIN:")
        __auth_cisco_vpn__(username, sn_pin[0], vpn_domain)
        return True


# Final call for VPN after set pin based on the hostname
def __auth_cisco_vpn__(username, pin, domain):
    # Generate RSA Token
    print("[INFO]  Generating RSA token")
    proc = subprocess.Popen(['stoken', 'tokencode'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    store = list(proc.stdout)
    token = store[0].strip()

    # Set vpn connection command
    credentials = "printf '" + username + "\\n" + pin + token + "\\ny'"
    vpn_cmd = "/opt/cisco/anyconnect/bin/vpn -s connect '" + domain + "'"
    cmd = credentials + " | " + vpn_cmd
    print("[INFO]  Parsing command and storage")

    try:
        # Command Execution
        print("[INFO]  Injecting connection command")
        subprocess.Popen(cmd,
                         shell=True,
                         executable="/bin/bash",
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE).communicate()
        return True

    except KeyboardInterrupt:
        print("[INFO]  sreboard interrupted via external signal")
        return False
