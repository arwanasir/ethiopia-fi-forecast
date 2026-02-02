import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_dataset_summary(df):
    return df.groupby(['record_type', 'pillar']).size().unstack(fill_value=0)


def plot_access_trajectory(df):
    acc_own = df[df['indicator_code'] ==
                 'ACC_OWN_TOT'].sort_values('observation_date')

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=acc_own, x='year', y='value_numeric',
                 marker='o', linewidth=3, color='#1f77b4')

    plt.title("Ethiopia: Account Ownership Trajectory (2011-2024)")
    plt.ylabel("% of Adults")
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    return plt


def plot_correlation_matrix(df):
    obs_df = df[df['record_type'] == 'observation']
    pivot_df = obs_df.pivot_table(
        index='year', columns='indicator', values='value_numeric')
    return pivot_df.corr()


def plot_quality_assessment(df):
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x='confidence', palette='viridis',
                  order=['low', 'medium', 'high'])
    plt.title('Plot 1: Data Quality (Confidence Distribution)')
    return plt


def plot_coverage_heatmap(df):
    obs_df = df[df['record_type'] == 'observation']
    coverage = obs_df.pivot_table(
        index='pillar', columns='year', values='value_numeric', aggfunc='count').fillna(0)
    plt.figure(figsize=(10, 4))
    sns.heatmap(coverage, annot=True, cmap="YlGnBu", cbar=False)
    plt.title('Plot 2: Temporal Coverage (Data Gaps)')
    return plt


def plot_access_trajectory(df):
    acc_own = df[df['indicator_code'] == 'ACC_OWN_TOT'].sort_values('year')
    plt.figure(figsize=(10, 6))
    plt.plot(acc_own['year'], acc_own['value_numeric'],
             marker='o', linewidth=3, label='Total Ownership')
    plt.title("Plot 3: Access Trajectory (2011-2024)")
    plt.ylim(0, 100)
    return plt


def plot_usage_gap(df):

    labels = [
        'Mobile Money Registered (2025 Est)', 'Active Usage (2024 Findex)']
    values = [139, 49]
    plt.figure(figsize=(8, 5))
    sns.barplot(x=labels, y=values, palette='Reds_d')
    plt.title("Plot 4: The 'Registration vs. Usage' Gap")
    plt.ylabel("Index / Millions")
    return plt


def plot_gender_gap(df):
    years = [2011, 2014, 2017, 2021, 2024]
    male = [26, 28, 41, 52, 55]
    female = [18, 16, 29, 40, 43]

    plt.figure(figsize=(10, 5))
    plt.fill_between(years, female, male, color='gray',
                     alpha=0.2, label='Gender Gap')
    plt.plot(years, male, marker='s', label='Male', color='blue')
    plt.plot(years, female, marker='s', label='Female', color='pink')
    plt.title("Plot 5: Evolution of the Gender Gap (2011-2024)")
    plt.legend()
    return plt
