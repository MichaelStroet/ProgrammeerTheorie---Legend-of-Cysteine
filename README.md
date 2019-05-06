# ProgrammeerTheorie - Legend of Cysteine

UvA minor programmeren 2019 - ProgrammeerTheorie / Heuristiek
periode 5


Ruby Bron       12474223

Sophie Stiekema 10992499

Michael Stroet  11293284


# Meer uitleg over eiwitten, algoritmen, requirements.txt, bounds, etc.


# Protein Pow(d)er
Eiwitten zijn strengen van aminozuren. Deze kunnen op allerlei manieren gevouwen zijn. Als een eiwit in het lichaam niet goed gevouwen is kan dit tot ziektes leiden zoals kanker, Diabetes, Parkinsons en Alzheimer. Door de optimale vouwing van een eiwit te bepalen kunnen wetenschappers efficientere medicijnen creëren.  

In dit experiment proberen wij een eiwit zo stabiel mogelijk te vouwen. Dit gebeurt als de hydrofobe of Cysteine aminozuren tegen over elkaar geplaatst zijn. Polaire aminozuren hebben geen invloed op stabiliteit.

Engstler, J., & Giovambattista, N. (2018). Comparative Study of the Effects of Temperature and Pressure on the Water-Mediated Interactions between Apolar Nanoscale Solutes. The Journal of Physical Chemistry B, 123(5), 1116-1128.

Selkoe, D. J. (2003). Folding proteins in fatal ways. Nature, 426(6968), 900.

# Branch 'n Bound
Branch 'n Bound is een paradigma dat gebaseerd is op het depth-first algorithme. Het is recursief en non-stack. Onze versie van Branch 'n Bound is "probability-based", omdat wij met een element van kans werken kunnen wij niet de beste oplossing garanderen. Deze methode zou wel sneller moeten zijn omdat er vaker gepruned wordt.
Als een aminozuur niet polair is wordt er gekeken naar de mogelijke volgende plaasting van het aminozuur, in 2D zijn er maximaal 3 mogelijke locaties, in 3D zijn er maximaal 5 mogelijke locaties. Het aminozuur wordt geplaatst en dan wordt de energie van het (partiele) eiwit berekend. Als deze lager is dan de minimale enrgie tot nu toe wordt de proteine opgeslagen. Dan wordt deze energie toegevoegd aan een dictionary zodat wij telkens de gemiddelde energie tot nu toe kunnen berekenen. Nu zijn er 3 opties:
1. De energie van deze proteine is lager is dan de minimale energie die tot nu toe gevonden is. Nu blijkt deze vouwing zeer belovend te zijn, en gaat het programma de volgende aminozuur plaatsen.
2. De energie van deze proteine is hoger dan de minimale energie maar alsnog lager dan de gemiddelde energie van de proteine die tot nu toe geplaatst is. Nu geeft het programma het aminozuur een kans om door te gaan. Een willekeurig cijfer tussen 0 en 1 wordt gegenereed en dit wordt vergeleken met de van te voren ingestelde kansen vor het prunen. Als het willekeurige getal lager of gelijk is aan deze kans  gaat het programma verder met plaatsen. Als het willekeurige getal groter is dan de kans, dan wordt dit aminozuur 'gepruned', het programma gaat dan een stap terug, naar de ouder en plaatst het volgende kind aminozuur.
3. De energie van deze proteine is hoger dan de gemiddelde energie van de proteine die tot nu toe geplaatst is. Nu geeft het programma het aminozuur ook een kans om door te gaan. Een willekeurig cijfer tussen 0 en 1 wordt gegenereed en dit wordt vergeleken met de van te voren ingestelde kansen vor het prunen. De kans zou wel kleiner moeten zijn dan bij de tweede optie omdat deze vouwing minder belovend is. Als het willekeurige getal lager of gelijk is aan deze kans  gaat het programma verder met plaatsen. Als het willekeurige getal groter is dan de kans, dan wordt dit aminozuur 'gepruned', het programma gaat dan een stap terug, naar de ouder en plaatst het volgende kind aminozuur.
Het programma runt net zo lang tot er geen aminozuren meer zijn om te plaatsen. Dan returnt hij de opgeslagen proteine met de laagste energie.
