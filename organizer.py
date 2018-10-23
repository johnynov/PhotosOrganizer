import os, subprocess
from datetime import datetime

is_windows = ("yes" if os.name == "nt" else "no")
sign = str(("\\" if is_windows == "yes" else "/" ))
move_command = str(("move /Y" if is_windows == "yes" else "mv" ))
directory = str(input("What is directory where you want to organize your photos?: "))
if directory.endswith("\\") or directory.endswith("\/") or directory.endswith("\>"):
    directory = directory[:-1]
# print(os.listdir(directory))
only_photos = str(input("Organize only photos? - '.jpg' and '.png' [y/n]: "))
# place = (input("What is a place you were into?"))

months_dir = {"01": "Styczen", "02": "Luty", "03": "Marzec", "04": "Kwiecien", "05": "Maj", "06": "Czerwiec", "07": "Lipiec", "08": "Sierpien", "09": "Wrzesien", "10": "Pazdziernik", "11": "Listopad", "12":"Grudzien"}
print(months_dir.values())
print(months_dir.keys())

def prepeare_file(instring):
    if is_windows == "yes":
        return "\"" + instring + "\""
    else:
        return instring.replace(" ", "\\ ")

def list_files(directory):
    files_list = list(os.listdir(str(directory)))
    for i in files_list:
        i = i.encode("utf-8")
    return files_list

def read_date(file_x):
    creation_time = datetime.fromtimestamp(os.stat(file_x).st_mtime)
    return creation_time

try:
    files_list = list_files(directory)
except:
    print("You typed wrong directory.\n")

def check_if_year_exists(year):
    if year in os.listdir(directory):
        return True
    else:
        return False
def check_if_month_exists(month, year):
    for year_folder in os.listdir(directory):
        if os.path.isdir(year_folder):
            print("Yes it is a dir " + year_folder)
            if year_folder == year:
                print("Yes this year exists: " + year)
                print(month)
                print(os.listdir(directory+"/"+str(year_folder)))
                if month in os.listdir(directory+"/"+str(year_folder)):
                    print("Yes this month folder exists: " +month)
                    return True
                else:
                    return False
        else:
            return "not directory"

os.chdir(directory)

print(files_list)
print (is_windows)
print(check_if_month_exists(months_dir["06"], 2017))
for i in files_list:
    if not ((not (i.endswith(".png") or i.endswith(".jpg"))) and only_photos == "y"):
        if not os.path.isdir(i):
            datestamp = str(read_date(i))
            print(datestamp)
            year = datestamp.split(" ")[0].split("-")[0]
            month = datestamp.split(" ")[0].split("-")[1]
            if check_if_year_exists(year) == True:
                if check_if_month_exists(months_dir[month], year) == False:
                    os.chdir(year)
                    os.mkdir(months_dir[month])
                    os.chdir("..")
            else:
                os.makedirs(year+ sign + months_dir[month])
            if (directory + sign + i) != (directory + sign + year + sign + months_dir[month]):
                subprocess.Popen((move_command + " " + directory + sign + prepeare_file(i) + " " + directory + sign + year + sign + months_dir[month]),shell=True)
                print("Moving file: " + i  + "-> to " + directory + sign + year + sign + months_dir[month]+ sign + i)
