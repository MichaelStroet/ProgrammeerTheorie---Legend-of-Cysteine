# Programmeer Theorie - Legend of Cysteine

UvA minor programmeren 2019 - ProgrammeerTheorie / Heuristiek
periode 5

### Auteurs

- Ruby Bron       12474223

- Sophie Stiekema 10992499

- Michael Stroet  11293284

## Aan de slag

### Vereisten
Deze codebase is volledig geschreven in Python3.6.3 In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

`pip install -r requirements.txt`

(I HAVE COPIED THIS FROM EXAMPLE WEBSITE )

### Structuur
Alle Python scripts staan in de folder Code. In de map Data zitten alle input waardes en in de map Results worden alle resultaten opgeslagen door de code.

### Test
Om de code te draaien gebruik de instructie:

`python3 main.py`

Dan kan de gebruiker de volgende keuze maken:
- Resultaten opslaan of niet
- Resulaten printen of niet
- Een dimensie
- Een algoritme
- Een eiwit
- Een matrix grootte

Per algoritme kunnen er nog meer keuzes gemaakt worden:
- De hoeveelheid iteraties (voor Random Walk, Greedy en Greedy Look-ahead)
- De Beam width (voor Beam Search)
- De kansen voor het prunen van eiwitten met een energie onder het minimum (Branch and Bound)


## Protein Pow(d)er
Eiwitten zijn strengen van aminozuren. Deze kunnen op allerlei manieren gevouwen zijn. Als een eiwit in het lichaam niet goed gevouwen is kan dit tot ziektes leiden zoals kanker, Diabetes, Parkinsons en Alzheimer. Door de optimale vouwing van een eiwit te bepalen kunnen wetenschappers efficientere medicijnen creëren.  

In dit experiment proberen wij een eiwit zo stabiel mogelijk te vouwen. Dit gebeurt als de hydrofobe of Cysteine aminozuren tegen over elkaar geplaatst zijn. Twee Cysteine eiwitten verlagen de energie met - 5, een Cysteine en een hydrofobe of twee hydrofoben aminozuuren verlagen de energie met -1. Polaire aminozuren hebben geen invloed op de stabiliteit.

## Algoritmes

Wij hebben 6 verschillende algoritmes geimplementeerd:
- Random Walk
- Greedy
- Greedy met look-ahead
- Beam Search
- Branch and Bound
- Hill Climber

Voor meer informatie zie: [code/algorithms/README.md](https://github.com/MichaelStroet/ProgrammeerTheorie---Legend-of-Cysteine/blob/master/code/algorithms/README.md)


## Dankwoord


## References

Engstler, J., & Giovambattista, N. (2018). Comparative Study of the Effects of Temperature and Pressure on the Water-Mediated Interactions between Apolar Nanoscale Solutes. The Journal of Physical Chemistry B, 123(5), 1116-1128.

Chen, M. & Huang, W. (2005). A Branch and Bound Algorithm for the Protein Folding Problem in the HP Lattice Model. Genomics, Proteomics & Bioinformatics, 3(4), 225-230.

Selkoe, D. J. (2003). Folding proteins in fatal ways. Nature, 426(6968), 900.

Zhang, Jinfeng, Samuel C. Kou, and Jun S. Liu. (2007). Biopolymer structure simulation and optimization via fragment regrowth Monte Carlo. Journal of Chemical Physics 126(22): 225101.
