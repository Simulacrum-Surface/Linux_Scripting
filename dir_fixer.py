#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""

Autor: Simulacrum


(probably) Upcoming options:


"""
import os, shutil, optparse

def args():
    parser = optparse.OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", help="Print progress to stdout.", action="store_true")
    (options, path) = parser.parse_args()
    return (options, path)


def main():
    options, path = args()
    if path == []:
        print("[-] No DIR specified.\nExiting...")
        exit(0)
    else:
        path = "".join((path[0], "/"))
        #TODO Check if path is existing
        if os.path.isdir(path) == False:
            print("[-] The given path does not lead to a directory.\nExiting...")
            exit(0)
        else:
            print("[+] Reading subDIRs from target DIR...")
            in_path, *no_usage = os.walk(path)
            if in_path[1] == []:
                print("[-] No subDIRs found.\nExiting...")
                exit(0)
            else:
                print("[+] {} subDIRs found. Starting the extraction...".format(len(in_path[1])))
                for folder in in_path[1]:
                    old_path_name = "".join((path, folder))
                    new_path_name = "".join((path, folder, "lol_i_hope_this_fileextension_is_random_enough/"))
                    if options.verbose == True:
                        print("[+] Renaming subDIR.")

                    os.rename(old_path_name, new_path_name)
                    in_new_path, *no_usage = os.walk(new_path_name)
                    try:
                        for file in in_new_path[2]:
                            file_path = "".join((new_path_name, file))
                            shutil.move(file_path, path)
                            if options.verbose == True:
                                print("moving {} -> {}".format(file, path))
                        shutil.rmtree(new_path_name)
                    except:
                        print("[-] An Error occured in directory {}\nSkipping this...".format(old_path_name))
                        os.rename(new_path_name, old_path_name)
    return
if __name__ == '__main__':
    main()
