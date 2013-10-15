# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Commit.repo'
        db.add_column(u'repos_commit', 'repo',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['repos.Repo']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Commit.repo'
        db.delete_column(u'repos_commit', 'repo_id')


    models = {
        u'repos.actor': {
            'Meta': {'object_name': 'Actor'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'repos.repo': {
            'Meta': {'object_name': 'Repo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['repos']