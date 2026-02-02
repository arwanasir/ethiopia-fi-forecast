import pandas as pd
import os
from datetime import datetime


def load_and_unify_data(file_path):
    """
    Step 1: Understand the Schema.
    Loads sheets, adds record_type, and unifies them into a single long-format DataFrame.
    """
    # Load all sheets
    all_sheets = pd.read_excel(file_path, sheet_name=None)

    # Standardize column names to lowercase and underscores
    def clean_cols(df):
        df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
        return df

    # Process main data (Observations, Events, Targets)
    data_df = clean_cols(all_sheets.get(
        'ethiopia_fi_unified_data', pd.DataFrame()))

    # Process Impact Links
    links_df = clean_cols(all_sheets.get('impact_sheet', pd.DataFrame()))
    links_df['record_type'] = 'impact_link'

    # Combine data_df and links_df into the Unified Schema
    # Note: record_type for data_df should already be present in the 'record_type' column
    master_df = pd.concat([data_df, links_df], ignore_index=True)

    if 'observation_date' in master_df.columns:
        master_df['observation_date'] = pd.to_datetime(
            master_df['observation_date'])

    return master_df


def add_enriched_record(df, record_data, log_path='../data_enrichment_log.md'):
    """
    Logic: Validates the record against Task 1 schema rules and updates the doc log.
    """
    # 1. Automatic Metadata
    record_data['collection_date'] = datetime.now().strftime('%Y-%m-%d')

    # 2. Schema Rule: Events must have an empty pillar (as per instructions)
    if record_data.get('record_type') == 'event':
        record_data['pillar'] = None

    # 3. Append to the main DataFrame
    new_row = pd.DataFrame([record_data])
    updated_df = pd.concat([df, new_row], ignore_index=True)

    # 4. Document Your Additions (Markdown Log)
    log_content = f"\n## New Record: {record_data.get('indicator', 'Event/Link')}\n"
    log_content += f"- **Source URL:** {record_data.get('source_url')}\n"
    log_content += f"- **Original Text:** {record_data.get('original_text')}\n"
    log_content += f"- **Confidence:** {record_data.get('confidence')}\n"
    log_content += f"- **Collected By:** {record_data.get('collected_by')}\n"
    log_content += f"- **Notes:** {record_data.get('notes')}\n"
    log_content += "---\n"

    # Write to the log file
    with open(log_path, "a") as f:
        f.write(log_content)

    return updated_df
