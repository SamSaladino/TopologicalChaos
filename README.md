# TopologicalChaos
Assesing and Mapping LC MS data onto HUMAN1 GEM

Load your list of side compund as a sidecomp.txt file stored in data/raw/human1

To run this code you will need to install met4j

git clone https://forgemia.inra.fr/metexplore/met4j.git;
cd met4j;
mvn clean install 

cd met4j-toolbox
mvn clean package

java -jar target/met4j-toolbox-<version>.jar
java -cp target/met4j-toolbox-<version>.jar <Package>.<App name> -h

First step

Run in the terminal to dowload HUMAN1 network into your raw data file
cd scripts
./import_human1.sh

Then run this (arrow down) to create undirected compound graph without comparments and isolated nodes, 
also remove side compounds
./human1_net.sh
## Tasks

- [x]  Load HUMAN1 xml file, code (import, save, charge from local folder) @SamSaladino
- [ ]  Create venv requirements @SamSaladino
- [ ]  Create graph, shell (load from local repository and export to local repository @SamSaladino
- [ ]  Remove isolated nodes @SamSaladino
