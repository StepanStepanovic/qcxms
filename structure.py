#! /opt/ebsofts/Python/3.8.2-GCCcore-9.3.0/bin/python

import numpy as np
import os, shutil, sys
np.set_printoptions(suppress=True)

# Atomic mass dictionary (only integer Z supported, some missing)
mass = {0: 0, 1: 1.007825, 2: 4.002603, 3: 7.016005, 4: 9.012183, 5: 11.009305, 6: 12.0, 7: 14.003074, 8: 15.994915, 9: 18.998403, 10: 19.992439, 11: 22.98977, 12: 23.985045, 13: 26.981541, 14: 27.976928, 15: 30.973763, 16: 31.972072, 17: 34.968853, 18: 39.962383, 19: 38.963708, 20: 39.962591, 21: 44.955914, 22: 47.947947, 23: 50.943963, 24: 51.94051, 25: 54.938046, 26: 55.934939, 27: 58.933198, 28: 57.935347, 29: 62.929599, 30: 63.929145, 31: 68.925581, 32: 73.921179, 33: 74.921596, 34: 79.916521, 35: 78.918336, 36: 83.911506, 37: 84.9118, 38: 87.905625, 39: 88.905856, 40: 89.904708, 41: 92.906378, 42: 97.905405, 43: None, 44: 101.904348, 45: 102.905503, 46: 105.903475, 47: 106.905095, 48: 113.903361, 49: 114.903875, 50: 119.902199, 51: 120.903824, 52: 129.906229, 53: 126.904477, 54: 131.904148, 55: 132.905433, 56: 137.905236, 57: 138.906355, 58: 139.905442, 59: 140.907657, 60: 141.907731, 61: None, 62: 151.919741, 63: 152.921243, 64: 157.924111, 65: 158.92535, 66: 163.929183, 67: 164.930332, 68: 165.930305, 69: 168.934225, 70: 173.938873, 71: 174.940785, 72: 179.946561, 73: 180.948014, 74: 183.950953, 75: 186.955765, 76: 191.961487, 77: 192.962942, 78: 194.964785, 79: 196.96656, 80: 201.970632, 81: 204.97441, 82: 207.976641, 83: 208.980388, 84: None, 85: None, 86: None, 87: None, 88: None, 89: None, 90: 232.038054, 91: None, 92: 238.050786}

# Numpy array for vectorized mass lookups
np_M = np.array([mass.get(k, 0) for k in range(0, 93)])

def calc_mass(fragment_row):
    """
    Calculates the mass of a fragment from a res line.
    """
    atomic_nums = fragment_row[6::2].astype(int)
    counts = fragment_row[7::2]
    return np_M[atomic_nums] @ counts

def res_np(filename):
    """
    Parses the .res file, calculates spectrum, and optionally fetches fragment structures for specific m/z values.
    """
    with open(filename) as f:
        md_res = np.array([[float(j) for j in line.split()] for line in f])

    # Pad all fragment entries to same length (max number of atoms)
    max_atoms = int(np.max(md_res[:, 5]))
    padded = np.array([row + [0] * (2 * (max_atoms - int(row[5]))) for row in md_res])

    # Compute unique masses and assign fragments
    fragment_masses = np.apply_along_axis(calc_mass, 1, padded)
    unique_masses, inverse_indices = np.unique(fragment_masses, return_inverse=True)

    # Combine mass + intensity + index info
    for_nl = np.hstack((fragment_masses.reshape(-1, 1), padded[:, :5]))

    # Aggregate intensities by m/z
    summed_intensity = np.zeros_like(unique_masses)
    np.add.at(summed_intensity, inverse_indices, padded[:, 0])
    scaled_intensity = summed_intensity * 100 / np.max(summed_intensity)

    # Output spectrum
    spectrum = np.column_stack((unique_masses, scaled_intensity))

    # If m/z values are passed, copy relevant .xyz structures
    if len(sys.argv) > 1:
        try:
            peaks = [float(i) for i in sys.argv[1:]]
        except:
            print('Arguments provided after "structure" are not valid m/z numbers.')
            sys.exit(1)

        for peak in peaks:
            folder = f'{peak}'
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder)

            matches = for_nl[for_nl[:, 0] == peak]
            matches = matches[matches[:, 1] > 0.8][:, 2:].astype(int)

            for row in matches:
                frag_path = f'TMPQCXMS/TMP.{row[0]}/{".".join(map(str, row[1:]))}.xyz'
                out_path = f'{folder}/{row[0]}.{".".join(map(str, row[1:]))}.xyz'
                if os.path.exists(frag_path):
                    shutil.copy(frag_path, out_path)
                else:
                    print(f'Warning: Missing file {frag_path}')
    else:
        print("m/z     Intensity")
        for mz, intensity in spectrum:
            print(f"{mz:.1f}    {intensity:.2f}")

    return spectrum, padded


# Main execution
spectrum, all_fragments = res_np('qcxms_cid.res')
