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
		
		
	/* collective.amberjack.windmill integration   @author: Andrea Benetti##################################################*/	
		w_click: {
			highlight: function(obj) {
				jq(obj).addClass(AmberjackPlone.theAJClass+' '+AmberjackPlone.theAJClassBehaviour)
				},
			step: function(obj,locator,options,locatorValue) {
			
					if(locator=='link'){
						AmberjackPlone.setAmberjackCookies();
						controller.click(obj)
					}
					else{
						if(jq(obj).attr('class')=='context'){
							jq(obj).click();	
							return;
						}
					controller.click(obj)
					}
				},
				
			checkStep: null
		},
		
		w_highlight:{
				
				highlight: function(locators){
					for(i=0; i<locators.length;i++){
						jq(locators[i]).addClass(AmberjackPlone.theAJClass)
					}
			
				},
				
				
				step:null,
				checkStep: null
			
			
		},

		w_type: {
			highlight: null,
			step: function(obj,locator,options,locatorValue) {
				var testo=options['text'];
				controller.type(obj,testo)
				},
			checkStep: function (obj, options,locatorValue) {
				var testo=options['text'];
	            if(testo!="") return jq(obj).val()==testo;
	            else return true;
	        }
		},
		
		w_select: {
			highlight: null,
			checkStep: null,
			step: function(obj,locator,options,locatorValue) {
				AmberjackPlone.setAmberjackCookies();
				for(var i in options){
					var opt=i;
					var value=options[i];
					controller.select(obj,opt, value);
					break;
				}
			}
		},
		
		w_check: {
			highlight: function(obj) {
				jq(obj).parent().addClass(AmberjackPlone.theAJClass);
				jq(obj).addClass(AmberjackPlone.theAJClassBehaviour);
				},
			step: function(obj,locator,options,locatorValue) {
				controller.check(obj)
				},
			checkStep: null
		},
		
		w_radio: {
			highlight: null, // AmberjackPlone.stepAdapters.checkbox.highlight,
			checkStep: null, // AmberjackPlone.stepAdapters.checkbox.checkStep,
			step:function(obj,locator,options,locatorValue) {
				controller.radio(obj)
				}
		},
		
		w_editor:{
			  highlight:function(obj){
				jq('#'+obj.id+'_ifr').addClass(AmberjackPlone.theAJClass);
				},
			  step:function(obj,locator,options,locatorValue) {
				  var tx=options['editor'];
				  tx=tx.replace(/&lt\;/g,'<');
				  tx=tx.replace(/&gt\;/g,'>')
				  controller.editor(tx,locatorValue);
				},
			  checkStep:null
			/*checkStep: function (obj,options,locatorValue) {
				  var tx=options['editor']
				  return (tinyMCE.get(locatorValue).getContent({format : 'text'}).replace(/<[^>]+>/gi, "")==tx || tinyMCE.get(locatorValue).getContent()==tx)
		        }*/
		},
		
		w_editorSelect:{
			highlight:null,
			step:function(obj,locator,options,locatorValue) {
				var bookmark=options['bookmark'];
				controller.editorSelect(locatorValue, bookmark);
				},
			checkStep:null
			/*checkStep: function (obj,options,locatorValue) {
				 var selected=options['text'];
				 return tinyMCE.get(locatorValue).selection.getContent({format : 'text'})==selected
	        }*/
			
		},
		
		
		/*###################################################################################################################*/	
		
	
	link: {
		highlight: null,
        checkStep: null,
		step: function(obj, type_obj, jq_obj, value) {
			AmberjackPlone.setAmberjackCookies();
			location.href = obj.attr('href');
		}
	},
	button: {
		highlight: null,
        checkStep: null,
		step: function(obj, type_obj, jq_obj, value) {
			obj.click();
		}
	},
	collapsible: {
		highlight: null,
        checkStep: function (obj, jq_obj, value) {
            if (value=="collapse") {
                return obj.hasClass("collapsedInlineCollapsible");
            }
            else return obj.hasClass("expandedInlineCollapsible");
        },
		step: function(obj, type_obj, jq_obj, value) {
			if (value == 'collapse') 
				obj.removeClass('expandedInlineCollapsible').addClass('collapsedInlineCollapsible');
			else
				obj.removeClass('collapsedInlineCollapsible').addClass('expandedInlineCollapsible');
		}
	},
	text: {
		highlight: null,
        checkStep: function (obj, jq_obj, value) {
            if(value!="") return obj.val()==value;
            else return true;
        },
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
        checkStep: function (obj, jq_obj, value) {
            if(value!="") return obj.val()==value;
            else return true;
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
        checkStep: function (obj, jq_obj, value) {
            return obj.attr("checked");
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
		checkStep: null, // AmberjackPlone.stepAdapters.checkbox.checkStep,
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
        checkStep: function (obj, jq_obj, value) {
            var tmp = value.split(",");
            var selected = true;
            for (var i=0;i<tmp.length;i++){
                //TODO
                //selected = selected && jq("option[value="+tmp[i]+"]").attr("selected","selected");
                selected = true;
            }
            return selected;
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
        checkStep: function (obj, jq_obj, value) {
            var obj_contents = obj.contents().find('p');
            return obj_contents.text() == value;
        },
		step: function(obj, type_obj, jq_obj, value) {
			var obj_contents = obj.contents().find('p');
	        obj_contents.replaceWith("<p>" + value + "</p>");
		}
	},
	form_save_new: {
		highlight: null,
        checkStep: null,
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
        checkStep: null,
		step: null // AmberjackPlone.stepAdapters.form_save_new.step
	},
	form_actions_save: {
		highlight: null,
        checkStep: null,
		step: null // AmberjackPlone.stepAdapters.form_save_new.step
	},
	form_save_default_page: {
		highlight: null,
        checkStep: null,
		step: null // AmberjackPlone.stepAdapters.form_save_new.step
	},
	file: {
		highlight: null,
        checkStep: null,
		step: function(obj, type_obj, jq_obj, value) {
			AmberjackBase.alert(this.aj_plone_consts['BrowseFile']);
		}
	},
	tiny_button_exec: {
		highlight: null,
        checkStep: null,
		step: function(obj, type_obj, jq_obj, value) {
			tinyMCE.get('text').execCommand(value);
		}
	},
	tiny_button_click: {
		highlight: null,
        checkStep: null,
		step: function(obj, type_obj, jq_obj, value) {
			tinyMCE.get('text').buttons[value].onclick();
		}
	},
	iframe_click: {
		highlight: null,
        checkStep: null,
		step: function(obj, type_obj, jq_obj, value) {
			jq('.plonepopup iframe').contents().find(jq_obj).click();
		}
	},
	iframe_text: {
		highlight: null,
        checkStep: function(obj, jq_obj, value) {
            obj = jq('.plonepopup iframe').contents().find(jq_obj);
            if(value!="") return obj.val()==value;
            else return true;
        },
		step: function(obj, type_obj, jq_obj, value) {
			obj = jq('.plonepopup iframe').contents().find(jq_obj);
			changeValue(obj, value);
		}
	},
	iframe_select: {
		highlight: null,
        checkStep: function(obj, jq_obj, value) {
            obj = jq('.plonepopup iframe').contents().find(jq_obj);
            if(value!="") return obj.val()==value;
            else return true;
        },
		step: function(obj, type_obj, jq_obj, value) {
			AmberjackPlone.setAmberjackCookies();
			obj = jq('.plonepopup iframe').contents().find(jq_obj);
			changeSelectValue(obj, value);
		}
	},
	iframe_radio: {
		highlight: null,
        checkStep: function(obj, jq_obj, value) {
            obj = jq('.plonepopup iframe').contents().find(jq_obj);
            return obj.attr("checked");
        },
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
AmberjackPlone.stepAdapters.radio.checkStep = AmberjackPlone.stepAdapters.checkbox.checkStep;
AmberjackPlone.stepAdapters.radio.step = AmberjackPlone.stepAdapters.checkbox.step;
AmberjackPlone.stepAdapters.form_save.step = AmberjackPlone.stepAdapters.form_save_new.step;
AmberjackPlone.stepAdapters.form_actions_save.step = AmberjackPlone.stepAdapters.form_save_new.step;
AmberjackPlone.stepAdapters.form_save_default_page.step = AmberjackPlone.stepAdapters.form_save_new.step;
