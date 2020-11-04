#!/bin/bash

# Config
shopt -s nullglob
shopt -s extglob

# Change this before deploying
dataPath="$HOME/weather_app/weatherapp/data/"

# Function to clean files older than a week
function clean_file() {
	tmp_file="${dataPath}tmp"
	head -1 "$1" > "$tmp_file"
	tail -1 "$1" >> "$tmp_file"
	mv "$tmp_file" "${dataPath}${1//+(*\/)}"
}

# Read all filenames in data dir if it exists
if [[ -e "$dataPath" ]]; then
	fileList=(${dataPath}*)
else
	echo "No data logged yet" >&2
	exit 1
fi

# Get current date
#NOW=$(date -j "+%s") # For BSD
NOW=$(date '+%s') # For GNU

# Remove stale files(older than 1 month/30 days)
# Clean old files(older than 1 week/7 days)
for file in "${fileList[@]}"
do
	fileDate="${file//+(*\/|.*)}"
	#fileDate="$(date -j -f "%Y-%m-%d" ${fileDate} '+%s')" # For BSD
	fileDate="$(date -d ${fileDate} '+%s')" # For GNU
	dateDiff=$(( ($NOW - $fileDate)/(60*60*24) ))
	if [[ $dateDiff -gt 30 ]]; then
		rm -f "$file"
	elif [[ $dateDiff -gt 7 ]]; then
		clean_file "$file"
	fi
done
