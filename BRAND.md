# brainboiled — charte graphique

Charte de l'éditeur **brainboiled** et règles communes à ses applis (FlowDay, Diafra, Origins, MorseTree, RingWise).
Les chartes détaillées de chaque appli sont dans `charte/<appli>/` et suivent toutes le même plan, celui de la charte Diafra.

Source du logo : création Canva « Identité visuelle Brainboiled ». Les fichiers web en sont tirés (`assets/brand/`).

---

## 1. Le nom

- **brainboiled** : un seul mot, tout en minuscules dans le logo et sur le site. En début de phrase dans un texte courant, on peut écrire « Brainboiled ».
- « brain » + « boiled » : un cerveau en ébullition, qui bouillonne d'idées. Jamais « Brain Boiled » en deux mots, jamais « BB ».
- Domaines : **brainboiled.com** (site) et **brainboiled.app** (redirige vers le .com).
- Noms des applis, à écrire exactement ainsi, dans toutes les langues : **FlowDay**, **Diafra**, **Origins**, **MorseTree**, **RingWise**.
- Identifiants d'applis : `com.brainboiled.<appli>` pour toutes les nouvelles applis (FlowDay garde `fr.flowday`, MorseTree `fr.MorseTree` : un identifiant publié ne change plus).

## 2. La signature

Deux niveaux, comme sous le logo Canva :

| | Français | English |
|---|---|---|
| **Accroche** (grande) | L'esprit en ébullition | Minds on the boil |
| **Sous-titre** (petit) | Des applis pour apprendre, s'organiser et progresser. | Apps to learn, get organised and improve. |

L'accroche reprend le nom (*boiled* = en ébullition). Le sous-titre dit ce que font les cinq applis : apprendre (Diafra, Origins, MorseTree), s'organiser (FlowDay), progresser (RingWise).
Traductions des 9 langues dans `tools/i18n.py`. Dans l'accroche, le dernier mot est en dégradé.

Remplace l'ancienne signature « Innovation technologique — Applications grand public » : à mettre à jour aussi dans la création Canva et dans la charte Diafra (page « L'éditeur »).

## 3. Le logo

Un cerveau vu de dessus dont les deux hémisphères dessinent les lettres **b** et **b** reliées par un circuit, en dégradé cyan → violet, et le nom « brainboiled » : « brain » en blanc (bleu nuit sur fond clair), « boiled » en dégradé.

| Fichier (`assets/brand/`) | Usage |
|---|---|
| `brainboiled-logo-stacked-on-dark.svg` | Logo principal, symbole au-dessus du nom, sur fond sombre |
| `brainboiled-logo-stacked-on-light.svg` | Même chose sur fond clair (documents, factures) |
| `brainboiled-logo-horizontal-on-dark.svg` / `-on-light.svg` | Barre de site, pied de page, en-têtes |
| `brainboiled-symbol.svg` | Symbole seul : favicon, mentions « une appli brainboiled » |
| `…-mono-dark.svg` / `…-mono-white.svg` | Une couleur : gravure, tampon, fond photo chargé |
| `brainboiled-app-icon-512.png` | Icône carrée (page développeur Google Play, réseaux) |
| `og-brainboiled.jpg` | Image de partage 1200 × 630 |

Règles :
- Zone de protection : au moins la hauteur du « b » de « boiled » autour du logo.
- Taille minimale : 24 px de haut pour le logo horizontal, 16 px pour le symbole.
- Ne jamais recolorer le dégradé, l'inverser, ajouter ombre ou contour, déformer, ni séparer « brain » et « boiled ».
- Sur une photo, utiliser la version mono blanche.

## 4. Les couleurs

La marque est **toujours sombre** : un bleu nuit profond, jamais du noir pur, éclairé par le dégradé du cerveau.

| Rôle | Jeton CSS | Valeur |
|---|---|---|
| Fond le plus profond (pied de page, bas des dégradés) | `--bb-nuit-0` | `#020B21` |
| Fond de page | `--bb-nuit` | `#041431` |
| Surfaces (cartes) | `--bb-nuit-2` | `#0A1F47` |
| Surfaces au survol | `--bb-nuit-3` | `#13295B` |
| Dégradé — départ | `--bb-cyan` | `#00D4FF` |
| Dégradé — milieu | `--bb-bleu` | `#3D7BFF` |
| Dégradé — arrivée | `--bb-violet` | `#9B2CFF` |
| Violet pour du texte | `--bb-violet-clair` | `#B98CFF` |
| Texte | `--bb-blanc` | `#F4F6FB` |
| Texte secondaire | `--bb-gris` | `#A3AECB` |
| Encre sur fond clair | `--bb-encre` | `#051840` |

