Creates a new tour
------------------

First of all you need to define the tour.

A tour has this shape:

    {'tourId': u'example_tour',
     'title': _(u"Example tour"),
     'steps': <steps>}

<steps> has this shape:

    ({'url': u'/',
      'xpath': u'',
      'xcontent': u'',
      'title': _(u"Some title"),
      'text': _(u"Some text"),
      'steps': ({'description': _(u"Some description"),
                 'idStep': u'',
                 'selector': u'',
                 'text': u''},
                ...
               )       
     },
     ...
    )                     
                      
The set of current tour's steps:

* the description for the user (use [] to <span class="ajHighlight">highlight</span> parts), 
* the step id, [see ajStandardSteps section below]
* an optional selector
* an optional text used by the step

An example:

    >>> add_folder = {
    >>>			   'url': u'/',
    >>>            'xpath': u'',
    >>>            'xcontent': u'',
    >>>            'title': _(u"Create a new folder"),
    >>>            'text': _(u"Folders are ..."),
    >>>            'steps': ({'description': _(u"Click the [Add new...] drop-down menu."),
    >>>                       'idStep': u'menu_add-new',
    >>>                       'selector': u'',
    >>>                       'text': u''},
    >>>                      {'description': _(u"Select [Folder] from the menu."),
    >>>                       'idStep': u'new_folder',
    >>>                       'selector': u'',
    >>>                       'text': u''})}
    >>> 
    >>> ajTour = {'tourId': u'basic01_add_a_folder',
    >>>           'title': _(u'Add a Folder'),
    >>>           'steps': (add_folder,
    >>>                    )}


Then you have to register it.

    >>> <collective.amberjack:tour
    >>>         tourdescriptor=".example_tour.ajTour"
    >>>         />

ajStandardSteps
---------------

* link : click on the link, need a selector to <a>
* button : click on the button, need a selector to a <input type="button|submit|reset|...">
* collapsible : if [value] is "collapse", switch the class of the element from expandedInlineCollapsible to collapsedInlineCollapsible, else the contrary
* select : replace the value of the element
* text : replace the value of the element
* checkbox : if [value] is "checked", then check the element, else uncheck
* radio : if [value] is "checked", then check the element, else uncheck
* multiple_select : select the options with value given by [value] (can be a list separated by coma without space)
* manage_portlets : click on the Manage portlets   
* go_home', '#portal-breadcrumbs > a'),
* go_uplevel', '#portal-breadcrumbs span a:last'),
    
* site_sitemap', '#siteaction-sitemap a'),
* site_accessibility', '#siteaction-accessibility a'),
* site_contact', '#siteaction-contact a'),
* site_setup', '#siteaction-plone_setup a'),
    
* action_cut : for perform cut operation
* action_copy : for perform copy operation
* action_delete : for perform delete operation
* action_rename : for perform rename operation
    
* new_folder : for add a new folder
* new_link : for add a new link
* new_event : for add a new event
* new_image : for add a new image
* new_news : for add a new news-item
* new_document : for add a new document
* new_file : for add a new file
    
* view_standard : for call folder_listing_view,
* view_summary : for call folder_summary_view
* view_tabular : for call folder_tabular_view,
* view_thumbnail : for call atct_album_view,
    
* default_page', '#contextSetDefaultPage'),
    
* contentview_content', '#contentview-folderContents a'),
* contentview_view', '#contentview-view a'),
* contentview_edit', '#contentview-edit a'),
* contentview_rules', '#contentview-contentrules a'),
* contentview_sharing', '#contentview-local_roles a'),
    
* content_publish', '#workflow-transition-publish'),
* content_sendback', '#workflow-transition-reject'),
    
