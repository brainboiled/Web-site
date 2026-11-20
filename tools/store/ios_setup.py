"""Prépare le projet iOS d'une appli Flutter pour l'App Store.

Usage : python3 ios_setup.py <dépôt> <config.json>
config.json : {
  "display_name": "MorseTree",
  "bundle_id": "com.BrainBoiled.MorseTree",
  "icon": "play-store/icone-512.png",          # source carrée, la plus grande possible
  "iphone_only": true,                          # TARGETED_DEVICE_FAMILY = 1
  "portrait_only": true,
  "localizations": ["fr", "en", ...],           # CFBundleLocalizations (noms de dossiers .lproj)
  "development_region": "fr",
  "usage": {"NSMicrophoneUsageDescription": {"en": "...", "fr": "...", ...}},
  "extra_plist": {"UIBackgroundModes": ["audio"]}   # facultatif
}
Ce que fait le script :
- Info.plist : nom affiché, ITSAppUsesNonExemptEncryption = NO, CFBundleLocalizations,
  textes d'autorisation (texte anglais par défaut), orientations ;
- un fichier <langue>.lproj/InfoPlist.strings par langue avec les textes d'autorisation traduits,
  rattaché au projet Xcode (groupe de variantes « InfoPlist.strings », phase Resources) ;
- project.pbxproj : identifiant de lot, famille d'appareils, régions connues ;
- AppIcon.appiconset : l'icône de l'appli à toutes les tailles, sans transparence.
Relancer le script ne crée pas de doublons.
"""
import hashlib, json, os, plistlib, re, sys
from PIL import Image


def oid(seed):
    return hashlib.md5(seed.encode()).hexdigest()[:24].upper()


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def main(repo, cfg_path):
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    ios = os.path.join(repo, 'ios')
    assert os.path.isdir(ios), 'pas de dossier ios/ : lancer « flutter create --platforms ios . » d\'abord'

    # ---------- Info.plist ----------
    ip = os.path.join(ios, 'Runner', 'Info.plist')
    with open(ip, 'rb') as f:
        pl = plistlib.load(f)
    pl['CFBundleDisplayName'] = cfg['display_name']
    pl['CFBundleName'] = cfg['display_name']
    pl['ITSAppUsesNonExemptEncryption'] = False
    pl['CFBundleLocalizations'] = cfg['localizations']
    pl['CFBundleDevelopmentRegion'] = cfg.get('development_region', 'en')
    for key, texts in cfg.get('usage', {}).items():
        pl[key] = texts['en']
    for key, val in cfg.get('extra_plist', {}).items():
        pl[key] = val
    if cfg.get('portrait_only'):
        pl['UISupportedInterfaceOrientations'] = ['UIInterfaceOrientationPortrait']
    if cfg.get('iphone_only'):
        pl.pop('UISupportedInterfaceOrientations~ipad', None)
    with open(ip, 'wb') as f:
        plistlib.dump(pl, f)

    # ---------- InfoPlist.strings ----------
    usage = cfg.get('usage', {})
    langs = cfg['localizations'] if usage else []
    for l in langs:
        d = os.path.join(ios, 'Runner', f'{l}.lproj')
        os.makedirs(d, exist_ok=True)
        lines = ['/* Textes d\'autorisation affichés par iOS. */']
        lines += [f'"{k}" = "{esc(v.get(l) or v["en"])}";' for k, v in usage.items()]
        with open(os.path.join(d, 'InfoPlist.strings'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')

    # ---------- project.pbxproj ----------
    pp = os.path.join(ios, 'Runner.xcodeproj', 'project.pbxproj')
    s = open(pp, encoding='utf-8').read()
    bid = cfg['bundle_id']
    s = re.sub(r'PRODUCT_BUNDLE_IDENTIFIER = [^;]*RunnerTests;', f'PRODUCT_BUNDLE_IDENTIFIER = {bid}.RunnerTests;', s)
    s = re.sub(r'PRODUCT_BUNDLE_IDENTIFIER = (?![^;]*RunnerTests)[^;]*;', f'PRODUCT_BUNDLE_IDENTIFIER = {bid};', s)
    if cfg.get('iphone_only'):
        s = re.sub(r'TARGETED_DEVICE_FAMILY = "?[0-9,]+"?;', 'TARGETED_DEVICE_FAMILY = 1;', s)
    regions = ['Base'] + sorted(set(['en'] + cfg['localizations']))
    s = re.sub(r'knownRegions = \([^)]*\);',
               'knownRegions = (\n' + ''.join(f'\t\t\t\t{r if re.match(r"^[A-Za-z]+$", r) else chr(34) + r + chr(34)},\n' for r in regions) + '\t\t\t);', s)
    if langs:
        vg, bf = oid('InfoPlist.strings group'), oid('InfoPlist.strings build')
        if vg not in s:
            refs = {l: oid('InfoPlist.strings ' + l) for l in langs}
            lines = ''.join(
                f'\t\t{r} /* {l} */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.strings; name = {json.dumps(l)}; path = {json.dumps(l + ".lproj/InfoPlist.strings")}; sourceTree = "<group>"; }};\n'
                for l, r in refs.items())
            s = s.replace('/* End PBXFileReference section */', lines + '/* End PBXFileReference section */')
            s = s.replace('/* End PBXBuildFile section */',
                          f'\t\t{bf} /* InfoPlist.strings in Resources */ = {{isa = PBXBuildFile; fileRef = {vg} /* InfoPlist.strings */; }};\n/* End PBXBuildFile section */')
            kids = ''.join(f'\t\t\t\t{r} /* {l} */,\n' for l, r in refs.items())
            s = s.replace('/* End PBXVariantGroup section */',
                          f'\t\t{vg} /* InfoPlist.strings */ = {{\n\t\t\tisa = PBXVariantGroup;\n\t\t\tchildren = (\n{kids}\t\t\t);\n\t\t\tname = InfoPlist.strings;\n\t\t\tsourceTree = "<group>";\n\t\t}};\n/* End PBXVariantGroup section */')
            # groupe Runner et phase Resources de la cible Runner
            s = re.sub(r'(97C146F01CF9000F007C117D /\* Runner \*/ = \{\s*isa = PBXGroup;\s*children = \()',
                       r'\1' + f'\n\t\t\t\t{vg} /* InfoPlist.strings */,', s, count=1)
            s = re.sub(r'(97C146EC1CF9000F007C117D /\* Resources \*/ = \{\s*isa = PBXResourcesBuildPhase;\s*buildActionMask = \d+;\s*files = \()',
                       r'\1' + f'\n\t\t\t\t{bf} /* InfoPlist.strings in Resources */,', s, count=1)
    open(pp, 'w', encoding='utf-8').write(s)

    # ---------- icône ----------
    ad = os.path.join(ios, 'Runner', 'Assets.xcassets', 'AppIcon.appiconset')
    src = Image.open(os.path.join(repo, cfg['icon'])).convert('RGBA')
    bg = Image.new('RGBA', src.size, (0, 0, 0, 255))
    src = Image.alpha_composite(bg, src).convert('RGB')
    contents = json.load(open(os.path.join(ad, 'Contents.json')))
    for im in contents['images']:
        if 'filename' not in im:
            continue
        pt = float(im['size'].split('x')[0])
        px = round(pt * int(im['scale'][0]))
        src.resize((px, px), Image.LANCZOS).save(os.path.join(ad, im['filename']))
    print('ios ok :', repo)


if __name__ == '__main__':
    main(*sys.argv[1:3])
