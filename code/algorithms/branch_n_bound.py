# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np
import copy

from datastructure import Protein, Acid
'''
09/04
ಠ_ಠ
TO DO:
    implement energy function
    ¬_¬
'''


def branch_n_bound(protein_string):
    global protein_str, length_total, prob_below_average, prob_above_average
    protein_str = protein_string
    length_total = len(protein_string)

    #create protein matrix
    protein = Protein(length_total)
    print(protein)

    energy_min_all = 0
    energy_min_partial = [0] * length_total
    average_list = [[] for i in range(length_total)]

    #set probabilities for pruning
    prob_below_average = 0.8
    prob_above_average = 0.5


    #place first & second amino acid underneath [row, column]
    start_location = [length_total - 1, length_total - 1]
    protein.add_acid(protein_string[0], start_location,"")
    previous_location = start_location
    location = [previous_location[0] + 1, previous_location[1]]
    protein.add_acid(protein_string[1], location, "")
    previous_location = location

    print(protein)

    amino_acid = protein_string[2]
    new_protein = copy.deepcopy(protein)

    #call searching function
    searching(new_protein, amino_acid, energy_min_all, energy_min_partial, average_list, previous_location)

def searching(protein, amino_acid, energy_min_all, energy_min_partial, average_list, previous_location):

        new_protein = copy.deepcopy(protein)
        print("length:",new_protein.length)

        #see possible_sites for monomer k (see whether matrix box left, up & right are empty, if so store adresses in list)

        location_bottom = [previous_location[0] + 1 ,previous_location[1]]
        location_top = [previous_location[0] - 1 ,previous_location[1]]
        location_right = [previous_location[0] ,previous_location[1] + 1]
        location_left = [previous_location[0] ,previous_location[1] - 1]

        locations = [location_bottom, location_top, location_right, location_left]

        possible_sites = []
        #print(locations)

        for loc in locations:
            #print(loc)
            #print(new_protein.acids[loc[0],loc[1]])
            print(loc[0])
            print(len(protein_str) *2 - 2)
            #if not at the borders of the matrix
            if 0 <= loc[0] <= (len(protein_str) *2 - 2) and 0 <= loc[1] <= (len(protein_str) *2 - 2):
                if new_protein.acids[loc[0],loc[1]] == 0:
                    print("ok")
                    possible_sites.append(loc)
            else:
                print("stop")

        print("possible sites are",possible_sites)

        if len(possible_sites) > 0:

            #calculate energy of current partial protein for each site (when pseudo placing)
            for site in possible_sites:
                print(site)

                #get neighbor locations
                neighbor_bottom = [previous_location[0] + 1 ,previous_location[1]]
                neighbor_top = [previous_location[0] - 1 ,previous_location[1]]
                neighbor_right = [previous_location[0] ,previous_location[1] + 1]
                neighbor_left = [previous_location[0] ,previous_location[1] - 1]

                neighbors = [neighbor_bottom, neighbor_top, neighbor_right, neighbor_left]

                print(neighbors)

                #only look at the acids that are not directly connected
                for neighbor in neighbors:
                    if neighbor != previous_location and 0 <= neighbor[0] <= (len(protein_str) *2 - 2) and 0 <= neighbor[1] <= (len(protein_str) *2 - 2):
                        print(new_protein.acids[neighbor[0],neighbor[1]])
                        if str(new_protein.acids[neighbor[0],neighbor[1]]) == 'H':
                            print('h-bond')
                            new_protein.energy -=1
                            print(new_protein.energy)

                #update list for average energy & calculate average
                average_list[new_protein.length - 1].append(new_protein.energy)
                energy_average_partial = np.average(average_list[new_protein.length - 1])
                #print(average_list, energy_average_partial)

                #place the monomer and update the energy

                #if it is the last monomer
                if new_protein.length == length_total:
                    new_protein.add_acid(amino_acid, site, "")
                    print("last",new_protein)

                    previous_location = site

                    #update lowest energy among all completed proteins
                    if new_protein.energy < energy_min_all:
                        energy_min_all = new_protein.energy
                    return

                #if it is a polar monomer
                elif amino_acid == "P":
                    new_protein.add_acid(amino_acid, site, "")
                    print("p",new_protein)

                    previous_location = site
                    amino_acid = protein_str[new_protein.length - 1]
                    searching(new_protein, amino_acid, energy_min_all, energy_min_partial, average_list, previous_location)

                #if it is a hydrophobic monomer
                else:

                    #if the curent energy is equal to or below the lowest energy of the partial protein
                    if new_protein.energy <= energy_min_partial[new_protein.length - 1]:
                        energy_min_partial[new_protein.length - 1] = new_protein.energy
                        #print(energy_min_partial)
                        new_protein.add_acid(amino_acid, site, "")
                        print("h",new_protein)

                        previous_location = site
                        amino_acid = protein_str[new_protein.length - 1]
                        searching(new_protein, amino_acid, energy_min_all, energy_min_partial, average_list, previous_location)

                    #if the curent energy is equal to or below the average energy of all partial proteins
                    elif new_protein.energy <= energy_average_partial:
                        r = np.random.random()

                        if r > prob_below_average:
                            new_protein.add_acid(amino_acid, site, "")
                            print("h",new_protein)

                            previous_location = site
                            amino_acid = protein_str[new_protein.length - 1]
                            searching(new_protein, amino_acid, energy_min_all, energy_min_partial, average_list, previous_location)

                    #if the curent energy is bigger than the average energy of all partial proteins
                    else:
                        r = np.random.random()
                        if r > prob_above_average:
                            new_protein.add_acid(amino_acid, site, "")
                            print("h",new_protein)

                            previous_location = site
                            amino_acid = protein_str[new_protein.length - 1]
                            searching(new_protein, amino_acid, energy_min_all, energy_min_partial, average_list, previous_location)

        else:
            print("no sites")

        print(energy_min_partial)


