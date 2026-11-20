# RingWise — charte graphique

RingWise compte les points des cartons de tir sportif à partir d'une photo et explique au tireur ce qui ne va pas : causes probables, correction du dioptre en clics, suivi par arme et par munition. Elle est éditée par **BrainBoiled**.

L'identité est celle du **pas de tir** : le noir et le crème du carton, l'orange de la mouche, la rigueur du règlement. Elle part de l'icône existante (cible avec trois tireurs et mouche orange) et du thème de l'appli (graine `#D9480F`).

## Le nom

- On écrit **RingWise** : R et W majuscules, en un mot. Toujours avec cette casse, y compris dans les visuels : pas de version tout en capitales.
- Titre sur le store : « RingWise – Score & Coach ».
- Éditeur : « une appli BrainBoiled ».
- Attention (voir `docs/play-store.md` du dépôt) : le nom commence par « Ring », marque très protégée en classe 9. Faire la recherche TMview/USPTO avant d'investir dans le logo définitif.

## Le logo et l'icône

- **Symbole** : un carton de tir (anneaux noirs et crème) avec la mouche orange au centre, et les silhouettes d'un tireur à la carabine, au pistolet et à l'arbalète.
- **Icône** : `app/assets/icon/icon.png` du dépôt RingWise (copie web : `assets/apps/ringwise-icon-192.png`).
- Recommandation : l'icône est très détaillée et se lit mal en 48 px. Garder la version actuelle pour le store et prévoir une **version simplifiée** (anneaux + mouche, sans silhouettes) pour le monochrome Android 13 et les petites tailles.
- **Logo avec le nom** : l'icône suivie de « RingWise » en Barlow Condensed Bold.

## Les couleurs

| Rôle | Jeton | Valeur |
|---|---|---|
| Couleur signature : mouche, boutons, titres des captures | `mouche` | `#FF6A2B` |
| Orange de l'interface (graine Material 3) | `orange-appli` | `#D9480F` |
| Fond de la marque, site | `charbon` | `#161A20` |
| Surfaces, cartes | `charbon-clair` | `#222830` |
| Bas des dégradés, anneaux noirs | `noir-carton` | `#0E1115` |
| Texte et anneaux clairs | `creme-carton` | `#F3F0E4` |
| Texte secondaire | `gris-cible` | `#B6B4AA` |
| Bon tir, progression | `vert-stand` | `#2B7A4B` |

Contraste : mouche sur charbon 6,1:1, crème 15,3:1.

## La typographie

- **Barlow Condensed** Bold (700) pour le nom, les titres et les **scores** (chiffres étroits, lisibles comme un tableau d'affichage).
- **IBM Plex Sans** pour le texte de l'appli (déjà utilisé dans le prototype).
- Sur le site, le texte courant est en Urbanist (voix commune BrainBoiled).

## Formes et espacements

- Cartes à coins arrondis 16 px ; les cibles sont toujours dessinées aux cotes officielles.
- Pas de dégradé dans l'interface : aplats nets, comme un carton.

## Le ton

- Celui d'un entraîneur : direct, factuel, sans jugement. « 5 clics vers T ».
- Les causes d'erreur sont toujours présentées comme des hypothèses.
- Vouvoiement dans la fiche du store et l'appli (public sportif adulte, fédéral).
- Ne jamais montrer d'arme pointée vers une personne ni de violence : RingWise parle de sport, de cibles et de matériel.

## Les visuels du store

- **Icône** 512 × 512.
- **Image de présentation** 1024 × 500 : dégradé horizontal `charbon-clair` → `noir-carton`, icône à gauche, « RingWise » en `mouche`, sous-titre « Score & Coach » en `mouche`.
- **Captures** 1080 × 1920 (6 par langue, FR, EN, DE) : titre en `mouche`, sous-titre en `creme-carton`, écran réel dans un téléphone coupé par le bas.

## L'éditeur

RingWise est éditée par BrainBoiled (identifiant `com.brainboiled.ringwise`). Mention « une appli BrainBoiled » sur le site et en fin de description du store ; jamais de logo BrainBoiled dans l'icône ni sur les captures.
