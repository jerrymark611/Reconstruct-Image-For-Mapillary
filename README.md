# Reconstruct-Image-For-Mapillary
## Introduction
Picture taken using GoPro MAX can't be directly upload to Mapillary due to metadata (EXIF) issue
<br>
We can solve this  by loading image and metadata separately and then save them into the save file using python

## Prerequisites
- Python 3
- piexif 1.1.3
- Pillow 8.3.1

## Usage
Run the command below to reconstruct images
```
python reconstruct_Image.py <source_directory> <output_directory> <worker>
```
  
folder structure should like this
```
.
+-- source_directory
|   +-- img_folder1
|       +-- img1
|       +-- img2
|   +-- img_folder2
|       +-- img1
|       +-- img2

```
  
worker is the number of processes run concurrently (default value is 4)
## Test Environment
- Ubuntu 21.04
