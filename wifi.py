#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

A Script to start a netctl profile for an interface.
In case you are not using something like NetworkManager


Author: Simulacrum-Surface

"""


import subprocess
import re

print("[+] Stopping all Profiles")
netclt_stop = subprocess.Popen(["netctl", "stop-all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
netclt_stop.wait()
netclt_stop_answer = netclt_stop.communicate()
if netclt_stop_answer[0] != b'' or netclt_stop_answer[1] != b'':
    print(netclt_stop_answer)
    exit(0)
else:
    pass

interface = subprocess.Popen(["ip", "a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
interface.wait()
answer = interface.communicate()
answer = answer[0].decode("utf-8")

if_match = re.compile(r"[0-9]{1}\:[\s]{1}[a-z0-9]*")

answer = answer.split("\n")
if_select = []


for line in answer:
    if re.match(if_match, line):
        line = line.split("<")
        line = line[0].strip()
        if_select.append(line[:-1])
        if "virbr" not in line[:-1]:
            print(line[:-1])

if_answer = input("[?] Select Interface: ")

if True:
    interface = if_select[int(if_answer)-1][3:]
    print("[+] Using Interface {}".format(interface))
else:
    print("[-] {} was never an option....\nExiting...".format(if_answer))
    exit(0)
print("###################################################################")

profiles = subprocess.Popen(["netctl", "list"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
profiles.wait()
answer = profiles.communicate()


answer = answer[0].decode("utf-8").split("\n")

counter = 0
for x in answer[:-1]:
    x = x.strip()
    counter += 1
    print(str(counter) + ": " + x)
profile_select = input("[?] Select the Profile:")
profile = answer[int(profile_select)-1].strip()

print("[+] Using Profile {}".format(profile))
print("###################################################################")

print("[+] Taking down Interface")
if_down = subprocess.Popen(["ip", "link", "set", "dev", interface, "down"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
if_down.wait()
if_down_answer = if_down.communicate()
if if_down_answer[1] != b'' or if_down_answer[0] != b'':
    print(if_down_answer)
    exit(0)
else:
    pass


print("[+] Starting Profile {}".format(profile))
if_up = subprocess.Popen(["netctl", "start", profile], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
if_up.wait()
if_up_answer = if_up.communicate()
if if_down_answer[1] != b'' or if_down_answer[0] != b'':
    print(if_down_answer)
    exit(0)
else:
    pass


print("[+] All Done, bye bye :)")
exit(0)