- Le dégradé va toujours de gauche (cyan) à droite (violet), en `linear-gradient(90deg, #00D4FF, #3D7BFF 50%, #9B2CFF)`.
- Il sert au logo, au dernier mot de l'accroche, aux filets de titres de section. Jamais en aplat de grande surface, jamais derrière du texte courant.
- `--bb-violet` (#9B2CFF) n'atteint pas 4,5:1 sur le bleu nuit : pour du texte, `--bb-violet-clair` ou `--bb-cyan`.
- Contrastes sur `--bb-nuit` : blanc 17:1, gris 8:1, cyan 10:1.

## 5. La typographie

- **Urbanist** : la police de la marque et la voix commune de tous les sites (texte courant de l'accueil **et** des mini-sites d'applis). C'est la police la plus proche du nom dessiné dans le logo (« a » à un étage, géométrique, arrondie).
  - ExtraBold 800 : accroches et grands titres. Bold 700 : titres de cartes. SemiBold 600 : boutons, étiquettes. Medium 500 : texte courant.
- Japonais : polices système (Hiragino Sans, Noto Sans JP, Yu Gothic), jamais d'Urbanist forcé.
- Les polices sont auto-hébergées dans `assets/fonts/` (aucun appel à Google Fonts : rien à déclarer au titre du RGPD).
- Petites capitales espacées (0,14 em) pour les titres de section : « NOS APPLIS ».

## 6. Formes et espacements

- Pas de base : 8 px. Marges de page 24 px, largeur utile 1080 px (760 px pour les pages de texte).
- Arrondis : 10 px (petits éléments), 16 px (cartes), 24 px (grandes cartes, panneaux), pilules pour les boutons et étiquettes, 22,5 % pour les icônes d'applis (carré arrondi Android).
- Pas d'ombres décoratives sur le texte. Une ombre douce seulement sous les icônes et au survol des cartes.
- Lueurs : deux halos très diffus en haut de page (violet à droite, cyan à gauche) rappellent le dégradé.

## 7. Le ton

- brainboiled (le studio) **vouvoie** et parle simplement : « Vos données restent à vous ».
- Chaque appli garde sa propre voix dans ses pages (Diafra tutoie, comme un ami photographe).
- Phrases courtes, sans superlatifs publicitaires ni emoji dans les textes de marque.
- On ne promet que ce que l'appli fait vraiment (pas de « n°1 », pas de « révolutionnaire »).

---

## 8. Le système des applis : comment rester harmonieux

Chaque appli a sa personnalité, mais toutes suivent les mêmes règles. C'est ce qui fait qu'elles se reconnaissent comme une famille sur l'accueil et sur la page développeur.

### Ce que chaque appli choisit
1. **Un fond sombre teinté** qui lui est propre (jamais noir pur, jamais blanc).
2. **Une couleur signature lumineuse**, et une seule, pour le nom, les boutons et les titres de captures.
3. **Une couleur secondaire** discrète.
4. **Une police de titre** qui porte son caractère (titres et nom seulement).
5. **Un symbole** unique et lisible en 48 px.

### Ce qui est commun à toutes
- **L'icône** : un seul symbole lumineux, centré, sur le fond sombre de l'appli (dégradé vertical léger), dans un carré plein (Android le découpe). Pas de texte dans l'icône.
- **Le texte courant** des sites : Urbanist (voir §5). Dans l'appli elle-même, chacune garde ses polices.
- **Le gabarit du mini-site** : même barre « une appli brainboiled » en haut, même pied de page brainboiled, mêmes composants (`assets/css/brainboiled.css`). Une appli ne change que ses jetons `[data-app="…"]`.
- **Les visuels du store** (même gabarit que Diafra) :
  - Image de présentation **1024 × 500** : icône à gauche, nom en couleur signature, sous-titre de la langue en couleur de texte, dégradé horizontal du fond de l'appli.
  - **6 captures 1080 × 1920 par langue** : titre court en couleur signature (une promesse), sous-titre clair, écran réel de l'appli dans un téléphone coupé par le bas. Jamais de maquette retouchée.
  - Icône **512 × 512** PNG.
- **La mention éditeur** : « une appli brainboiled » avec le symbole, dans le pied des pages, sur la page développeur et en fin de description longue du store (« Diafra est éditée par brainboiled. »). Le logo brainboiled n'apparaît **jamais** dans l'icône ni sur les captures : l'appli garde son identité.
- **Les pages obligatoires du Play Store**, toutes à la même adresse type :
  - `brainboiled.com/<appli>/` (présentation), `/<appli>/privacy/` (confidentialité), `/<appli>/terms/` (conditions), `/<appli>/delete-account/` (suppression des données), dans chaque langue de l'appli (`/<appli>/fr/privacy/`…).
- **La charte** : un dossier `charte/<appli>/` avec `README.md` (même plan : nom, logo, couleurs, typo, formes, ton, visuels du store, éditeur) et `tokens.json`.

### Les cinq applis

| Appli | Fond | Signature | Secondaire | Police de titre | Symbole |
|---|---|---|---|---|---|
| **FlowDay** | Bleu canard `#123F4E` | Soleil `#FFC438` | Turquoise clair `#7FD3E3` | Nunito ExtraBold | Le « f » qui part en flèche, point de départ jaune |
| **Diafra** | Brun profond `#16110A` | Or `#F0C454` | Jaune collimateur `#FFC400` | Roboto Bold | Diaphragme or à six lames |
| **Origins** | Nuit cosmique `#0B0E1C` | Or gravé `#D9B25F` | Lavande stellaire `#AEB8E6` | IM Fell English | Galaxie dorée dans un médaillon gravé |
| **MorseTree** | Graphite `#11151E` | Vert diode `#3DDC84` | Or antenne `#E6C56F` | Rajdhani Bold capitales | Antenne, trait rouge et point vert |
| **RingWise** | Charbon `#161A20` | Orange mouche `#FF6A2B` | Crème carton `#F3F0E4` | Barlow Condensed Bold capitales | Cible noire et crème, mouche orange |

Les deux ors (Diafra et Origins) restent distincts : l'or de Diafra est vif et chaud sur un brun, celui d'Origins est patiné, sur un bleu nuit, avec une police à l'ancienne.

### Ajouter une nouvelle appli
1. Choisir fond, signature, secondaire, police de titre en vérifiant que la signature ne ressemble à aucune autre du tableau (écart de teinte d'au moins 40°, ou bien fond et police très différents).
2. Vérifier les contrastes : signature et texte ≥ 4,5:1 sur le fond.
3. Créer `charte/<appli>/` en copiant le plan d'une charte existante.
4. Ajouter le bloc `[data-app="<appli>"]` dans `assets/css/brainboiled.css`, l'icône dans `assets/apps/`, l'entrée dans `tools/i18n.py`, puis `python3 tools/build.py`.
