from django.contrib import admin
from django import forms
from django.template.defaultfilters import slugify

from mptt.forms import TreeNodeChoiceField
from editor.tree_editor import TreeEditor
from models import Bunch

class NullTreeNodeChoiceField(forms.ModelChoiceField):
    """A ModelChoiceField for tree nodes."""
    def __init__(self, level_indicator=u'---', *args, **kwargs):
        self.level_indicator = level_indicator
        #kwargs['empty_label'] = None
        super(NullTreeNodeChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        """
        Creates labels which represent the tree level of each node when
        generating option labels.
        """
        return u'%s %s' % (self.level_indicator * getattr(obj, obj._meta.level_attr),
                                obj)


class BunchAdminForm(forms.ModelForm):
    parent = NullTreeNodeChoiceField(queryset=Bunch.tree.all(), 
                                 level_indicator=u'+-', 
                                 empty_label='------', 
                                 required=False)
    class Meta:
        model = Bunch

class BunchAdmin(TreeEditor, admin.ModelAdmin):
    form = BunchAdminForm
    list_display = ('__unicode__',)
    search_fields = (('uid','content',))
    
    class Media:
        js = ('js/genericcollections.js',)
    

admin.site.register(Bunch, BunchAdmin)

