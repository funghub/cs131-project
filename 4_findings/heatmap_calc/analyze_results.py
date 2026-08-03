"""
Phase 4 graph creation

1. Pull the Spark output from GCS

    gcloud storage cp -r gs://cs131-project/cs131_proj/output/run_1w/chromosome_heatmap_data .

    Create figures directory for output

2. Run with

    python3 analyze_results.py 

Produces:
    chr_heatmap.png              : chromosome heatmap of mean |z|
    chr_barplot.png              : bar chart, mean |z| by chromosome
    heterogeneity_crosscheck.png : our z-score vs Pan-UKBB's hq stat
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

INPUT_FILE="./chromosome_heatmap_data/part-00000-4903b2aa-f708-4eb4-bd52-e680c71e2095-c000.csv"
# Make sure to create figures dir before running ----
OUTPUT_DIR="./figures"

def load_by_chr(input_file: str) -> pd.DataFrame:
    """load dataframe into pandas"""
    df = pd.read_csv(input_file)
 
    # Sort chromosomes in genome order (1, 2, 3, ... 22, X) instead of alphabetical order ----
    chr_order = [str(n) for n in range(1, 23)] + ["X"]
    df["chr"] = pd.Categorical(df["chr"], categories=chr_order, ordered=True)
    df = df.sort_values("chr").reset_index(drop=True)
 
    return df

def make_barplot(df: pd.DataFrame, out_path: str):
    ax = df.plot(
        x="chr",
        y=["mean_abs_z_triglyceride", "mean_abs_z_diabetes"],
        kind="bar",
        figsize=(14, 6),
        color=["#2E86AB", "#E85D75"]
    )
    
    ax.legend(["Triglyceride", "Type 2 Diabetes"])
    ax.set_xlabel("Chromosome")
    ax.set_ylabel("Mean |z-score| (CSA vs EUR effect-size divergence)")
    ax.set_title("Ancestry-Divergent Effect Sizes by Chromosome")
 
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

def make_heatmap(df: pd.DataFrame, out_path: str):
    """
    Prepare data for imshow using an array to form a grid. Generates a heatmap
    """
    grid = np.array([
        df["mean_abs_z_triglyceride"],
        df["mean_abs_z_diabetes"],
    ])
 
    fig, ax = plt.subplots(figsize=(14, 3.5))
    im = ax.imshow(grid, aspect="auto", cmap="magma")
 
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Triglyceride", "Type 2 Diabetes"])
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df["chr"], rotation=45, ha="right")
    ax.set_title("Mean |z-score| Heatmap: CSA vs EUR Effect-Size Divergence")
 
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Mean |z|")
 
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_crosscheck(df: pd.DataFrame, out_path: str):
    """
    Calculation check plot: our CSA-vs-EUR z-score for diabetes vs Pan-UKBB's
    heterogeneity_hq statistic. If our calculations are correct they should reflect each other.
    """
    ax = df.plot.scatter(
        x="mean_db_heterogeneity_hq",
        y="mean_abs_z_diabetes",
        s=60, color="#E85D75", edgecolor="black", linewidth=0.5,
        figsize=(7, 6),
    )
 
    # Label each dot with its chromosome ----
    x_vals = df["mean_db_heterogeneity_hq"]
    y_vals = df["mean_abs_z_diabetes"]
    labels = df["chr"]
    for x, y, label in zip(x_vals, y_vals, labels):
        ax.annotate(str(label), (x, y), fontsize=7,
                    xytext=(3, 3), textcoords="offset points")
 
    ax.set_xlabel("Pan-UKBB mean neglog10(p) heterogeneity_hq (diabetes)")
    ax.set_ylabel("Our mean |z-score| (diabetes, CSA vs EUR)")
    ax.set_title("Cross-Check: Our Pairwise Z-Test vs\nPan-UKBB's Heterogeneity Statistic")
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

def main():

    df = load_by_chr(INPUT_FILE)
    print(f"Loaded {len(df)} chromosome rows.")
    print(df.head())
 
    make_barplot(df, f"{OUTPUT_DIR}/chr_barplot.png")
    make_heatmap(df, f"{OUTPUT_DIR}/chr_heatmap.png")
    make_crosscheck(df, f"{OUTPUT_DIR}/heterogeneity_crosscheck.png")
 
    print(f"\nFigures written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
