#!/bin/bash

while true; do
    clear
    $@
    read -n 1 -s -r -p "Press any [Key] to restart the Atom Console…";
done