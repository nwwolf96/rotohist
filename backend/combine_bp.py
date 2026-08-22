#!/usr/bin/env python3

import sys
import pandas as pd


def main():
    # -----------------------------
    # Validate arguments
    # -----------------------------
    if len(sys.argv) != 3:
        print("Usage: python combine_rankings.py <batters.csv> <pitchers.csv>")
        sys.exit(1)

    batters_path = sys.argv[1]
    pitchers_path = sys.argv[2]

    # -----------------------------
    # Load CSVs
    # -----------------------------
    hitters = pd.read_csv(batters_path)
    pitchers = pd.read_csv(pitchers_path)

    # -----------------------------
    # Prefix columns
    # -----------------------------
    hitters = hitters.add_prefix("H-")
    pitchers = pitchers.add_prefix("P-")

    # -----------------------------
    # Ensure ACV numeric
    # -----------------------------
    hitters["H-ACV"] = pd.to_numeric(hitters["H-ACV"], errors="coerce")
    pitchers["P-ACV"] = pd.to_numeric(pitchers["P-ACV"], errors="coerce")

    # -----------------------------
    # Add missing columns to each
    # -----------------------------
    for col in pitchers.columns:
        if col not in hitters.columns:
            hitters[col] = None

    for col in hitters.columns:
        if col not in pitchers.columns:
            pitchers[col] = None

    # -----------------------------
    # Combine
    # -----------------------------
    combined = pd.concat([hitters, pitchers], ignore_index=True)

    # -----------------------------
    # Unified ACV for ranking
    # -----------------------------
    combined["ACV"] = combined["H-ACV"].combine_first(combined["P-ACV"])

    # Sort by ACV descending
    combined = combined.sort_values(by="ACV", ascending=False).reset_index(drop=True)

    # Insert TRank
    combined.insert(0, "TRank", combined.index + 1)

    # -----------------------------
    # Order columns
    # -----------------------------
    h_cols = [c for c in combined.columns if c.startswith("H-")]
    p_cols = [c for c in combined.columns if c.startswith("P-")]

    final_columns = ["TRank"] + h_cols + p_cols + ["ACV"]
    combined = combined[final_columns]

    # -----------------------------
    # Output file
    # -----------------------------
    output_path = "combined_rankings_full.csv"
    combined.to_csv(output_path, index=False)

    print(f"Saved combined rankings to {output_path}")


if __name__ == "__main__":
    main()
