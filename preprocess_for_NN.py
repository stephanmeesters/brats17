import sys, os
import argparse

if len(sys.argv) < 6:
	print(str(len(sys.argv)-1)+" argument(s) received, expected 5")
	print("usage: preprocess_for_NN.py [output dir] [t1 image] [t1 ce image] [flair image] [t2 image]")
	sys.exit()

root_dir = sys.argv[1]
t1_path = sys.argv[2]
t1ce_path = sys.argv[3]
flair_path = sys.argv[4]
t2_path = sys.argv[5]

# create output dir
output_dir = os.path.join(root_dir)
try:
    os.mkdir(output_dir)
except:
    pass

# copy files
if os.path.isfile(t1_path):
    newpath = os.path.join(output_dir,"t1.nii.gz")
    os.system("cp " + t1_path + " " + newpath)
    t1_path = newpath
else:
    print("t1 file not found")
    sys.exit()

if os.path.isfile(t1ce_path):
    newpath = os.path.join(output_dir,"t1ce.nii.gz")
    os.system("cp " + t1ce_path + " " + os.path.join(output_dir,"t1ce.nii.gz"))
    t1ce_path = newpath
else:
    print("t1ce file not found")
    sys.exit()

if os.path.isfile(flair_path):
    newpath = os.path.join(output_dir,"flair.nii.gz")
    os.system("cp " + flair_path + " " + os.path.join(output_dir,"flair.nii.gz"))
    flair_path = newpath
else:
    print("flair file not found")
    sys.exit()

if os.path.isfile(t2_path):
    newpath = os.path.join(output_dir,"t2.nii.gz")
    os.system("cp " + t2_path + " " + os.path.join(output_dir,"t2.nii.gz"))
    t2_path = newpath
else:
    print("t2 file not found")
    sys.exit()

# if T2 is a 4D nifti (DWI images), pick first volume (b=0)
os.system("fslroi "+t2_path+" "+t2_path+" 0 1")

# unpack all
os.system("gunzip " + os.path.join(output_dir, "*"))

# turn into abspaths
t1_path = os.path.abspath(t1_path)[:-3];
t2_path = os.path.abspath(t2_path)[:-3];
t1ce_path = os.path.abspath(t1ce_path)[:-3];
flair_path = os.path.abspath(flair_path)[:-3];

# coreg all to T1
os.system("matlab -nodisplay -nosplash -nodesktop -r \"cd "+sys.path[0]+";coreg(\'"+t1_path+"\', \'"+t2_path+"\');quit;\"")
os.system("matlab -nodisplay -nosplash -nodesktop -r \"cd "+sys.path[0]+";coreg(\'"+t1_path+"\', \'"+t1ce_path+"\');quit;\"")
os.system("matlab -nodisplay -nosplash -nodesktop -r \"cd "+sys.path[0]+";coreg(\'"+t1_path+"\', \'"+flair_path+"\');quit;\"")

# brain extract T1
cwd = os.getcwd()
os.chdir(output_dir)
os.system("bet \""+os.path.basename(t1_path)+"\" \""+os.path.basename(t1_path)[:-4]+"m.nii\" -m -f 0.3 -R")
os.system("rm t1m.nii.gz")
os.system("mv t1m_mask.nii.gz mask.nii.gz")

# mask all
os.system("fslmaths "+os.path.basename(t1_path)+" -mul mask.nii.gz "+os.path.basename(t1_path)+" -odt short")
os.system("fslmaths "+os.path.basename(t2_path)+" -mul mask.nii.gz "+os.path.basename(t2_path)+" -odt short")
os.system("fslmaths "+os.path.basename(t1ce_path)+" -mul mask.nii.gz "+os.path.basename(t1ce_path)+" -odt short")
os.system("fslmaths "+os.path.basename(flair_path)+" -mul mask.nii.gz "+os.path.basename(flair_path)+" -odt short")

# remove all .nii
os.system("rm *.nii")

os.chdir(cwd)
