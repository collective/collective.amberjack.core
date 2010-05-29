/**
 * An "adapter-like" structure for making choises inside the highlightStep and doStep methods
 * 
 * the idea:
 * 
 * type_obj: {
 * 		highlight: function() {...},
 * 		step: function() {...}
 * },
 * ...
 * 
 */

AmberjackPlone.stepAdapters = {
	
	link: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			AmberjackPlone.setAmberjackCookies();
			location.href = obj.attr('href');
		}
	},
	button: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			obj.click();
		}
	},
	collapsible: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			if (value == 'collapse') 
				obj.removeClass('expandedInlineCollapsible').addClass('collapsedInlineCollapsible');
			else
				obj.removeClass('collapsedInlineCollapsible').addClass('expandedInlineCollapsible');
		}
	},
	text: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			changeValue(obj, value);
		}
	},
	select: {
		highlight: function(obj, type_obj, jq_obj, value) {
			var highlightThis = jq(obj + " option[value="+ AjSteps[num].getValue() +"]");
			highlightThis.addClass(AmberjackPlone.theAJClass);
			obj.addClass(AmberjackPlone.theAJClassBehaviour);
		},
		step: function(obj, type_obj, jq_obj, value) {
			AmberjackPlone.setAmberjackCookies();
			changeSelectValue(obj, value);
		}
	},
	checkbox: {
		highlight: function(obj, type_obj, jq_obj, value) {
			obj.parent().addClass(AmberjackPlone.theAJClass);
			obj.addClass(AmberjackPlone.theAJClassBehaviour);
		},
		step: function(obj, type_obj, jq_obj, value) {
	        if (obj.is(':checked'))
	            obj.attr('checked', false);
	        else
	            obj.attr('checked', true);
		}
	},
	radio: {
		highlight: null, // AmberjackPlone.stepAdapters.checkbox.highlight,
		step: null // AmberjackPlone.stepAdapters.checkbox.step
	},
	multiple_select: {
		highlight: function(obj, type_obj, jq_obj, value) {
			var tmp = AjSteps[num].getValue().split(",");
			for (var i=0;i<tmp.length;i++){
				jq("option[value="+tmp[i]+"]").addClass(AmberjackPlone.theAJClass);
			}
			obj.addClass(AmberjackPlone.theAJClassBehaviour);
		},
		step: function(obj, type_obj, jq_obj, value) {
			var tmp = value.split(",");
			for (var i=0;i<tmp.length;i++){
				jq("option[value="+tmp[i]+"]").attr("selected","selected");
			}
		}
	},
	form_text: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			var obj_contents = obj.contents().find('p');
	        obj_contents.replaceWith("<p>" + value + "</p>");
		}
	},
	form_save_new: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			var form = obj.parents("form");
			form.submit(function() {
				AmberjackPlone.setAmberjackCookies();
			});
			// For some reason, using form.submit ignores the kupu content...
			// ... so we simulate the click
			window.onbeforeunload = null;
			jq(obj).click();
		}
	},
	form_save: {
		highlight: null,
		step: null // AmberjackPlone.stepAdapters.form_save_new.step
	},
	form_actions_save: {
		highlight: null,
		step: null // AmberjackPlone.stepAdapters.form_save_new.step
	},
	form_save_default_page: {
		highlight: null,
		step: null // AmberjackPlone.stepAdapters.form_save_new.step
	},
	file: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			AmberjackBase.alert(this.aj_plone_consts['BrowseFile']);
		}
	},
	tiny_button_exec: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			tinyMCE.get('text').execCommand(value);
		}
	},
	tiny_button_click: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			tinyMCE.get('text').buttons[value].onclick();
		}
	},
	iframe_click: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			jq('.plonepopup iframe').contents().find(jq_obj).click();
		}
	},
	iframe_text: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			obj = jq('.plonepopup iframe').contents().find(jq_obj);
			changeValue(obj, value);
		}
	},
	iframe_select: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			AmberjackPlone.setAmberjackCookies();
			obj = jq('.plonepopup iframe').contents().find(jq_obj);
			changeSelectValue(obj, value);
		}
	},
	iframe_radio: {
		highlight: null,
		step: function(obj, type_obj, jq_obj, value) {
			obj = jq('.plonepopup iframe').contents().find(jq_obj);
			if (obj.is(':checked'))
	            obj.attr('checked', false);
	        else
	            obj.attr('checked', true);
		}
	}
	
};


AmberjackPlone.stepAdapters.radio.highlight = AmberjackPlone.stepAdapters.checkbox.highlight;
AmberjackPlone.stepAdapters.radio.step = AmberjackPlone.stepAdapters.checkbox.step;
AmberjackPlone.stepAdapters.form_save.step = AmberjackPlone.stepAdapters.form_save_new.step;
AmberjackPlone.stepAdapters.form_actions_save.step = AmberjackPlone.stepAdapters.form_save_new.step;
AmberjackPlone.stepAdapters.form_save_default_page.step = AmberjackPlone.stepAdapters.form_save_new.step;


