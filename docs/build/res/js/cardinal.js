/*!
 * Cardinal (WebAidBox) 
 * cardinal.js v 1.0
 * @Author Adepitan Caleb
 * Caleb Pitan for short or say it's wha'I prefer [grin]
 * Twitter, Instagram: RealLongman
 * https://webpaddy.blogspot.com/
 * Copyright 2018 RealLongman, Adepitan Caleb
 *
 * Dependencies : jQuery;
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 */

 !function($,global,doc) {

	"use-strict";
	

 	function Navigation() {
 		['foreign code'];
	}
	function Rectangle(x1=-1,y1=-1, x2=-1,y2=-1) {
		this.coordsX = {
			x1 : x1,
			x2 : x2
		}
		this.coordsY = {
			y1 : y1,
			y2 : y2
		}
	}
	
	
	var opacity = "opacity",
		display = "display",
		left = "left",
		right = "right",
		style = "ease",
		effect = "transition",
		hash = "menu",
		back = "back",
		forth = "forth",
		unit = "px";

	(function(){
		var logged = false;
		var iLogged = false;
		function checkRequirements() {
			
			if(jQueryNotInstalled() && !logged)
				displayError("jQuery not installed"), logged = true;
			if(!jQueryNotInstalled() && !iLogged)
				displayStr("jQuery found!"), clearInterval(checkRequirements), iLogged = true;
		}
		setInterval(checkRequirements, 600);	
	})();

	//Rectangle class useful later around the navigation drawer
	Rectangle.prototype.getWidth = function() {
		return Math.abs(this.coordsX.x2 - this.coordsX.x1);
	}
	Rectangle.prototype.getHeight = function() {
		return Math.abs(this.coordsY.y2 - this.coordsY.y1);
	}
	Rectangle.prototype.wGTh = function() {
		return this.getWidth() > this.getHeight()
	}
	Rectangle.prototype.hGTw = function() {
		return !this.wGTh();
	}
	 
 	Navigation.fn = Navigation.prototype = {
		
 		constructor: Navigation,

		deviceWidth: ((global.screen.availWidth + global.innerWidth)/2),
		 
 		drawable: {
 			allowBackdrop: !0,
 			nextaction: forth
		},
		 
 		hash: {
 			allowBackdrop: !0
		},
		 
		listen: {
			hashchange: "hashchange",
			touchstart: "touchstart",
			touchmove: "touchmove",
			touchend: "touchend",
			click: "click",
			scroll: "scroll"
		},

 		defaultConfig: {
 			type: "navigation",
 			transition: 500,
 			event: "click",
 			direction: "left",
			backdrop: true,
			backdropClass: "backdrop",
			dataAccessAttribute: "data-target"
 		},

 		init: function(_element, options) {
 			var element,
				event,
				backdrop,
				dataAccess,
				options,
 			    configurationObject,
 			    dataHashNavMaxWidth,
 			    dataNavDrawerMaxWidth,
 			    destinationId,
				destination,
				__proto__ = this;
			
			__proto__.xAxis = 0;
 			__proto__.options = options;
			configurationObject = this.defaultConfig;
			

 			if(options && "object" == typeof options) {
 				configurationObject = $.extend(configurationObject, options);
			}

			backdrop = configurationObject.backdropClass;
			backdrop = /^\./.test(backdrop) ? backdrop : ("." + backdrop);
			__proto__.backdrop = $(backdrop);
			dataAccess = configurationObject.dataAccessAttribute;
			 
			element = $(_element);
			
			var destinationId = element.attr(dataAccess),
				isCSSSelector = /^(?:\#|\.)/.test(destinationId),
				isClass = /^[\.]/.test(destinationId),
				destination,
				classname;
			destinationId = isCSSSelector ? destinationId : "#" + destinationId;

			// The default selector provided by the program is the CSS id selector (#...).

			destination = $(destinationId);

			// If it was a CSS selector, and a class selector classname remains the same; else the target's classname is transversed.

			classname = isClass ? destinationId : destination.attr("class");
			classname = classname.split(/\s+/);
			classname = "." + ((classname.length >= 2) ? classname[0] + "." + classname[1] : classname);
			destination = isClass ? destination : $(classname);
			
			
			// These attributes are used for the RWD(Responsive Web Design) features. The navigation drawer module is best suited for mobile touch devices. The program shouldn't listen for certain events on desktop devices as side-nav may be hidden. The attribute here is the screen sizes for which the nav is hidden.
 			dataHashNavMaxWidth = destination.attr("data-hash-nav-max-width") + "px";
			 dataNavDrawerMaxWidth = destination.attr("data-nav-drawer-max-width") + "px";
			 
 			if(window.matchMedia(("(max-width:" + dataNavDrawerMaxWidth + ")")).matches) {
 				this.drawer(destination, configurationObject.direction, (configurationObject.transition/1e3));
			}

			event = ("object" == typeof configurationObject && ("event" in configurationObject)) ? configurationObject.event : "click";
			event += "." + configurationObject.type;

			element.on(event,function(e) {
				e.preventDefault();
				__proto__.handle(destination, configurationObject);
			});

			if(configurationObject.backdrop) {
				this.backdrop.on(event, function() {
					reverse(this, destination, configurationObject.transition, configurationObject.direction);

				});
			}

			$(global).on(__proto__.listen.hashchange, function() {
				if(global.matchMedia(("(max-width:" + dataHashNavMaxWidth + ")")).matches) {
					__proto__.hashNav(element, destination, configurationObject.transition, configurationObject.direction,configurationObject.backdrop);
				}
			});

			$(doc).ready(function() {
				if(global.matchMedia(("(max-width:" + dataHashNavMaxWidth + ")")).matches) {
					__proto__.hashNav(element, destination, configurationObject.transition, configurationObject.direction, configurationObject.backdrop);
				}
			});
		} ,

		handle: function(destination, options) {
			var transitionPropValue,
				hidden,
				width,
				dimension,
				optionsIsObject = "object" == typeof options,
				transition = (optionsIsObject && ("transition" in options)) ? options.transition : 500,
				direction = (optionsIsObject && ("direction" in options)) ? options.direction : left,
				time = transition/1e3;

			transitionPropValue = direction + " " + style + " " + time + "s";

			hidden = destination.css(direction);
			hidden = hidden.replace(/[^\d]+$/, "");
			hidden = /\.(?=\d)/.test(hidden) ? Math.floor(parseFloat(hidden)) : parseInt(hidden);
			width = Math.floor(destination.width());

			// Sets xAxis to width to be used by the reverse function that closes the nav using the backdrop.

			this.xAxis = width;

			if(hidden == ("-" + width)) {
				if(direction == left) {
					destination.css({
						left: "0px",
						transition: transitionPropValue
					});
				} else if (direction == right) {
					destination.css({
						right: "0px",
						transition: transitionPropValue
					});
				} else {
					destination.show(transition);
				}
				options.backdrop && this.backdrop.css(opacity,1).fadeIn(transition);
				
				global.location.hash = hash;
				this.drawable.nextaction = back;

			} else {
				dimension = "-" + (width.toString()) + "px";
				if(direction == left) {
					destination.css({
						left: dimension,
						transition: transitionPropValue
					});
				} else if(direction == right) {
					destination.css({
						right: dimension,
						transition: transitionPropValue
					});
				} else {
					destination.hide(transition);
				}
				options.backdrop && this.backdrop.fadeOut(transition);
				global.history.back();
				this.drawable.nextaction = forth;
			}
		} ,

		hashNav: function(element, destination, transition, direction, usebackdrop) {
			

			var currentHash = global.location.hash,
				href = element.attr("href"),
				width = destination.width(),
				time = transition/1e3;

			var dimension = "-" + width + unit,
				transitionPropValue = direction + " " + style + " " + time + "s";

			if(currentHash == href) {
				if ((destination.css(direction) != "0px")) {
					destination.css(direction, "0px")
					.css(effect, transitionPropValue);
					usebackdrop && this.backdrop.fadeIn(transition);
					this.drawable.nextaction = back;
				}

			} else {
				destination.css(direction, dimension)
				.css(effect, transitionPropValue);
				this.drawable.nextaction = forth;
				usebackdrop && this.backdrop.fadeOut(transition);
			}
		} ,	
		
		drawer: function(destination, direction, time) {

			var transitionPropValue = direction + " " + style + " " + time + "s";

			var body = $("body"),
				overflow = "overflow",
		    	__doc = $(document),
				__proto__ = this,
				drawable = this.drawable,
				width = destination.width(),
				minimumDragArea = 25,
				minimumRightDragArea = this.deviceWidth - minimumDragArea,
				windowWidth = this.deviceWidth,
				currentMenuPosition,
				start = -1,
				startX = start,
				startY = start,
				resumeX = start,
				resumeY = start,
				resume,
			    	scrollControl,
			    	scrollControlSet = false,
				fraction = 3/2;

			var zero = "0px";
			var non_zero_dimen = "-" + (width.toString()) + "px";
			
			__doc.on(__proto__.listen.touchstart, function(e) {
				touchStarted(e);
			});
			__doc.on(__proto__.listen.touchmove, function(e) {
				touchMoves(e);
			});
			__doc.on(__proto__.listen.touchend, function(e) {
				touchEnded(e);
			});
			
			// Define event handlers....Event handler for touch start. Pull out the menu on touchstart for touches from, or less than the `minimumDragArea`, and touches from, or greater than the `minimumRightDragArea`. The menu drawer should be easily discoverable.

			function touchStarted(e) {
				e.stopPropagation();

				start = e.changedTouches[0].pageX || e.changedTouches[0].clientX;
				startX = start;
				startY = e.changedTouches[0].pageY || e.changedTouches[0].clientY;

				currentMenuPosition = destination.css(direction);
				var right_dimension = ("-" + ((width - (windowWidth - start)).toString()) + unit);
				var left_dimension = ("-" + ((width - start).toString()) + unit);

				windowWidth = __proto__.deviceWidth;
				

				// Logic: when `start` for `direction = left` > 0 and <= `minimumDragArea` -- roll out menu.

				if((direction == left ) && (!(start < 0)) && (start <= minimumDragArea) && (currentMenuPosition != zero)) {
					destination.css(direction, left_dimension).css(effect, "none");

					// Block all other scrolls on the body. 
					body.css(overflow, "hidden");
				}

				// Logic: when `start` for `direction = right` >= `minimumRightDragArea` -- roll out menu.

				if((direction == right) && (start >= minimumRightDragArea) && (!(start > windowWidth)) && (currentMenuPosition != zero)) {
					destination.css(direction, right_dimension).css(effect, "none");
					body.css(overflow, "hidden");
				}
				return 0;
			}

			// Touchmoves: drag menu across pixels as the touch moves over the screen. If the menu has been dragged out as much as the width of the menu the drag stops -- even when the touch still moves. If otherwise the touchend event handles the rest and decides whether the position has reached threshold. The threshold is a dependent variable.

			function touchMoves(e) {
				resume = e.changedTouches[0].pageX || e.changedTouches[0].clientX;
				resumeX = resume;
				resumeY = e.changedTouches[0].pageY || e.changedTouches[0].clientY;
				
				var virtualLeftStart = start > width ? width : start;
				var virtualRightStart = start < (windowWidth - width) ? (windowWidth - width) : start;

				currentMenuPosition = destination.css(direction);

				var left_dimension = "-" + ((width - resume).toString()) + unit;
				var right_dimension = ("-" + ((width - (windowWidth - resume).toString())) + unit);

				var vleftDimension = "-" + ((virtualLeftStart - resume).toString()) + unit;
				var vrightDimension = "-" + ((resume - virtualLeftStart ).toString()) + unit;

				var sSheet = {
					"opacity": (resume/width),
					"display": "block"
				};
				var rsSheet = {
					"opacity": ((windowWidth - resume)/width),
					"display": "block"
				};

				var rect = new Rectangle(startX,startY, resumeX,resumeY);
				var wGTh = rect.wGTh();
				!scrollControlSet && (scrollControl=wGTh), (scrollControlSet=true)

				// This is the logic behind left side nav opening

				if ((!(start < 0)) && (start <= minimumDragArea) && (direction == left) && (currentMenuPosition != zero) && (drawable.nextaction === forth) && wGTh && scrollControl) {
					destination.css(direction, left_dimension);
					__proto__.backdrop.css(sSheet);
				}

				// This is the logic behind left side nav closing

				if ((!(resume > width)) && (drawable.nextaction === back) && (direction == left) && (currentMenuPosition != non_zero_dimen) && wGTh && scrollControl) {
					
					destination.css(direction, vleftDimension)
					.css(effect, "none");
					__proto__.backdrop.css(sSheet);
					body.css(overflow, "hidden");
				}

				// This is the logic behind right side nav opening
				if ((!(start < 0)) && (start >= minimumRightDragArea) && (direction == right) && (currentMenuPosition != zero) && wGTh && scrollControl) {
					destination.css(direction, right_dimension);
					__proto__.backdrop.css(rsSheet);
				} 

				// This is the logic behind right side nav closing
				if ((!(resume < (windowWidth - width))) && (drawable.nextaction == back) && (direction == right) && (currentMenuPosition != non_zero_dimen) && wGTh && scrollControl) {
					
					destination.css(direction, vrightDimension)
					.css(effect, "none");
					__proto__.backdrop.css(rsSheet);
					body.css(overflow, "hidden");

				}
			}

			function touchEnded(e) {
				var offsetSide = destination.css(direction).replace(/[^\d]+$/, '');
				offsetSide = Math.abs(parseInt(offsetSide));
				fraction = 3/2;
				
				scrollControlSet = false;
				scrollControl = false;

				// left opening touchend event
				if (direction == left) {
					if (offsetSide <= (width/fraction) && (start <= minimumDragArea)){
						__proto__.backdrop.css(opacity, 1);
						location.hash = hash;
						__proto__.drawable.nextaction = back;
						body.css(overflow, "hidden");
					} else {
						destination.css(direction, non_zero_dimen)
						.css(effect, transitionPropValue);
						__proto__.backdrop.hide();
						body.css(overflow, "initial");
					}

					// for backward 
					if (start > minimumDragArea && currentMenuPosition != non_zero_dimen) {
						fraction = fraction + 1;
						if (offsetSide > Math.floor(width/fraction)) {
							__proto__.drawable.nextaction = forth;
							__proto__.backdrop.css(opacity, "0");
							global.history.back();
							body.css(overflow, "initial");
							
						} else {
							destination.css(direction, zero);
							__proto__.backdrop.show(10);
							body.css(overflow, "hidden");
						}
					}
				}

				// right opening touchend event
				if (direction == right) {

					if (offsetSide <= (width/fraction) && start >= minimumRightDragArea) {
						__proto__.backdrop.css(opacity, 1);
						location.hash = hash;
						__proto__.drawable.nextaction = back;
						body.css(overflow, hidden);

					} else {
						destination.css(direction, non_zero_dimen)
						.css(effect, transitionPropValue);
						__proto__.backdrop.hide();
						body.css(overflow, "initial");
					}

					// right closing touchend event
					if (__proto__.drawable.nextaction == back) {
						fraction += 1
						if (offsetSide >= (width/fraction)) {

							__proto__.drawable.nextaction = forth;
							__proto__.backdrop.css(opacity, 0);
							global.history.back();
							body.css(overflow, "initial");

						} else {
							destination.css(direction, zero);
							__proto__.backdrop.show(10);
							body.css(overflow, "hidden");
						}
					}
				}
			}
		}
	};


	setInterval(function() {
		Navigation.fn.deviceWidth = global.screen.availWidth;
	}, 1000);

	function jQueryNotInstalled() {
		return (!(window.jQuery instanceof Object));
	}

	function displayStr(string) {
		console.info(string);
	}

	function displayError(error) {
		console.error(error);
	}

	function reverse(backdrop, destination, transition, direction) {
		global.history.back();

		var dimension = "-" + destination.width() + "px";
		destination.css(direction, dimension);
		$(backdrop).fadeOut(transition);
	}

	// Cause no commotion load previous definitions so as not to override
	var former = $.fn.nav;

	// Define new Navigation class entry and expose it to a jQuery object
	$.fn.nav = function(command, options) {
		if(command !== "init")
			return;
		return this.each(function() {
			var $this = $ (this),
				data = $this.data("WAB_NAV");
			if(!data)
				$this.data("WAB_NAV", (data = new Navigation()));
				console.log($this.data("WAB_NAV"))
			data[command](this, options);
		});
	}

	// Sign the class
	$.fn.nav.Constructor = Navigation;

	//jQuery no conflict
	$.fn.noConflict = function() {
		$.fn.nav = former;
		return this;
	}
	// Hey Presto! Try it out. A component of Web Aid Box (WAB). Check out available documentations for the easy how-to-use.
	
}(window.jQuery, window, document);
