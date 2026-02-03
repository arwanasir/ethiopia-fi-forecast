import numpy as np
import pandas as pd


def generate_multi_indicator_forecast(indicators_data):
    years = [2024, 2025, 2026, 2027]
    all_results = []

    for item in indicators_data:
        for scenario, multiplier in [('Pessimistic', 0.5), ('Base', 1.0), ('Optimistic', 1.5)]:
            adj_growth = item['growth'] + (sum(item['impacts']) * multiplier)

            for y in years:
                val = item['start_val'] * (1 + adj_growth)**(y - 2024)
                all_results.append({
                    'Indicator': item['name'],
                    'Scenario': scenario,
                    'Year': y,
                    'Value': round(min(val, 95.0), 2)
                })

    return pd.DataFrame(all_results)
