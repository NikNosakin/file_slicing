import sys
import subprocess
import argparse
import os


def cut_file(path_to_file):
    """Функция для ''нарезки'' исходного файла по особому разделителю.
    Итогом ''нарезки'' является перемещение получившихся файлов в директорию archive_folder."""
    os.mkdir('archive_folder')
    handlers = {}
    count = 0
    names =[]
    with open(path_to_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '###' in line:
                count += 1
            new_file = f'words_{count}.txt'
            if new_file not in names:
                names.append(new_file)
            f = handlers.setdefault(new_file, open(new_file, 'w+'))
            f.write(f"{line}\n")
    for handler in handlers.values():
        handler.close()
    for name in names:
        os.replace(name, 'archive_folder/' + name)


def archive_compression(archive_name, a):
    """Функция для архивации и сжатия папки archive_folder, в которой лежат файлы, полученные в результате выполнения функции cut_file""" 
    if 'gzip' in a:
        command = f'tar zcvf {archive_name}.tar.gz archive_folder/'
        return command
    elif 'bz2' in a:
        command = f'tar jcvf {archive_name}.tar.bz2 archive_folder/'
        return command
    elif a == '0':
        command = f'tar cvf {archive_name}.tar archive_folder/'
        return command

def com(command):
        try:
            subprocess.run(path_to_file, shell=True)
            subprocess.run(command, shell=True)
        except subprocess.CalledProcessError as comm:
            sys.stderr.write(str(comm))
            
            
parser = argparse.ArgumentParser()
parser.add_argument('--path_to_file',
                    help='В аргументах указать абсолютный путь до файла, который надо "нарезать".',
                    type=str)
parser.add_argument('--archive_name',
                    help='В аргументах указать имя итогового архива, куда будут добавлены новые файлы.',
                    type=str)
parser.add_argument('-a',
                    help='В аргументах указать тип сжатия архива. Доступные аргументы для сжатия: gzip, bz2. Для создания архива без сжатия использовать аргумент "0".',
                    type=str)


args = parser.parse_args()
path_to_file = args.path_to_file
archive_name = args.archive_name
a = args.a


cut_file(path_to_file)
com(archive_compression(archive_name, a))
