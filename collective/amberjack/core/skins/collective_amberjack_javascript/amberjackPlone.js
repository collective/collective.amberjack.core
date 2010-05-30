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
			AmberjackPlone.highlightStep(steps[i]);
		}
	},

	/**
	 * Highlight the step for better view
	 * @author Giacomo Spettoli
	 * 
	 * @param num dictionary's label of the step
	 */
	highlightStep: function(num) {
		if(Amberjack.pageId){
			var obj;
			try {
				obj = AjSteps[num].getObj();
			} catch (e) {
				var msg = "Error in highlightStep(): Step " + (num+1) +" not found";
				AmberjackBase.alert(msg);
				AmberjackBase.log(msg, e);
				return false;
			}
			var type_obj = AjSteps[num].getType();
			
			if (AmberjackPlone.stepAdapters[type_obj] && AmberjackPlone.stepAdapters[type_obj].highlight)
				AmberjackPlone.stepAdapters[type_obj].highlight(obj, type_obj, null, null);	
			else if (type_obj.match("menu")){
				obj.children('dt').children('a').addClass(AmberjackPlone.theAJClass+' '+AmberjackPlone.theAJClassBehaviour);
			}
			else {
				obj.addClass(AmberjackPlone.theAJClass+' '+AmberjackPlone.theAJClassBehaviour);
			}
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
	 * BBB needs to be revised: type_obj is not a complete range of all the cases
	 */
	doStep: function(step) {
		var obj, type_obj, jq_obj, value;
		var allClasses = jq(step).attr("class").split(" ");
		var firstClass = allClasses[0].split('-');
		var num = parseInt(firstClass[1])-1;
        
        var prevStepDone = AmberjackPlone.checkPreviousSteps(num) 
        if (!prevStepDone)
            return prevStepDone;
	
		try {
			obj = AjSteps[num].getObj();
			type_obj = AjSteps[num].getType();
			jq_obj = AjSteps[num].getJq();
			value = AjSteps[num].getValue();
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
            var type_obj = AjSteps[steps[i]].getType();
            thisStep = AmberjackPlone.checkStep(steps[i]);
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
	 * Check that the step has been done.
	 * @author Giacomo Spettoli
	 *  
	 * @param num dictionary's label of the step
	 * @return true if done else false
	 */
	checkStep: function(num) {
		var obj;
		try {
			obj = AjSteps[num].getObj();
		} catch(e) {
			var msg = "Error in checkStep(): Step " + num +" not found"; 
			AmberjackBase.alert(msg);
			AmberjackBase.log(msg, e);
			return false;
		}
		
		var type_obj = AjSteps[num].getType();
        var jq_obj = AjSteps[num].getJq();
		var value = AjSteps[num].getValue();
		var stepDone = true;
        var stepRequired = true;
        
        if (stepRequired) {
            if (AmberjackPlone.stepAdapters[type_obj] && AmberjackPlone.stepAdapters[type_obj].checkStep)
                stepDone = AmberjackPlone.stepAdapters[type_obj].checkStep(obj, jq_obj, value)
            else if (value!="") {
                stepDone = obj.val()==value;
            }
        }
        return stepDone;
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
