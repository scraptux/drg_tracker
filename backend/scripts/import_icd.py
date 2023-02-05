from icd.models import Version, Kapitel, Gruppen, MorbL, MortL1Grp, MortL1, MortL2, MortL3Grp, MortL3, MortL4, Kodes
from icd.models import CodingHints, Definition, Exclusion, Inclusion, Note, Preferred, PreferredLong, Text
from icd.models import Umsteiger

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
    bar = progressbar.ProgressBar(maxval=9).start()

    # Kapitel
    imports = []
    with open("data/"+year+"/icd10gm"+year+"syst_kapitel.txt", 'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(Kapitel(KapNr=row[0], KapTi=row[1], Year=y))
    Kapitel.objects.bulk_create(imports)
    bar.update(1)

    # Gruppen
    imports = []
    with open("data/"+year+"/icd10gm"+year+"syst_gruppen.txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if int(year) <= 2006:
                imports.append(Gruppen(GrVon=row[0], GrBis=None, KapNr=Kapitel.objects.get(KapNr=row[1], Year=y), GrTi=row[2], Year=y))
            else:
                imports.append(Gruppen(GrVon=row[0], GrBis=row[1], KapNr=Kapitel.objects.get(KapNr=row[2], Year=y), GrTi=row[3], Year=y))
    Gruppen.objects.bulk_create(imports)
    bar.update(2)

    # MorbL
    imports = []
    with open("data/"+year+"/morbl_"+year+".txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(MorbL(MorbLCode=row[0], MorbLTti=row[1], Year=y))
    MorbL.objects.bulk_create(imports)
    bar.update(3)

    # MortL1Grp
    imports = []
    with open("data/"+year+"/mortl1grp_"+year+".txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(MortL1Grp(MortL1GrpCode=row[0], MortL1GrpTi=row[1], Year=y))
    MortL1Grp.objects.bulk_create(imports)
    bar.update(4)

    # MortL1
    imports = []
    with open("data/"+year+"/mortl1_"+year+".txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(MortL1(MortL1Code=row[0], MortL1GrpCode=MortL1Grp.objects.get(MortL1GrpCode=row[1], Year=y), MortL1Ti=row[2], Year=y))
    MortL1.objects.bulk_create(imports)
    bar.update(5)

    # MortL2
    imports = []
    with open("data/"+year+"/mortl2_"+year+".txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(MortL2(MortL2Code=row[0], MortL2Ti=row[1], Year=y))
    MortL2.objects.bulk_create(imports)
    bar.update(6)

    # MortL3Grp
    imports = []
    with open("data/"+year+"/mortl3grp_"+year+".txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(MortL3Grp(MortL3GrpCode=row[0], MortL3GrpTi=row[1], Year=y))
    MortL3Grp.objects.bulk_create(imports)
    bar.update(7)

    # MortL3
    imports = []
    with open("data/"+year+"/mortl3_"+year+".txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(MortL3(MortL3Code=row[0], MortL3GrpCode=MortL3Grp.objects.get(MortL3GrpCode=row[1], Year=y), MortL3Ti=row[2], Year=y))
    MortL3.objects.bulk_create(imports)
    bar.update(8)

    # MortL4
    imports = []
    with open("data/"+year+"/mortl4_"+year+".txt") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            imports.append(MortL4(MortL4Code=row[0], MortL4Ti=row[1], Year=y))
    MortL4.objects.bulk_create(imports)
    bar.update(9)
    print()


    # Codes
    print("Importiere Code Meta-Daten")
    with open("data/"+year+"/icd10gm"+year+"syst_kodes.txt", 'r') as file:
        line_count = len(file.readlines())
    bar = progressbar.ProgressBar(maxval=line_count).start()
    imports = []
    with open("data/"+year+"/icd10gm"+year+"syst_kodes.txt") as file:
        reader = csv.reader(file, delimiter=";")
        row_current = 0
        for row in reader:
            row_current += 1
            bar.update(row_current)
            if int(year) <= 2012:
                imports.append(Kodes(Ebene=row[0], Ort=row[1], Art=row[2], KapNr=Kapitel.objects.get(KapNr=row[3], Year=y),
                GrVon=Gruppen.objects.get(GrVon=row[4], Year=y), Code=row[5], NormCode=row[6], CodeOhnePunkt=row[7],
                Titel=row[8], Dreisteller=None, Viersteller=None, Fünfsteller=None, P295=row[9],
                P301=row[10], MortL1Code=MortL1.objects.get(MortL1Code=row[11], Year=y),
                MortL2Code=MortL2.objects.get(MortL2Code=row[12], Year=y),
                MortL3Code=MortL3.objects.get(MortL3Code=row[13], Year=y),
                MortL4Code=MortL4.objects.get(MortL4Code=row[14], Year=y),
                MorbLCode=MorbL.objects.get(MorbLCode=row[15], Year=y),
                SexCode=row[16], SexFehlerTyp=row[17], AltUnt=row[18], AltOb=row[20], AltFehlerTyp=[22],
                Exot=row[23], Belegt=row[24], IfSGMeldung=row[25], IfSGLabor=[26], Year=y))
            else:
                imports.append(Kodes(Ebene=row[0], Ort=row[1], Art=row[2], KapNr=Kapitel.objects.get(KapNr=row[3], Year=y),
                GrVon=Gruppen.objects.get(GrVon=row[4], Year=y), Code=row[5], NormCode=row[6], CodeOhnePunkt=row[7],
                Titel=row[8], Dreisteller=row[9], Viersteller=row[10], Fünfsteller=row[11], P295=row[12],
                P301=row[13], MortL1Code=MortL1.objects.get(MortL1Code=row[14], Year=y),
                MortL2Code=MortL2.objects.get(MortL2Code=row[15], Year=y),
                MortL3Code=MortL3.objects.get(MortL3Code=row[16], Year=y),
                MortL4Code=MortL4.objects.get(MortL4Code=row[17], Year=y),
                MorbLCode=MorbL.objects.get(MorbLCode=row[18], Year=y),
                SexCode=row[19], SexFehlerTyp=row[20], AltUnt=row[21], AltOb=row[22], AltFehlerTyp=row[23],
                Exot=row[24], Belegt=row[25], IfSGMeldung=row[26], IfSGLabor=row[27], Year=y))
    Kodes.objects.bulk_create(imports)
    imports = []
    print()


    # CLAML - XML
    if int(year) <= 2008:
        print("XML-Daten existieren nicht und werden somit nicht importiert.")
    else:
        print("Importiere XML-Data")
        icodinghints = []
        idefinitions = []
        iexclusions = []
        iinclusions = []
        inotes = []
        ipreferreds = []
        ipreferredlongs = []
        itexts = []
        tree = ET.parse("data/"+year+"/icd10gm"+year+"syst_claml.xml")
        root = tree.getroot()
        line_count = len(root.findall('./Class[@kind="category"]'))
        bar = progressbar.ProgressBar(maxval=line_count).start()
        count = 0
        for category in root.findall('./Class[@kind="category"]'):
            count += 1
            bar.update(count)
            for rubric in category.findall('./Rubric'):
                if rubric.attrib['kind'] == 'coding-hint':
                    s = ' '.join(rubric[0].itertext()).strip()
                    icodinghints.append(CodingHints(Code=Kodes.objects.get(NormCode__exact=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'definition':
                    s = ' '.join(rubric[0].itertext()).strip()
                    idefinitions.append(Definition(Code=Kodes.objects.get(NormCode__exact=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'exclusion':
                    s = ' '.join(rubric[0].itertext()).strip()
                    l = rubric[0].itertext()
                    s = re.sub(" +", " ", ' '.join([m.rstrip() for m in l]).strip())
                    iexclusions.append(Exclusion(Code=Kodes.objects.get(NormCode__exact=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'inclusion':
                    s = ' '.join(rubric[0].itertext()).strip()
                    l = rubric[0].itertext()
                    s = re.sub(" +", " ", ' '.join([m.rstrip() for m in l]).strip())
                    iinclusions.append(Inclusion(Code=Kodes.objects.get(NormCode__exact=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'note':
                    s = ' '.join(rubric[0].itertext()).strip()
                    inotes.append(Note(Code=Kodes.objects.get(NormCode__exact=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'preferred':
                    s = rubric[0].text
                    ipreferreds.append(Preferred(Code=Kodes.objects.get(NormCode__exact=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'preferredLong':
                    s = rubric[0].text
                    ipreferredlongs.append(PreferredLong(Code=Kodes.objects.get(NormCode__exact=category.attrib['code'], Year=y), Text=s, Year=y))
                elif rubric.attrib['kind'] == 'text':
                    s = ' '.join(rubric[0].itertext()).strip()
                    itexts.append(Text(Code=Kodes.objects.get(NormCode__exact=category.attrib['code'], Year=y), Text=s, Year=y))
        CodingHints.objects.bulk_create(icodinghints)
        icodinghints = []
        Definition.objects.bulk_create(idefinitions)
        idefinitions = []
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
        Text.objects.bulk_create(itexts)
        itexts = []
        print()
    

    # Umsteiger
    if not Version.objects.filter(Year=(int(year)-1)).exists():
        print("Umsteiger nicht geladen, da vorheriges Jahr nicht importiert.")
    else:
        print("Importiere Umsteiger-Data")
        with open("data/"+year+"/icd10gm"+year+"syst_umsteiger.txt", 'r') as file:
            line_count = len(file.readlines())
        bar = progressbar.ProgressBar(maxval=line_count).start()
        imports = []
        with open("data/"+year+"/icd10gm"+year+"syst_umsteiger.txt") as file:
            reader = csv.reader(file, delimiter=";")
            y2 = Version.objects.get(Year=(int(year)-1))
            count = 0
            for row in reader:
                count += 1
                bar.update(count)
                if row[0] == 'UNDEF':
                    imports.append(Umsteiger(Old=None, New=Kodes.objects.get(NormCode=row[1], Year=y), AutoAnte=row[2], AutoRetro=row[3]))
                elif row[1] == 'UNDEF':
                    imports.append(Umsteiger(Old=Kodes.objects.get(NormCode=row[0], Year=y2), New=None, AutoAnte=row[2], AutoRetro=row[3]))
                else:
                    imports.append(Umsteiger(Old=Kodes.objects.get(NormCode=row[0], Year=y2), New=Kodes.objects.get(NormCode=row[1], Year=y), AutoAnte=row[2], AutoRetro=row[3]))
        Umsteiger.objects.bulk_create(imports)
        imports = []
        print()