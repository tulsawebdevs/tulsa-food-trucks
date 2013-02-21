# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PhoneVerification'
        db.create_table('accounts_phoneverification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20)),
        ))
        db.send_create_signal('accounts', ['PhoneVerification'])

        # Adding model 'EmailVerification'
        db.create_table('accounts_emailverification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('accounts', ['EmailVerification'])


    def backwards(self, orm):
        # Deleting model 'PhoneVerification'
        db.delete_table('accounts_phoneverification')

        # Deleting model 'EmailVerification'
        db.delete_table('accounts_emailverification')


    models = {
        'accounts.emailverification': {
            'Meta': {'object_name': 'EmailVerification'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        'accounts.phoneverification': {
            'Meta': {'object_name': 'PhoneVerification'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['accounts']