* form_apply', '#form\\.actions\\.apply'),
* form_save', 'input[name=form\\.button\\.save]'),  # in Archetypes >= 1.5.11 (Plone >= 3.2.3)
* form_save_default_page', 'input[name=form\\.button\\.Save]'),  # in contextSetDefaultPage there's a capital letter 
* form_actions_save', 'input[name=form\\.actions\\.save]'), #BBB has problems
* form_remove', 'input[name=form\\.button\\.remove]'),
* form_cancel', 'input[name=form\\.button\\.cancel]'),
    
* form_title', '#archetypes-fieldname-title input'),
* form_description', '#archetypes-fieldname-description textarea'),
* form_text', '#archetypes-fieldname-text iframe'),
* form_location', '#archetypes-fieldname-location input'),
* form_url', '#remoteUrl'),
    
* form_header', 'input[id="form\\.header"]'),
* form_footer', 'input[id="form\\.footer"]'),
    
* folder_copy', 'input[name="folder_copy:method"]'),
* folder_cut', 'input[name="folder_cut:method"]'),
* folder_paste', 'input[name="folder_paste:method"]'),
* folder_delete', 'input[name="folder_delete:method"]'),
* folder_rename', 'input[name="folder_rename_form:method"]'),
* content_status_history', 'input[name="content_status_history:method"]'),
    
* image_title', '#title'),
* image_description', '#description'),
* image_file', '#image_file'),
* image_save', '.formControls input.context'),
* file_file', '#file_file'),
    
* button_bold', '#kupu-bold-button'),
* button_italic', '#kupu-italic-button'),
* button_justify', '#kupu-bg-justify'),
* button_justify_left', '#kupu-justifyleft-button'),
* button_justify_center', '#kupu-justifycenter-button'),
* button_justify_rigth', '#kupu-justifyright-button'),
* button_internal_link', '#kupu-linklibdrawer-button'),
* button_external_link', '#kupu-linkdrawer-button'), 
* button_insert_image', '#kupu-imagelibdrawer-button'),
* button_dialog_ok', '#kupu-librarydrawer div.kupu-dialogbuttons button.kupu-dialog-button'), # there are 3 buttons of the same kind
* button_dialog_cancel', '#kupu-librarydrawer div.kupu-dialogbuttons button.kupu-dialog-button'), # there are 3 buttons of the same kind
* button_dialog_reload', '#kupu-librarydrawer div.kupu-dialogbuttons button.kupu-dialog-button'), # there are 3 buttons of the same kind
* text_area','#kupu-editor-iframe-text'), #* text_area','#kupu-editor-text .ajHighlight'),
* preview', '#linkdrawer-preview'),
* image_align_left', '#image-align-left'),

    
* link_to_home', '#root'),
* radio_button_welcome_to_plone', '#5eaaf087c2c71011ec51b44776235ae5'),
    
* calendar_next', '#calendar-* ,
* calendar_previous', '#calendar-previous'),
* subtype_videocontainer', '#IVideoContainerEnhanced'),
    
* menu_sub-types', '#subtypes'),
* menu_display', '#plone-contentmenu-display'),
* menu_add-new', '#plone-contentmenu-factories'),
* menu_state', '#plone-contentmenu-workflow'),

Meta directive registration
===========================

collective.amberjack.core provides useful tour registration using zcml approach. 
First we need to include meta.zcml in our package::
	
	>>> from Products.Five import zcml
	>>> import collective.amberjack.core
	>>> zcml.load_config('meta.zcml', collective.amberjack.core)
		
Than registration is as simple as::

    >>> simple_directive = '''
    ... <collective.amberjack:tour
    ...     tourdescriptor="collective.amberjack.core.tests.DummyTour"
    ... />'''
    >>> config_zcml = template % simple_directive
    >>> zcml.load_string(config_zcml) 

Let's check the TourDefinition utility to see our dummy tour::

	>>> from collective.amberjack.core.interfaces import ITourDefinition
	>>> from zope.component import getUtility
	>>> tour = getUtility(ITourDefinition, name='dummy_id')
	>>> tour.title
	u'Dummy title'

