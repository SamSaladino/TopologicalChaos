import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships
import seaborn as sns
import numpy as np
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

    def build_memberships(self):
        if self.presence_matrix is None:
            self.build_presence_matrix()
        memberships = []
        for index, row in self.presence_matrix.iterrows():
            present = row[row == 1].index.tolist()
            if present:
                memberships.append(present)
        self.memberships = memberships
        return memberships
    
    def plot_upset(self, figsize=(10, 6), title="Upset Plot of Identifier Overlap Across Datasets", save_path=None):
        """
        Plot an UpSet plot including all intersections (including the intersection of all datasets).
        """
        memberships = self.build_memberships()  # Do not exclude any intersections
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


class HeatmapPlotter:
    def __init__(self, data, names=None):
        """
        Accepts:
        - dict of {name: list/array}
        - list of lists/arrays (names must be provided)
        - DataFrame (columns are assays, rows are features/classes)
        """
        if isinstance(data, dict):
            self.df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            self.df = data.copy()
        elif isinstance(data, (list, tuple)):
            if names is None or len(names) != len(data):
                raise ValueError("If data is a list, 'names' must be provided and match its length.")
            self.df = pd.DataFrame({name: lst for name, lst in zip(names, data)})
        else:
            raise ValueError("Unsupported data type for HeatmapPlotter.")
        # Drop non-numeric columns if any
        self.df_numeric = self.df.select_dtypes(include=[np.number])

    def plot_heatmap(self, figsize=(10, 8), cmap="viridis", title="Assay Heatmap", save_path=None, clustermap=False):
        plt.figure(figsize=figsize)
        if clustermap:
            sns.clustermap(self.df_numeric, cmap=cmap, figsize=figsize, standard_scale=1)
            plt.title(title)
            if save_path:
                plt.savefig(save_path, dpi=300)
            plt.show()
        else:
            ax = sns.heatmap(self.df_numeric, cmap=cmap, annot=False)
            plt.title(title)
            plt.tight_layout()
            if save_path:
                plt.savefig(save_path, dpi=300)
            plt.show()

# Example usage in your notebook:
# Suppose you have your data as a dict of lists (like your 'data' variable in the notebook)class AssayHeatmap:
    def __init__(self, assay_df, refmet):
        """
        assay_df: DataFrame with chebi IDs as index and assay columns (1/0 or True/False)
        refmet: DataFrame with chebi_id, super_class, main_class, sub_class
        """
        self.assay_df = assay_df
        self.refmet = refmet

    def merge_with_classes(self):
        # Merge assay_df with refmet on CHEBI index
        merged = pd.merge(
            self.assay_df,
            self.refmet[['chebi_id', 'super_class', 'main_class', 'sub_class']],
            left_index=True,
            right_on='chebi_id',
            how='inner'
        )
        self.df_with_class = merged

    def group_and_normalize(self, groupby=['super_class', 'main_class']):
        # Group and sum
        count_df = self.df_with_class.groupby(groupby)[self.assay_df.columns].sum()
        # Normalize by group size (mean)
        group_sizes = self.df_with_class.groupby(groupby).size()
        normalized = count_df.div(group_sizes, axis=0)
        self.count_df = count_df
        self.normalized = normalized
        return normalized

    def plot_clustermap(self, cmap='viridis', figsize=(10,10), normalized=True, **kwargs):
        data = self.normalized if normalized else self.count_df
        sns.clustermap(data, cmap=cmap, figsize=figsize, **kwargs)
        plt.title("Assay Clustermap (normalized)" if normalized else "Assay Clustermap (counts)")
        plt.show()



# Example usage:
if __name__ == "__main__":
    # Example with dict of lists
    data = {
        "COMETS": ["A", "B", "C", "A"],
        "Gonzalez": ["B", "C", "D"],
        "Liu": ["A"],
        "Pietzner": ["C", "E", "F"]
    }
    plotter = UpSetPlotter(data)
    print(plotter.build_presence_matrix())
    print(plotter.build_memberships())
    #print(plotter.summary())
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