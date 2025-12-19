"""Script to combine multiple JSON files into a single CSV file,
then combine multiple CSV files into one.
Then reorders by column 'at' (timestamp)
Then checks for duplicate entries.
The transform steps in the ETL"""

import os
import pandas as pd
import json


def find_json_files() -> list[str]:
    """Return a list of JSON files in the './bucket_data' directory
    that begin with 'lmnh'."""
    all_files = os.listdir('./bucket_data')
    return [f for f in all_files if f.startswith('lmnh') and f.endswith('.json')]


def combine_jsons(filenames: list[str]) -> pd.DataFrame:
    """Combine multiple JSON files into a single DataFrame."""
    combined_df = pd.DataFrame()
    for file in filenames:
        file_path = os.path.join('./bucket_data', file)
        with open(file_path, 'r') as f:
            data = json.load(f)
            df = pd.json_normalize(data)
            print(f'Processing file: {file} with {len(df)} records')
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    print(f'Total records combined: {len(combined_df)}')
    # make all columns lowercase
    combined_df.columns = [col.lower() for col in combined_df.columns]
    # rename column 'exhibition_id' to 'exhibition_code'
    if 'exhibition_id' in combined_df.columns:
        combined_df = combined_df.rename(
            columns={'exhibition_id': 'exhibition_code'})
    return combined_df


def save_to_csv(df: pd.DataFrame) -> None:
    """Save the DataFrame to a CSV file in './combined_data' directory."""
    output_path = './combined_data/combined_exhibition_data.csv'
    df.to_csv(output_path, index=False)
    print(f'Saved combined data to {output_path}.')


def find_csv_files(file_list: list[str]) -> list[str]:
    """Return a list of CSV files from the provided file list."""
    return [f for f in file_list if f.endswith('.csv')]


def combine_csv_files(csv_files: list[str], output_file: str) -> None:
    """Combine multiple CSV files into a single CSV file."""
    combined_df = pd.DataFrame()
    for file in csv_files:
        df = pd.read_csv(os.path.join('./bucket_data', file))
        print(f'Processing file: {file} with {len(df)} records')
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    print(f'Total records combined: {len(combined_df)}')
    combined_df = reorder_by_timestamp(combined_df)
    combined_df.to_csv(output_file, index=False)


def reorder_by_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    """Reorder Dataframe by 'at' timestamp column, return a dataframe."""
    df['at'] = pd.to_datetime(df['at'])
    df = df.sort_values(by='at').reset_index(drop=True)
    print('Dataframe reordered by timestamp.')
    return df


if __name__ == "__main__":
    json_files = find_json_files()
    combined_df = combine_jsons(json_files)
    save_to_csv(combined_df)
    files = os.listdir('./bucket_data')
    csv_files = find_csv_files(files)
    combine_csv_files(csv_files, './combined_data/combined_museum_data.csv')
