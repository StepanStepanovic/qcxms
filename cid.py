#! /usr/bin/python3
import os, shutil, sys

# Path to directory containing QCXMS executables and orca test.inp, it needs to be changed accordingly
d = '/home/users/s/stepanos/QCXMS/'

def mol_to_angs(name):
    """
    Extracts atomic coordinates from a .mol file and writes them to geo.angs
    in angstrom format expected by ORCA.
    """
    if 'geo.angs' not in os.listdir():
        with open(name) as f:
            data = [ [el for el in i.split()[:4]] for i in f if len(i.split()) > 15 ]
        with open('geo.angs', 'w') as f:
            for i, e in enumerate(data):
                f.write(f'{e[-1]}   ' + '  '.join(e[:-1]) + '\n')

def prepare_for_orca(name, E='60'):
    """
    Creates directory structure, copies .mol file, converts it to geo.angs,
    and prepares an ORCA input file for geometry optimization.
    """
    if E not in os.listdir(name):
        os.mkdir(name + '/' + E)
    shutil.copyfile(name + '.mol', name + '/' + E + '/' + name + '.mol')
    os.chdir(name + '/' + E)
    
    mol_to_angs(name + '.mol')
    
    if 'orca' not in os.listdir():
        os.mkdir('orca')
    shutil.copyfile(d + 'test.inp', 'orca/test.inp')
    shutil.move('geo.angs', 'orca/geo.angs')
    os.chdir('orca')
    
    with open('test.inp') as f: data = f.readlines()[:-1]
    with open('geo.angs') as f: angs = f.readlines()
    with open('test.inp', 'w') as f:
        print(*data, *angs, '*\n', file=f)

def coord(E):
    """
    Converts geo.angs to TURBOMOLE format (coord file), writes charge, 
    and updates qcxms.in with the correct energy.
    """
    with open('geo.angs') as f:
        data = [ [str((float(el)/0.529177)) if ind>0 else el.lower() 
                  for ind, el in enumerate(i.split())] for i in f if i.split() ]
    
    with open('coord', 'w') as f:
        f.write('$coord\n')
        for i, e in enumerate(data):
            f.write('  '.join(e[1:]) + f' {e[0]}\n')
        f.write('$end\n')
        f.write('$set\n')
        f.write('chrg  1\n')  # ?? Hardcoded charge!
        f.write('$end\n\n')
    
    with open('qcxms.in') as f: data = f.readlines()
    with open('qcxms.in', 'w') as f:
        for line in data:
            if 'elab' in line:
                line = f'elab {E} \n'
            print(line.rstrip(), file=f)

def after_orca(name, E=60):
    """
    Extracts optimized geometry from ORCA .xyz output, removes orca folder,
    prepares input for QCXMS, and submits the job.
    """
    with open('test.xyz') as f:
        data = f.readlines()[2:]  # Skip first two comment lines
    with open('../geo.angs', 'w') as f:
        print(*data, file=f)
    
    os.chdir('..')
    shutil.rmtree('orca')
    
    for fname in ['qcxms.in', 'submit']:
        shutil.copyfile(d + fname, os.getcwd() + '/' + fname)
    
    coord(E)
    os.system('sbatch submit')
    os.chdir('..')

# ---------- MAIN EXECUTION ----------
i = sys.argv[1:]

# Case 1: Range of energies (start, end, step)
if len(i) > 3:
    name, start, end, step = i
    if name not in os.listdir():
        os.mkdir(name)
    prepare_for_orca(name, 'priprema')
    os.system('orca test.inp > test.out') 
    os.chdir('../..')
    
    for energy in range(int(start), int(end) + int(step), int(step)):
        os.mkdir(f'{energy}')
        os.mkdir(f'{energy}/orca')
        shutil.copyfile('priprema/orca/test.xyz', f'{energy}/orca/test.xyz')
        os.chdir(f'{energy}/orca')
        after_orca(name, E=f'{energy}')
    os.chdir('..')

# Case 2: Single energy
elif len(i) > 1:
    name, E = i
    if name not in os.listdir():
        os.mkdir(name)
    prepare_for_orca(name, E)
    os.system('orca test.inp > test.out') 
    after_orca(name, E)
    os.chdir('..')

# Case 3: Default (E = 60)
else:
    if i[0] not in os.listdir():
        os.mkdir(i[0])
    prepare_for_orca(i[0])
    os.system('orca test.inp > test.out') 
    after_orca(i[0])
    os.chdir('..')
