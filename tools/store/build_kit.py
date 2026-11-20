"""Assemble le dossier de publication d'une appli : Google Play et App Store.

Usage : python3 build_kit.py <dépôt de l'appli> <visuels> <sortie>
  <dépôt>/store/kit.json         : textes de toutes les langues et informations communes
  <dépôt>/store/play-reponses.md : réponses aux formulaires de la Play Console
  <dépôt>/store/apple-reponses.md: réponses aux formulaires d'App Store Connect
  <visuels>                      : sortie de compose.py (play/, apple/, ipad/) et paywall_<lang>.png
Le script vérifie les limites de caractères et la taille des images ; il s'arrête au moindre écart.
"""
import json, os, shutil, sys
from PIL import Image

PLAY_LIMITS = {'title': 30, 'short': 80, 'full': 4000, 'notes': 500}
APPLE_LIMITS = {'name': 30, 'subtitle': 30, 'promo': 170, 'keywords': 100, 'description': 4000,
                'whatsnew': 4000, 'iap_name': 30, 'iap_desc': 45}
APPLE_LOCALE = {'fr-FR': 'fr-FR', 'en-US': 'en-US', 'es-ES': 'es-ES', 'pt-BR': 'pt-BR', 'de-DE': 'de-DE',
                'it-IT': 'it', 'ja-JP': 'ja', 'pl-PL': 'pl', 'nl-NL': 'nl-NL'}
LANG_NAME = {'fr-FR': 'Français (France)', 'en-US': 'Anglais (États-Unis)', 'es-ES': 'Espagnol (Espagne)',
             'pt-BR': 'Portugais (Brésil)', 'de-DE': 'Allemand', 'it-IT': 'Italien', 'ja-JP': 'Japonais',
             'pl-PL': 'Polonais', 'nl-NL': 'Néerlandais'}


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text.strip() + '\n')


def check_image(path, size, alpha_ok=True):
    im = Image.open(path)
    assert im.size == tuple(size), (path, im.size, size)
    if not alpha_ok:
        assert im.mode == 'RGB', (path, im.mode)


def rgb_copy(src, dst, size=None):
    im = Image.open(src).convert('RGB')
    if size and im.size != size:
        im = im.resize(size, Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, optimize=True)


