import codecs
import csv
import re
import sys
from typing import Dict

from tqdm import tqdm


def find_asset_occurences(asset_blocks: Dict, delimeter=";") -> Dict:
    occurences = dict()
    items = asset_blocks.items()
    with tqdm(
        desc="Find duplicate assets ...",
        unit="assets",
        total=len(items),
    ) as bar:
        for _, value in items:
            asset_title = value[0]
            writers = re.sub("\s+", " ", ",".join(value[1:])) if len(value) > 1 else ""
            asset_record_key = f"{asset_title}{delimeter}{writers}"
            if not occurences.get(asset_record_key):
                occurences[asset_record_key] = 1
            else:
                occurences[asset_record_key] = occurences.get(asset_record_key) + 1
            bar.update(1)
    return occurences


def write_unique(
    occurences: Dict, output_file: str = "unique_assets_results.csv"
) -> None:
    with open(output_file, "w") as csv_file:
        total_occurences = occurences.items()
        with tqdm(
            desc=f"Write unique assets in file {output_file} ...",
            unit="assets",
            total=len(total_occurences),
        ) as bar:
            writer = csv.writer(csv_file, delimiter=";")
            header = ["asset_title", "writers"]
            writer.writerow(header)
            for asset_columns, occurence in total_occurences:
                # unique are with occurence == 1
                if occurence == 1:
                    csv_row = asset_columns.split(";")
                    writer.writerow(csv_row)
                bar.update(1)


def write_duplicates(
    occurences: Dict, output_file: str = "duplicate_assets_results.csv"
) -> None:
    output_file = "duplicate_assets_results.csv"
    with open(output_file, "w") as csv_file:
        total_occurences = occurences.items()
        with tqdm(
            desc=f"Write duplicate assets in file {output_file} ...",
            unit="assets",
            total=len(total_occurences),
        ) as bar:
            writer = csv.writer(csv_file, delimiter=";")
            header = ["asset_title", "writers", "occurences"]
            writer.writerow(header)
            for asset_columns, occurence in total_occurences:
                # duplicates are the ones with occurence>1
                if occurence > 1:
                    csv_row = asset_columns.split(";")
                    csv_row.append(occurence)
                    writer.writerow(csv_row)
                bar.update(1)


def parse_cwr_file(cwr_filename: str) -> Dict:
    asset_writer_dictionary = {}
    asset_index_key = 0

    with codecs.open(cwr_filename, encoding="latin-1") as cwr_file:
        total_lines = cwr_file.readlines()
        with tqdm(
            desc="Parsing CWR File Line by Line ...",
            unit="lines",
            total=len(total_lines),
        ) as bar:
            for line in total_lines:
                if line.startswith(("NWR", "REV", "EXC", "ISW")):
                    asset_index_key += 1
                    asset_title = line[19:80].strip()
                    asset_writer_dictionary[asset_index_key] = [asset_title]
                if line.startswith(("SWR", "OWR")):
                    writer = line[28:104].strip()
                    existing_value = asset_writer_dictionary.get(asset_index_key)
                    if existing_value:
                        existing_value.append(writer)
                        asset_writer_dictionary[asset_index_key] = existing_value
                bar.update(1)
    return asset_writer_dictionary


def main():

    cwr_filename = sys.argv[1]
    asset_blocks = parse_cwr_file(cwr_filename)
    occurences = find_asset_occurences(asset_blocks)
    write_unique(occurences)
    write_duplicates(occurences)


if __name__ == "__main__":
    main()
