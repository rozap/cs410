# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TouchedFile'
        db.delete_table(u'repos_touchedfile')

        # Adding model 'CommonFileChange'
        db.create_table(u'repos_commonfilechange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('change1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='file_change1', to=orm['repos.FileChange'])),
            ('change2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='file_change2', to=orm['repos.FileChange'])),
        ))
        db.send_create_signal(u'repos', ['CommonFileChange'])

        # Adding model 'FileChange'
        db.create_table(u'repos_filechange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=512)),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repos.Actor'])),
        ))
        db.send_create_signal(u'repos', ['FileChange'])


    def backwards(self, orm):
        # Adding model 'TouchedFile'
        db.create_table(u'repos_touchedfile', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('actor2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='file_actor2', to=orm['repos.Actor'])),
            ('actor1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='file_actor1', to=orm['repos.Actor'])),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=512)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'repos', ['TouchedFile'])

        # Deleting model 'CommonFileChange'
        db.delete_table(u'repos_commonfilechange')

        # Deleting model 'FileChange'
        db.delete_table(u'repos_filechange')


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
        u'repos.commonfilechange': {
            'Meta': {'object_name': 'CommonFileChange'},
            'change1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'file_change1'", 'to': u"orm['repos.FileChange']"}),
            'change2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'file_change2'", 'to': u"orm['repos.FileChange']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'repos.filechange': {
            'Meta': {'object_name': 'FileChange'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repos.Actor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
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