if __name__ == "__main__":
    branch_n_bound("HHPHHHPH")



'''
Pseudo-code Branch & Bound algorithm

--------------------------------------------------------------------------------

Mao Chen, Wen-Qi Huang,
A Branch and Bound Algorithm for the Protein Folding Problem in the HP Lattice Model,
Genomics, Proteomics & Bioinformatics,
Volume 3, Issue 4,
2005,
Pages 225-230

--------------------------------------------------------------------------------

Energy of the protein E = - Sum(i, n, 1) Sum(j, i-1, 1) (sigma_i sigma_j)
    where sigma = 1 if monomer is hydrophobic (H)

We want to know the lowest energy state and configuration
    => Minimalise E / Maximise unconnected H-H neighbors

Variables:
    k     : Length of the partial protein
    Mk    : Total possible sites (or nodes) at length k
    E_k   : Energy of the current partial protein of length k
    E_min : Lowest energy among all completed proteins (length k = n)
    U_k   : Lowest energy of partial protein of length k
    Z_k   : Average energy of all partial proteins of length k
    p_1   : Threshold value for pruning nodes where E_k > Z_k
    p_2   : Threshold value for pruning nodes where U_k < E_k <= Z_k


Initial values variables:
    k     : 3
    Mk    : not initialised
    E_k   : 0
    E_min : 0
    U_k   : 0
    Z_k   : 0
    p_1   : Predetermined constant (0.8)
    p_2   : Predetermined constant (0.5)

Pseudo-code:
    Place first two monomers                                                    # Position monomers k = 1 & 2 not important
    k_0 = 3

    Call the recursive function Searching(E_k, k)

    ------------------------

    Searching(E_k-1, k)

        Compute M_k

        if not M_k == 0:                                                        # Protein is not yet finished, k < n

            for each site a in M_k:

                Compute new E_k for monomer k at a

                if k == n:                                                      # Protein is now finished, k == n
                    place monomer k at a

                    if E_k < E_min:                                             # New lowest energy configuration found
                        E_min = E_k

                        ¿Een datastructuur voor visualisatie opslaan hier?
                        (niet noodzakelijk dezelfde als in graph.py)

                elif monomer k == P:                                            # next monomer is Polar
                    place monomer k at a
                    Call Searching(E_k, k+1)

                else:                                                           # next monomer is Hydrophobic

                    if E_k <= U_k:                                              # New energy is lower than the lowest energy yet, very promising!
                        place monomer k at a
                        Call Searching(E_k, k+1)

                    elif E_k <= Z_k:                                            # New energy is between the lowest and average energies, less promising
                        draw uniformly random number r in range [0,1]

                        if r > p_2:
                            place monomer k at a
                            Call Searching(E_k, k+1)

                    else:                                                       # New energy is higher than the average energie, not promising
                        draw uniformly random number r in range [0,1]

                        if r > p_1:
                            place monomer k at a
                            Call Searching(E_k, k+1)

--------------------------------------------------------------------------------

Stuff missing in pseudo-code: (Heb ik iets gemist?)
    Update U_k and Z_k
    ...


'''
