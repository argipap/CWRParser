import codecs
import csv
import re
import sys
from tqdm import tqdm


def find_duplicates(initial_dictionary):
    temp_list = []
    occurences = dict()
    unique_asset_blocks = dict()
    items = initial_dictionary.items()
    with tqdm(
        desc="Find duplicate assets ...",
        unit="parsing",
        total=len(items),
    ) as bar:
        for key, value in items:
            if value not in temp_list:
                temp_list.append(value)
                unique_asset_blocks[key] = value

            asset_title = value[0]
            if not occurences.get(asset_title):
                occurences[asset_title] = 1
            else:
                occurences[asset_title] = occurences.get(asset_title) + 1
            bar.update(1)
    return unique_asset_blocks, occurences


def write_unique(unique_asset_blocks):
    output_file = "unique_assets_results.csv"
    with open(output_file, "w") as csv_file:
        total_uniq_assets = unique_asset_blocks.items()
        with tqdm(
            desc=f"Write unique assets in file {output_file} ...",
            unit="write_file",
            total=len(total_uniq_assets),
        ) as bar:
            writer = csv.writer(csv_file, delimiter=";")
            header = ["asset_title", "writers"]
            writer.writerow(header)
            for _, value in unique_asset_blocks.items():
                csv_row = []
                asset_title = value[0]
                writers_list = value[1:]
                csv_row.append(asset_title)
                # deconstruct writers list to a string with comma seperated values
                writers = ",".join(writers_list)
                # use regular expression to replace multiple spaces into one and then write row
                csv_row.append(re.sub('\s+',' ',writers))
                writer.writerow(csv_row)
                bar.update(1)


def write_duplicates(occurences):
    output_file = "duplicate_assets_results.csv"
    with open(output_file, "w") as csv_file:
        total_occurences = occurences.items()
        with tqdm(
            desc=f"Write duplicate assets in file {output_file} ...",
            unit="write_file",
            total=len(total_occurences),
        ) as bar:
            writer = csv.writer(csv_file, delimiter=";")
            header = ["asset_title", "occurences"]
            writer.writerow(header)
            for asset_title, occurence in total_occurences:
                if occurence > 1:
                    csv_row = []
                    csv_row.append(asset_title)
                    # add occurence
                    csv_row.append(occurence)
                    writer.writerow(csv_row)
                bar.update(1)


def main():

    cwr_filename = sys.argv[1]
    with codecs.open(cwr_filename, encoding="latin-1") as cwr_file:
        asset_writer_dictionary = {}
        counter = 0
        total_lines = cwr_file.readlines()
        with tqdm(
            desc="Parsing CWR File Line by Line ...",
            unit="read_file",
            total=len(total_lines),
        ) as bar:
            for line in total_lines:
                if line[:3] in ["NWR", "REV", "EXC", "ISW"]:
                    counter +=1
                    asset_title = line[19:80].strip()
                    asset_writer_dictionary[counter] = [asset_title]
                elif line[:3] in ["SWR", "OWR"]:
                    writer = line[28:104].strip()
                    existing_value = asset_writer_dictionary.get(counter)
                    if existing_value:
                        existing_value.append(writer)
                        asset_writer_dictionary[counter] = existing_value
                else:
                    pass
                bar.update(1)


        
        unique_asset_blocks, occurences = find_duplicates(asset_writer_dictionary)

    write_unique(unique_asset_blocks)
    write_duplicates(occurences)


if __name__ == "__main__":
    main()
