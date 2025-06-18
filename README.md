# TopologicalChaos

Assessing and Mapping LC-MS Data onto HUMAN1 GEM

---

## Table of Contents
- [Overview](#overview)
- [Second Section](#secondsection)
- [Installation](#installation)
- [Usage](#usage)
- [Tasks](#tasks)
---

## Overview
This initially is for a classification of different assays onto the HUMAN1
network Ring Trial data

### Tasks

---

## Second Section

This project maps LC-MS data onto the HUMAN1 genome-scale metabolic model (GEM).

- **Input:** List of side compounds as `sidecomp.txt` in `data/raw/human1/`
- **Tools:** [met4j](https://forgemia.inra.fr/metexplore/met4j)

---

## Installation

### 1. Clone met4j and Build

```bash
git clone https://forgemia.inra.fr/metexplore/met4j.git
cd met4j
mvn clean install
cd met4j-toolbox
mvn clean package
```

---

## Usage

### 1. Download HUMAN1 Network

```bash
cd scripts
./import_human1.sh
```

### 2. Create Undirected Compound Graph

Removes compartments, isolated nodes, and side compounds:

```bash
./human1_net.sh
```

---

## Tasks

[x] Load HUMAN1 XML file (import, save, load from local folder) @SamSaladino
[ ] Create venv requirements @SamSaladino
[ ] Create graph shell (load from local repository and export to local repository) @SamSaladino
[ ] Remove isolated nodes @SamSaladino

---
