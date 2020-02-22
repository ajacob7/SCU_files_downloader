# SCU_files_downloader
    Navigates to the files section on camino and downloads all files into directories that match 
    the structure found online i.e. if a file is found in classA > notes > filename, it will be 
    saved in a path that ends in classA > notes > filename.


Notes:
  - May have extra imports than necessary, I recycled the base from another project initially, 
    but plan to omit any unneccessary lines soon

Bugs: 
 - There is one bug that I need to address still. If a professor listed a file as a name other 
   than what actually downloads from camino, then the program will get hung up because it will 
   wait for the file it is expecting. I can simply add a timeout, but sometimes downloading a 
   large file can take a long time and could invoke the timeout. 
