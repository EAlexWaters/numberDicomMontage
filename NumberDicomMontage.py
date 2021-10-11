'''
Updated: 10/11/2021
Author: Alex Waters

This is a piece of utility code that unzips a Bruker Paravision 6 dicom archive,
appends scan numbers to the dicom file names, and saves a montage of the dicom images
for quick reference.

Input: Use file selection interface to choose a .tar.gz file containing Bruker 
       DICOM folders as exported from the scanner (PV6)

Output: 
    - Creates a directory 'tmpDICOM' into which the archive is unpacked
    - Inside the dicom folder for each scan, the scan number is appended to the dicom filenames
      (example: MRIm01.dcm becoms MRIm01__E5.dcm). This is useful when interleaving scans from 
      different acquisitions.
    - Creates a montage for each scan and saves it as a .png file. The montage is also displayed
      as a plot, which is useful when running this code inside Spyder or a similar tool with an 
      inline plot editor. Otherwise you may wish to comment it out.
      
Limitations: The tmpDICOM directory can already exist, but should be empty at
             the time of running the script. Unpacked files and newly created
             montages should be transferred to a different directory after 
             the script is run.

'''


import os, re, tarfile
import numpy as np
import imageio
from skimage.util import montage
from matplotlib import pyplot as plt
from tkinter.filedialog import askopenfilename



# Rewrite the splitext function to handle .tar.gz
def splitext(path):
    for ext in ['.tar.gz', '.tar.bz2']:
        if path.endswith(ext):
            return path[:-len(ext)], path[-len(ext):]
    return os.path.splitext(path)


# Get the filename and directory of the dicom archive
dcmArchive = askopenfilename(initialdir="E:/MRI_Data/2018/Sandbox",
                       filetypes =(("tarball", "*.tar.gz"),("All Files","*.*")),
                       title = "Choose a DICOM archive."
                       )

# Untar the dicom archive if it exists
try:
    print (dcmArchive)
    if tarfile.is_tarfile(dcmArchive):
        print("it is a tar file.")
    tfile=tarfile.open(dcmArchive,'r:gz')
    tfile.extractall(os.path.dirname(dcmArchive))
    tfile.close()
except:
    print("There was an error extracting the DICOM archive. The file might be corrupt or missing.")


orgDir=os.path.join(os.path.dirname(dcmArchive),'tmpDICOM')


scanNumRegex=re.compile(r'__E\d+')

allDcmFolders=os.listdir(orgDir)

for dcmFolder in allDcmFolders:
    scanNumSrch=scanNumRegex.search(dcmFolder)
    if scanNumSrch == None:
        scanNum=''
    else:
        scanNum=scanNumSrch.group(0)

    allDcmFiles=os.listdir(os.path.join(orgDir,dcmFolder))
    image_list=[]
    for dcmFile in allDcmFiles:
        if scanNumRegex.search(dcmFile) == None:
            base_name, fileext=splitext(dcmFile)
            oldPath = os.path.join(orgDir,dcmFolder,base_name+fileext)
            newPath = os.path.join(orgDir,dcmFolder,base_name+scanNum+fileext)
            os.rename(oldPath,newPath)
            # ds = pydicom.dcmread(newPath)
            # cur_image = ds.pixel_array
            # image_list.append(cur_image)
    # num_images = len(image_list)
    # image_size = np.shape(image_list[0])
    # image_array = np.array(image_list)
    
    vol = imageio.volread(os.path.join(orgDir,dcmFolder), 'DICOM')
    
    #this_montage = montage(image_array)
    
    if np.ndim(vol) == 2:
        this_montage = vol
    else:
        this_montage = montage(vol)
    this_montage = (this_montage/np.amax(this_montage))*255
    
    # Remove these lines if you are not using a tool that supports inline plotting
    plt.imshow(this_montage.squeeze(), interpolation='nearest')
    plt.show()
    
    
    montage_name = dcmFolder+'_montage.png'
    imageio.imwrite(os.path.join(orgDir,montage_name),this_montage.astype('uint8'))

