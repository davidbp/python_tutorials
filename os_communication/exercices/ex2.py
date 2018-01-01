### DESCRIPTION
### Create an script that reads from the terminal a `source_path` and a `file_extension` (such as mp3). 
### Then the script searches all files with the given `file_extension` then writes them
### in a file with the size of the fize.

### Exercise
### Extend this script so that it works with multiple extensions (done in ex3.py)


import os       # for navigating the filesystem
import shutil   # for copying files
import csv      # for creating the table
import datetime # for creating datime

print('\nScript per a buscar arxius de una certa extensió i crear una taula amb els resultats.')

file_extension = input('\nIntrodueix extensió a considerar (mp3, mkv, mp4):\n')

source_path = input('\nIntroduir carpeta de entrada (on es busquen els fixers):\n')
unit_size   = input('\nIntroduir unitat de mesura (MB o GB):\n')

### Verify if the source and target folders exist, if not warn the user.
while not os.path.exists(source_path):
    source_path = input('\nLa carpeta de entrada no existeix, introdueix una nova:\n')

while not unit_size in ['MB', 'GB']:
    unit_size = input('\nLa unitat de mesura no és ni MB ni GB, introdueix una de les dues:\n')


print("\nBuscant fitxers ...")
print('\tHas introduit extensió: ', file_extension)
print('\tHas introduit carpeta de entrada: ', source_path)


### Print how many files have been found and will be copied

def find_files_with_provided_extension(file_extension, source_path, unit_size):
    files = []
    files_full_path = []
    file_sizes = []
    
    for dirpath, dirnames, filenames in os.walk(source_path):
        for f in filenames:
            if f.endswith(file_extension):
                fpath = os.path.join(dirpath, f)
                files.append(f)
                files_full_path.append(fpath)
    
                if unit_size == "MB":
                    file_sizes.append(os.stat(fpath).st_size*10**(-6)) 
                if unit_size == "GB":
                    file_sizes.append(os.stat(fpath).st_size*10**(-9)) 
    
    return files, files_full_path, file_sizes

files, files_full_path, file_sizes = find_files_with_provided_extension(file_extension, source_path, unit_size)

print("\nResultats")
print("\tS'han trobat ", len(files), " arxius,", len(set(files)), "arxius amb noms diferents." )
print('\tTots els arxius ocupen: {:.2f} {}'.format(sum(file_sizes), unit_size))


def make_csv_with_gathered_information(file_extension, files, files_full_path, file_sizes, unit_size):
    
    d = datetime.datetime.today()

    data = [['Nom', 'Carpeta', unit_size]]
    for i in range(len(files)):
        folder_path = os.path.split(files_full_path[i])[0]
        data.append([files[i], folder_path, file_sizes[i]])

    name_file = 'results_' + file_extension + '({0},{1},{2})'.format(d.day, d.month, d.year) +'.csv' 

    with open(name_file, 'w') as fp:
        a = csv.writer(fp)
        a.writerows(data)

    print('\tArxiu {} ha sigut creat.'.format(name_file))


make_csv_with_gathered_information(file_extension, files, files_full_path, file_sizes, unit_size)
print('')



