# -----------------------------------------------------------
# Reconstruct images captured using GoPro MAX, making them conform to specification of Mapillary Uploader
# We achieve this by loading image and exif separately and then save them into the save file
#
# Input: images in folder <source_directory>
# Output: images in folder <output_directory>
# -----------------------------------------------------------

import argparse
import os
import time
import traceback
from multiprocessing import Pool
import piexif
from PIL import Image


def handle_error(e):
    traceback.print_exception(type(e), e, e.__traceback__)


def process_image(image_path, export_path):
    image = Image.open(image_path)
    # extract exif of an image
    exif_dict = piexif.load(image.info["exif"])
    exif_dict = {k: v for k, v in exif_dict.items()}
    exif_bytes = piexif.dump(exif_dict)
    # save image with new exif
    image.save(export_path, exif=exif_bytes)


def main(source_directory, output_directory, worker):
    print(f'Processing images from {source_directory}')
    print(f'Export new images to {output_directory}')

    path_list = []
    for folder in os.listdir(source_directory):
        if not os.path.isdir(os.path.join(output_directory, folder)):
            os.makedirs(os.path.join(output_directory, folder))

        # iterate all images in folder
        for file in os.listdir(os.path.join(source_directory, folder)):
            path_list.append(
                (os.path.join(source_directory, folder, file), os.path.join(output_directory, folder, file)))

    start = time.time()

    with Pool(processes=worker) as p:
        for image_path, export_path in path_list:
            p.apply_async(process_image, args=(image_path, export_path), error_callback=handle_error)
        print('Waiting all child processes complete')
        p.close()
        p.join()
    print('All child processes completed')
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source_directory", help="Source directory contains image folder", type=str)
    parser.add_argument("output_directory", help="Output directory", type=str)
    parser.add_argument("worker", help="Number of workers in multiprocessing", type=str, default=4)
    args = parser.parse_args()
    main(**vars(parser.parse_args()))
