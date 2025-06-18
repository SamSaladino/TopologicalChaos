import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships
import seaborn as sns
import numpy as np

class AssaySetPlotter:
    def __init__(self, data, refmet=None, names=None):
        """
        data: dict of {assay_name: list of CHEBI IDs} or DataFrame (CHEBI IDs as index, assays as columns, 1/0)
        refmet: DataFrame with columns ['chebi_id', 'super_class', 'main_class', 'sub_class'] (optional, for class heatmap)
        names: list of names if data is a list of lists
        """
        # Build presence matrix
        if isinstance(data, dict):
            all_chebis = sorted(set.union(*(set(v) for v in data.values())))
            presence_matrix = pd.DataFrame(index=all_chebis)
            for name, chebis in data.items():
                presence_matrix[name] = presence_matrix.index.isin(chebis).astype(int)
            self.presence_matrix = presence_matrix
        elif isinstance(data, pd.DataFrame):
            self.presence_matrix = data.copy()
        elif isinstance(data, (list, tuple)):
            if names is None or len(names) != len(data):
                raise ValueError("If data is a list, 'names' must be provided and match its length.")
            all_chebis = sorted(set.union(*(set(lst) for lst in data)))
            presence_matrix = pd.DataFrame(index=all_chebis)
            for name, lst in zip(names, data):
                presence_matrix[name] = presence_matrix.index.isin(lst).astype(int)
            self.presence_matrix = presence_matrix
        else:
            raise ValueError("Unsupported data type for AssaySetPlotter.")
        self.assay_cols = list(self.presence_matrix.columns)
        self.refmet = refmet
        self.df_with_class = None
        self.count_df = None
        self.normalized = None

    # --- UpSet plot methods ---
    def build_memberships(self):
        memberships = []
        for index, row in self.presence_matrix.iterrows():
            present = row[row == 1].index.tolist()
            if present:
                memberships.append(present)
        return memberships

    def plot_upset(self, figsize=(10, 6), title="UpSet Plot", save_path=None):
        memberships = self.build_memberships()
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

    # --- Heatmap/class methods ---
    def merge_with_classes(self):
        if self.refmet is None:
            raise ValueError("refmet DataFrame required for class-based heatmap.")
        merged = pd.merge(
            self.presence_matrix,
            self.refmet[['chebi_id', 'super_class', 'main_class', 'sub_class']],
            left_index=True,
            right_on='chebi_id',
            how='inner'
        )
        self.df_with_class = merged

    def group_and_normalize(self, groupby=['super_class', 'main_class']):
        if self.df_with_class is None:
            raise ValueError("Run merge_with_classes() first.")
        count_df = self.df_with_class.groupby(groupby)[self.assay_cols].sum()
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
    refmet = pd.DataFrame({
        'chebi_id': ["A", "B", "C", "D", "E", "F"],
        'super_class': ["Class1", "Class1", "Class2", "Class2", "Class3", "Class3"],
        'main_class': ["Main1", "Main1", "Main2", "Main2", "Main3", "Main3"],
        'sub_class': ["Sub1", "Sub1", "Sub2", "Sub2", "Sub3", "Sub3"]
    })
    plotter = AssaySetPlotter(data, refmet=refmet, names=list(data.keys()))
    plotter.plot_upset(title="Example UpSet Plot")
    plotter.merge_with_classes()
    normalized_data = plotter.group_and_normalize()
    plotter.plot_clustermap(normalized=True, cmap='coolwarm', figsize=(12, 12))
    plotter.plot_clustermap(normalized=False, cmap='coolwarm', figsize=(12, 12))

# This code defines the `AssaySetPlotter` class for plotting UpSet plots and heatmaps of assay data. It supports various input formats and includes methods for merging with class data, normalizing counts, and plotting clustermaps. The example usage demonstrates how to create an instance of the class and generate plots.

 