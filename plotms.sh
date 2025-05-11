#!/bin/bash

# Load modules – adjust based on your cluster environment
ml GCC/9.3.0 OpenMPI/4.0.3 IPython/7.15.0-Python-3.8.2

# Clear the terminal for readability
clear

# Check if any *.res file exists in current directory
if [ -f *.res ]; then
    # If .res exists, plot directly
    plot
else
    # Go into temporary directory with QCXMS simulations
    cd TMPQCXMS || { echo "TMPQCXMS folder not found"; exit 1; }

    # Loop over all TMP* subfolders
    for i in TMP*; do
        cd "$i" || continue
        
        # Check if a .res file exists
        if [ -f qcxm*.res ]; then
            name=$(ls *.res)
            cat "$name" >> ../../"$name"
        else
            echo "res file is missing in folder $i"
        fi
        
        cd ..
    done

    cd ..
    plot
fi

# Generate spectrum plot (requires Python 3.x, numpy, matplotlib)
plt_mass

# Filter out peaks with intensity ≤ 1, save result to spectra.csv
awk -F',' '$2>1' result.csv > spectra.csv
