#
# photosort.py
#
# To Do:
#	* Fix bug when creating new directories
#	* Check if Thumbs bug is fixed
#
# For documentation, see README.md
#
# Aron Lebani
# 23 January 2017
#
# aron.lebani@gmail.com
#
# Copyright (c) 2017 by Aron Lebani
#

from PIL import Image
from PIL import ExifTags
from operator import attrgetter
import os
import sys
import shutil

class Photo :
	def __init__( self, file_name ) :
		# Constructor for class Photo
		# Initialises member variables using datetime EXIF data
		# Inputs: string file_name - absolute path to file
		self.path = os.path.dirname( file_name )
		self.newpath = None
		self.name = os.path.basename( file_name )
		self.newname = None
		self.tempname = None
		self._datetime_exists = False
		_datetime = self._get_datetime( file_name )
		self.year = _datetime[0:4]
		self.month = _datetime[5:7]
		self.day = _datetime[8:10]
		self.hour = _datetime[11:13]
		self.minute = _datetime[14:16]
		self.second = _datetime[17:19]
		self.number = None

	def _get_datetime( self, file_name ) :
		# Extract datetime from exif data and store in string
		# If exif data exists, member variable "exifexists" is set to True
		# Inputs: -
		# Outputs: list of strings datetime - unformated datetime data
		#		   if self is not an image, returns an empty string
		try :
			img = Image.open( file_name )	# Open file
			exif_data = img._getexif()	# Retrieve exif data
			decoded_exif_data = {}	# Initialise dictionary to store decoded exif data
			for tag, value in exif_data.items() :
				i = ExifTags.TAGS.get( tag, tag )
				decoded_exif_data[i] = value	# Relabel exif data by value in dictionary instead of hex number
			datetime = decoded_exif_data['DateTimeOriginal']	# Retrieve datetime value from exif data
			if not datetime == "" :
				self._datetime_exists = True	# Only set to True if datetime is not empty
			return datetime
		except (IOError, AttributeError, KeyError) :
			return ""

	def rename( self, newname, n=0, message=True ) :
		# Rename photo "self" from "name" to "newname"
		# Inputs: int n - current number of files renamed before function is called
		#		  string newname - a new name for the photo
		#		  bool message - Set to False if you don't want the error message to be printed
		# Outputs: int - updated numberr of files moved after the function is called
		#		   if n not specified, function will return 0
		try :
			os.rename(self.path + "\\" + self.name, self.path + "\\" + newname)	# Name changes, path remains constant
			self.name = newname	# Update name
			n += 1	# Another file renamed
		except FileExistsError :
			if message :
				print("Warning: File " + self.name + " in " + self.path + " not renamed as there is already another file with the same name.")
		return n

	def move( self, newpath, n=0 ) :
		# Move photo "self" from "path" to "newpath"
		# Inputs: int n - current number of files moved before function is called
		#		  string newpath - a new path for the photo
		# Outputs: int - updated number of files moved after the function is called
		#		   if n not specified, function will return 0

		if os.path.exists( newpath ) :	# Only move if destination path exists
			if not newpath == self.path :	# Do not move if already in destination folder
				try :
					shutil.move(self.path + "\\" + self.name, newpath + "\\" + self.name)	# Path changes, name remains constant
					self.path = newpath	# Update path
					n += 1	# Another file moved
				except shutil.Error :
					print("Warning: File " + self.name + " in " + self.path + " not moved as there is already a file with the same name in the destination folder.")
			else :
				n += 1	# Still counts as a move even though it has not moved anywhere
		else :
			print("Warning: File " + self.name + " in " + self.path + " not moved because the destination folder does not exist.")
		return n

	def exifexists( self ) :
		return self._datetime_exists

	def isjpeg( self ) :
		# Checks if self is a jpeg file
		# Inputs: -
		# Outputs: bool - true if self is a jpeg, else false
		return self.name[-3:].lower() == 'jpg'.lower() or self.name[-4:].lower() == 'jpeg'.lower()	# Check self extension (case insensitive)

	def isthisfile( self ) :
		# Checks if self is this Python file
		# Inputs: -
		# Outputs: bool - true if self is this file, else false
		this_file = "photosort-1.1.0.py"
		readme = "readme.txt"
		return self.name == this_file or self.name == readme

	def isthumbs( self ) :
		# Checks if self is a Thumbs.db file
		# Inputs: -
		# Outputs: bool - true if self is Thumbs.db, else false
		return self.name == "Thumbs.db"

print("Welcome to Photosort!")

print("Processing photos...")

