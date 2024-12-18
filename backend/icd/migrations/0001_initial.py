# Generated by Django 4.1.2 on 2023-02-05 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gruppen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GrVon', models.TextField(blank=True)),
                ('GrBis', models.TextField(blank=True, null=True)),
                ('GrTi', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kapitel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('KapNr', models.TextField(blank=True)),
                ('KapTi', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ebene', models.TextField(blank=True, null=True)),
                ('Ort', models.TextField(blank=True, null=True)),
                ('Art', models.TextField(blank=True, null=True)),
                ('Code', models.TextField(blank=True)),
                ('NormCode', models.TextField(blank=True, null=True)),
                ('CodeOhnePunkt', models.TextField(blank=True, null=True)),
                ('Titel', models.TextField(blank=True, null=True)),
                ('Dreisteller', models.TextField(blank=True, null=True)),
                ('Viersteller', models.TextField(blank=True, null=True)),
                ('Fünfsteller', models.TextField(blank=True, null=True)),
                ('P295', models.TextField(blank=True, null=True)),
                ('P301', models.TextField(blank=True, null=True)),
                ('SexCode', models.TextField(blank=True, null=True)),
                ('SexFehlerTyp', models.TextField(blank=True, null=True)),
                ('AltUnt', models.TextField(blank=True, null=True)),
                ('AltOb', models.TextField(blank=True, null=True)),
                ('AltFehlerTyp', models.TextField(blank=True, null=True)),
                ('Exot', models.TextField(blank=True, null=True)),
                ('Belegt', models.TextField(blank=True, null=True)),
                ('IfSGMeldung', models.TextField(blank=True, null=True)),
                ('IfSGLabor', models.TextField(blank=True, null=True)),
                ('GrVon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.gruppen')),
                ('KapNr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kapitel')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('Year', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Umsteiger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AutoAnte', models.TextField(blank=True, null=True)),
                ('AutoRetro', models.TextField(blank=True, null=True)),
                ('New', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='New', to='icd.kodes')),
                ('Old', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Old', to='icd.kodes')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(blank=True, null=True)),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kodes')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='PreferredLong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(blank=True, null=True)),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kodes')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='Preferred',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(blank=True, null=True)),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kodes')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(blank=True, null=True)),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kodes')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='MortL4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MortL4Code', models.TextField(blank=True)),
                ('MortL4Ti', models.TextField(blank=True, null=True)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='MortL3Grp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MortL3GrpCode', models.TextField(blank=True)),
                ('MortL3GrpTi', models.TextField(blank=True, null=True)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='MortL3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MortL3Code', models.TextField(blank=True)),
                ('MortL3Ti', models.TextField(blank=True, null=True)),
                ('MortL3GrpCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.mortl3grp')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='MortL2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MortL2Code', models.TextField(blank=True)),
                ('MortL2Ti', models.TextField(blank=True, null=True)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='MortL1Grp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MortL1GrpCode', models.TextField(blank=True)),
                ('MortL1GrpTi', models.TextField(blank=True, null=True)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='MortL1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MortL1Code', models.TextField(blank=True)),
                ('MortL1Ti', models.TextField(blank=True, null=True)),
                ('MortL1GrpCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.mortl1grp')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='MorbL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MorbLCode', models.TextField(blank=True)),
                ('MorbLTti', models.TextField(blank=True, null=True)),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.AddField(
            model_name='kodes',
            name='MorbLCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.morbl'),
        ),
        migrations.AddField(
            model_name='kodes',
            name='MortL1Code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.mortl1'),
        ),
        migrations.AddField(
            model_name='kodes',
            name='MortL2Code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.mortl2'),
        ),
        migrations.AddField(
            model_name='kodes',
            name='MortL3Code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.mortl3'),
        ),
        migrations.AddField(
            model_name='kodes',
            name='MortL4Code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.mortl4'),
        ),
        migrations.AddField(
            model_name='kodes',
            name='Year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version'),
        ),
        migrations.AddField(
            model_name='kapitel',
            name='Year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version'),
        ),
        migrations.CreateModel(
            name='Inclusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(blank=True, null=True)),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kodes')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.AddField(
            model_name='gruppen',
            name='KapNr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kapitel'),
        ),
        migrations.AddField(
            model_name='gruppen',
            name='Year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version'),
        ),
        migrations.CreateModel(
            name='Exclusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(blank=True, null=True)),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kodes')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(blank=True, null=True)),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kodes')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
        migrations.CreateModel(
            name='CodingHints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(blank=True, null=True)),
                ('Code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.kodes')),
                ('Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icd.version')),
            ],
        ),
    ]