def main(repo, visuels, out):
    k = json.load(open(os.path.join(repo, 'store/kit.json'), encoding='utf-8'))
    a = k['assets']
    app = k['app']
    L = k['listing']
    errors = []
    for lc, v in L.items():
        for f, lim in PLAY_LIMITS.items():
            if len(v['play'][f]) > lim:
                errors.append(f'Play {lc} {f} : {len(v["play"][f])} > {lim}')
        for f, lim in APPLE_LIMITS.items():
            if f in v['apple'] and len(v['apple'][f]) > lim:
                errors.append(f'Apple {lc} {f} : {len(v["apple"][f])} > {lim}')
        kw = v['apple']['keywords']
        if ', ' in kw:
            errors.append(f'Apple {lc} mots-clés : pas d\'espace après les virgules')
    assert not errors, '\n'.join(errors)

    if os.path.exists(out):
        shutil.rmtree(out)
    gp, ap = os.path.join(out, 'Google Play'), os.path.join(out, 'App Store')
    n_shots = len(os.listdir(os.path.join(visuels, 'play', 'fr')))
    has_ipad = os.path.isdir(os.path.join(visuels, 'ipad'))

    # ---------- Google Play ----------
    c = os.path.join(gp, 'commun')
    rgb_copy(os.path.join(repo, a['icon512']), os.path.join(c, 'icone-512x512.png'), (512, 512))
    Image.open(os.path.join(c, 'icone-512x512.png')).convert('RGBA').save(os.path.join(c, 'icone-512x512.png'))
    rgb_copy(os.path.join(repo, a['feature']), os.path.join(c, 'image-presentation-1024x500.png'), (1024, 500))
    shutil.copy(os.path.join(repo, 'store/play-reponses.md'), os.path.join(c, 'reponses-formulaires.md'))
    for p in a.get('privacy', []):
        shutil.copy(os.path.join(repo, p), os.path.join(c, os.path.basename(p)))
    write(os.path.join(c, 'coordonnees-et-categorie.md'), f"""
# Paramètres du Store — {app}

| Champ | Valeur |
|---|---|
| Type | {k.get('play_type', 'Application')} |
| Catégorie | {k['play_category']} |
| Tags | {k.get('play_tags', 'à choisir dans la liste proposée (5 au plus)')} |
| Adresse e-mail | {k['email']} |
| Site web | {k['website']} |
| Numéro de téléphone | facultatif, laisser vide |
| Politique de confidentialité | {k['privacy_url']} |
| Prix | {k['price']} |
""")
    for lc, v in L.items():
        d = os.path.join(gp, lc)
        p = v['play']
        write(os.path.join(d, '1-titre.txt'), p['title'])
        write(os.path.join(d, '2-description-courte.txt'), p['short'])
        write(os.path.join(d, '3-description-complete.txt'), p['full'])
        write(os.path.join(d, '4-notes-de-version.txt'), p['notes'])
        lg = lc[:2]
        fp = os.path.join(repo, a['feature_lang'].format(lang=lg))
        rgb_copy(fp if os.path.exists(fp) else os.path.join(repo, a['feature']),
                 os.path.join(d, 'image-presentation-1024x500.png'), (1024, 500))
        sd = os.path.join(d, 'captures-telephone')
        os.makedirs(sd)
        for i in range(1, n_shots + 1):
            s = os.path.join(visuels, 'play', lg, f'{i}.jpg')
            check_image(s, (1080, 1920))
            shutil.copy(s, os.path.join(sd, f'{i}.jpg'))
    notes_all = '\n'.join(f'<{lc}>\n{v["play"]["notes"]}\n</{lc}>' for lc, v in L.items())
    write(os.path.join(gp, 'commun', 'notes-de-version-toutes-langues.txt'), notes_all)
    langs_list = ', '.join(f'`{lc}`' for lc in L)
    write(os.path.join(gp, '00-A-LIRE-Google-Play.md'), f"""
# {app} — publication sur Google Play

Identifiant de l'application (package) : `{k['package']}`. Éditeur : **{k['developer']}**.
Langue par défaut : {LANG_NAME[k['default_lang']]} (`{k['default_lang']}`). Autres langues : {langs_list}.

## Dans la Play Console, dans cet ordre

1. **Créer l'application** : nom « {L[k['default_lang']]['play']['title']} », langue par défaut {LANG_NAME[k['default_lang']]}, *Application*, *{('Gratuite' if 'ratuit' in k['price'] else 'Payante')}*. Coche les déclarations (règles du programme, lois d'exportation américaines).
2. **Contenu de l'application** (menu *Règles et programmes > Contenu de l'application*) : suivre `commun/reponses-formulaires.md` (politique de confidentialité, accès, annonces, classification, public cible, sécurité des données).
3. **Paramètres du Store** : `commun/coordonnees-et-categorie.md`.
4. **Fiche principale du Play Store** (langue par défaut, dossier `{k['default_lang']}/`) :
   - Nom : `1-titre.txt` (30 caractères max)
   - Description courte : `2-description-courte.txt` (80 max)
   - Description complète : `3-description-complete.txt` (4000 max)
   - Icône : `commun/icone-512x512.png`
   - Image de présentation : `image-presentation-1024x500.png` du dossier de la langue
   - Captures d'écran du téléphone : `captures-telephone/1.jpg` à `{n_shots}.jpg`, dans l'ordre
5. **Traductions** (même page, *Gérer les traductions > Ajouter vos propres traductions*) : coche toutes les langues de la liste ci-dessus, puis pour chacune colle ses trois textes et envoie ses visuels (*Éléments graphiques localisés*).
6. **Monétisation** : {('créer le produit intégré `' + k['iap']['id'] + '` (' + k['iap']['type'] + '), avec son prix.') if k.get('iap') else 'aucun produit intégré.'}
7. **Tests** : piste de test fermé, App Bundle signé : `{k['build_play']}` → `build/app/outputs/bundle/release/app-release.aab`. Les notes de version de toutes les langues, au format attendu par la console, sont dans `commun/notes-de-version-toutes-langues.txt` (à coller tel quel).
8. **Production** : un compte développeur personnel créé après le 13 novembre 2023 doit d'abord faire tourner un test fermé avec au moins 12 testeurs pendant 14 jours.

Les intitulés des menus de la Play Console changent de temps en temps : si un nom ne correspond pas, cherche la rubrique par son sujet.

Les captures sont des rendus réels de l'appli (code de l'appli exécuté avec des données de démonstration), régénérés par `tools/store/` du dépôt Web-site.
""")

    # ---------- App Store ----------
    c = os.path.join(ap, 'commun')
    rgb_copy(os.path.join(repo, a['icon1024']), os.path.join(c, 'icone-1024x1024.png'), (1024, 1024))
    check_image(os.path.join(c, 'icone-1024x1024.png'), (1024, 1024), alpha_ok=False)
    shutil.copy(os.path.join(repo, 'store/apple-reponses.md'), os.path.join(c, 'reponses-formulaires.md'))
    write(os.path.join(c, 'notes-revue.txt'), k['review_notes'])
    pw = os.path.join(visuels, 'paywall_en.png')
    if os.path.exists(pw):
        rgb_copy(pw, os.path.join(c, 'achat-capture-revue.png'))
    write(os.path.join(c, 'informations-generales.md'), f"""
# Informations générales — {app}

| Champ d'App Store Connect | Valeur |
|---|---|
| Nom (langue principale) | {L[k['default_lang']]['apple']['name']} |
| Langue principale | {LANG_NAME[k['default_lang']]} |
| Identifiant de lot (Bundle ID) | `{k['bundle_id']}` |
| SKU | `{k['bundle_id'].split('.')[-1].upper()}-001` (libre, jamais affiché) |
| Catégorie principale | {k['apple_category']} |
| Catégorie secondaire | {k.get('apple_category2', 'aucune')} |
| URL d'assistance | {k['support_url']} |
| URL marketing | {k['website']} |
| URL de la politique de confidentialité | {k['privacy_url']} |
| Copyright | {k['copyright']} |
| Prix | {k['price']} |
| Achat intégré | {(k['iap']['id'] + ' — ' + k['iap']['type']) if k.get('iap') else 'aucun'} |
""")
    for lc, v in L.items():
        d = os.path.join(ap, APPLE_LOCALE[lc])
        p = v['apple']
        write(os.path.join(d, '1-nom.txt'), p['name'])
        write(os.path.join(d, '2-sous-titre.txt'), p['subtitle'])
        write(os.path.join(d, '3-texte-promotionnel.txt'), p['promo'])
        write(os.path.join(d, '4-description.txt'), p['description'])
        write(os.path.join(d, '5-mots-cles.txt'), p['keywords'])
        write(os.path.join(d, '6-nouveautes.txt'), p['whatsnew'])
        if 'iap_name' in p:
            write(os.path.join(d, 'achat-nom.txt'), p['iap_name'])
            write(os.path.join(d, 'achat-description.txt'), p['iap_desc'])
        lg = lc[:2]
        sd = os.path.join(d, 'captures-iphone-6.9')
        os.makedirs(sd)
        for i in range(1, n_shots + 1):
            s = os.path.join(visuels, 'apple', lg, f'{i}.png')
            check_image(s, (1320, 2868))
            rgb_copy(s, os.path.join(sd, f'{i}.png'))
        if has_ipad:
            sd = os.path.join(d, 'captures-ipad-13')
            os.makedirs(sd)
            for i in range(1, n_shots + 1):
                s = os.path.join(visuels, 'ipad', lg, f'{i}.png')
                check_image(s, (2064, 2752))
                rgb_copy(s, os.path.join(sd, f'{i}.png'))
    loc_list = ', '.join(f'`{APPLE_LOCALE[lc]}`' for lc in L)
    ipad_line = ("   - iPad 13 pouces : `captures-ipad-13/1.png` à `" + str(n_shots) + ".png` (2064 × 2752)\n") if has_ipad else ''
    write(os.path.join(ap, '00-A-LIRE-App-Store.md'), f"""
# {app} — publication sur l'App Store

Identifiant de lot (Bundle ID) : `{k['bundle_id']}`. Éditeur : **{k['developer']}**.
Langue principale : {LANG_NAME[k['default_lang']]}. Localisations : {loc_list}.

## Avant App Store Connect

1. **Compte Apple Developer** (99 USD par an) au nom sous lequel l'appli doit apparaître.
2. **Identifiant** : dans *Certificates, Identifiers & Profiles > Identifiers*, créer l'App ID `{k['bundle_id']}`{' avec la capacité *In-App Purchase*' if k.get('iap') else ''}.
3. **Compilation** : sur un Mac avec Xcode, `{k['build_apple']}`, puis envoyer `build/ios/ipa/*.ipa` avec l'appli *Transporter* (ou ouvrir `ios/Runner.xcworkspace` dans Xcode : *Product > Archive > Distribute App*). Signature : *Automatically manage signing* avec ton équipe.

## Dans App Store Connect, dans cet ordre

1. **Mes apps > + > Nouvelle app** : plateforme iOS, nom, langue principale, Bundle ID, SKU : voir `commun/informations-generales.md`.
2. **Informations sur l'app** : catégories, URL de confidentialité, copyright, droits sur le contenu (`commun/informations-generales.md`).
3. **Confidentialité de l'app** : `commun/reponses-formulaires.md`.
4. **Prix et disponibilité** : {k['price']}.
{'5. **Achats intégrés** : créer `' + k['iap']['id'] + '` (' + k['iap']['type'] + '), nom et description de chaque langue dans `achat-nom.txt` et `achat-description.txt`, capture de revue `commun/achat-capture-revue.png`.' if k.get('iap') else '5. **Achats intégrés** : aucun.'}
6. **Page de version 1.0**, pour chaque langue (menu des langues en haut à droite), avec le dossier de la langue :
   - Texte promotionnel : `3-texte-promotionnel.txt` (170 max, modifiable sans nouvelle version)
   - Description : `4-description.txt`
   - Mots-clés : `5-mots-cles.txt` (100 max, virgules sans espace)
   - Nom et sous-titre : `1-nom.txt`, `2-sous-titre.txt` (30 max chacun ; ils sont dans *Informations sur l'app*)
   - Nouveautés : `6-nouveautes.txt` (le champ n'apparaît qu'à partir de la 2e version)
   - Captures iPhone 6,9 pouces : `captures-iphone-6.9/1.png` à `{n_shots}.png` (1320 × 2868) ; Apple les réduit pour les autres tailles d'iPhone
{ipad_line}   - URL d'assistance et URL marketing : `commun/informations-generales.md`
7. **Build** : choisir la compilation envoyée, répondre à la question sur le chiffrement (`commun/reponses-formulaires.md`).
8. **Classification par âge** et **informations pour la revue** : `commun/reponses-formulaires.md`, notes à coller : `commun/notes-revue.txt`.
9. **Soumettre pour vérification.**

Les captures sont des rendus réels de l'appli (code de l'appli exécuté avec des données de démonstration), régénérés par `tools/store/` du dépôt Web-site.
""")
    print('kit ok :', out)


if __name__ == '__main__':
    main(*sys.argv[1:4])
