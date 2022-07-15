import codecs
import csv
import re
import sys


def find_duplicates(initial_dictionary):
    temp_list = []
    occurences = dict()
    unique_asset_blocks = dict()
    progress = 0
    for key, value in initial_dictionary.items():
        if value not in temp_list:
            temp_list.append(value)
            unique_asset_blocks[key] = value

        asset_title = value[0]
        if not occurences.get(asset_title):
            occurences[asset_title] = 1
        else:
            occurences[asset_title] = occurences.get(asset_title) + 1
        progress += 1
        print(f"find_duplicates_progress: {progress}")
    return unique_asset_blocks, occurences


def write_unique(unique_asset_blocks):
    progress = 0
    with open("unique_assets_results.csv", "w+") as csv_file:
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
            progress += 1
            print(f"unique assets progress: {progress}")


def write_duplicates(occurences):
    progress = 0
    with open("duplicate_assets_results.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        header = ["asset_title", "occurences"]
        writer.writerow(header)
        for asset_title, occurence in occurences.items():
            if occurence > 1:
                csv_row = []
                csv_row.append(asset_title)
                # add occurence
                csv_row.append(occurence)
                writer.writerow(csv_row)
            progress += 1
            print(f"duplicate assets progress: {progress}")


def main():

    cwr_filename = sys.argv[1]
    with codecs.open(cwr_filename, encoding="latin-1") as cwr_file:
        asset_writer_dictionary = {}
        counter = 0

        for progress, line in enumerate(cwr_file.readlines()):
            print(f"Line: {progress} - {line}")
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


        
        unique_asset_blocks, occurences = find_duplicates(asset_writer_dictionary)

    write_unique(unique_asset_blocks)
    write_duplicates(occurences)


if __name__ == "__main__":
    main()
