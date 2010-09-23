
var numberMicrostep=0;  //used to set the number of each microstep

/**
 * The model of a windmill microstep
 * 
 * @author Andrea Benetti
 * 
 * @param {String} method to execute (mandatory)
 * @param {String} locator (optional,depends on method passed,example {'option' : "optionValue",...})
 * @param {String} a string with method's options (optional,depends on method passed, example { "locatorValue" : 'locator'})
 */
function AjWindmillStep(method,locator,options,required,condition,description) {
	
	this._METHOD = method;
	this._LOCATOR = '';
	this._LOCVALUE='';	
	this._OPTIONS = '';
	this._CONDITION = condition;
	this._DESCRIPTION = description
	
	this._NUM=numberMicrostep;
	numberMicrostep++;
	
	if(windmillMethods[this._METHOD]['locator']){
		if( method !='highlight'){
			var dict=eval('('+locator+')')
			for(var k in dict){
				this._LOCATOR = dict[k];
				this._LOCVALUE = k;
				break;
    			}
		}
		else{
		if(locator!='{}' && locator !='')
			this._LOCATOR=eval('('+locator+')');	
		 }
	}
	
	if(windmillMethods[this._METHOD]['option']){
		
		if(this._METHOD=='type' || this._METHOD=='editor'){
			
			var startOp=options.indexOf(':');
			var end=options.lastIndexOf('\"');
			var sub=options.substring(startOp,end);
			var start=sub.indexOf('\"');
			sub=options.substring(start+startOp+1,end);
			sub = sub.replace(/"/g,'\\"');
			options=options.substring(0,startOp).trim()+' : "'+sub+'"}';
			}
		
		else if(this._METHOD=='editorSelect') {
			
				var startOp=options.indexOf(":");
				var pre=options.substring(0,startOp);
				var ind=pre.indexOf('bookmark');
				if(ind!=-1){ //text option after bookmark options
					var ind=0;
					var a=options;
					var count=0;
					for(k=0;k<10;k++){
                        ind=a.indexOf('"');
						a=a.substr(ind+1);
                        count+=ind+1;
					}
					start=options.indexOf('"',count)
					var end=options.lastIndexOf('"');
					var sub=options.substring(start+1,end);
					sub = sub.replace(/"/g,'\\"');
					options=options.substring(0,start+1).trim()+sub+'"}';
					
				}else{
					var ind=0;
					var a=options;
					for(k=0;k<10;k++){
						ind=a.lastIndexOf('"');
						a=a.substr(0,ind);
					}
					var end=a.lastIndexOf('"',ind);
					start=options.indexOf('"');
					var sub=options.substring(start+1,end);
					sub = sub.replace(/"/g,'\\"');
					options=options.substring(0,startOp).trim()+' : "'+sub+options.substr(end).trim();
				}
				
		}
		this._OPTIONS = eval('('+options+')');
	}
	
	this.getLocator= function() {
		if(this._METHOD=='highlight' && this._LOCATOR!=''){
			var curLocators=this._LOCATOR;
			var l=new Array();
			i=0;
			for(var k in curLocators){
					this._LOCATOR = curLocators[k];
					this._LOCVALUE= k;
					l[i]=this.getObj(this._LOCATOR,this._LOCVALUE);
					i+=1;
				}
			this._LOCATOR=curLocators;
			return l;
		}
		else
			return this._LOCATOR;
	};
	
	this.getMethod= function() {
		return this._METHOD;
	};
	
	this.getNum= function() {
		return this._NUM;
	};
	
	this.getLocValue= function() {
		return this._LOCVALUE;
	};
	
	this.getOptions= function() {
		return this._OPTIONS;
	};
	
	this.getCondition= function() {
		return this._CONDITION;
	};
	
	this.getDescription= function() {
		return this._DESCRIPTION;
	};

	this.highlightStep = function(){
		var metodo=this._METHOD;
		if(metodo=='highlight'){
			AmberjackPlone.stepAdapters['w_highlight'].highlight(this.getLocator());
			return;
			}
		try {
			obj = this.getObj(this._LOCATOR,this._LOCVALUE);
			} catch (e) {
				var msg = "Error in highlightStep(): Step " + (this._NUM+1) +" not found";
				AmberjackBase.alert(msg);
				AmberjackBase.log(msg, e);
				return false;
			}
		if(metodo.indexOf('waits.')!=-1 || metodo =='editorSelect') 
				return;
		if (obj && AmberjackPlone.stepAdapters['w_'+metodo] && AmberjackPlone.stepAdapters['w_'+metodo].highlight){
				if(obj.parentNode.tagName=='a' || obj.parentNode.tagName=='A')
					AmberjackPlone.stepAdapters['w_'+metodo].highlight(obj.parentNode);	
				else
					AmberjackPlone.stepAdapters['w_'+metodo].highlight(obj);
		}
		else if(obj) {
			jq(obj).addClass(AmberjackPlone.theAJClass+' '+AmberjackPlone.theAJClassBehaviour);
		}
		return;
		
	};
	
	this.checkStep = function(){
		
		var metodo=this._METHOD;
		if(metodo=='highlight') return true;
		var obj;
		try {
			obj = this.getObj(this._LOCATOR,this._LOCVALUE);
		} catch(e) {
			var msg = "Error in checkStep(): Step " + (this._NUM+1) +" not found"; 
			AmberjackBase.alert(msg);
			AmberjackBase.log(msg, e);
			return false;
		}
		
		if(jq(obj).parent().children('.required').length)
			if (jq(obj).val()=='') {
				var field_name = jq(obj).parent().children('label').text()
				var msg = "The field \"" + field_name + "\" can't be empty, it's required by Plone"; 
				AmberjackBase.alert(msg);
				return false;
			}
		
		var stepDone = true;
	    var stepCondition = this._CONDITION;
			 
        if (stepCondition && obj) {
			if (stepCondition == 'checkstep') {
				if (AmberjackPlone.stepAdapters['w_' + metodo] && AmberjackPlone.stepAdapters['w_' + metodo].checkStep) 
					stepDone = AmberjackPlone.stepAdapters['w_' + metodo].checkStep(obj, this._OPTIONS, this._LOCVALUE)
			}
			else 
				stepDone = this.checkCondition();
    	}
       	if (!stepDone)
			AmberjackBase.alert("Complete the step: \"" + AjSteps[steps[i]].getDescription() + "\"");        
       	return stepDone;
		
	};
	
	this.checkCondition = function(){
		var stepCondition = jq.parseJSON(this._CONDITION);
		var testo = stepCondition['value'];
		var operator = stepCondition['operator'];
		var selector = stepCondition['selector'];
		var locator = ""
		var locavalue = ""
		for (var x in selector) {
			locator = selector[x];
			locvalue = x;
		}
		var obj = this.getObj(locator,locvalue);
		switch (operator) {
			case 'eq': return jq(obj).val()==testo; break;
			case 'ne': return jq(obj).val()!=testo; break;
			case 'co': return Boolean(jq(obj).val().match(testo)); break;	
			case 'ne': return Boolean(jq(obj).val().match(testo)); break;
			default: return true;
		}
	};
	
	this.doStep = function(){
	
		var obj;
		var metodo=this._METHOD;
		try {
			obj = this.getObj(this._LOCATOR,this._LOCVALUE);
		} catch(e) {
			var msg = "Error in doStep(): Step " + (this._NUM+1) +" not found";
			AmberjackBase.alert(msg);
			AmberjackBase.log(msg, e);
			return false;
		}
			
		this.checkIfStyleList();

		var multSelect=this.checkifMultipleSelect(obj);
			
		if(multSelect==true)
			return;
		
		$(document).unbind('click');  //forbid exit from current context when click on document because the AmberjackControls is part of body
		if (AmberjackPlone.stepAdapters['w_'+metodo] && AmberjackPlone.stepAdapters['w_'+metodo].step && obj)
			AmberjackPlone.stepAdapters['w_'+metodo].step(obj,this._LOCATOR,this._OPTIONS,this._LOCVALUE);
			
	};
	
	
	this.getObj= function(locator,locvalue) {
		  var element = null;
		  //If a link was passed, lookup as link
		  if(locator =='link') {
		    element = elementslib.Element.LINK(locvalue);
		  }
		  //if xpath was passed, lookup as xpath
		  else if(locator=='xpath') {        
		    element = elementslib.Element.XPATH(locvalue);
		  }
		  
		  //if id was passed, do as such
		  else if(locator=='id') {
		    element = elementslib.Element.ID(locvalue);
		  }
		   
		  //if jsid was passed
		  else if(locator=='jsid') {
		    var jsid = window.eval(locvalue);
		    element = elementslib.Element.ID(jsid);
		  }
		  //if name was passed
		  else if(locator=='name') {
		    element = elementslib.Element.NAME(locvalue);
		  }
		  //if value was passed
		  else if(locator=='value') {
		    element = elementslib.Element.VALUE(locvalue);
		  }
		  //if classname was passed
		  else if(locator=='classname') {
		    element = elementslib.Element.CLASSNAME(locvalue);
		  }
		  //if tagname was passed
		  else if(locator=='tagname') {
		    element = elementslib.Element.TAGNAME(locvalue);
		  }
		  //if label was passed
		  else if(locator=='label') {
		    element = elementslib.Element.LABEL(locvalue);
		  }
		  //if jquery was passed
		  else if(locator=='jquery') {
			  locvalue = helpers.repAll(locvalue, ").", ")<*>");
		    var jQ = jQuery(window.document);
		    var chain= locvalue.split('<*>');
		    
		    locvalue= helpers.repAll(locvalue, "<*>", ".");
		    var start = eval('jQ.find'+chain[0]);
		    var theRest = locvalue.replace(chain[0],'');
		    element = eval('start'+theRest);
		  }
		  return element;

	};
	
	//check if the previous microstep was a click for open tiny drop-down style list
	this.checkIfStyleList= function(){
		var num=this._NUM
		if(tinyMCE.activeEditor){
			while(num-1>=0 && (AjSteps[num-1].getMethod()=='highlight' || AjSteps[num-1].getMethod().indexOf('waits.')!=-1))
				num=num-1;
			if(num-1>=0){
			         if(AjSteps[num-1].getLocValue()==tinyMCE.activeEditor.id+'_style_text_text' || AjSteps[num-1].getLocValue()==tinyMCE.activeEditor.id+"_style_text_open"){  //if in the previous microstep i opened the tiny drop-down style list, now i want to select an entry.
						   AmberjackPlone.stepAdapters['w_'+AjSteps[num-1].getMethod()].step(AjSteps[num-1].getObj(this._LOCATOR,this._LOCVALUE),AjSteps[num-1].getLocator(),AjSteps[num-1].getOptions(),AjSteps[num-1].getLocValue());
				}
			}
		}
		
	};
	
	
	//perform microstep if i clicked on an option of a multiple selection list
	this.checkifMultipleSelect= function(element){
	   			
			if(this._LOCATOR=='value'){
	   				var parent=jQuery(element).parent().get(0);
	   				if(parent && parent.tagName.toLowerCase()=='select')
	   					if(jQuery(element).parent().attr("multiple")){
	   						if(jQuery(element).attr("selected")==true)
	   								jQuery(element).removeAttr("selected");
	   						else
	   								jQuery(element).attr("selected","selected");
	   						return true;
	   					}
	   			}
			return false;
	};
	
	
};


/**
 * Change the value of a textbox
 * @author Giacomo Spettoli
 *
 * @param obj object to modify
 * @param value new value of the object
 */
function changeValue(obj, value){
	obj.focus();
	obj.val(value);
	obj.blur();
}

// BBB -- this function maybe is not usefull... jQuery can perform this in one line?!
function changeSelectValue(obj, value){
	var o = obj[0].options;   
	var oL = o.length;
	for(var i = 0; i<oL; i++){
	  if (o[i].value == value){
	      o[i].selected = true;
	  }
	}
	
	jq(obj[0]).trigger('change', true);
}


AmberjackPlone = {
    /**
     * some utility constants
     */
    aj_xpath_exists:     'aj_xpath_exists',    // used to just check if a given xpath exists on a page
    aj_any_url:          'aj_any_url',         // we accept any url in the title
	aj_plone_consts:     {},                   // all the plone constants we need to check
    aj_canMove_validators: ['validationError'],// set of use case in which aj cannot go further to the next step

	theAJClass: 'ajHighlight',
	theAJClassBehaviour: 'ajedElement',

	init: function() {
		AmberjackPlone.highlightAllSteps();
		AmberjackPlone.ajTour();
	    // restore previous window position
	    AmberjackPlone.restoreWindowPosition()
		AmberjackPlone.disableLinks();
	    var last_step = jq('#ajControl').find('#ajLastStep')
	    // if it's the last step add this tour to the completed cookie
	    if (last_step.length !== 0){
	        completed = Amberjack.readCookie('ajcookie_completed')
	        if(completed){
	            completed = completed + '#another one'
	        } else {
	            completed = 'first one'
	        }
	        Amberjack.createCookie('ajcookie_completed', completed, 1);
	    }
		jq('#ajControl').draggable({ 
	                        handle: '#ajControlNavi', 
	                        cursor: 'crosshair',
	                        containment: 'body',
	                        stop: function(event, ui) {
	                            Amberjack.createCookie('ajcookie_controlposition', ui.position.left + "#" + ui.position.top, 10);
	                        }
	                    })
	                    
		jq('#ajControlNavi').css('cursor', 'move')
	},

    
	/**
	 *  checks if saving an object we get a validation error
	 */
	validationError: function(){
		return !(
		  (jq('#region-content dl.portalMessage.error dt').text() == this.aj_plone_consts['Error']) &
		  (jq('#region-content dl.portalMessage.error dd').text() == this.aj_plone_consts['ErrorValidation'])
		  )
	},
	
	canMoveToNextStep: function(){
        canMove = true
	    for (i = 0; i < this.aj_canMove_validators.length; i++){
			canMove = (canMove & this[this.aj_canMove_validators[i]]())
	    }
		return canMove
	}, 
    
    restoreWindowPosition: function(){
        coords = Amberjack.readCookie('ajcookie_controlposition')
        if (coords){
            point = coords.split('#')
            jq('#ajControl').css('left', point[0]+'px').css('top',point[1]+ 'px');
        } else {
            var winW = jq(window).width();
            var startPosition = winW/2-jq('#ajControl').width()/2; 
            jq('#ajControl').css('left', startPosition + 'px').css('top','30px');
        }
    },
	
	/**
	 * Highlight all current page's steps
	 * @author Giacomo Spettoli
	 */
	highlightAllSteps: function() {
		var steps = AmberjackPlone.getPageSteps();
		for(var i=0; i < steps.length;i++){
			 AjSteps[steps[i]].highlightStep()
		}
	},


	/**
	 * Utility function that prepare the page for the tour.
	 * sets the plone elements that can be "pressed" as "highlight"
	 * next we need to alert the user if he tries to click somewhere else..
	 * 
	 * @author Massimo Azzolini
	 * @author Giacomo Spettoli
	 */
	ajTour: function() {
		
		jq('.' + AmberjackPlone.theAJClassBehaviour).click(function() {
			AmberjackPlone.setAmberjackCookies();
		});
		
		// manages the << >> buttons
		var ajNext = jq('#ajNext');
		var ajPrev = jq('#ajPrev');
		
		ajNext.click(AmberjackPlone.setAmberjackCookies);
		
		// jq(".ajSteps a").click(AmberjackPlone.doStep);
	},

	/**
	 * Function for disabling all links that can break the tour.
	 * @author Giacomo Spettoli
	 * @author Massimo Azzolini
	 */
	disableLinks: function() {
		if (Amberjack.pageId) {
			var notAj = jq("a").not(".ajHighlight,.ajedElement,[id^='aj'],[class^='aj']");
			//NOTE: we assume that there are no other 'ajXXX' ids
			notAj.click(function(){
				AmberjackBase.alert("You cannot click on other links, please use the console's exit button");
				return false;
			});
			notAj.addClass("aj_link_inactive");
			var actionAjtour = jq("#ajtour").addClass("aj_link_inactive");
			var ajClose = jq("#ajClose");
			var goHome = false;
			
			var sURL = unescape(window.location.pathname);
			if(goHome)
				ajClose.attr("onClick","Amberjack.close();location.href='" + Amberjack.BASE_URL + "';return false");
			else
				ajClose.attr("onClick","Amberjack.close();location.href = window.location.pathname;return false");	

			var ajNext = jq("#ajNext");
			
			// BBB
			ajNext.attr("onClick","AmberjackPlone.doAllSteps(); return false");
		}
	},


	/**
	 * Function for doing steps
	 * @author Giacomo Spettoli
	 * 
	 * @param num dictionary's label of the step
	 * 
	 */
	doStep: function(step) {
		
		var allClasses = jq(step).attr("class").split(" ");
		var firstClass = allClasses[0].split('-');
		var num = parseInt(firstClass[1])-1;
        
        var prevStepDone = AmberjackPlone.checkPreviousSteps(num) 
        if (!prevStepDone)
            return prevStepDone;
        
        AjSteps[num].doStep();
        
	}, 
	
	/**
	 * Function for doing all step
	 * @author Mirco Angelini
	 */
	doAllSteps: function() {
		
		var steps = AmberjackPlone.getPageSteps();
		for(var i = 0; i < steps.length; i++) {
			var prevStepDone = AmberjackPlone.checkPreviousSteps(steps[i])
			if (!prevStepDone) 
				return prevStepDone;
			AjSteps[steps[i]].doStep();
		}
	}, 
	
    /**
     * Check all current page's steps
     * @author Giacomo Spettoli
     * 
     * @return true if all steps done else false
     */
    checkAllSteps: function(){
        var steps = AmberjackPlone.getPageSteps();
        return AmberjackPlone.checkPreviousSteps(steps[steps.length-1]);
    },

  
    /**
     * Check that all the previous steps have been done.
     *  
     * @param num dictionary's label of the actual step, 0 means all
     * @return true if done else false
     */
    checkPreviousSteps:function(num){
        var allDone = true;
        var thisStep = true;
        var steps = AmberjackPlone.getPageSteps();
        
        for (var i = 0; i < steps.length && steps[i] < num; i++) {
            thisStep = AjSteps[steps[i]].checkStep();
            if(!thisStep){
                allDone = false;
                break;
            }
            allDone = allDone && thisStep;
        }
        return allDone;
    },
   	

	/**
	 * Get all current page's step
	 * @author Giacomo Spettoli
	 * @return steps array of current page step's id
	 */
	getPageSteps: function() {
		var steps = [];
		if(Amberjack.pageId){
			var link = jq(Amberjack.pages[Amberjack.pageId].content).find('a[class^="ajStep"]');
			link.each(function(i){
				var allClasses = jq(this).attr('class').split(' ');
				var firstClass = allClasses[0].split('-');
				steps.push(parseInt(firstClass[1])-1);
			});
		}
		return steps;
	},


	/*
	 * BBB: refactor the calls to this function
	 */
	setAmberjackCookies: function(){
		Amberjack.createCookie('ajcookie_tourId', Amberjack.tourId, 1);
	    Amberjack.createCookie('ajcookie_skinId', Amberjack.skinId, 1);
		Amberjack.createCookie('ajcookie_pageCurrent', Amberjack.pageCurrent + 1)
	}


}


/* 
 * @author Mirco Angelini
 */
var handledFunctions = ['mcTabs','displayPanel','getFolderListing','tinyMCEPopup','getCurrentFolderListing'];

var popup_interval = setInterval(function(){
	if(jq('.plonepopup iframe').length){
		clearInterval(popup_interval);
		var element_interval = setInterval(function(){
			if(jq("a[href^=javascript\\:]", jq('.plonepopup iframe').contents()).length){
				clearInterval(element_interval);
				jq.each(jq("a[href^=javascript\\:]", jq('.plonepopup iframe').contents()), function(key, value){
					var old_href = value.href;
					for (var i=0;i<handledFunctions.length;i++)
						old_href = old_href.replace(handledFunctions[i],'window.frames[1].'+handledFunctions[i]);
					var new_href = unescape(old_href.substring(11));
					jq(value).bind('click', function(e){
						e.preventDefault;
						eval(new_href);
					});
					value.href = 'javascript:;';
				})
			}
		}, 300)
	}
}, 300);


/**
 * Start the tour and set some timeout
 * @author Giacomo Spettoli
 */

jq(document).ready(function () {
	loadDefaults();
	Amberjack.open();
	setTimeout(AmberjackPlone.init, 300);
});
