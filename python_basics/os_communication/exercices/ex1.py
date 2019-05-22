### DESCRIPTION
### Create an script that reads from the terminal a `source_path` a `target_path` and a `file_extension`
### (such as mp3). Then the script copies all the files of the specified type 
### (from all folders and subfolders of the source path) to the target_path.  

import os      # for navigating the filesystem
import shutil  # for copying files


print('\nScript per a copiar dades de una certa extensió.')

file_extension = input('\nIntrodueix extensió a considerar (mp3, mkv, mp4):\n')
source_path = input('\nIntroduir carpeta de entrada (on es busquen els fixers):\n')
target_path = input('\nIntroduir carpeta de sortida (on es copien els fitxers):\n')


### Verify if the source and target folders exist, if not warn the user.
while not os.path.exists(source_path):
    source_path = input('\nLa carpeta de entrada no existeix, introdueix una nova:\n')

while not os.path.exists(target_path):
    target_path = input('\nLa carpeta de sortida no existeix, introdueix una nova:\n')

print("\nBuscant i copiant fitxers ...")
print('\tHas introduit extensió: ', file_extension)
print('\tHas introduit carpeta de entrada: ', source_path)
print('\tHas introduit carpeta de sortida: ', target_path)


### Print how many files have been found and will be copied

def find_files_with_provided_extension(file_extension, source_path):
    files = []
    files_full_path = []
    file_sizes_GB = []
    
    for dirpath, dirnames, filenames in os.walk(source_path):
        for f in filenames:
            if f.endswith(file_extension):
                fpath = os.path.join(dirpath, f)
                files.append(f)
                files_full_path.append(fpath)
                file_sizes_GB.append(os.stat(fpath).st_size*10**(-9)) 

    return files, files_full_path, file_sizes_GB

files, files_full_path, file_sizes_GB = find_files_with_provided_extension(file_extension, source_path)

print("\nResultats")
print("\tS'han trobat ", len(files), " arxius,", len(set(files)), "arxius amb noms diferents." )
print('\tTots els arxius ocupen: {:.2f} GB'.format(sum(file_sizes_GB)))


### Copy the files to the target_path
def copy_files_to_target_path(files_full_path, target_path):
    
    for f in files_full_path:
        fname = os.path.split(f)[1]
        new_path = os.path.join(target_path, fname)
        if os.path.exists(new_path):
            print("\tL'arxiu ", f, " ja existeix a la carpeta de sortida.")
    
    for f in files_full_path:
        fname = os.path.split(f)[1]
        new_path = os.path.join(target_path, fname)     
        if os.path.exists(new_path):
            pass
        else:
            shutil.copy2(f, new_path)
    print("\nTots els fitxers ja s'han copiat.")

copy_files_to_target_path(files_full_path, target_path)


