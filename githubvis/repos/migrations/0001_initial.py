# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Repo'
        db.create_table(u'repos_repo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'repos', ['Repo'])

        # Adding model 'Actor'
        db.create_table(u'repos_actor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lat', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('lng', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('loc', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal(u'repos', ['Actor'])

        # Adding model 'Commit'
        db.create_table(u'repos_commit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repos.Repo'])),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repos.Actor'])),
            ('hexsha', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'repos', ['Commit'])

        # Adding model 'Function'
        db.create_table(u'repos_function', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('commit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repos.Commit'])),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=512)),
        ))
        db.send_create_signal(u'repos', ['Function'])

        # Adding model 'FunctionCall'
        db.create_table(u'repos_functioncall', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='function_call_caller', to=orm['repos.Function'])),
            ('callee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='function_call_callee', to=orm['repos.Function'])),
        ))
        db.send_create_signal(u'repos', ['FunctionCall'])


    def backwards(self, orm):
        # Deleting model 'Repo'
        db.delete_table(u'repos_repo')

        # Deleting model 'Actor'
        db.delete_table(u'repos_actor')

        # Deleting model 'Commit'
        db.delete_table(u'repos_commit')

        # Deleting model 'Function'
        db.delete_table(u'repos_function')

        # Deleting model 'FunctionCall'
        db.delete_table(u'repos_functioncall')


    models = {
        u'repos.actor': {
            'Meta': {'object_name': 'Actor'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'lng': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'loc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        u'repos.commit': {
            'Meta': {'object_name': 'Commit'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repos.Actor']"}),
            'hexsha': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repos.Repo']"})
        },
        u'repos.function': {
            'Meta': {'object_name': 'Function'},
            'commit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repos.Commit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
        },
        u'repos.functioncall': {
            'Meta': {'object_name': 'FunctionCall'},
            'callee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'function_call_callee'", 'to': u"orm['repos.Function']"}),
            'caller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'function_call_caller'", 'to': u"orm['repos.Function']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'repos.repo': {
            'Meta': {'object_name': 'Repo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['repos']