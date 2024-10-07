import os
import shutil


def copy_static(source, target):
    if not os.path.exists(target):
        print("make directory :", target)
        os.mkdir(target)

    for file in os.listdir(source):
        spath = os.path.join(source, file)
        tpath = os.path.join(target, file)

        if os.path.isfile(spath):
            print(f"copying file from {spath} to {tpath}")
            shutil.copy(spath, tpath)
        else:
            copy_static(spath, tpath)


def main():

    source = "static"
    target = "public"

    if os.path.exists(target):
        shutil.rmtree(target)

    copy_static(source, target)


main()
