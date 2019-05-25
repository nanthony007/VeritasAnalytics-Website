# Generated by Django 2.1.5 on 2019-05-12 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vws_main', '0003_auto_20190512_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fs_match',
            name='focus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='focus_wrestler2', to='vws_main.FS_Wrestler'),
        ),
        migrations.AlterField(
            model_name='fs_match',
            name='focus_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='focus_team_name2', to='vws_main.FS_Team'),
        ),
        migrations.AlterField(
            model_name='fs_match',
            name='opp_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opp_team_name2', to='vws_main.FS_Team'),
        ),
        migrations.AlterField(
            model_name='fs_match',
            name='opponent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opp_wrestler2', to='vws_main.FS_Wrestler'),
        ),
    ]