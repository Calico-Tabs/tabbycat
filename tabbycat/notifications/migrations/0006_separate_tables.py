# Generated by Django 2.0.8 on 2018-10-23 19:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0005_remove_tournament_current_round'),
        ('notifications', '0005_auto_20180915_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulkNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(blank=True, choices=[('p', 'team points'), ('c', 'ballot confirmed'), ('f', 'feedback URL'), ('b', 'ballot URL'), ('u', 'landing page URL'), ('d', 'draw released'), ('t', 'registration'), ('m', 'motion(s) released')], max_length=1, verbose_name='event')),
                ('timestamp', models.DateTimeField(auto_now_add=False, verbose_name='timestamp')),
                ('round', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournaments.Round', verbose_name='round')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.Tournament', verbose_name='tournament')),
            ],
            options={
                'verbose_name': 'bulk notification',
                'verbose_name_plural': 'bulk notifications',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddField(
            model_name='sentmessagerecord',
            name='notification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='notifications.BulkNotification', verbose_name='notification'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='EmailStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('event', models.CharField(choices=[('processed', 'Processed'), ('dropped', 'Dropped'), ('deferred', 'Deferred'), ('delivered', 'Delivered'), ('bounce', 'Bounced'), ('open', 'Opened'), ('click', 'Clicked'), ('unsubscribe', 'Unsubscribed'), ('spamreport', 'Marked as spam'), ('group_unsubscribe', 'Unsubscribed from group'), ('group_resubscribe', 'Resubscribed to group')], max_length=20, verbose_name='event')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='context')),
            ],
            options={
                'verbose_name': 'email status',
                'verbose_name_plural': 'email statuses',
                'ordering': ['-timestamp'],
                'get_latest_by': '-timestamp'
            },
        ),
        migrations.AddField(
            model_name='sentmessagerecord',
            name='message_id',
            field=models.CharField(null=True, max_length=254, unique=True, verbose_name='Message-ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailstatus',
            name='email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.SentMessageRecord', verbose_name='email message'),
        ),
        migrations.AlterField(
            model_name='sentmessagerecord',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='timestamp'),
        ),
    ]
