#!/bin/bash

# Check if directory "archive" exists, if not create it
if [ ! -d "archive" ]; then
    mkdir archive
    echo "Directory 'archive' created successfully."
fi

# Timestamp generation
timestamp=$(date +"%Y%m%d_%H%M%S")

# Rename grades.csv
if [ -f  "grades.csv" ]; then
    mv grades.csv archive/grades_${timestamp}.csv
    echo "File 'grades.csv' renamed and moved to 'archive' directory."
else
    echo "File 'grades.csv' not found."
fi

touch grades.csv
echo "New file 'grades.csv' created."

#Logging timestamp, original file name and new file name to organiser.log
log_file="organiser.log"
log_entry="[$timestamp] Renamed 'grades.csv' to 'archive/grades_${timestamp}.csv'"
echo "$log_entry" >> "$log_file"




