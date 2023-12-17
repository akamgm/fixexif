import os
import sys
import piexif
from PIL import Image
from datetime import datetime

def modify_exif_and_rename(folder_path, new_year=2023):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpg'):
            file_path = os.path.join(folder_path, filename)
            
            try:
                # Load the image and its EXIF data
                img = Image.open(file_path)
                exif_dict = piexif.load(img.info['exif'])

                # Modify the year in the EXIF data and rename the file
                if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
                    original_date_str = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode()
                    original_date = datetime.strptime(original_date_str, '%Y:%m:%d %H:%M:%S')
                    new_date = original_date.replace(year=new_year)
                    new_date_str = new_date.strftime('%Y:%m:%d %H:%M:%S')
                    new_file_name = new_date.strftime('%Y%m%d') + '.jpg'
                    new_file_path = os.path.join(folder_path, new_file_name)

                    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date_str.encode()

                    # Remove problematic tag if exists
                    if 41729 in exif_dict['Exif']:
                        del exif_dict['Exif'][41729]

                    # Save the image with modified EXIF data
                    exif_bytes = piexif.dump(exif_dict)
                    img.save(new_file_path, exif=exif_bytes)

                    # Delete the original file if the new file was written successfully
                    if os.path.exists(new_file_path):
                        os.remove(file_path)
                        print(f"Processed and renamed {filename} to {new_file_name} and deleted the original file.")
                else:
                    print(f"No DateTimeOriginal data in {filename}, skipping.")

            except KeyError:
                print(f"No EXIF data in {filename}, skipping.")
            except ValueError:
                print(f"Invalid or unexpected date format in {filename}: '{original_date_str}', skipping.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fixer.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    modify_exif_and_rename(directory_path)

