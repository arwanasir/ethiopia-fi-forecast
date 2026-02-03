import pandas as pd
import numpy as np
import os


def build_impact_model(data_path):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")

    df = pd.read_csv(data_path)

    events = df[df['record_type'] == 'event'].copy()
    links = df[df['record_type'] == 'impact_link'].copy()
    mag_map = {'high': 0.15, 'medium': 0.07, 'low': 0.02}
    dir_map = {'positive': 1, 'negative': -1}

    links['weight'] = links['impact_magnitude'].str.lower().map(mag_map) * \
        links['impact_direction'].str.lower().map(dir_map)

    matrix = links.pivot_table(
        index='parent_id',
        columns='related_indicator',
        values='weight',
        aggfunc='sum'
    ).fillna(0)

    return matrix, events, links


def reality_check(actual_start, actual_end, years, predicted_annual_impact):
    total_growth = (actual_end - actual_start) / actual_start
    annual_actual = (1 + total_growth) ** (1/years) - 1

    error = annual_actual - predicted_annual_impact
    return annual_actual, error


if __name__ == "__main__":
    PATH = '../data/processed/ethiopia_fi_enriched.csv'
    matrix, _, _ = build_impact_model(PATH)
    print("Association Matrix Created Successfully.")
    print(matrix)
