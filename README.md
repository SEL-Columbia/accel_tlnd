# Accelerated Two-Level Network Design Model (Training Version)

## In the training version (Phase 1)

- There is **no parallel processing** in this phase.
- The **merging process is moved out** and handled separately.

### Training on Google Colab

To run the training version on Google Colab, follow these steps:

1. **Open a new Colab notebook** in your browser.
2. **Clone this GitHub repository** into your Colab environment:
   ```python
   !git clone <repository_url>
   %cd <repository_folder>
   ```
3. **A - Run the UI notebook for TLND:**
   - Open and run `network_design_ui.ipynb` to perform the two-level network design process.
   - You can run it directly in Colab with:
     ```python
     %run network_design_ui.ipynb
     ```
4. **B - Run the UI notebook for merging:**
   - open and run `merging_ui.ipynb` to perform or structure the merging process.
   - Run it in Colab with:
     ```python
     %run merging_ui.ipynb
     ```

> **Note:**  
> - Make sure to upload or place your input files in the appropriate directories as required by the notebooks.
> - Adjust any parameters or file paths in the UI notebooks as needed for your specific case.

This workflow separates the network design and merging steps, and is intended for interactive use in a Colab environment.


## Outlier Exclusion Function

Functions in `scripts/outlier_exclusion.py` use DBSCAN clustering to automatically identify and remove geospatial outliers that can distort community distribution metrics. When `outlier_exclusion_case` is True in the params.yaml, it runs as a preprocessing step before network design to ensure robust cost calculations.

**Usage:**
```python
filtered_nodes = exclude_outliers(nodes_gdf, eps=100, min_samples=5)
```

**Parameters:**
- `nodes_gdf`: GeoDataFrame containing node geographic information
- `eps`: Distance threshold in meters (default: 100)
- `min_samples`: Minimum nodes to form a cluster (default: 5)

The function leverages sklearn's DBSCAN implementation and can be used independently from the main model for outlier detection in geospatial datasets.


## Structure Merging Function

This is a preprocessing step. Open-source building footprint data, developed from satellite imagery, reflects predicted building structures. In rural areas, it’s common for a single household to have multiple nearby structures. According to Uganda’s 2024 census, there are 10.7 million households, while Google’s Open Buildings data detects 18.4 million structures. In urban areas, merging may not be necessary due to multi-family housing, but in rural regions, it helps approximate household locations for further analysis. And in our study,
See details about the process here: [Strutcure Merge Preparation](scripts/preparation/README_str_merge.md)
