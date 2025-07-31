import numpy as np
import pandas as pd
import geopandas as gpd
import pathlib
import argparse
import time

PROJECT_DIR = pathlib.Path(__file__).parent.parent

def process_merging_process(origin_points, merging_radius):
    # Add required columns
    origin_points = origin_points.copy()
    origin_points['origin_id'] = range(len(origin_points))
    origin_points['structure_no'] = 1

    # Create buffers and spatial join
    points_buffer_gdf = origin_points.copy()
    points_buffer_gdf['buffers'] = points_buffer_gdf.geometry.buffer(merging_radius)
    points_buffer_gdf = points_buffer_gdf.explode('buffers', index_parts=True).set_geometry('buffers')
    del points_buffer_gdf['geometry']
    points_buffer_gdf.crs = origin_points.crs
    points_buffer_sj = gpd.sjoin(origin_points, points_buffer_gdf, how='inner')
    points_buffer_sj.index = range(len(points_buffer_sj))

    # Iteratively merge structures in overlapping buffers
    merged_buffer_sj = points_buffer_sj.copy()
    while True:
        buffer_counts = merged_buffer_sj['origin_id_right'].value_counts()
        multi_str_list = buffer_counts[buffer_counts >= 2].index.tolist()
        if not multi_str_list:
            break
        
        buffer_id = multi_str_list[0]
        rows_in_buffer = merged_buffer_sj[merged_buffer_sj['origin_id_right'] == buffer_id]
        pts_id_list = rows_in_buffer['origin_id_left'].tolist()
        
        if pts_id_list:
            rows_of_pts = merged_buffer_sj[merged_buffer_sj['origin_id_left'].isin(pts_id_list)]
            add_row = rows_of_pts.loc[(rows_of_pts['origin_id_right'] == buffer_id) & 
                                      (rows_of_pts['origin_id_left'] == buffer_id)].copy()
            
            if not add_row.empty:
                add_row.loc[add_row.index[0], 'structure_no_left'] = len(rows_in_buffer)
                add_row.loc[add_row.index[0], 'aggr_area_m2'] = rows_in_buffer['area_in_meters_left'].sum()
                rows_to_drop = merged_buffer_sj[
                    (merged_buffer_sj['origin_id_left'].isin(pts_id_list)) |
                    (merged_buffer_sj['origin_id_right'].isin(pts_id_list))
                ]
                merged_buffer_sj.drop(rows_to_drop.index, inplace=True)
                merged_buffer_sj = pd.concat([merged_buffer_sj, add_row], ignore_index=True)
            else:
                merged_buffer_sj.drop(rows_in_buffer.index, inplace=True)

    # Set area for non-merged points
    mask = merged_buffer_sj.index.isin(merged_buffer_sj[merged_buffer_sj['structure_no_left'] == 1].index)
    merged_buffer_sj.loc[mask, 'aggr_area_m2'] = merged_buffer_sj.loc[mask, 'area_in_meters_left']

    # Convert CRS to EPSG:32636
    merged_buffer_sj = merged_buffer_sj.set_crs("EPSG:32636", allow_override=True)

    # Select and rename columns to match merge_structures output
    # If 'd_left' is not present, you may need to adjust this line accordingly
    cols_to_keep = ['d_left', 'geometry', 'origin_id_left', 'structure_no_left', 'aggr_area_m2']
    merged_buffer_sj = merged_buffer_sj[cols_to_keep]
    merged_buffer_sj.columns = ['district', 'geometry', 'origin_id', 'str_no', 'AggArea_m2']

    return merged_buffer_sj



import matplotlib.pyplot as plt

def visualize_merging(input_gdf, results_gdf, merging_radius, output_file):
    fig, ax = plt.subplots(figsize=(10, 10))
    input_gdf.plot(ax=ax, color='#0a2540', markersize=0.5, alpha=0.9, label="Original Structures", zorder=2)
    results_gdf_buffered = results_gdf.copy()
    results_gdf_buffered['geometry'] = results_gdf_buffered.geometry.buffer(merging_radius)
    results_gdf_buffered.plot(ax=ax, color='red', alpha=0.5, label="Merged Buffers", zorder=1, linewidth=0)
    ax.legend()
    ax.set_title("Structure Merging Visualization")
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(output_file, format="jpg", dpi=600)
    plt.close()


if __name__ == "__main__":
    
    
    parser = argparse.ArgumentParser(description='Merge structures within specified radius')
    parser.add_argument('--input_file', '-i', required=True, help='Input file path')
    parser.add_argument('--output_file', '-o', required=True, help='Output file path')
    parser.add_argument('--radius', '-r', type=float, default=20, help='Merging radius in meters')
    
    args = parser.parse_args()
    
    # Convert to Path objects
    input_file = pathlib.Path(args.input_file)
    output_file = PROJECT_DIR / "structure_merging_model" / "results" / args.output_file
    
    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading input data from: {input_file}")
    
    # Only allow parquet file
    if str(input_file).endswith('.parquet'):
        input_gdf = gpd.read_parquet(input_file)
    else:
        raise ValueError(f"Only parquet files are supported as input. Got: {input_file}")
    
    total_before = len(input_gdf)
    print(f"Before merging: {total_before} structures")
    
    print("Processing merging algorithm...")
    start_time = time.time()
    
    results = process_merging_process(input_gdf, args.radius)
    
    processing_time = time.time() - start_time
    total_after = len(results)
    
    print(f"After merging: {total_after} structures")
    print(f"Processing time: {processing_time:.2f} seconds")
    
    # Save results based on output extension
    # Only allow saving as parquet file
    results.to_parquet(output_file, index=False, compression='snappy')
    print(f"Results saved to: {output_file}")
