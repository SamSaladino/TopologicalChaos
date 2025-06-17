import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships

# Load the four uploaded identifier lists
comets = pd.read_csv("/home/scostagonza/Documents/Hackathlon/TopologicalChaos/data/raw/COMETS.txt", header=None, names=["ID"])
gonzalez = pd.read_csv("/home/scostagonza/Documents/Hackathlon/TopologicalChaos/data/raw/gonzalez.txt", header=None, names=["ID"])
liu = pd.read_csv("/home/scostagonza/Documents/Hackathlon/TopologicalChaos/data/raw/liu.txt", header=None, names=["ID"])
pietzner = pd.read_csv("/home/scostagonza/Documents/Hackathlon/TopologicalChaos/data/raw/pietznzer.txt", header=0)  # Already has column name
# Already has column name

# Convert all to sets
datasets = {
    "COMETS": set(comets["ID"]),
    "Gonzalez": set(gonzalez["ID"]),
    "Liu": set(liu["ID"]),
    "Pietzner": set(pietzner["HUMAN1_ID"])
}

# Create binary presence matrix
all_ids = sorted(set.union(*datasets.values()))
presence_matrix = pd.DataFrame(index=all_ids)

for name, ids in datasets.items():
    presence_matrix[name] = presence_matrix.index.isin(ids).astype(int)


#############
# Convert to membership list
memberships = []
all_datasets = set(datasets.keys())
for index, row in presence_matrix.iterrows():
    present = row[row == 1].index.tolist()
    # Exclude the membership if it contains all datasets
    if present and set(present) != all_datasets:
        memberships.append(present)

# Create UpSet data
upset_data = from_memberships(memberships)

# Plot styled like your image
plt.figure(figsize=(10, 6))
upset = UpSet(
    upset_data,
    subset_size='count',
    show_counts=True,
    sort_by='degree',
    orientation='horizontal'
)

upset.plot()
plt.suptitle("Upset Plot of Identifier Overlap Across Datasets", fontsize=14)
plt.tight_layout()
plt.savefig("~/Documents/Hackathlon/TopologicalChaos/figures/upset_plot.png", dpi=300)
plt.show()
