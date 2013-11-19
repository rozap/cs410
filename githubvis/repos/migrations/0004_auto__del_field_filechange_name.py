# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'FileChange.name'
        db.delete_column(u'repos_filechange', 'name')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'FileChange.name'
        raise RuntimeError("Cannot reverse this migration. 'FileChange.name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'FileChange.name'
        db.add_column(u'repos_filechange', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=512),
                      keep_default=False)


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
            'change1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'file_changeyes1'", 'to': u"orm['repos.FileChange']"}),
            'change2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'file_change2'", 'to': u"orm['repos.FileChange']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'repos.filechange': {
            'Meta': {'object_name': 'FileChange'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repos.Actor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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