# Create base directories
missing_exif_dir = "Missing EXIF Data"	# Directory to store photos with missing EXIF data
not_jpeg_dir = "Non JPEG Files"	# Directory to store non-jpeg files
if not os.path.exists(missing_exif_dir) :
	os.mkdir(missing_exif_dir)	# Create directory to store photos with missing EXIF data
if not os.path.exists(not_jpeg_dir) :
	os.mkdir(not_jpeg_dir)	# Create directory to store non-jpeg files

# Recursively scan through directories in . and store file names in a list
n_scanned = 0	# Stores number of files scanned
n_notjpg = 0	# Stores number of files found which are not jpegs
n_noexif = 0	# Stores number of files found with no EXIF data
photo_list = []	# Initialise list to store Photo instances
notjpg_list = []	# Initialise list to store non-jpeg Photo instances
noexif_list = []	# Initialise list to store Photo instances with no EXIF data
integer = 0
digits = 6	# Number of digits for temp names
for dirpaths, dirs, files in os.walk(".") :
	for file in files :
		photo = Photo(dirpaths + "\\" + file)	# Create instance of Photo for file
		if photo.isthumbs() :
			os.remove(dirpaths + "\\" + file)	# Check if file is a Thumbs.db and if so, skip the rest of the loop for this file
		elif not photo.isthisfile() :	# Do not sort yourself or your readme file, photosort!
			n_scanned += 1	# Another file scanned
			photo.tempname = str(integer).zfill(digits) + os.path.splitext(photo.name)[1]	# Give photos a temporary name
			integer += 1	# Increment integer
			photo.rename(photo.tempname, message=False)	# Rename photo to temp name
			if not photo.isjpeg() :
				n_notjpg += 1
				notjpg_list.append(photo)
				print("Warning: File " + photo.name + " in " + photo.path + " not processed as it is not a jpeg file.")
			elif not photo.exifexists() :
				n_noexif += 1
				noexif_list.append(photo)
				print("Warning: File " + photo.name + " in " + photo.path + " not processed as it is missing datetime exif data.")
			else :
				photo_list.append(photo)

# Sort files by yyyy:mm:dd:hh:mm:ss
sorted_photo_list = sorted( photo_list, key=attrgetter( 'year', 'month', 'day', 'hour', 'minute', 'second' ) )

print("Renaming photos...")

# Only rename "good" photos
n_renamed = 0	# Stores number of files renamed
index = 1
prev_photo = None	# Stores the previous file in the list
for photo in sorted_photo_list :
	if prev_photo is not None :
		if photo.day == prev_photo.day and photo.month == prev_photo.month and photo.year == prev_photo.year :
			index += 1
		else :
			index = 1
	photo.number = index
	prev_photo = photo
	photo.newname = photo.day + '-' + photo.month + '-' + photo.year + '-' + str(photo.number).zfill(3) + '.jpg'	# Get new photo name
	n_renamed = photo.rename( photo.newname, n=n_renamed )	# Rename file

print("Organising photos in folders...")

# Move "good" photos
n_moved = 0	# Stores number of files moved
for photo in sorted_photo_list :
	photo.newpath = photo.year + "\\" + photo.month + '-' + photo.year	# Get new directory name
	if not os.path.exists(photo.year) :
		os.mkdir(photo.year)	# Make new directory if not already exists
	if not os.path.exists(photo.newpath) :
		os.mkdir(photo.newpath)	# Make new directory if not already exists
	n_moved = photo.move( photo.newpath, n=n_moved )	# Move file

# Move non-jpeg photos
for photo in notjpg_list :
	photo.newpath = not_jpeg_dir	# Get new directory name
	photo.move( photo.newpath )	# Move file

# Move photos without EXIF data
for photo in noexif_list :
	photo.newpath = missing_exif_dir	# Get new directory name
	photo.move( photo.newpath )	# Move file

print("Tidying up...")

# Remove empty directories
for dirpaths, dirs, files in os.walk(".") :
	if not os.listdir( dirpaths ) :
		os.rmdir( dirpaths )	# Remove directory if empty

print("Photosort done!")

# Print summary
print( str(n_scanned) + " files scanned." )
print( str(n_notjpg) + " non jpeg files found.")
print( str(n_noexif) + " files found without EXIF data.")
print( str(n_renamed) + " files successfully renamed." )	# Photos that don't have datetime data wont be renamed
print( str(n_moved) + " files successfully moved.")	# Photos that don't have datetime data wont be moved

# Exit
print("Have a nice day.\n")
exit = input("Press enter to exit")