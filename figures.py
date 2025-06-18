import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships

import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships

class UpSetPlotter:
    def __init__(self, data, names=None):
        """
        Initialize with data as:
        - dict of {name: set/list}
        - list of lists/sets (names must be provided)
        - DataFrame (columns are datasets, rows are IDs, values are 1/0 or True/False)
        """
        if isinstance(data, dict):
            self.datasets = {k: set(v) for k, v in data.items()}
        elif isinstance(data, pd.DataFrame):
            # Assume columns are datasets, index are IDs, values are 1/0 or True/False
            self.datasets = {col: set(data.index[data[col].astype(bool)]) for col in data.columns}
        elif isinstance(data, (list, tuple)):
            if names is None or len(names) != len(data):
                raise ValueError("If data is a list, 'names' must be provided and match its length.")
            self.datasets = {name: set(lst) for name, lst in zip(names, data)}
        else:
            raise ValueError("Unsupported data type for UpSetPlotter.")
        self.all_datasets = set(self.datasets.keys())
        self.presence_matrix = None
        self.memberships = None

    def build_presence_matrix(self):
        all_ids = sorted(set.union(*self.datasets.values()))
        presence_matrix = pd.DataFrame(index=all_ids)
        for name, ids in self.datasets.items():
            presence_matrix[name] = presence_matrix.index.isin(ids).astype(int)
        self.presence_matrix = presence_matrix
        return presence_matrix

    def build_memberships(self, exclude_all=True):
        if self.presence_matrix is None:
            self.build_presence_matrix()
        memberships = []
        for index, row in self.presence_matrix.iterrows():
            present = row[row == 1].index.tolist()
            if present and (not exclude_all or set(present) != self.all_datasets):
                memberships.append(present)
        self.memberships = memberships
        return memberships

    def plot_upset(self, figsize=(10, 6), title="Upset Plot of Identifier Overlap Across Datasets", exclude_all=True, save_path=None):
        memberships = self.build_memberships(exclude_all=exclude_all)
        upset_data = from_memberships(memberships)
        plt.figure(figsize=figsize)
        upset = UpSet(
            upset_data,
            subset_size='count',
            show_counts=True,
            sort_by='degree',
            orientation='horizontal'
        )
        upset.plot()
        plt.suptitle(title, fontsize=14)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    # Placeholder for future methods
    def summary(self):
        """Print a summary of the datasets."""
        for name, ids in self.datasets.items():
            print(f"{name}: {len(ids)} IDs")

# Example usage:
if __name__ == "__main__":
    # Example with dict of lists
    data = {
        "COMETS": ["A", "B", "C"],
        "Gonzalez": ["B", "C", "D"],
        "Liu": ["A", "D"],
        "Pietzner": ["C", "E", "F", "G"]
    }
    plotter = UpSetPlotter(data)
    plotter.plot_upset(save_path="upset_plot.png")


# # Load the four uploaded identifier lists
# comets = pd.read_csv("/home/scostagonza/Documents/Hackathlon/TopologicalChaos/data/raw/COMETS.txt", header=None, names=["ID"])
# gonzalez = pd.read_csv("/home/scostagonza/Documents/Hackathlon/TopologicalChaos/data/raw/gonzalez.txt", header=None, names=["ID"])
# liu = pd.read_csv("/home/scostagonza/Documents/Hackathlon/TopologicalChaos/data/raw/liu.txt", header=None, names=["ID"])
# pietzner = pd.read_csv("/home/scostagonza/Documents/Hackathlon/TopologicalChaos/data/raw/pietznzer.txt", header=0)  # Already has column name
# # Already has column name

# # Convert all to sets
# datasets = {
#     "COMETS": set(comets["ID"]),
#     "Gonzalez": set(gonzalez["ID"]),
#     "Liu": set(liu["ID"]),
#     "Pietzner": set(pietzner["HUMAN1_ID"])
# }

# # Create binary presence matrix
# all_ids = sorted(set.union(*datasets.values()))
# presence_matrix = pd.DataFrame(index=all_ids)

# for name, ids in datasets.items():
#     presence_matrix[name] = presence_matrix.index.isin(ids).astype(int)


# #############
# # Convert to membership list
# memberships = []
# all_datasets = set(datasets.keys())
# for index, row in presence_matrix.iterrows():
#     present = row[row == 1].index.tolist()
#     # Exclude the membership if it contains all datasets
#     if present and set(present) != all_datasets:
#         memberships.append(present)

# # Create UpSet data
# upset_data = from_memberships(memberships)

# # Plot styled like your image
# plt.figure(figsize=(10, 6))
# upset = UpSet(
#     upset_data,
#     subset_size='count',
#     show_counts=True,
#     sort_by='degree',
#     orientation='horizontal'
# )

# upset.plot()
# plt.suptitle("Upset Plot of Identifier Overlap Across Datasets", fontsize=14)
# plt.tight_layout()

# plt.show()
# plt.savefig("upset_plot.png", dpi=300)