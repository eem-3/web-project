from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_media_file'),
    ]

    operations = [
        # Remove redundant up_votes integer (use votes.count() instead)
        migrations.RemoveField(
            model_name='entity',
            name='up_votes',
        ),
        # Allow entities to be created without an AI summary
        migrations.AlterField(
            model_name='entity',
            name='description_ai',
            field=models.TextField(blank=True, default=''),
        ),
        # Add choices to entity type discriminator
        migrations.AlterField(
            model_name='entity',
            name='type',
            field=models.SmallIntegerField(choices=[(1, 'Media'), (2, 'Project')]),
        ),
        # Allow Media fields to be blank for programmatic/partial creation
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='media',
            name='storage_url',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='media',
            name='filename',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='media',
            name='mimetype',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='media',
            name='size',
            field=models.BigIntegerField(default=0),
        ),
        # Add related_name='replies' for clean reverse access to nested comments
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='replies',
                to='core.comment',
            ),
        ),
    ]
