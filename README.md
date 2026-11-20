# brainboiled.com

Site de l'éditeur **BrainBoiled** : un accueil qui présente les applis, et un mini-site par appli avec les pages exigées par Google Play (présentation, confidentialité, conditions, suppression des données).

| Dossier | Contenu |
|---|---|
| `/` , `/fr/` … `/pl/` | Accueil en 9 langues (généré) |
| `flowday/` | Site FlowDay, repris de flowdayapp.com (9 langues, pages légales, vidéos) |
| `diafra/`, `origins/`, `morsetree/`, `ringwise/` | Pages d'attente (générées) en attendant leurs vraies pages |
| `assets/css/brainboiled.css` | La seule feuille de style ; un bloc `[data-app="…"]` par appli |
| `assets/brand/` | Logos BrainBoiled (exports de la création Canva, fond retiré) |
| `assets/apps/` | Icônes des applis |
| `assets/fonts/` | Polices auto-hébergées |
| `BRAND.md` | Charte BrainBoiled et règles communes aux applis |
| `charte/<appli>/` | Charte de chaque appli (`README.md` + `tokens.json`) |
| `tools/` | `i18n.py` (textes) et `build.py` (génération) |
| `tools/legal/<appli>/privacy.<langue>.html` | Texte des politiques de confidentialité ; génère `/<appli>/privacy/` (anglais) et `/<appli>/<langue>/privacy/`, avec un lien depuis la page de l'appli |

## Régénérer

```
python3 tools/build.py
```

Les pages de `flowday/` ne sont pas réécrites (sauf si on passe le chemin du dépôt flowday-legal en argument, pour refaire la migration).

## Mise en ligne (GitHub Pages)

1. Settings → Pages → Source : branche `main`, dossier `/ (root)`.
2. Domaine personnalisé : `brainboiled.com` (fichier `CNAME`), cocher « Enforce HTTPS ».
3. DNS de brainboiled.com : 4 enregistrements A vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` et un CNAME `www` vers `brainboiled.github.io`.
4. brainboiled.app : redirection 301 chez le registrar vers `https://brainboiled.com` (GitHub Pages n'accepte qu'un domaine par site).
