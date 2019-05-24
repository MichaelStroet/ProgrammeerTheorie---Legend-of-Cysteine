# Algoritmes

1. [Random Walk](#random-walk)
2. [Greedy (Look-ahead)](#greedy-look-ahead)
3. [Beam Search](#beam-search)
4. [Probability based Branch and Bound](#probability-based-branch-and-bound)
5. [Hill Climber](#hill-climber)


## **Random Walk**<a name="Randomwalk"></a>
![Random Walk](assets/README-0e88c2fc.png)

## **Greedy (Look-ahead)**<a name="Greedy"></a>

![Greedy Lookahead](assets/README-73a621af.png)

## **Beam Search**<a name="Beam"></a>

Beam Search is een algoritme dat per lengte alle mogelijke opties sorteert en doorgaat met de paar beste. Bij aanvang van het programma kiest de gebruiker de "Beam Width", dit is hoeveel verschillende eiwitten bijgehouden worden. Beam Search garandeert alleen de beste oplossing als de Beam width op oneindig gezet wordt. Dan gedraagt hij zich al een breadth-first algoritme en gaat zo de hele toestandsruimte af. Bij elke nieuwe lengte kijkt het algoitme naar de energie van elk eiwit die tot nu toe gevouwen is, dan plaatst hij de volgende aminozuur alleen bij die eiwitten en ordert dan weer alle mogelijke locaties van de volgende aminozuur bij deze eiwitten, dan maakt hij weer een selectie van de beste enzovoort.
Het programma runt net zo lang tot er geen aminozuren meer zijn om te plaatsen. Dan retourneert hij de proteine met de laagste energie, die bovenaan de lijst staat.
![Beam Search](assets/README-25a489a1.png)

## **Probability based Branch and Bound**<a name="BranchnBound"></a>

Branch and Bound is een paradigma dat gebaseerd is op het depth-first algorithme. Het is recursief en non-stack. Onze versie van Branch and Bound is "probability-based", omdat wij met een element van kans werken kunnen wij niet de beste oplossing garanderen. Deze methode zou wel sneller moeten zijn omdat er vaker gepruned wordt.
Als een aminozuur niet polair is wordt er gekeken naar de mogelijke volgende plaasting van het aminozuur, in 2D zijn er maximaal 3 mogelijke locaties, in 3D zijn er maximaal 5 mogelijke locaties. Het aminozuur wordt geplaatst en dan wordt de energie van het (partiele) eiwit berekend. Als deze lager is dan de minimale enrgie tot nu toe wordt de proteine opgeslagen. Dan wordt deze energie toegevoegd aan een dictionary zodat wij telkens de gemiddelde energie tot nu toe kunnen berekenen. Nu zijn er 3 opties:
1. De energie van deze proteine is lager is dan de minimale energie die tot nu toe gevonden is. Nu blijkt deze vouwing zeer belovend te zijn, en gaat het programma de volgende aminozuur plaatsen.
2. De energie van deze proteine is hoger dan de minimale energie maar alsnog lager dan de gemiddelde energie van de proteine die tot nu toe geplaatst is. Nu geeft het programma het aminozuur een kans om door te gaan. Een willekeurig cijfer tussen 0 en 1 wordt gegenereed en dit wordt vergeleken met de van te voren ingestelde kansen vor het prunen. Als het willekeurige getal lager of gelijk is aan deze kans  gaat het programma verder met plaatsen. Als het willekeurige getal groter is dan de kans, dan wordt dit aminozuur 'gepruned', het programma gaat dan een stap terug, naar de ouder en plaatst het volgende kind aminozuur.
3. De energie van deze proteine is hoger dan de gemiddelde energie van de proteine die tot nu toe geplaatst is. Nu geeft het programma het aminozuur ook een kans om door te gaan. Een willekeurig cijfer tussen 0 en 1 wordt gegenereed en dit wordt vergeleken met de van te voren ingestelde kansen vor het prunen. De kans zou wel kleiner moeten zijn dan bij de tweede optie omdat deze vouwing minder belovend is. Als het willekeurige getal lager of gelijk is aan deze kans  gaat het programma verder met plaatsen. Als het willekeurige getal groter is dan de kans, dan wordt dit aminozuur 'gepruned', het programma gaat dan een stap terug, naar de ouder en plaatst het volgende kind aminozuur.
Het programma runt net zo lang tot er geen aminozuren meer zijn om te plaatsen. Dan retourneert hij de opgeslagen proteine met de laagste energie.
![Branch n Bound](assets/README-886c390f.png)

## **Hill Climber**<a name="Hillclimber"></a>
