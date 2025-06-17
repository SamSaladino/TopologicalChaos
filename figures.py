import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_memberships

# Load your presence matrix CSV or build from sets like before
# Example: assume you already have a binary matrix called `presence_matrix`

# Convert to membership list
# memberships = []
# for index, row in presence_matrix.iterrows():
#     present = row[row == 1].index.tolist()
#     if present:
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
