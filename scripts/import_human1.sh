#!/bin/bash
echo "Select the folder path to the repository"
cd ~/Documents/Hackathlon/TopologicalChaos/data/raw/human1

path_to_data=$(pwd)

echo "Saving Human-GEM.xml in $path_to_data"
curl -L "https://www.ebi.ac.uk/biomodels/model/download/MODEL2204280001?filename=Human-GEM.xml" \
     -o $path_to_data/Human-GEM.xml