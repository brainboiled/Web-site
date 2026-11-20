# MorseTree — charte graphique

MorseTree est un traducteur morse dont l'écran principal est une carte électronique animée : chaque point et chaque trait allume une diode et fait avancer dans l'arbre du morse. Quatre modes : Manipuler, Écrire, Écouter, Apprendre. Elle est éditée par **brainboiled**.

L'identité est celle d'un **circuit imprimé de radioamateur, la nuit** : graphite, pistes dorées, diodes rouges et vertes. Elle part de l'icône et de l'image de présentation existantes.

## Le nom

- On écrit **MorseTree** : un seul mot, M et T majuscules. Jamais « Morse Tree », « Morsetree » ni « MORSE TREE ». Toujours avec cette casse, y compris dans les visuels : pas de version tout en capitales. L'adresse web est `/morsetree/`.
- À mettre à jour : le nom affiché sous l'icône (`android:label="Morse Tree"`) et l'image de présentation, qui écrit encore « MORSE / TREE » sur deux lignes.
- Invariable dans toutes les langues.
- Éditeur : « une appli brainboiled ».

## Le logo et l'icône

- **Symbole** : une antenne en Y, reliée à gauche à un trait rouge (le tiret) et à droite à un point vert (le point), dans un cadre d'acier arrondi, sur graphite.
- **Icône** : `play-store/icone-512.png` du dépôt MorseTree (copie web : `assets/apps/morsetree-icon-192.png`).
- **Logo avec le nom** : antenne dorée + « MorseTree » en Rajdhani Bold, avec la ligne de tirets rouges et points verts.
- Le rouge est toujours le **trait**, le vert toujours le **point** : ne jamais les inverser.

## Les couleurs

| Rôle | Jeton | Valeur |
|---|---|---|
| Couleur signature : point, boutons, titres des captures | `diode-verte` | `#3DDC84` |
| Vert de la carte (diode éteinte, piste active) | `vert-carte` | `#0B9648` |
| Trait morse | `diode-rouge` | `#E5484D` |
| Pistes, antenne, accents | `or-antenne` | `#E6C56F` |
| Fond de la marque, site | `graphite` | `#11151E` |
| Surfaces, carte électronique | `graphite-clair` | `#1B2130` |
| Bas des dégradés | `graphite-nuit` | `#0A0D13` |
| Texte sur fond sombre | `blanc-ecran` | `#EDEFF2` |
| Texte secondaire, cadre | `acier` | `#A3ABB8` |

Contraste : diode-verte sur graphite 10,2:1, blanc 15,9:1.

## La typographie

- **Rajdhani** : Bold (700) pour le nom et les titres ; Medium pour les libellés de la carte.
- Sur le site, le texte courant est en Urbanist (voix commune brainboiled).
- Les alphabets non latins des cartes (cyrillique, grec, japonais) utilisent les polices Noto correspondantes.

## Formes et espacements

- Cartes à coins arrondis 16 px, filets fins comme des pistes de circuit.
- Une seule lueur à la fois : les diodes « brillent », le reste reste mat.
- Fond : grille fine très discrète (comme sur l'image de présentation).

## Le ton

- Simple et ludique, sans jargon radio non expliqué.
- Verbes d'action pour les modes : Manipuler, Écrire, Écouter, Apprendre.

## Les visuels du store

- **Icône** 512 × 512.
- **Image de présentation** 1024 × 500 : graphite avec grille, antenne dorée et ligne morse à gauche, « MorseTree » sur une ligne, la carte animée inclinée à droite. Modèle actuel, à garder en corrigeant le nom.
- **Captures** 1080 × 1920 : titre en `diode-verte`, sous-titre en `blanc-ecran`, écran réel dans un téléphone coupé par le bas.

## L'éditeur

MorseTree est éditée par brainboiled. Mention « une appli brainboiled » sur le site et en fin de description du store ; jamais de logo brainboiled dans l'icône ni sur les captures.

À faire : la politique de confidentialité est aujourd'hui prévue sur `easydore78.github.io/MorseTree-legal/`. Elle doit passer sur `brainboiled.com/morsetree/privacy/` avant la publication.
