from django.db import models


class Version(models.Model):
    Year = models.IntegerField(primary_key=True)


class Kapitel(models.Model):
    KapNr = models.TextField(blank=True)
    KapTi = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Gruppen(models.Model):
    KapNr = models.ForeignKey(Kapitel, on_delete=models.CASCADE)
    GrVon = models.TextField(blank=True)
    GrBis = models.TextField(blank=True, null=True)
    GrTi = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Dreisteller(models.Model):
    KapNr = models.ForeignKey(Kapitel, on_delete=models.CASCADE)
    GrVon = models.ForeignKey(Gruppen, on_delete=models.CASCADE)
    DCode = models.TextField(blank=True)
    DTi = models.TextField(blank=True, null=True)
    Year = models.ForeignKey(Version, on_delete=models.CASCADE)


class Kodes(models.Model):
    Ebene = models.TextField(blank=True, null=True)
    Ort = models.TextField(blank=True, null=True)
    Art = models.TextField(blank=True, null=True)
    KapNr = models.ForeignKey(Kapitel, on_delete=models.CASCADE)
    GrVon = models.ForeignKey(Gruppen, on_delete=models.CASCADE)
    DCode = models.ForeignKey(Dreisteller, on_delete=models.CASCADE)
    Code = models.TextField(blank=True)
    Seite = models.TextField(blank=True, null=True)
    Titel = models.TextField(blank=True, null=True)
    Viersteller = models.TextField(blank=True, null=True)
    Fünfsteller = models.TextField(blank=True, null=True)
    Sechssteller = models.TextField(blank=True, null=True)
    Para17bd = models.TextField(blank=True, null=True)
    DRG = models.TextField(blank=True, null=True)
    ZusatzK = models.TextField(blank=True, null=True)
    EinmalK = models.TextField(blank=True, null=True)
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


class Umsteiger(models.Model):
    Old = models.ForeignKey(Kodes, related_name="Old", blank=True, null=True, on_delete=models.CASCADE)
    SideOld = models.TextField(blank=True, null=True)
    New = models.ForeignKey(Kodes, related_name="New", blank=True, null=True, on_delete=models.CASCADE)
    SideNew = models.TextField(blank=True, null=True)
    AutoAnte = models.TextField(blank=True, null=True)
    AutoRetro = models.TextField(blank=True, null=True)