# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

from graph import draw_graph

if __name__ == "__main__":
    pass

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

                if k == n:                                                  # Protein is now finished, k == n
                    place monomer k at a

                    if E_k < E_min:                                         # New lowest energy configuration found
                        E_min = E_k

                        ¿Een datastructuur voor visualisatie opslaan hier?
                        (niet noodzakelijk dezelfde als in graph.py)

                if monomer k == P:                                              # next monomer is Polar
                    place monomer k at a
                    Call Searching(E_k, k+1)

                else:                                                           # next monomer is Hydrophobic

                    elif E_k <= U_k:                                            # New energy is lower than the lowest energy yet, very promising!
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
