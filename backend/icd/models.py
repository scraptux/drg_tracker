from django.db import models


class Version(models.Model):
    Year = models.IntegerField(primary_key=True)


class Kapitel(models.Model):
    KapNr = models.TextField(blank=True)
    KapTi = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Gruppen(models.Model):
    GrVon = models.TextField(blank=True)
    GrBis = models.TextField(blank=True, null=True)
    KapNr = models.ForeignKey(Kapitel, on_delete=models.CASCADE)
    GrTi = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class MorbL(models.Model):
    MorbLCode = models.TextField(blank=True)
    MorbLTti = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class MortL1Grp(models.Model):
    MortL1GrpCode = models.TextField(blank=True)
    MortL1GrpTi = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class MortL1(models.Model):
    MortL1Code = models.TextField(blank=True)
    MortL1GrpCode = models.ForeignKey(MortL1Grp, on_delete=models.CASCADE)
    MortL1Ti = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class MortL2(models.Model):
    MortL2Code = models.TextField(blank=True)
    MortL2Ti = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class MortL3Grp(models.Model):
    MortL3GrpCode = models.TextField(blank=True)
    MortL3GrpTi = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class MortL3(models.Model):
    MortL3Code = models.TextField(blank=True)
    MortL3GrpCode = models.ForeignKey(MortL3Grp, on_delete=models.CASCADE)
    MortL3Ti = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class MortL4(models.Model):
    MortL4Code = models.TextField(blank=True)
    MortL4Ti = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Kodes(models.Model):
    Ebene = models.TextField(blank=True, null=True)
    Ort = models.TextField(blank=True, null=True)
    Art = models.TextField(blank=True, null=True)
    KapNr = models.ForeignKey(Kapitel, on_delete=models.CASCADE)
    GrVon = models.ForeignKey(Gruppen, on_delete=models.CASCADE)
    Code = models.TextField(blank=True)
    NormCode = models.TextField(blank=True, null=True)
    CodeOhnePunkt = models.TextField(blank=True, null=True)
    Titel = models.TextField(blank=True, null=True)
    Dreisteller = models.TextField(blank=True, null=True)
    Viersteller = models.TextField(blank=True, null=True)
    Fünfsteller = models.TextField(blank=True, null=True)
    P295 = models.TextField(blank=True, null=True)
    P301 = models.TextField(blank=True, null=True)
    MortL1Code = models.ForeignKey(MortL1, on_delete=models.CASCADE)
    MortL2Code = models.ForeignKey(MortL2, on_delete=models.CASCADE)
    MortL3Code = models.ForeignKey(MortL3, on_delete=models.CASCADE)
    MortL4Code = models.ForeignKey(MortL4, on_delete=models.CASCADE)
    MorbLCode = models.ForeignKey(MorbL, on_delete=models.CASCADE)
    SexCode = models.TextField(blank=True, null=True)
    SexFehlerTyp = models.TextField(blank=True, null=True)
    AltUnt = models.TextField(blank=True, null=True)
    AltOb = models.TextField(blank=True, null=True)
    AltFehlerTyp = models.TextField(blank=True, null=True)
    Exot = models.TextField(blank=True, null=True)
    Belegt = models.TextField(blank=True, null=True)
    IfSGMeldung = models.TextField(blank=True, null=True)
    IfSGLabor = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class CodingHints(models.Model):
    Code = models.ForeignKey(Kodes, on_delete=models.CASCADE)
    Text = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)

class Definition(models.Model):
    Code = models.ForeignKey(Kodes, on_delete=models.CASCADE)
    Text = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Exclusion(models.Model):
    Code = models.ForeignKey(Kodes, on_delete=models.CASCADE)
    Text = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Inclusion(models.Model):
    Code = models.ForeignKey(Kodes, on_delete=models.CASCADE)
    Text = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Note(models.Model):
    Code = models.ForeignKey(Kodes, on_delete=models.CASCADE)
    Text = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Preferred(models.Model):
    Code = models.ForeignKey(Kodes, on_delete=models.CASCADE)
    Text = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class PreferredLong(models.Model):
    Code = models.ForeignKey(Kodes, on_delete=models.CASCADE)
    Text = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Text(models.Model):
    Code = models.ForeignKey(Kodes, on_delete=models.CASCADE)
    Text = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Umsteiger(models.Model):
    Old = models.ForeignKey(Kodes, related_name="Old", blank=True, null=True, on_delete=models.CASCADE)
    New = models.ForeignKey(Kodes, related_name="New", blank=True, null=True, on_delete=models.CASCADE)
    AutoAnte = models.TextField(blank=True, null=True)
    AutoRetro = models.TextField(blank=True, null=True)