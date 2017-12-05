/*

Template Name: Myway
Template Demo: http://awerest.com/demo/myway

Purchase: http://themeforest.net/item/myway-onepage-bootstrap-parallax-retina-template/4058880?ref=awerest

Author: Awerest

Description: Onepage Bootstrap Multi-Purpose Parallax Retina Template
Tags: Responsive, Mobile First, Retina, Bootstrap 3, One Page, Multi Page, Multi-Purpose, Agency, Clean, Creative, Minimal, Components, Photography, Portfolio, Business, Corporate, White, Modern

Version: 2.5

---------------

Table of Contents:

1) Fix for Internet Explorer 10 in Windows 8 and Windows Phone 8
2) Animated elements
3) Carousels
	- Intro slider
	- Works slider
4) Intro section height
5) Contact form
6) SVG icons
7) Google map
	- Marker image and position
	- Map position
8) Collapse menu on tap/select
9) Smooth scroll on anchors
10) Gallery lightbox
11) Preloader
12) Href # fix for demo

---------------

*/

$(document).ready(function() {
	'use strict';

/* ==== 1) Fix for Internet Explorer 10 in Windows 8 and Windows Phone 8 ==== */

	if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
		var msViewportStyle = document.createElement("style")
		msViewportStyle.appendChild(
			document.createTextNode(
				"@-ms-viewport{width:auto!important}"
			)
		)
		document.getElementsByTagName("head")[0].appendChild(msViewportStyle)
	}

/* ==== 2) Animated elements ==== */

/* After all images are loaded, and if it's no-touch device, run script */

	imagesLoaded(document.body, function(){
		if ($('.no-touch').length) {
			skrollr.init({
				smoothScrolling: false,
				easing: 'sqrt',
				forceHeight: false
			});
		}
	});

/* ==== 3) Carousels ==== */

/* Intro text slider */

	$('#carousel-intro').carousel({
		interval: 3500,
		pause: "false"
	})

/* Works sliders */

	$('#carousel-1, #carousel-2, #carousel-3').carousel({
		interval: false
	})

/* ==== 4) Make intro section height of viewport / Minimum height is set to 445px in style.css ==== */

	$(function(){
		$('#intro').css({'height':($(window).height())+'px'});
		$(window).resize(function(){
		$('#intro').css({'height':($(window).height())+'px'});
		});
	});

/* ==== 5) Contact form ==== */

	$('.flowuplabels').FlowupLabels({
		feature_onInitLoad: false, 
		class_focused: 'focused',
		class_populated: 'populated' 
	});

	var options = {
		target: '.message .alert',
		beforeSubmit: showRequest,
		success: showResponse
	};

	$('#contactForm').ajaxForm(options);
	function showRequest(formData, jqForm, options) {
		var queryString = $.param(formData);
			return true;
		}
	function showResponse(responseText, statusText) {
		}

/* ==== 6) SVG icons ==== */

	var url ='css/streamline-icons.svg';
	var c=new XMLHttpRequest(); c.open('GET', url, false); c.setRequestHeader('Content-Type', 'text/xml'); c.send();
	document.body.insertBefore(c.responseXML.firstChild, document.body.firstChild)

	var url ='css/simpleline-icons.svg';
	var c=new XMLHttpRequest(); c.open('GET', url, false); c.setRequestHeader('Content-Type', 'text/xml'); c.send();
	document.body.insertBefore(c.responseXML.firstChild, document.body.firstChild)

	var url ='css/social-icons.svg';
	var c=new XMLHttpRequest(); c.open('GET', url, false); c.setRequestHeader('Content-Type', 'text/xml'); c.send();
	document.body.insertBefore(c.responseXML.firstChild, document.body.firstChild)

/* Add your set / See documentation */

/*
	var url ='css/your-file-name.svg';
	var c=new XMLHttpRequest(); c.open('GET', url, false); c.setRequestHeader('Content-Type', 'text/xml'); c.send();
	document.body.insertBefore(c.responseXML.firstChild, document.body.firstChild)
*/

/* ==== 7) Google map ==== */

	google.maps.event.addDomListener(window, 'load', init);

	function init() {
		var mapOptions = {
			disableDefaultUI: true,
			scrollwheel: false,
			draggable: true,
/* Map position latitude and longitude */
			center: new google.maps.LatLng(45.255, 19.845),
/* Map zoom / 0 is "Earth" and 21 is fully zoomed */
			zoom: 15,
/* Custom map color / See documentation */
			styles: []
		};
		var mapElement = document.getElementById('gmap');
		var map = new google.maps.Map(mapElement, mapOptions);
		var image = 'img/map-pin.png';
/* Marker #1 */
		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(45.253, 19.845),
			map: map,
			icon: image
		});
/* Marker #2 */
		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(45.255, 19.850),
			map: map,
			icon: image
		});
/* Marker #3 */
		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(45.257, 19.840),
			map: map,
			icon: image
		});
	}

});

$(window).load(function() {
	'use strict';

/* ==== 8) Collapse menu on tap/select on mobile and tablet devices ==== */

	if ($(window).width() < 768) {
		$('.navbar a').click(function () { $(".navbar-collapse").collapse("hide") });
	}

	$(window).resize(function(){
		if ($(window).width() > 752) {
			$(".navbar-collapse").collapse("hide")
		}
	});

/* ==== 9) Smooth scroll on anchors ==== */

/* Add your anchor parent element class or ID */

	$.localScroll.hash();
	$('.nav, .navbar-header, footer, #intro').localScroll({
		target: 'body',
		queue: true,
		duration: 1000,
		hash: false,
		offset: -60,
		easing: 'easeInOutExpo'
	});

/* ==== 10) Gallery lightbox ==== */

	$(document).delegate('*[data-toggle="lightbox"]', 'click', function(event) {
		event.preventDefault();
		$(this).ekkoLightbox();
	});

/* ==== 11) Preloader ==== */

	$('.spinner').fadeOut('slow');
	$('.preloader').delay(350).fadeOut('slow');

/* ==== 12) Href # fix for demo ==== */

	$('a[href="#"]').click(function() {
		return false;
	});

});