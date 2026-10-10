"""
AHP analysis for the football-player evaluation survey.

Input:
    survey_clean.csv

Outputs:
    results/ahp_aggregate_weights.csv
    results/ahp_consistency_summary.csv
    results/ahp_respondent_diagnostics.csv

Scale assumption:
    1 = first criterion strongly preferred
    2 = first criterion moderately/clearly preferred
    3 = first criterion slightly preferred
    4 = equal importance
    5 = second criterion slightly preferred
    6 = second criterion moderately/clearly preferred
    7 = second criterion strongly preferred

This is a documented conversion from the survey's directional 1–7 scale
to reciprocal AHP ratios. It is a modelling assumption, not a conversion
uniquely determined by the raw survey values.
"""

from pathlib import Path

import numpy as np
import pandas as pd

CRITERIA = [
    "Club Goals",
    "International Goals",
    "World Cup Performance",
    "Assists",
    "Team Win Rate",
    "Team Trophies",
    "Individual Awards",
    "Career Longevity",
]

# 1–3 favour the first criterion; 4 means equal; 5–7 favour the second.
# Ratios are reciprocal around the midpoint.
SCALE_TO_RATIO = {
    1: 7.0,
    2: 5.0,
    3: 3.0,
    4: 1.0,
    5: 1.0 / 3.0,
    6: 1.0 / 5.0,
    7: 1.0 / 7.0,
}

# Saaty's commonly used Random Index for an 8 x 8 matrix.
RANDOM_INDEX_N8 = 1.41


def comparison_columns(criteria):
    """Return the 28 survey columns in the order expected from the criteria."""
    return [
        f"{criteria[i]} vs. {criteria[j]}"
        for i in range(len(criteria))
        for j in range(i + 1, len(criteria))
    ]


def build_matrix(row, criteria=CRITERIA):
    """Convert one respondent's 28 directional answers into an 8 x 8 AHP matrix."""
    matrix = np.ones((len(criteria), len(criteria)), dtype=float)

    for i in range(len(criteria)):
        for j in range(i + 1, len(criteria)):
            column = f"{criteria[i]} vs. {criteria[j]}"
            answer = int(row[column])
            ratio = SCALE_TO_RATIO[answer]
            matrix[i, j] = ratio
            matrix[j, i] = 1.0 / ratio

    return matrix


def calculate_priority_vector(matrix):
    """Calculate normalized principal-eigenvector weights and consistency ratio."""
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    principal_index = np.argmax(eigenvalues.real)
    lambda_max = float(eigenvalues[principal_index].real)

    # Eigenvectors can have a negative sign; use the magnitude and normalize.
    weights = np.abs(eigenvectors[:, principal_index].real)
    weights = weights / weights.sum()

    n = matrix.shape[0]
    consistency_index = (lambda_max - n) / (n - 1)
    consistency_ratio = consistency_index / RANDOM_INDEX_N8

    return weights, lambda_max, consistency_index, consistency_ratio


def geometric_mean_group_matrix(matrices):
    """Aggregate reciprocal matrices using element-wise geometric means."""
    matrices = np.asarray(matrices, dtype=float)
    n = matrices.shape[1]
    group_matrix = np.ones((n, n), dtype=float)

    for i in range(n):
        for j in range(i + 1, n):
            group_matrix[i, j] = np.exp(np.mean(np.log(matrices[:, i, j])))
            group_matrix[j, i] = 1.0 / group_matrix[i, j]

    return group_matrix


def main():
    input_path = Path("D:\GOAT-AHP\data\processed\survey_clean.csv")
    output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    columns = comparison_columns(CRITERIA)

    missing_columns = sorted(set(columns) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing expected comparison columns: {missing_columns}")

    comparisons = df[columns]
    if comparisons.isna().any().any():
        raise ValueError("Missing values found in pairwise comparison responses.")

    invalid_values = sorted(
        set(pd.unique(comparisons.to_numpy().ravel())) - set(SCALE_TO_RATIO)
    )
    if invalid_values:
        raise ValueError(f"Unexpected comparison values: {invalid_values}")

    matrices = []
    individual_weights = []
    diagnostics = []

    for row_number, (_, row) in enumerate(df.iterrows(), start=1):
        matrix = build_matrix(row)
        weights, lambda_max, ci, cr = calculate_priority_vector(matrix)

        matrices.append(matrix)
        individual_weights.append(weights)
        diagnostics.append(
            {
                # Row number is for local diagnostics only; don't publish
                # respondent-level diagnostics alongside demographic data.
                "row_number": row_number,
                "lambda_max": lambda_max,
                "consistency_index": ci,
                "consistency_ratio": cr,
                "cr_at_most_0_10": cr <= 0.10,
            }
        )

    individual_weights = np.asarray(individual_weights)
    group_matrix = geometric_mean_group_matrix(matrices)
    group_weights, group_lambda, group_ci, group_cr = calculate_priority_vector(
        group_matrix
    )

    aggregate = pd.DataFrame(
        {
            "criterion": CRITERIA,
            "group_ahp_weight": group_weights,
            "mean_individual_weight": individual_weights.mean(axis=0),
            "sd_individual_weight": individual_weights.std(axis=0, ddof=1),
        }
    ).sort_values("group_ahp_weight", ascending=False)
    aggregate.to_csv(output_dir / "ahp_aggregate_weights.csv", index=False)

    diagnostics_df = pd.DataFrame(diagnostics)
    diagnostics_df.to_csv(output_dir / "ahp_respondent_diagnostics.csv", index=False)

    consistency_summary = pd.DataFrame(
        [
            {
                "respondents": len(df),
                "group_lambda_max": group_lambda,
                "group_consistency_index": group_ci,
                "group_consistency_ratio": group_cr,
                "individual_cr_min": diagnostics_df["consistency_ratio"].min(),
                "individual_cr_median": diagnostics_df["consistency_ratio"].median(),
                "individual_cr_mean": diagnostics_df["consistency_ratio"].mean(),
                "individual_cr_max": diagnostics_df["consistency_ratio"].max(),
                "individuals_cr_at_most_0_10": int(
                    diagnostics_df["cr_at_most_0_10"].sum()
                ),
            }
        ]
    )
    consistency_summary.to_csv(
        output_dir / "ahp_consistency_summary.csv", index=False
    )

    print("\nAggregate AHP weights (group geometric-mean matrix):")
    print(aggregate.to_string(index=False, formatters={
        "group_ahp_weight": "{:.4f}".format,
        "mean_individual_weight": "{:.4f}".format,
        "sd_individual_weight": "{:.4f}".format,
    }))
    print("\nConsistency summary:")
    print(consistency_summary.to_string(index=False, formatters={
        "group_lambda_max": "{:.4f}".format,
        "group_consistency_index": "{:.4f}".format,
        "group_consistency_ratio": "{:.4f}".format,
        "individual_cr_min": "{:.4f}".format,
        "individual_cr_median": "{:.4f}".format,
        "individual_cr_mean": "{:.4f}".format,
        "individual_cr_max": "{:.4f}".format,
    }))
    print(f"\nSaved outputs to: {output_dir.resolve()}")
    print("Do not publish respondent-level diagnostics without reviewing privacy/ethics.")


if __name__ == "__main__":
    main()
