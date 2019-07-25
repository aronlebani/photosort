# photosort

## About
Photosort recursively searches its directory and all sub-directories and renames all jpeg files in the format xx-yy-zzzz-nnn. xx, yy, zzzz are the day, month, and year respectively that the photo was taken, and nnn is a number incrementing by one for each photo taken on the same day, in chronological order. Photosort then sorts files into folders labelled by year, in a folder named "Sorted Photos".

Any files that:
* Are not jpeg's
* Have no datetime data
* Are duplicates
Will be moved to a folder labelled "Unsorted Photos".

## Installation
1. Copy the file photsort.py to the root directory of the hardrive.
2. Run python-3.5.1.exe and follow the prompts to install Python 3.5. This is a software enviromnent which Photosort will run in. Make sure the box "Add Python to environment variables" is ticked.
3. Download and install the necessary Python Libraries. To do this, open the Windows Command Prompt, and type "pip install Pillow". Note that this is case sensitive. This requires an internet connection to download the files.
4. Make sure there is no folder labelled "Sorted Photos" or "Unsorted Photos" in the root directory of the hardrive. If there is, rename it to something else.

## Instructions for use

Simply double click on the file Photosort.py to run the program. A command prompt will pop up, giving details of the process. The sorted photos will be placed in a folder called "Sorted Photos". Any unsorted photos will be placed in a folder labelled "Unsorted Photos". Warning messages will be displayed if any problems occur. The meaning of each message is described below.

For sorting new photos in the future, copy any photos to be sorted into the root directory of the hardrive, and rerun the program.

It is highly unlikely that anything will go wrong, but just to be safe, it is recommended that a back up of the photos be made prior to running this program.

## Warning messages
File "filename" not processed as it is missing datetime exif data.

* The date and time that the photo was taken is not recorded in the photo's metadata. Therefore, the photo cannot be renamed and moved.

File "filename" not processed as it is not a jpeg file.

* Only jpeg files are sorted, so any files that are not jpegs will create a warning message

File "filename" not renamed as there is already another file with the same name.

* There is another file in the same folder as "filename" with the same name that "filename" is being renamed to.

File "filename" not moved as there is already a file with the same name in the destinatin folder.

* There is another file in the folder that "filename" is being moved to with the same name as "filename".

File "filename" not moved because the destination folder does not exist.

* The folder that "filename" is being moved to does not exist.