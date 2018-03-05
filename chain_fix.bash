#!/usr/bin/bash


# Author: SimulacrumSurface
# A Script for tor daemon routines

# Requires:
# -- systemd
# -- tor
# -- proxychains


# Check the status of the tor daemon

daemon_status=$(systemctl status tor | grep "Active:")
wait
if [[ "$daemon_status" = *inactive* ]]
then	
	echo Test
	# The tor daemon is inactiv. Ask to start.
	echo -e "[?] The tor daemon is inactiv. Want me to start it? [Y/N]";
	read -r answer	
	if [[ $answer = y || $answer =  Y ]]
	# Start the daemon
	then
		echo "[+] Starting the daemon..."
		sudo systemctl start tor
		wait
		daemon_status_start=$(systemctl status tor | grep "Active:")
		if [[ $daemon_status_start = *inactive* ]]
		then
			echo -e "[-] The daemon failed to start. Please check manually.\\nExiting..."
		else [[ $daemon_status_start = *active* ]]
			echo -e "[+] The daemon started."
			sleep 2
		fi	
	elif [[ $answer = n || $answer =  N ]]
	# Do not start the daemon, exit.
	then	
		echo -e "[+] Alright. Bye bye, have a good time :)"
		exit
	else
	# Invalid input, exit.
		echo -e "[-] This is not an option. Exiting..."
		exit
	fi

elif [[ "$daemon_status" = *activ* ]]
then
	echo -e "[?] The daemon is already running. Want me to restart it? [Y/N]"
	read -r answer	
	if [[ $answer = y || $answer =  Y ]]
	then 	# Restart the daemon
		echo "[+] Restarting the daemon..."
		sudo systemctl restart tor
		wait		
		daemon_status_restart=$(systemctl status tor | grep "Active:")
		if [[ $daemon_status_restart = *inactive* ]]
		then
			echo -e "[-] The daemon failed to restart. Please check manually.\\nExiting..."
		else [[ $daemon_status_restart = *active* ]]
		
			echo -e "[+] The daemon restarted."
			wait
			sleep 2
		fi
	elif [[ $answer = n || $answer =  N ]]
	# Do not restart the daemon, exit.
	then	
		echo -e "[+] Leaving the daemon untouched."
	else
	# Invalid input, exit.
		echo -e "[-] This is not an option. Exiting..."
		exit 1
	fi
fi

# Daemon is now running or script -> exit.
# Check the connection & exit node.

echo -e "[+] Sending request to check.torproject.org via HTTPS..."
response=$(proxychains curl "https://check.torproject.org" 2>/dev/null) #
wait

connection=$(echo "$response" | grep Congrat)
exit_node=$(echo "$response" | grep -m 1 -o '[0-9]\{1,3\}'.'[0-9]\{1,3\}'.'[0-9]\{1,3\}'.'[0-9]\{1,3\}')

#echo $connection

NC='\033[0m' # No Color, ANSII escape code
if [ -n "$connection" ]
then
	COLOR="\033[0;32m" # Colorize the output green, ANSII escape code
	echo -e "${COLOR}[+] You are connected to tor.${NC}"
else
	COLOR="\033[0;31m" # Colorize the output red, ANSII escape code
	echo -e "${COLOR}[-] You are not connected to tor.${NC}"
fi

echo "[+] Your ExitNode is: ${exit_node}"
exit 0










