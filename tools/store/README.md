# Dossiers de publication Google Play + App Store

Chaîne commune aux applis BrainBoiled. Elle produit, pour une appli, un dossier `<Appli>/Google Play/` et `<Appli>/App Store/` prêt à saisir dans les consoles : textes de chaque langue, captures, icônes, bannière, réponses aux formulaires et marche à suivre.

**Règle : les captures sont de vrais rendus de l'appli**, pas des maquettes. Le code de l'appli est exécuté dans un test Flutter (`flutter test --update-goldens`) avec des données de démonstration réalistes, à la taille d'un iPhone 6,9 pouces (1290 × 2796) ; seul le cadre (titre, sous-titre, téléphone) est ajouté ensuite.

Déjà faits : **Diafra** (9 langues, iPhone + iPad), **Origins** (9 langues ; le contenu du jeu n'est traduit qu'en anglais), **MorseTree** (17 langues sur Google Play, 16 sur l'App Store qui n'a pas le bulgare), **RingWise** (fr, en, de) et **FlowDay** (9 langues ; captures sous `withClock`, voir son `tool/store_shots.sh`).

## Ce qu'il faut dans le dépôt de l'appli

| Fichier | Rôle |
|---|---|
| `tool/store_shots_test.dart` | Le test qui rend les écrans. Variables : `SHOT_LANG`, `OUT`, `SHOT_W`, `SHOT_H`, `SHOT_DPR`. Il charge les polices à la main (en test, Flutter n'a que des polices de substitution) ; pour le japonais, Noto CJK. Il doit aussi rendre l'écran d'achat (`8_paywall`) si l'appli a un achat intégré. Exemples : dépôts Diafra et Origins |
| `store/shots.json` | Couleurs de l'appli, polices du cadre, ordre des captures, titre et sous-titre de chaque capture dans chaque langue |
| `store/ios.json` | Réglages du projet iOS pour `ios_setup.py` (nom, identifiant, icône, iPhone seul, langues, textes d'autorisation traduits, clés en plus comme `GIDClientID`) |
| `store/kit.json` | Identifiants, adresses, catégories, achat intégré, chemins des visuels, notes pour la revue Apple, et pour chaque langue les textes Play (`title` 30, `short` 80, `full` 4000, `notes` 500) et Apple (`name` 30, `subtitle` 30, `promo` 170, `keywords` 100 sans espace après les virgules, `description` 4000, `whatsnew`, `iap_name` 30, `iap_desc` 45) |
| `store/play-reponses.md`, `store/apple-reponses.md` | Réponses aux formulaires (sécurité des données, classification, public cible, App Privacy, âge, chiffrement, achat intégré) |
| Politique de confidentialité fr + en | Publiée aussi sur le site : `python3 tools/legal/md2html.py <md> tools/legal/<appli>/privacy.<l>.html` puis `python3 tools/build.py` |

## Les commandes

```
# 0. Projet iOS (après « flutter create --platforms ios . » s'il manque) : Info.plist, InfoPlist.strings par langue, pbxproj, icônes
python3 tools/store/ios_setup.py <dépôt> <dépôt>/store/ios.json

# 1. Captures brutes (une langue à la fois ; ajouter SHOT_W=2064 SHOT_H=2752 SHOT_DPR=2 pour l'iPad)
flutter test tool/store_shots_test.dart --update-goldens --dart-define=SHOT_LANG=fr --dart-define=OUT=/tmp/gold/<appli>

# 2. Cadres : play/<l>/N.jpg 1080x1920, apple/<l>/N.png 1320x2868 (+ ipad/ 2064x2752)
python3 tools/store/compose.py <dépôt>/store/shots.json /tmp/gold/<appli> /tmp/visuels/<appli> [play,apple,ipad]
cp /tmp/gold/<appli>/en_8_paywall.png /tmp/visuels/<appli>/paywall_en.png

# 3. Dossier final (vérifie limites de caractères et tailles d'images)
python3 tools/store/build_kit.py <dépôt> /tmp/visuels/<appli> /tmp/kit/<Appli>
```

## Points à vérifier pour chaque appli

- **Langues** : ne proposer une langue de fiche que si l'appli est vraiment traduite dans cette langue (interface **et** contenu).
- **Identifiant** : `com.BrainBoiled.<Appli>` sur Android et iOS (FlowDay : le nouvel identifiant, pas `fr.flowday`).
- **iOS** : dossier `ios/` présent, `PRODUCT_BUNDLE_IDENTIFIER`, icône de l'appli dans `AppIcon.appiconset` (pas celle de Flutter), `ITSAppUsesNonExemptEncryption = NO`, `CFBundleLocalizations`, textes d'autorisation (`NS…UsageDescription`) pour chaque permission utilisée. iPhone seul (`TARGETED_DEVICE_FAMILY = 1`) si l'appli n'est pas pensée pour la tablette : pas de captures iPad à fournir.
- **Nom affiché** sous l'icône : le nom exact de l'appli.
- **Faits cités** dans les textes (nombre de leçons, d'éléments…) : vérifiés dans le code.

## Langues au-delà des 9 du site

- `kit.json` : chaque langue de fiche peut porter `"shots": "<code>"` (dossier des captures, ex. `nb` pour la fiche `no-NO`). Une langue sans bloc `apple` n'a pas de fiche App Store (le bulgare n'existe pas dans App Store Connect).
- `shots.json` : `"fonts_by_lang": {"ru": [titre, texte]}` pour une écriture absente de la police du cadre.
- Politiques : `tools/build.py` publie aussi les langues de `EXTRA_LANGS` (ru, el, bg, id, fi, ca, sv, da, nb) ; le bandeau du site reste alors en anglais.
- `tools/store/fonts/` : Nunito complet (latin + latin-ext) pour les cadres de FlowDay.

## Polices de test

En test, Flutter n'a aucune police de secours : une police doit être chargée ET désignée. Les emoji (FlowDay) passent par `fontFamilyFallback: ['Noto Color Emoji']`, activé seulement avec `--dart-define=STORE_SHOTS=true`.
