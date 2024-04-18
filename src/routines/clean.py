

import os, shutil
def pycache(directory):
    def delete_junk(f):
        try:
            shutil.rmtree(f)
        except:
            os.unlink(f)

    msk_dirs = os.listdir(directory)  

    for f in msk_dirs:
        if f.startswith('.') or f=='__pycache__' or f.endswith('txt'):
            junk_p = os.path.join(directory, f)
            print('deleted-->', junk_p)
            delete_junk(junk_p)
        else:
            if os.path.isdir(f):
                subfolder_p = os.path.join(directory, f)
                clean_all_from_junk(subfolder_p)
    return 'All cleaned!'

 
