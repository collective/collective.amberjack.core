from Products.Five.browser import BrowserView


ajStandardSteps = (
    ('manage_portlets', 'div.managePortletsLink a'),
    
    ('go_home', '#portal-breadcrumbs > a'),
    ('go_uplevel', '#portal-breadcrumbs span a:last'),
    
    ('site_sitemap', '#siteaction-sitemap a'),
    ('site_accessibility', '#siteaction-accessibility a'),
    ('site_contact', '#siteaction-contact a'),
    ('site_setup', '#siteaction-plone_setup a'),
    
    ('action_cut', '#cut'),
    ('action_copy', '#copy'),
    ('action_delete', '#delete'),
    ('action_rename', '#rename'),
    
    ('new_folder', '#folder'),
    ('new_link', '#link'),
    ('new_event', '#event'),
    ('new_image', '#image'),
    ('new_news', '#news-item'),
    ('new_document', '#document'),
    
    ('view_standard', '#folder_listing'),
    ('view_summary', '#folder_summary_view'),
    ('view_tabular', '#folder_tabular_view'),
    ('view_thumbnail', '#atct_album_view'),
    
    ('default_page', '#contextSetDefaultPage'),
    
    ('contentview_content', '#contentview-folderContents a'),
    ('contentview_view', '#contentview-view a'),
    ('contentview_edit', '#contentview-edit a'),
    ('contentview_rules', '#contentview-contentrules a'),
    ('contentview_sharing', '#contentview-local_roles a'),
    
    ('content_publish', '#workflow-transition-publish'),
    ('content_sendback', 'workflow-transition-reject'),
    
    ('form_apply', '#form\\.actions\\.apply'),
    ('form_save_old', 'input[name=form_submit]'),  # in Archetypes 1.5.10 (Plone 3.2.2)
    ('form_save', 'input[name=form\\.button\\.save]'),  # in Archetypes >= 1.5.11 (Plone >= 3.2.3)
    ('form_save_new', 'input[name=form\\.button\\.save]'),
    ('form_remove', 'input[name=form\\.button\\.remove]'),
    ('form_cancel', 'input[name=form\\.button\\.cancel]'),
    
    ('form_title', '#archetypes-fieldname-title input'),
    ('form_description', '#archetypes-fieldname-description textarea'),
    ('form_url', '#remoteUrl'),
    
    ('calendar_next', '#calendar-next'),
    ('calendar_previous', '#calendar-previous'),
    ('subtype_videocontainer', '#IVideoContainerEnhanced'),
    
    ('menu_sub-types', '#subtypes'),
    ('menu_display', '#plone-contentmenu-display'),
    ('menu_add-new', '#plone-contentmenu-factories'),
    ('menu_state', '#plone-contentmenu-workflow'),
)

class AmberjackStandardSteps(BrowserView): 
    def __call__(self, context, request):
        js = 'AjStandardSteps = {'
        for (key, value) in ajStandardSteps:
            js += "'%s':'%s',\n" % (key, value)
        
        js += '}'
        return js

