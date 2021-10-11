# numberDicomMontage
Unzips a Bruker Paravision 6 dicom archive, appends scan numbers to the dicom file names, and saves a montage of the dicom images for quick reference.

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
