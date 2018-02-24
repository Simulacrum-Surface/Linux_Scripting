#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""

A script to start / restart the tor demon an to test if the connection actually tunnels through tor.
Requires: Proxychains


Autor: Simulacrum

"""


import subprocess
import re
import time

def main():

    # Check if tor daemon is running. there should be Active: active (running) on stdout

    daemon_status = subprocess.Popen(["systemctl", "status", "tor"], stdout=subprocess.PIPE)
    running = daemon_status.communicate()

    #print(type(running))
    #print(running)

    if b"Active: active (running)" in running[0]:
        print("[+] Looks like the tor daemon is already running...")
        answer = input("[?] Restart this bad boy?(Y/n)")

        if answer == "n":
            pass
        else:
            daemon_restart = subprocess.Popen(["systemctl", "restart", "tor"], stdout=subprocess.PIPE)
            time.sleep(2)
            print("[+] Daemon restarted.")
    else:
        print("[+] Tor daemon seems to be inactiv. Starting Tor Daemon...")
        daemon_start = subprocess.Popen(["systemctl", "start", "tor"], stdout=subprocess.PIPE)
        daemon_start.communicate()
        time.sleep(2)

    print("[+] Checking your identity")
    chain_check = subprocess.Popen(["proxychains", "curl", "https://check.torproject.org/?lang=en_US"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chain_check_filter = subprocess.Popen(["grep", "Congrat*"], stdin=chain_check.stdout, stdout=subprocess.PIPE)
    chain_check.stdout.close()

    #print(chain_check.args, chain_check_filter.args)

    is_hidden = chain_check_filter.communicate()
    time.sleep(3)
    if b"Congratulations. This browser is configured to use Tor." in is_hidden[0]:
        print("[+] Looks good, you seem to be connected to the tor network :)")

    else:
        print("[-] !WARINING! Looks like you are not connected to tor.\nEXITING...")
        daemon_start = subprocess.Popen(["systemctl", "stop", "tor"], stdout=subprocess.PIPE)
        exit(0)


    return


if __name__ == '__main__':
    main()