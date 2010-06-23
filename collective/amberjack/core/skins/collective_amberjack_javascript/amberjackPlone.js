/**
 * The model of a single step of the tour.
 * 
 * @param {String} type the type of action for this step. See ajStandardSteps.py
 * @param {String} jq a jQuery selector
 * @param {String} value an optional value (depends on type choosen)
 */
function AjStep(type, jqElement, value) {
	this._JQ = jqElement;
	this._TYPE = type;
	this._VALUE = value;
	
	
	this.getJq= function() {
		return this._JQ;
	};
	
	this.getType= function() {
		return this._TYPE;
	};
	
	this.getValue= function() {
		return this._VALUE;
	};
	
	this.getObj= function() {
		var type_obj = this._TYPE;
		if(this._JQ=='') return jq(AjStandardSteps[this._TYPE]);
		else return jq(this._JQ);
	};
	
   /* Highlight the step for better view
	* @author Giacomo Spettoli*/
	 this.highlightStep = function(){
		try {
			obj = this.getObj();
			} catch (e) {
			var msg = "Error in highlightStep(): Step " + (num+1) +" not found";
			AmberjackBase.alert(msg);
			AmberjackBase.log(msg, e);
			return false;
			}
			var type_obj = this._TYPE;
		
			if (AmberjackPlone.stepAdapters[type_obj] && AmberjackPlone.stepAdapters[type_obj].highlight)
				AmberjackPlone.stepAdapters[type_obj].highlight(obj, type_obj, null, null);	
			else if (type_obj.match("menu")){
				obj.children('dt').children('a').addClass(AmberjackPlone.theAJClass+' '+AmberjackPlone.theAJClassBehaviour);
			}
			else {
				obj.addClass(AmberjackPlone.theAJClass+' '+AmberjackPlone.theAJClassBehaviour);
			}
		}
	 
	 
	 /* Check that the step has been done.
	 * @author Giacomo Spettoli*/
	 this.checkStep = function(){
		 
			var obj;
			try {
				obj = this.getObj();
			} catch(e) {
				var msg = "Error in checkStep(): Step " + num +" not found"; 
				AmberjackBase.alert(msg);
				AmberjackBase.log(msg, e);
				return false;
			}
			
			var stepDone = true;
		    var stepRequired = true; 
		    var type_obj = this._TYPE;
		    var jq_obj = this._JQ;
		    var value = this._VALUE;
		        
		        if (stepRequired) {
		            if (AmberjackPlone.stepAdapters[type_obj] && AmberjackPlone.stepAdapters[type_obj].checkStep)
		                stepDone = AmberjackPlone.stepAdapters[type_obj].checkStep(obj, jq_obj, value)
		            else if (value!="") {
		                stepDone = obj.val()==value;
		            }
		        }
		        return stepDone;
		 
	 }
	 
	 /* Function for doing step
	  * @author Giacomo Spettoli*/
	 this.doStep = function(){
			var obj, type_obj, jq_obj, value;
			
			try {
				obj = this.getObj();
				type_obj = this._TYPE;
				jq_obj = this._JQ;
				value = this._VALUE;
			} catch(e) {
				var msg = "Error in doStep(): Step " + num +" not found";
				AmberjackBase.alert(msg);
				AmberjackBase.log(msg, e);
				return false;
			}
		    
			if (AmberjackPlone.stepAdapters[type_obj] && AmberjackPlone.stepAdapters[type_obj].step)
				AmberjackPlone.stepAdapters[type_obj].step(obj, type_obj, jq_obj, value);		
			else if (value!="") {
				changeValue(obj, value);
			}
			else if (type_obj.match("menu")) {
				if (value=='deactivate') obj.removeClass('activated').addclass('deactivated');
				else obj.removeClass('deactivated').addClass('activated');
			}
			else if (jq_obj=="") {
				obj.click(function(){
		            AmberjackPlone.setAmberjackCookies()
				});	
				obj.click();
				if (obj.attr("href"))
					location.href = obj.attr("href");
			}
	 }
	
};

/**
 * The model of a windmill microstep
 * 
 * @author Andrea Benetti
 * 
 * @param {String} method to execute (mandatory)
 * @param {String} locator (optional,depends on method passed,example: "'locator'^>'locatorValue'")
 * @param {String} a string with method's options (depends on method passed, example: "'optionName'<^'optionValue'^>...")
 */
