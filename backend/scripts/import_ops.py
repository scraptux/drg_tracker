from ops.models import Version, Kapitel, Gruppen, Dreisteller, Kodes
from ops.models import Exclusion, Inclusion, Note, Preferred, PreferredLong
from ops.models import Umsteiger

import csv, subprocess, os, re, progressbar
import xml.etree.ElementTree as ET


def run(*script_args):
    year = script_args[0]
    
    if Version.objects.filter(Year=year).exists():
        Version.objects.get(Year=year).delete()

    if not os.path.exists("data/"+year):
        return
    
    print("Starte Import für", year)
    y = Version(Year=year)
    y.save()
    
    print("Importiere Meta-Daten (ausgenommen Codes)")
    bar = progressbar.ProgressBar(maxval=3).start()

    # Kapitel
    imports = []
    with open("data/"+year+"/ops"+year+"syst_kapitel.txt", 'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(Kapitel(KapNr=row[0], KapTi=row[1], Year=y))
    Kapitel.objects.bulk_create(imports)
    bar.update(1)

    # Gruppen
    imports = []
    with open("data/"+year+"/ops"+year+"syst_gruppen.txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(Gruppen(KapNr=Kapitel.objects.get(KapNr=row[0], Year=y), GrVon=row[1], GrBis=row[2], GrTi=row[3], Year=y))
    Gruppen.objects.bulk_create(imports)
    bar.update(2)

    # Dreisteller
    imports = []
    with open("data/"+year+"/ops"+year+"syst_dreisteller.txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(Dreisteller(KapNr=Kapitel.objects.get(KapNr=row[0], Year=y), GrVon=Gruppen.objects.get(GrVon=row[1], Year=y),
            DCode=row[2], DTi=row[3], Year=y))
    Dreisteller.objects.bulk_create(imports)
    bar.update(3)
    print()


    # Codes
    print("Importiere Code Meta-Daten")
    with open("data/"+year+"/ops"+year+"syst_kodes.txt", 'r') as file:
        line_count = len(file.readlines())
    bar = progressbar.ProgressBar(maxval=line_count).start()
    imports = []
    with open("data/"+year+"/ops"+year+"syst_kodes.txt") as file:
        reader = csv.reader(file, delimiter=";")
        row_current = 0
        for row in reader:
            row_current += 1
            bar.update(row_current)
            if int(year) <= 2008:
                imports.append(Kodes(Ebene=row[0], Ort=row[1], Art=row[2], KapNr=Kapitel.objects.get(KapNr=row[3], Year=y),
                GrVon=Gruppen.objects.get(GrVon=row[4], Year=y), DCode=Dreisteller.objects.get(DCode=row[5], Year=y),
                Code=row[6], Seite=row[7], Titel=row[8], Viersteller=None, Fünfsteller=None,
                Sechssteller=None, Para17bd=None, DRG=None, ZusatzK=None, EinmalK=None, Year=y))
            elif int(year) <= 2010:
                imports.append(Kodes(Ebene=row[0], Ort=row[1], Art=row[2], KapNr=Kapitel.objects.get(KapNr=row[3], Year=y),
                GrVon=Gruppen.objects.get(GrVon=row[4], Year=y), DCode=Dreisteller.objects.get(DCode=row[5], Year=y),
                Code=row[6], Seite=row[7], Titel=row[8], Viersteller=None, Fünfsteller=None,
                Sechssteller=None, Para17bd=None, DRG=row[9], ZusatzK=None, EinmalK=None, Year=y))
            elif int(year) <= 2012:
                imports.append(Kodes(Ebene=row[0], Ort=row[1], Art=row[2], KapNr=Kapitel.objects.get(KapNr=row[3], Year=y),
                GrVon=Gruppen.objects.get(GrVon=row[4], Year=y), DCode=Dreisteller.objects.get(DCode=row[5], Year=y),
                Code=row[6], Seite=row[7], Titel=row[8], Viersteller=None, Fünfsteller=None,
                Sechssteller=None, Para17bd=row[9], DRG=row[10], ZusatzK=None, EinmalK=None, Year=y))
            elif int(year) <= 2013:
                imports.append(Kodes(Ebene=row[0], Ort=row[1], Art=row[2], KapNr=Kapitel.objects.get(KapNr=row[3], Year=y),
                GrVon=Gruppen.objects.get(GrVon=row[4], Year=y), DCode=Dreisteller.objects.get(DCode=row[5], Year=y),
                Code=row[6], Seite=row[7], Titel=row[8], Viersteller=row[9], Fünfsteller=row[10],
                Sechssteller=row[11], Para17bd=row[12], DRG=row[13], ZusatzK=None, EinmalK=None, Year=y))
            elif int(year) <= 2015:
                imports.append(Kodes(Ebene=row[0], Ort=row[1], Art=row[2], KapNr=Kapitel.objects.get(KapNr=row[3], Year=y),
                GrVon=Gruppen.objects.get(GrVon=row[4], Year=y), DCode=Dreisteller.objects.get(DCode=row[5], Year=y),
                Code=row[6], Seite=row[7], Titel=row[8], Viersteller=row[9], Fünfsteller=row[10],
                Sechssteller=row[11], Para17bd=row[12], DRG=row[13], ZusatzK=row[14], EinmalK=row[15], Year=y))
            else:
                imports.append(Kodes(Ebene=row[0], Ort=row[1], Art=row[2], KapNr=Kapitel.objects.get(KapNr=row[3], Year=y),
                GrVon=Gruppen.objects.get(GrVon=row[4], Year=y), DCode=Dreisteller.objects.get(DCode=row[5], Year=y),
                Code=row[6], Seite=row[7], Titel=row[8], Viersteller=row[9], Fünfsteller=row[10],
                Sechssteller=row[11], Para17bd=row[12], DRG=None, ZusatzK=row[13], EinmalK=row[14], Year=y))
    Kodes.objects.bulk_create(imports)
    imports = []
    print()

    
    # CLAML - XML
    if int(year) <= 2009:
        print("XML-Daten existieren nicht und werden somit nicht importiert.")
    else:
        print("Importiere XML-Data")
        iexclusions = []
        iinclusions = []
        inotes = []
        ipreferreds = []
        ipreferredlongs = []
        tree = ET.parse("data/"+year+"/ops"+year+"syst_claml.xml")
        root = tree.getroot()
        line_count = len(root.findall('./Class[@kind="category"]'))
        bar = progressbar.ProgressBar(maxval=line_count).start()
        count = 0
        for category in root.findall('./Class[@kind="category"]'):
            count += 1
            bar.update(count)
            if len(category.attrib['code']) <= 4:
                continue
            for rubric in category.findall('./Rubric'):
                if rubric.attrib['kind'] == 'exclusion':
                    s = ' '.join(rubric[0].itertext()).strip()
                    l = rubric[0].itertext()
                    s = re.sub(" +", " ", ' '.join([m.rstrip() for m in l]).strip())
                    iexclusions.append(Exclusion(Code=Kodes.objects.get(Code=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'inclusion':
                    s = ' '.join(rubric[0].itertext()).strip()
                    l = rubric[0].itertext()
                    s = re.sub(" +", " ", ' '.join([m.rstrip() for m in l]).strip())
                    iinclusions.append(Inclusion(Code=Kodes.objects.get(Code=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'note':
                    s = ' '.join(rubric[0].itertext()).strip()
                    inotes.append(Note(Code=Kodes.objects.get(Code=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'preferred':
                    s = rubric[0].text
                    ipreferreds.append(Preferred(Code=Kodes.objects.get(Code=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'preferredLong':
                    s = rubric[0].text
                    ipreferredlongs.append(PreferredLong(Code=Kodes.objects.get(Code=category.attrib['code'], Year=y), Text=s, Year=y))
        Exclusion.objects.bulk_create(iexclusions)
        iexclusions = []
        Inclusion.objects.bulk_create(iinclusions)
        iinclusions = []
        Note.objects.bulk_create(inotes)
        inotes = []
        Preferred.objects.bulk_create(ipreferreds)
        ipreferreds = []
        PreferredLong.objects.bulk_create(ipreferredlongs)
        ipreferredlongs = []
        print()
    
    
    # Umsteiger
    if not Version.objects.filter(Year=(int(year)-1)).exists():
        print("Umsteiger nicht geladen, da vorheriges Jahr nicht importiert.")
    else:
        print("Importiere Umsteiger-Data")
        with open("data/"+year+"/ops"+year+"syst_umsteiger.txt", 'r') as file:
            line_count = len(file.readlines())
        bar = progressbar.ProgressBar(maxval=line_count).start()
        imports = []
        with open("data/"+year+"/ops"+year+"syst_umsteiger.txt") as file:
            reader = csv.reader(file, delimiter=";")
            y2 = Version.objects.get(Year=(int(year)-1))
            count = 0
            for row in reader:
                count += 1
                bar.update(count)
                if int(year) <= 2009:
                    if row[0] == 'UNDEF' or row[0] == 'None':
                        imports.append(Umsteiger(Old=None, SideOld=None, New=Kodes.objects.get(Code=row[1], Year=y), SideNew=row[3], AutoAnte=row[4], AutoRetro=row[5]))
                    elif row[1] == 'UNDEF' or row[1] == 'None':
                        imports.append(Umsteiger(Old=Kodes.objects.get(Code=row[0], Year=y2), SideOld=row[2], New=None, SideNew=None, AutoAnte=row[4], AutoRetro=row[5]))
                    else:
                        imports.append(Umsteiger(Old=Kodes.objects.get(Code=row[0], Year=y2), SideOld=row[2], New=Kodes.objects.get(Code=row[1], Year=y), SideNew=row[3], AutoAnte=row[4], AutoRetro=row[5]))
                else:
                    if row[0] == 'UNDEF' or row[0] == 'None':
                        imports.append(Umsteiger(Old=None, SideOld=None, New=Kodes.objects.get(Code=row[2], Year=y), SideNew=row[3], AutoAnte=row[4], AutoRetro=row[5]))
                    elif row[2] == 'UNDEF' or row[1] == 'None':
                        imports.append(Umsteiger(Old=Kodes.objects.get(Code=row[0], Year=y2), SideOld=row[1], New=None, SideNew=None, AutoAnte=row[4], AutoRetro=row[5]))
                    else:
                        imports.append(Umsteiger(Old=Kodes.objects.get(Code=row[0], Year=y2), SideOld=row[1], New=Kodes.objects.get(Code=row[2], Year=y), SideNew=row[3], AutoAnte=row[4], AutoRetro=row[5]))
        Umsteiger.objects.bulk_create(imports)
        imports = []
        print()
