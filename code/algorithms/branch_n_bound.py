# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

import numpy as np

from datastructure import Protein, Acid
'''
09/04
ಠ_ಠ
TO DO:
    get matrix positions for possible_sites
    implement energy function
    ¬_¬
'''


def branch_n_bound(protein_string):
    global protein_str, length_total, prob_below_average, prob_above_average

    protein_str = protein_string
    length_total = len(protein_string)
    energy_current = 0
    energy_min_all = 0
    energy_min_partial = [0] * length_total
    average_list = [[] for i in range(length_total)]

    #set probabilities for pruning
    prob_below_average = 0.8
    prob_above_average = 0.5

    #create protein matrix
    protein = Protein(length_total)
    print(protein)


    #place first & second amino acid underneath [row, column]
    start_location = [length_total - 1, length_total - 1]
    protein.add_acid(protein_string[0], start_location, "connection")
    previous_location = start_location
    location = [previous_location[0] + 1, previous_location[1]]
    protein.add_acid(protein_string[1], location, "connection")
    previous_location = location

    print(protein)

    length_partial = 3
    amino_acid = protein_string[2]

    #call searching function
    searching(protein, amino_acid, energy_current, length_partial, energy_min_all, energy_min_partial, average_list, previous_location)

def searching(protein, amino_acid, energy_current, length_partial, energy_min_all, energy_min_partial, average_list, previous_location):

        #new_protein = deepcopy oldprotein
        #see possible_sites for monomer k (see whether matrix box left, up & right are empty, if so store adresses in list)

        locations = []
        location_bottom = [previous_location[0]+1 ,previous_location[1]]
        locations.append(location_bottom)
        location_top = [previous_location[0]-1 ,previous_location[1]]
        locations.append(location_top)
        location_right = [previous_location[0] ,previous_location[1]+1]
        locations.append(location_right)
        location_left = [previous_location[0] ,previous_location[1]-1]
        locations.append(location_left)

        possible_sites = []

        for loc in locations:
            #if loc == 0:
            possible_sites.append(loc)

        print(possible_sites)

        if possible_sites:

            #calculate energy of current partial protein for each site (when pseudo placing)
            for site in possible_sites:
                print(site)
                energy_current +=1

                #update list for average energy & calculate average
                average_list[length_partial - 1].append(energy_current)
                energy_average_partial = np.average(average_list[length_partial - 1])
                print(average_list, energy_average_partial)

                #place the monomer and update the energy

                #if it is the last monomer
                if length_partial == length_total:
                    protein.add_acid(amino_acid, site, "connection")
                    print(protein)

                    previous_location = site
                    length_partial +=1

                    #update lowest energy among all completed proteins
                    if energy_current < energy_min_all:
                        energy_min_all = energy_current
                    return

                #if it is a polar monomer
                elif amino_acid == "P":
                    protein.add_acid(amino_acid, site, "connection")
                    print(protein)

                    previous_location = site
                    length_partial +=1
                    amino_acid = protein_str[length_partial - 1]
                    searching(protein, amino_acid, energy_current, length_partial, energy_min_all, energy_min_partial, average_list, previous_location)

                #if it is a hydrophobic monomer
                else:

                    #if the curent energy is equal to or below the lowest energy of the partial protein
                    if energy_current <= energy_min_partial[length_partial - 1]:
                        energy_min_partial[length_partial - 1] = energy_current
                        print(energy_min_partial)
                        protein.add_acid(amino_acid, site, "connection")
                        print(protein)

                        previous_location = site
                        length_partial +=1
                        amino_acid = protein_str[length_partial - 1]
                        searching(protein, amino_acid, energy_current, length_partial, energy_min_all, energy_min_partial, average_list, previous_location)

                    #if the curent energy is equal to or below the average energy of all partial proteins
                    elif energy_current <= energy_average_partial:
                        r = np.random.random()

                        if r > prob_below_average:
                            protein.add_acid(amino_acid, site, "connection")
                            print(protein)

                            previous_location = site
                            length_partial +=1
                            amino_acid = protein_str[length_partial - 1]
                            searching(protein, amino_acid, energy_current, length_partial, energy_min_all, energy_min_partial, average_list, previous_location)

                    #if the curent energy is bigger than the average energy of all partial proteins
                    else:
                        r = np.random.random()
                        if r > prob_above_average:
                            protein.add_acid(amino_acid, site, "connection")
                            print(protein)

                            previous_location = site
                            length_partial +=1
                            amino_acid = protein_str[length_partial - 1]
                            searching(protein, amino_acid, energy_current, length_partial, energy_min_all, energy_min_partial, average_list, previous_location)



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
