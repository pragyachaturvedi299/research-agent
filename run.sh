#!/bin/bash

# Ask user for a query
read -p "Enter research topic: " QUERY

# Run the project
source bin/activate

# Run the Python script with the query
python3 run.py "$QUERY"
