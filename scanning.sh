#!/bin/bash


RED='\033[0;31m'
NC='\033[0m' # No Color

function print_text {
    local text="$1"
    echo -e "${RED}${text}${NC}"
}


ip_regex="^([0-9]{1,3}\.){3}[0-9]{1,3}$"


function make_dir {
  mkdir -p scanning/hosts scanning/ports
}

function execute_command {
  if [[ $1 == "hosts" ]]
  then
    print_text "$(cat alive_hosts.txt)"
  elif [[ $1 =~ $ip_regex ]]
  then
    ip=$1
   print_text "$(cat ./scanning/ports/${ip%.*}.0/${ip}.nmap)"
  fi
  
}

function take_commands {
  count=1
  while [[ count -lt 2 ]]
  do
    read -p "[Pentester@Parrot]-[~]# " command
    if [ "$command" == "exit" ]
    then
      ((count++))
    else
      execute_command "$command"
    fi
  done
}

function host_scan {
  ip_address=$(echo $1 | cut -d'/' -f1)
  sudo nmap -PE -sn -n  $1 -oN ./scanning/hosts/sub_$ip_address.nmap | grep "for" | cut -d " " -f5 > hosts.txt
  echo "List of alive hosts of $ip_address" >> alive_hosts.txt
  cat hosts.txt >> alive_hosts.txt
  hosts=$(cat hosts.txt)
  for i in $hosts
  do
    port_scan $i
  done
}

function port_scan {
  mkdir -p scanning/ports/$ip_address
  sudo nmap -sS -Pn -n $1 -oN ./scanning/ports/$ip_address/$1.nmap
}

function main {
  array=()

  make_dir
  for arg in "$@"
  do
      array+=("$arg")
  done

  for subnet in "${array[@]}"
  do
    echo "coming here"
    host_scan $subnet
  done
  take_commands
}

main "$@"