function AjWindmStep(method,locator,options) {
	
	this._METHOD = method;
	this._LOCATOR = '';
	this._LOCVALUE='';	
	this._OPTIONS = '';
	
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
					l[i]=this.getObj();
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
	
	this.getLocValue= function() {
		return this._LOCVALUE;
	};
	
	this.getOptions= function() {
		return this._OPTIONS;
	};
	

	this.highlightStep = function(){
		var metodo=this._METHOD;
		if(metodo=='highlight'){
			AmberjackPlone.stepAdapters['w_highlight'].highlight(this.getLocator());
			return;
			}
		try {
			obj = this.getObj();
			} catch (e) {
				var msg = "Error in highlightStep(): Step " + (num+1) +" not found";
				AmberjackBase.alert(msg);
				AmberjackBase.log(msg, e);
				return false;
			}
		if(metodo.indexOf('waits.')!=-1 || metodo =='editorSelect') return;
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
			obj = this.getObj();
		} catch(e) {
			var msg = "Error in checkStep(): Step " + num +" not found"; 
			AmberjackBase.alert(msg);
			AmberjackBase.log(msg, e);
			return false;
		}
		
		var stepDone = true;
	    var stepRequired = true;
			 
       	        if (stepRequired && obj) {
		            if (AmberjackPlone.stepAdapters['w_'+metodo] && AmberjackPlone.stepAdapters['w_'+metodo].checkStep)
		                stepDone = AmberjackPlone.stepAdapters['w_'+metodo].checkStep(obj,this._OPTIONS,this._LOCVALUE)
		        }
       	        
       	        return stepDone;

		
	};
	
	this.doStep = function(){
		var obj;
		var metodo=this._METHOD;
		try {
			obj = this.getObj();
			} catch(e) {
			var msg = "Error in doStep(): Step " + num +" not found";
			AmberjackBase.alert(msg);
			AmberjackBase.log(msg, e);
			return false;
			}
			
			$(document).unbind('click');  //forbid exit from current context when click on document because the AmberjackControls is part of body
		if (AmberjackPlone.stepAdapters['w_'+metodo] && AmberjackPlone.stepAdapters['w_'+metodo].step)
			AmberjackPlone.stepAdapters['w_'+metodo].step(obj,this._LOCATOR,this._OPTIONS,this._LOCVALUE)
			
	};
	
	this.getObj= function() {
		  var element = null;
		  //If a link was passed, lookup as link
		  if(this._LOCATOR =='link') {
		    element = elementslib.Element.LINK(this._LOCVALUE);
		  }
		  //if xpath was passed, lookup as xpath
		  else if(this._LOCATOR=='xpath') {        
		    element = elementslib.Element.XPATH(this._LOCVALUE);
		  }
		  
		  //if id was passed, do as such
		  else if(this._LOCATOR=='id') {
		    element = elementslib.Element.ID(this._LOCVALUE);
		  }
		   
		  //if jsid was passed
		  else if(this._LOCATOR=='jsid') {
		    var jsid = window.eval(this._LOCVALUE);
		    element = elementslib.Element.ID(jsid);
		  }
		  //if name was passed
		  else if(this._LOCATOR=='name') {
		    element = elementslib.Element.NAME(this._LOCVALUE);
		  }
		  //if value was passed
		  else if(this._LOCATOR=='value') {
		    element = elementslib.Element.VALUE(this._LOCVALUE);
		  }
		  //if classname was passed
		  else if(this._LOCATOR=='classname') {
		    element = elementslib.Element.CLASSNAME(this._LOCVALUE);
		  }
		  //if tagname was passed
		  else if(this._LOCATOR=='tagname') {
		    element = elementslib.Element.TAGNAME(this._LOCVALUE);
		  }
		  //if label was passed
		  else if(this._LOCATOR=='label') {
		    element = elementslib.Element.LABEL(this._LOCVALUE);
		  }
		  //if jquery was passed
		  else if(this._LOCATOR=='jquery') {
			  this._LOCVALUE = helpers.repAll(this._LOCVALUE, ").", ")<*>");
		    var jQ = jQuery(window.document);
		    var chain= this._LOCVALUE.split('<*>');
		    
		    this._LOCVALUE= helpers.repAll(this._LOCVALUE, "<*>", ".");
		    var start = eval('jQ.find'+chain[0]);
		    var theRest = this._LOCVALUE.replace(chain[0],'');
		    element = eval('start'+theRest);
		  }
		  return element;

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
			ajNext.attr("onClick","if (AmberjackPlone.checkAllSteps()) {" + ajNext.attr('onClick') + "}");
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
                AmberjackBase.alert("Step " + (steps[i]+1) + " not completed");
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
