if (typeof $ !== 'function') {
	addScript('https://tsunami.he.net/~rawdatas/appslab/oracle/jquery.min.js');
	waitFor(
		function () {
			return (typeof $ == 'function');
		},
		function () {
			loadAfterJQ();
		}
	);
} else {
	loadAfterJQ();
}

function loadAfterJQ() {
	var result_ui = document.getElementById('orciWireframePopup');
	if (!result_ui) {
		result_ui = initUI();
	}
	if (result_ui.style.display === 'none') {
		gui2svg();
		result_ui.style.display = 'block';
		extractSvg();
	} else {
		$('#asvg').empty();
		result_ui.style.display = 'none';
	}
}

function initUI() {
	var result_ui = document.createElement('div');
	result_ui.style.position = 'fixed';
	result_ui.style.left = '0px';
	result_ui.style.top = '0px';
	result_ui.style.zIndex = 2147483647;
	result_ui.style.background = '#FFFFFFDD';
	result_ui.style.display = 'none';
	result_ui.style.height = '99%';
	result_ui.style.width = '100%';
	result_ui.id = 'orciWireframePopup';
	result_ui.innerHTML = '<svg id=asvg xmlns=http://www.w3.org/2000/svg width=100% height=100%></svg>' +
		'<a href=# id=link style="bottom:0px;position:fixed;display:block;background-color:red;color:white;">RIGHT-click here to download SVG</a>';
	document.body.appendChild(result_ui);
	return result_ui;
}

function gui2svg() {
	var all_inputs = $(':input, a');
	all_inputs.each(function () {
		var dims = getDims(this);
		if (isVisible(this, dims)) {
			var $this = $(this);
			//DISABLED			if (!$this.is('a'))
			//				drawRect(dims.x, dims.y, dims.w, dims.h, $this.is('a') ? 'blue' : 'green');
			var text = '',
				alt = '';
			var color = 'black';
			if ($this.is('button') || $this.is('a') || $this.attr('type') === 'submit') {
				alt = this.title || this.alt || '';
				if (this.childNodes && this.childNodes.length === 1 && !this.childNodes[0].childNodes.length) {
					//				if (this.innerHTML.indexOf('svg') < 0) {
					text = this.innerText || this.value || '';
					alt = alt || this.childNodes[0].title || this.childNodes[0].alt;
				}
				//				text = this.innerText || this.title || this.alt || this.value || '';
			} else if ($this.is('select')) {
				text = $this.find('option:selected').text();
				color = 'green';
				var half_h = 0.5 * dims.h;
				drawIcon('Dropdown', dims.x + dims.w - half_h - 1, dims.y + half_h * 0.5, half_h, half_h);
			} else if ($this.is('input:text') || $this.is('input[type="search"]') || $this.is('input[type="email"]')) {
				if ($this.val()) {
					text = $this.val() || '';
					color = 'green';
				} else if ($this.attr('placeholder')) {
					text = $this.attr('placeholder') || '';
					color = 'grey';
				}
			} else if ($this.is('input[type="checkbox"]')) {
				drawRect(dims.x, dims.y, dims.w, dims.h);
				if ($this.is(':checked')) {
					text = '&#10004;';
					color = 'green';
				}
			}
			if (text) {
				var cstyle = window.getComputedStyle(this);
				drawText(dims.x, dims.y, dims.w, dims.h, cstyle.fontSize.slice(0, -2), text, $this.is('a') ? 'blue' : color, cstyle.fontWeight);
				//				console.log('A:', text, cstyle.fontSize.slice(0, -2), cstyle.fontWeight);
			}
			if (alt) {
				var children = this.childNodes;
				if (children && children.length > 0 && ($(children[0]).is('img') || $(children[0]).is('svg'))) {
					var child_dims = getDims(children[0]);
					drawIcon(alt, child_dims.x, child_dims.y, child_dims.w, child_dims.h);
				} else
					drawIcon(alt, dims.x, dims.y, dims.w, dims.h);
			}
		}
	});

	var node = document.body;
	for (node = node.firstChild; node; node = node.nextSibling) {
		if (node.nodeType === 3 && node.data && $(node.parentElement).is(':not(a)')) {
			var text = node.data.trim();
			if (text) {
				var dims = getDims(node.parentElement);
				var cstyle = window.getComputedStyle(node.parentElement);
				drawText(dims.x, dims.y, dims.w, dims.h, cstyle.fontSize.slice(0, -2), text, null, cstyle.fontWeight);
				//DISABLE				drawRect(dims.x, dims.y, dims.w, dims.h);
				//				console.log('B:', text);
			}
		}
	}
	$(document.body).find(":not(iframe) :not(a)").addBack().contents().each(function () {
		if (this.nodeType === 3 && this.data) {
			var text = this.data.trim();
			if (text) {
				var dims = getDims(this.parentElement);
				if (isVisible(this.parentElement, dims)) {
					var cstyle = window.getComputedStyle(this.parentElement);
					drawText(dims.x, dims.y, dims.w, dims.h, cstyle.fontSize.slice(0, -2), text, null, cstyle.fontWeight);
					//DISABLE					drawRect(dims.x, dims.y, dims.w, dims.h);
					//					console.log('C:', text, cstyle.fontSize.slice(0, -2), cstyle.fontWeight);
				}
			}
		}
	});

	// for SUI springboard
	$('div').each(function () {
		var dims = getDims(this);
		if (this.click && (this.title || this.alt) && isVisible(this, dims)) {
			drawText(dims.x, dims.y, dims.w, dims.h, '10', '');
			//			drawText(dims.x, dims.y, dims.w, dims.h, '10', this.title || this.alt);
			//DISABLE			drawRect(dims.x, dims.y, dims.w, dims.h);
		}
	});

	$('*').each(function () {
		var dims = getDims(this);
		if (isVisible(this, dims)) {
			var mstyle = window.getComputedStyle(this);
			if (mstyle.borderTopWidth.indexOf('0px') < 0) {
				drawLine(dims.x, dims.y, dims.x + dims.w, dims.y);
			}
			if (mstyle.borderBottomWidth.indexOf('0px') < 0) {
				drawLine(dims.x, dims.y + dims.h, dims.x + dims.w, dims.y + dims.h);
			}
			if (mstyle.borderLeftWidth.indexOf('0px') < 0) {
				drawLine(dims.x, dims.y, dims.x, dims.y + dims.h);
			}
			if (mstyle.borderRightWidth.indexOf('0px') < 0) {
				drawLine(dims.x + dims.w, dims.y, dims.x + dims.w, dims.y + dims.h);
			}
			if (mstyle.borderImageWidth.indexOf('0px') < 0 && dims.w == 168 && dims.h == 20) { // infotile down arrow
				drawRect(dims.x - 1, dims.y + 1, dims.w + 2, dims.h);
			}
			var cstyle = window.getComputedStyle(this);
			if (cstyle.backgroundImage.indexOf('dropdown') > -1) {
				drawIcon('Dropdown', dims.x, dims.y, dims.w, dims.h);
			}
		}
	});

	$('svg').each(function () {
		var dims = getDims(this);
		var rounded_w = Math.round(dims.w);
		if (isVisible(this, dims) && dims.w == dims.h && (rounded_w == 48 || rounded_w == 51 || rounded_w == 58 || rounded_w == 96)) {
			var half_w = dims.w * 0.5;
			var half_h = dims.h * 0.5;
			drawCircle(dims.x + half_w, dims.y + half_h, half_w);
		}
	});

	$('img').each(function () {
		var dims = getDims(this);
		var rounded_w = Math.round(dims.w);
		if (isVisible(this, dims)) {
			if (dims.h == 48 && (rounded_w == 48 || rounded_w == 51)) {
				drawRect(dims.x, dims.y, dims.w, dims.h, null, 7);
			} else if (this.src.indexOf('disclosecollapsed') > -1 || this.src.indexOf('discloseexpanded') > -1) {
				drawIcon('Expand', dims.x, dims.y, dims.w, dims.h);
			} else if (this.src.indexOf('arrow_p_dwn') > -1 || this.src.indexOf('arrow_p_ena') > -1) {
				drawIcon('Dropdown', dims.x, dims.y, dims.w, dims.h);
			}
		}
	});
}

function extractSvg() { // https://stackoverflow.com/questions/23218174/how-do-i-save-export-an-svg-file-after-creating-an-svg-with-d3-js-ie-safari-an
	var svg = document.getElementById('asvg');
	var serializer = new XMLSerializer();
	var source = serializer.serializeToString(svg);

	//add name spaces.
	if (!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)) {
		source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
	}
	if (!source.match(/^<svg[^>]+"http\:\/\/www\.w3\.org\/1999\/xlink"/)) {
		source = source.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
	}

	//add xml declaration
	source = '<?xml version="1.0" standalone="no"?>\r\n' + source;

	//convert svg source to URI data scheme.
	var url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(source);

	//set url value to a element's href attribute.
	document.getElementById('link').href = url;
}

function drawLine(x, y, x2, y2) {
	var newLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
	newLine.setAttributeNS(null, 'x1', x);
	newLine.setAttributeNS(null, 'y1', y);
	newLine.setAttributeNS(null, 'x2', x2);
	newLine.setAttributeNS(null, 'y2', y2);
	newLine.setAttributeNS(null, 'stroke-width', '1');
	newLine.setAttributeNS(null, "stroke", "black")
	document.getElementById('asvg').appendChild(newLine);
}

function drawRect(x, y, w, h, color, radius) {
	// adapted from: https://stackoverflow.com/questions/12786797/draw-rectangles-dynamically-in-svg
	var svgns = "http://www.w3.org/2000/svg";
	var rect = document.createElementNS(svgns, 'rect');
	rect.setAttributeNS(null, 'x', x);
	rect.setAttributeNS(null, 'y', y);
	rect.setAttributeNS(null, 'height', h);
	rect.setAttributeNS(null, 'width', w);
	rect.setAttributeNS(null, 'stroke', '#000000');
	rect.setAttributeNS(null, 'stroke-width', '1');
	rect.setAttributeNS(null, 'fill', '#00000000');
	rect.setAttributeNS(null, 'stroke', color || '#000');
	//	rect.setAttributeNS(null, 'opacity', '.20');
	rect.setAttribute('rx', radius || 0);
	document.getElementById('asvg').appendChild(rect);
}

function drawCircle(x, y, r) {
	var svgns = "http://www.w3.org/2000/svg";
	var circle = document.createElementNS(svgns, 'circle');
	circle.setAttributeNS(null, 'cx', x);
	circle.setAttributeNS(null, 'cy', y);
	circle.setAttributeNS(null, 'r', r);
	circle.setAttributeNS(null, 'style', 'fill: none; stroke: black; stroke-width: 1px;');
	document.getElementById('asvg').appendChild(circle);
}

// https://stackoverflow.com/questions/14758125/setting-text-svg-element-dynamically-via-javascript
function drawText(x, y, w, h, size, t, color, weight) {
	var txt = document.createElementNS("http://www.w3.org/2000/svg", 'text');
	txt.setAttributeNS(null, 'x', x);
	txt.setAttributeNS(null, 'y', y + h + Math.floor((size - h) * 0.5));
	color = null; // DISABLE COLOR
	txt.setAttribute('fill', color || '#000');
	txt.setAttributeNS(null, 'font-size', size);
	txt.setAttributeNS(null, 'font-weight', weight);
	txt.setAttributeNS(null, 'font-family', 'sans-serif');
	txt.setAttributeNS("http://www.w3.org/XML/1998/namespace", 'xml:space', 'preserve'); // doesn't work.. https://stackoverflow.com/questions/8424422/adding-text-with-whitespaces-in-svg-text-element
	txt.innerHTML = t;
	document.getElementById('asvg').appendChild(txt);
}

function drawIcon(text, x, y, w, h) {
	var icon = '';
	if (text.indexOf('Notifications') === 0) { // bell
		icon = '<svg>' +
			'<g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 43, h / 50) + ')" id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><path d="M40.12179,26.4930748 C36.52402,21.1505919 31.84692,30.7670612 23.39217,10.9998742 C22.13295,7.4382188 16.19663,5.1231429 11.69942,5.3012256 C12.0592,4.5888946 11.69942,3.520398 11.69942,2.6299842 C10.62009,0.492991 8.10165,-0.5755056 5.76311,0.3149082 C3.42456,1.205322 2.16534,3.8765635 3.24467,6.0135567 C3.78433,6.9039705 4.324,7.7943844 5.04355,8.1505499 C1.98545,10.9998742 -1.07265,17.0546882 0.36645,20.6163436 C8.64132,40.2054479 -1.43243,36.6437925 0.36645,42.8766893 L3.42456,50 C3.42456,50 15.1173,47.1506757 23.21228,43.7671032 C31.48714,40.2054479 43,33.972551 43,33.972551 L40.12179,26.8492404 L40.12179,26.4930748 Z M6.48266,2.4519014 C7.56199,2.0957359 8.64132,2.4519014 9.18098,3.520398 C9.54076,4.5888946 9.18098,5.8354739 8.10165,6.1916395 C7.02232,6.547805 5.76311,6.1916395 5.40333,5.1231429 C5.40333,3.8765635 5.40333,2.8080669 6.66255,2.2738186 L6.48266,2.4519014 Z M29.57852,39 L29.40437,39 C30.75093,41.6855739 29.7373,44.9915223 27.14035,46.3840421 C24.54341,47.7765619 21.34656,46.7283344 20,44.0427605 L25.22465,41.7014788 L29.57852,39 Z" id="bell-icon" fill="#000000" fill-rule="nonzero"></path></g>' +
			'</svg>';
	} else if (text === 'Home' && x < 99 && y < 99) { // logo
		icon = '<svg width="260px" height="29px" viewBox="0 0 260 29" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 260, h / 29) + ')" id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><path d="M254.273128,4.0089186 L254.273128,2.812709 L254.796728,2.812709 L255.614852,2.845039 L255.843927,2.909699 L256.073002,2.974359 L256.203902,3.1036789 L256.269352,3.2653289 L256.269352,3.6209588 L256.203902,3.7826087 L255.909377,3.9442586 L255.483952,4.0412486 L254.273128,4.0412486 L254.273128,4.0089186 Z M253.225928,6.5306577 L253.225928,2.1337793 L255.811202,2.1337793 L256.236627,2.1984392 L256.662052,2.3600892 L256.956576,2.5540691 L257.185651,2.812709 L257.316551,3.3946488 L257.316551,3.6532887 L257.251101,3.8795987 L257.120201,4.1059086 L256.989301,4.2998885 L256.563877,4.5585284 L256.040277,4.6878484 L256.400252,4.9464883 L256.629327,5.1081382 L256.760227,5.2697882 L257.054751,5.722408 L257.643801,6.6276477 L256.400252,6.6276477 L255.745752,5.5607581 L255.516677,5.2051282 L255.287602,5.0434783 L255.058527,4.9141583 L254.534928,4.7848384 L254.240403,4.7848384 L254.240403,6.5953177 L253.225928,6.5953177 L253.225928,6.5306577 Z M251.982379,5.916388 L252.931403,6.9186176 L254.240403,7.5328874 L255.778477,7.6622074 L257.185651,7.2742475 L258.363751,6.4336678 L259.01825,5.2697882 L259.14915,3.9442586 L258.723726,2.6833891 L257.774701,1.6488294 L256.465702,1.0345596 L254.927627,0.9052397 L253.520453,1.3255295 L252.342354,2.1661093 L251.687854,3.3299889 L251.556954,4.6555184 L251.982379,5.916388 Z M251.164254,6.2720178 L251.753304,6.9509476 L252.407804,7.5005574 L253.127753,7.9531773 L254.011328,8.2441472 L254.894902,8.4057971 L255.843927,8.4057971 L256.727502,8.2441472 L257.611076,7.9208473 L258.331026,7.4682274 L258.985525,6.8862876 L259.509125,6.2073579 L259.8691,5.4637681 L260,4.6555184 L260,3.8149387 L259.8691,3.006689 L259.509125,2.2630992 L258.985525,1.5841695 L258.265576,1.0022297 L257.545626,0.5496098 L256.662052,0.2263099 L255.778477,0.06466 L254.829452,0.06466 L253.945878,0.2263099 L253.062303,0.5496098 L252.342354,1.0022297 L251.687854,1.5841695 L251.164254,2.2954292 L250.804279,3.039019 L250.673379,3.8472687 L250.673379,4.6555184 L250.804279,5.4637681 L251.164254,6.2720178 Z M21.893014,4.6555184 L16.231592,4.6555184 L14.039018,4.8494983 L11.977344,5.3991081 L9.98112,6.3043478 L8.279421,7.5328874 L6.970422,9.0200669 L5.955947,10.7335563 L5.301447,12.5440357 L5.072373,14.451505 L5.301447,16.3589744 L5.955947,18.2017837 L6.970422,19.8829431 L8.279421,21.3701226 L9.98112,22.5986622 L11.977344,23.5039019 L14.039018,24.0535117 L16.231592,24.2151616 L34.393958,24.2151616 L36.586532,24.0535117 L38.648206,23.5039019 L40.546256,22.5986622 L42.247955,21.3701226 L43.655129,19.8829431 L44.669604,18.2017837 L45.324103,16.3589744 L45.553178,14.451505 L45.324103,12.5440357 L44.669604,10.7335563 L43.655129,9.0200669 L42.247955,7.5328874 L40.546256,6.3043478 L38.648206,5.3991081 L36.586532,4.8494983 L34.393958,4.6555184 L21.66394,4.6555184 L21.893014,4.6555184 Z M55.468848,0.12932 L81.059786,0.12932 L81.943361,0.1939799 L82.892385,0.3232999 L83.84141,0.5172798 L84.724984,0.8082497 L85.543109,1.1638796 L86.426683,1.5841695 L87.146633,2.1014493 L87.801133,2.6510591 L88.455632,3.2653289 L89.044682,3.9119287 L89.470107,4.6555184 L89.895532,5.3991081 L90.190057,6.1750279 L90.419132,6.9832776 L90.550031,7.8238573 L90.615481,8.664437 L90.550031,9.5050167 L90.419132,10.3132664 L90.190057,11.1538462 L89.895532,11.9297659 L89.470107,12.6733556 L89.044682,13.3846154 L88.455632,14.0635452 L87.801133,14.6778149 L87.146633,15.2274247 L86.426683,15.7447046 L85.543109,16.1649944 L84.724984,16.5206243 L83.84141,16.7792642 L82.892385,17.0055741 L81.943361,17.1348941 L81.059786,17.1672241 L77.001888,17.1672241 L90.320957,28.87068 L82.826935,28.87068 L64.304594,12.6410256 L81.059786,12.6086957 L81.877911,12.5440357 L82.761485,12.3177258 L83.481435,11.9620959 L84.201385,11.477146 L84.495909,11.1861761 L84.921334,10.5395764 L85.150409,10.1839465 L85.281309,9.8283166 L85.346759,9.4726867 L85.412209,9.0847269 L85.412209,8.3411371 L85.281309,7.5652174 L85.150409,7.2095875 L84.921334,6.8539576 L84.495909,6.2073579 L84.201385,5.916388 L83.84141,5.657748 L83.481435,5.4314381 L82.761485,5.0758082 L81.877911,4.8494983 L81.059786,4.7848384 L60.835746,4.7848384 L60.835746,28.90301 L55.468848,28.90301 L55.468848,0.12932 Z M115.09377,5.851728 L107.665198,16.2619844 L104.58905,20.7235229 L98.862177,28.8383501 L92.546256,28.8383501 L111.657646,1.8428094 L111.952171,1.4225195 L112.377596,1.0668896 L112.737571,0.7435897 L113.261171,0.4849498 L113.686595,0.2909699 L114.275645,0.12932 L115.29012,0 L116.402769,0.12932 L116.926369,0.2909699 L117.449969,0.4849498 L117.875393,0.7435897 L118.300818,1.0668896 L118.660793,1.4225195 L119.020768,1.8428094 L138.295784,28.8383501 L131.979862,28.8383501 L126.089364,20.6265329 L111.886721,20.5942029 L108.876023,16.0356745 L122.849591,16.1003344 L115.486469,5.851728 L115.42102,5.754738 L115.29012,5.722408 L115.15922,5.754738 L115.09377,5.851728 Z M153.120201,24.2798216 L175.111391,24.2798216 L172.100692,28.8383501 L153.120201,28.8383501 L151.582127,28.7736901 L149.978603,28.5797101 L148.440529,28.2240803 L146.902454,27.7391304 L145.49528,27.1571906 L144.088106,26.4136009 L142.844556,25.5730212 L142.190057,25.1204013 L141.601007,24.6354515 L141.077407,24.1181717 L140.062933,23.0512821 L139.179358,21.8874025 L138.066709,19.9799331 L137.772184,19.3333333 L137.543109,18.6544036 L137.314034,18.0078038 L137.183134,17.296544 L137.052234,16.6176143 L136.921334,15.9063545 L136.921334,15.1950948 L136.855884,14.483835 L136.921334,13.7725753 L136.921334,13.0613155 L137.052234,12.3823857 L137.183134,11.671126 L137.314034,10.9921962 L137.543109,10.3132664 L137.772184,9.6666667 L138.066709,8.9877369 L138.786658,7.7268673 L139.146633,7.1125975 L140.030208,5.9487179 L140.553807,5.3991081 L141.077407,4.8494983 L141.601007,4.3322185 L142.190057,3.8472687 L142.844556,3.3946488 L144.088106,2.5540691 L145.49528,1.8104794 L146.902454,1.1962096 L148.440529,0.7435897 L149.978603,0.3879599 L151.582127,0.1616499 L153.120201,0.09699 L175.013216,0.09699 L172.067967,4.6555184 L153.087476,4.6555184 L152.073002,4.7201784 L150.960352,4.8494983 L149.847703,5.1081382 L148.833228,5.4314381 L147.884204,5.851728 L146.935179,6.3690078 L146.051605,6.9186176 L145.23348,7.5652174 L144.513531,8.2764771 L143.859031,9.0523969 L143.335431,9.8929766 L142.811831,10.7335563 L142.451857,11.638796 L142.222782,12.5763657 L142.091882,13.5139353 L142.026432,14.451505 L142.091882,15.4214047 L142.222782,16.3589744 L142.451857,17.296544 L142.811831,18.2017837 L143.335431,19.0746934 L143.859031,19.9152731 L144.513531,20.6911929 L145.23348,21.4024526 L146.051605,22.0490524 L146.935179,22.6309922 L147.884204,23.115942 L148.833228,23.5362319 L149.847703,23.8595318 L150.960352,24.1181717 L152.073002,24.2798216 L153.120201,24.2798216 Z M178.252989,26.5105909 L178.252989,0.09699 L183.619887,0.09699 L183.619887,24.1828317 L207.2146,24.2151616 L204.269352,28.7736901 L180.805538,28.7736901 L180.281938,28.7090301 L179.758339,28.5797101 L179.332914,28.3857302 L178.972939,28.0947603 L178.678414,27.7391304 L178.449339,27.3511706 L178.318439,26.9308807 L178.252989,26.5105909 Z M245.208307,0.12932 L242.197609,4.6878484 L221.679043,4.6878484 L220.730019,4.7525084 L219.846444,4.8494983 L218.89742,5.0111483 L218.013845,5.2697882 L217.130271,5.5930881 L216.312146,5.9487179 L215.494021,6.4013378 L214.774072,6.8862876 L214.119572,7.4358974 L213.465072,8.0178372 L212.876023,8.664437 L212.352423,9.3433668 L211.926998,10.0546265 L211.501573,10.7982163 L211.207048,11.574136 L210.977974,12.3500557 L242.819383,12.3823857 L240.03776,16.6499443 L211.010699,16.6499443 L211.239773,17.458194 L211.534298,18.2341137 L211.894273,18.9777035 L212.417873,19.7212932 L212.941473,20.400223 L213.530522,21.0468227 L214.119572,21.6610925 L214.839522,22.2107023 L215.559471,22.6956522 L216.377596,23.148272 L217.195721,23.5039019 L218.079295,23.8272018 L218.96287,24.0858417 L219.911894,24.2474916 L220.795469,24.3768116 L221.744493,24.4091416 L245.502832,24.4091416 L242.557583,28.96767 L221.744493,29 L220.140969,28.93534 L218.602895,28.7090301 L217.064821,28.3534002 L215.526746,27.9007804 L214.054122,27.2865106 L212.745123,26.5429208 L211.436123,25.7023411 L210.847074,25.2497213 L210.258024,24.7647715 L209.668974,24.2474916 L209.145374,23.6978818 L208.71995,23.148272 L208.19635,22.5663322 L207.770925,21.9843924 L207.41095,21.3701226 L207.050975,20.7235229 L206.167401,18.7513935 L205.938326,18.0724638 L205.807426,17.393534 L205.676526,16.6822742 L205.611076,15.9710145 L205.545626,15.2920847 L205.545626,13.8695652 L205.676526,12.4470457 L205.807426,11.735786 L205.938326,11.0568562 L206.167401,10.3779264 L207.050975,8.4057971 L207.41095,7.7591973 L207.770925,7.1449275 L208.19635,6.5629877 L208.71995,5.9810479 L209.145374,5.4314381 L209.668974,4.8818283 L210.258024,4.3645485 L210.847074,3.8795987 L211.436123,3.4269788 L212.745123,2.5863991 L214.054122,1.8428094 L215.526746,1.2608696 L217.064821,0.7759197 L218.602895,0.4202899 L220.140969,0.1939799 L221.744493,0.12932 L245.208307,0.12932 Z M21.53304,0.12932 L34.459408,0.12932 L35.997483,0.1939799 L37.601007,0.4202899 L39.139081,0.7759197 L40.677155,1.2285396 L42.08433,1.8428094 L43.491504,2.5863991 L44.800503,3.4269788 L45.389553,3.8795987 L45.978603,4.3645485 L46.502203,4.8818283 L47.025802,5.4314381 L47.549402,5.9810479 L48.432977,7.1449275 L48.858402,7.7591973 L49.218376,8.4057971 L49.807426,9.7313266 L50.036501,10.3779264 L50.461926,11.735786 L50.527376,12.4470457 L50.658276,13.1583055 L50.723726,13.8372352 L50.723726,15.2597547 L50.658276,15.9710145 L50.527376,16.6822742 L50.461926,17.361204 L50.232851,18.0724638 L50.003776,18.7513935 L49.774701,19.3979933 L49.185651,20.7235229 L48.825677,21.3377926 L48.400252,21.9843924 L47.516677,23.148272 L46.993077,23.6978818 L46.469478,24.2474916 L45.945878,24.7647715 L45.356828,25.2497213 L44.767778,25.7023411 L43.458779,26.5429208 L42.051605,27.2865106 L40.64443,27.8684504 L39.106356,28.3534002 L37.568282,28.7090301 L35.964758,28.90301 L34.426683,28.96767 L16.198867,28.96767 L14.595343,28.90301 L13.057269,28.7090301 L11.519194,28.3534002 L9.98112,27.8684504 L8.508496,27.2865106 L7.199497,26.5429208 L5.890497,25.7023411 L5.301447,25.2497213 L4.712398,24.7647715 L4.123348,24.2474916 L3.599748,23.6978818 L3.174323,23.148272 L2.650724,22.5663322 L2.225299,21.9843924 L1.865324,21.3377926 L1.505349,20.7235229 L0.621775,18.7513935 L0.490875,18.0724638 L0.2618,17.361204 L0.1309,16.6822742 L0,15.2597547 L0,13.8372352 L0.06545,13.1583055 L0.1309,12.4470457 L0.2618,11.735786 L0.490875,11.0568562 L0.621775,10.3779264 L1.505349,8.4057971 L1.865324,7.7591973 L2.225299,7.1449275 L2.650724,6.5629877 L3.174323,5.9810479 L3.599748,5.4314381 L4.123348,4.8818283 L4.712398,4.3645485 L5.301447,3.8795987 L5.890497,3.4269788 L7.199497,2.5863991 L8.508496,1.8428094 L9.98112,1.2285396 L11.519194,0.7759197 L13.057269,0.4202899 L14.595343,0.1939799 L16.198867,0.12932 L21.53304,0.12932 Z" id="oracle-logo" fill="#202E35" fill-rule="nonzero"></path></g></svg>';
	} else if (text === 'Hide Help' || text === 'Show Help') {
		icon = '<svg><g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 46, h / 46) + ')" id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><circle id="help-icon" fill="#000000" fill-rule="nonzero" cx="23" cy="23" r="23"></circle><text fill="#FFFFFF" font-family="Helvetica, Calibri, sans-serif" font-size="32" font-weight="normal"><tspan x="14.12695" y="35">?</tspan></text></g></svg>';
	} else if (text === 'Home') {
		icon = '<svg>' +
			'<g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 28, h / 26) + ')">' +
			'<g fill="#000000" fill-rule="nonzero">' +
			'<polygon points="17 26 17 17 11 17 11 26 3 26 3 13.4 14 6.08 25 13.41 25 26"></polygon>' +
			'<polygon points="0 9.18 14.014 0 28.004 9.323 26.459 11.751 14.016 3.671 1.462 11.689"></polygon>' +
			'</g>' +
			'</g>' +
			'</svg>';
	} else if (text === 'Expand') { // expand / collapse
		icon = '<svg><g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 640, h / 640) + ')"><polygon class="fil0" points="639.965,0.0236223 640,639.953 -0.0118112,639.976"/></g></svg>';
	} else if (text === 'Dropdown') { // dropdown
		icon = '<svg><g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 640, h / 640) + ')"><path d="M320 486.419l320.012 -332.839c-213.322,0 -426.702,0 -640.024,0l320.012 332.839z"/></g></svg>';
	} else if (text === 'Favorites and Recent Items') { // star
		icon = '<svg><g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 47, h / 42) + ')" id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><polygon id="favorite-star-icon" fill="#000000" fill-rule="nonzero" points="29.38966 15.8768511 47 15.8768511 33.22674 25.7957911 38.78966 42 23.49162 32.0974279 8.22709 42 13.05276 25.7957911 0 15.8768511 17.62709 15.8768511 23.49162 0"></polygon></g></svg>';
	} else if (text === 'Watchlist') { // flag
		icon = '<svg><g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 53, h / 53) + ')"><path d="M9.11207,9.6969697 C9.11207,9.6969697 7.13514,0 19.78751,0 C27.69525,0 38.173,10.8606061 45.48765,10.8606061 C48.25536,10.8606061 51.41845,6.5939394 51.41845,6.5939394 L53,6.9818182 C53,6.9818182 50.42999,15.5151515 48.45305,18.6181818 C46.08073,21.7212121 41.92917,24.8242424 36.59145,24.8242424 C31.25373,24.8242424 28.28833,21.1393939 21.96214,24.0484848 C15.63595,26.9575758 16.82211,31.4181818 16.82211,31.4181818 L15.83365,32 L9.11207,9.6969697 Z M7.20711,7.7932011 C7.20711,7.7932011 18.86469,44.5446637 19.89563,48.7059404 C20.92658,52.8672171 14.00737,55.0450816 12.87729,50.358784 C11.84635,45.9836098 1.53693,14.1517875 0.2879,9.9710655 C-0.24988,8.7232163 -0.02296,7.2844823 0.87411,6.2543349 C1.77118,5.2241875 3.18453,4.7793279 4.52526,5.105114 C5.86598,5.4309 6.90412,6.4714495 7.20711,7.7932011 Z" id="flag-icon" fill="#000000" fill-rule="nonzero"></path></g>';
	} else if (text === 'Accessibility') { // accessibility
		icon = '<svg>' +
			'<g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 48, h / 48) + ')" id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><path d="M24.07417,47.9998857 C14.35719,48.0297728 5.58107,42.1974355 1.84527,33.2272493 C-1.89053,24.2570631 0.15128,13.9193944 7.01695,7.0431288 C13.88262,0.1668632 24.21713,-1.8908914 33.19307,1.8310741 C42.16901,5.5530397 48.01487,14.3201539 47.99997,24.0371615 C47.91958,37.22359 37.26046,47.8991608 24.07417,47.9998857 Z M23.94494,7.6989404 C21.70184,7.6989404 19.88346,9.5173263 19.88346,11.7604191 C19.88346,14.0035118 21.70184,15.8218978 23.94494,15.8218978 C26.18803,15.8218978 28.00642,14.0035118 28.00642,11.7604191 C28.00642,9.5173263 26.18803,7.6989404 23.94494,7.6989404 Z M38.40011,18.1849399 C38.16011,17.3357216 36.99705,17.501873 36.00015,17.6864857 L23.9634,18.609549 C25.32953,18.8310842 11.59435,17.6311019 11.59435,17.6311019 C10.59744,17.4464892 9.74822,17.3541829 9.50822,18.1849399 C9.26823,19.0156969 9.60053,19.366461 10.76359,19.9387602 L17.83426,22.1541122 C18.33905,22.8147065 18.78388,23.5190277 19.16347,24.2586967 C19.57792,25.1541571 19.92354,26.079901 20.1973,27.0278867 L15.06507,38.8061748 C15.01325,39.21011 15.13052,39.617515 15.38917,39.9320815 C15.64781,40.246648 16.02487,40.4404555 16.4312,40.4676888 C17.26196,40.7630691 17.64964,40.1907698 18.42502,39.1754002 L24.00032,30.1293795 L29.5387,39.2677065 C30.351,40.135386 30.79407,40.7446078 31.62482,40.4676888 C32.45558,40.1907698 33.00942,39.858467 32.78788,38.8615586 L27.80334,27.0463479 C28.03841,26.0434932 28.37235,25.0664196 28.80025,24.1294678 C29.20344,23.3181947 29.69903,22.5562292 30.27715,21.858732 L37.25551,19.9756828 C37.66892,19.9368352 38.04133,19.7095887 38.26496,19.3597247 C38.48858,19.0098607 38.53845,18.5764452 38.40011,18.1849399 Z" id="accessibility-icon" fill="#000000" fill-rule="nonzero"></path></g>' +
			'</svg>';
	} else if (text === 'Create' || text === 'Manage Attachments') { // plus
		icon = '<svg>' +
			'<g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 34, h / 33) + ')" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">' +
			'<path d="M32.293744,20.85542 L21.438305,20.85542 L21.438305,31.34873 C21.206363,32.33471 20.290422,33.0252 19.248907,32.99922 L14.744553,32.99922 C13.693629,33.02651 12.764993,32.33958 12.513303,31.34873 L12.513303,20.85542 L1.701023,20.85542 C0.680786,20.6112 -0.026716,19.71044 0.000774,18.69074 L0.000774,14.34742 C-0.025481,13.33655 0.685601,12.44769 1.701023,12.22209 L12.510687,12.22209 L12.510687,1.65134 C12.762584,0.65954 13.692661,-0.02765 14.744553,0.00085 L19.254138,0.00085 C20.295654,-0.02513 21.211595,0.66536 21.443536,1.65134 L21.443536,12.22717 L32.298976,12.22717 C33.31469,12.45233 34.025994,13.34146 33.999225,14.35249 L33.999225,18.68947 C34.02678,19.71114 33.316556,20.61312 32.293744,20.85542 Z" id="tp_Work-Measures-+-button" fill="#000000" fill-rule="nonzero"></path>' +
			'</g>' +
			'</svg>';
	} else if (text === 'Delete') { // cancel X
		icon = '<svg>' +
			'<g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 34, h / 35) + ')" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">' +
			'<path d="M34.9926408,22.6473203 L22.2215358,22.6473203 L22.2215358,35.0484903 C21.9486638,36.2137503 20.8710858,37.0297803 19.6457738,36.9990703 L14.3465338,36.9990703 C13.1101518,37.0313303 12.0176398,36.2195003 11.7215338,35.0484903 L11.7215338,22.6473203 L-0.998795201,22.6473203 C-2.1990752,22.3586903 -3.0314302,21.2941603 -2.9990892,20.0890603 L-2.9990892,14.9560403 C-3.0299762,13.7613703 -2.1934102,12.7109103 -0.998795201,12.4442903 L11.7184558,12.4442903 L11.7184558,-0.0484097376 C12.0148048,-1.22054974 13.1090138,-2.03267974 14.3465338,-1.99898974 L19.6519278,-1.99898974 C20.8772408,-2.02969974 21.9548188,-1.21366974 22.2276908,-0.0484097376 L22.2276908,12.4502903 L34.9987958,12.4502903 C36.1937528,12.7163803 37.0305818,13.7671803 36.9990898,14.9620403 L36.9990898,20.0875603 C37.0315068,21.2949803 36.1959488,22.3609603 34.9926408,22.6473203 Z" id="tp_-Work-Measures-x-button" fill="#000000" fill-rule="nonzero" transform="translate(17.000001, 17.499999) rotate(45.000000) translate(-17.000001, -17.499999)"></path>' +
			'</g>' +
			'</svg>';
	} else if (text === 'Navigator') { // hamburger
		icon = '<svg>' +
			'<g transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 46, h / 41) + ')">' +
			'<g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">' +
			'<path d="M4.0563625,0.003452 L41.7961728,0.003452 C42.9302469,-0.0342868 44.0272161,0.414525 44.8160231,1.2389876 C45.6048302,2.0634501 46.0118932,3.1866554 45.9366282,4.3310633 C46.0344888,5.5126941 45.6423189,6.6823145 44.8538693,7.5603196 C44.0654196,8.4383247 42.9515558,8.9457996 41.7785539,8.9614293 L4.1796952,8.9614293 C3.0066933,8.9457996 1.8928295,8.4383247 1.1043798,7.5603196 C0.3159302,6.6823145 -0.0762397,5.5126941 0.0216209,4.3310633 C-0.0972467,3.1977393 0.2779823,2.0682668 1.0494685,1.2371514 C1.8209547,0.406036 2.9122281,-0.0443418 4.0387436,0.003452 L4.0563625,0.003452 Z M4.0563625,15.9960237 L41.7961728,15.9960237 C42.9409694,15.9815694 44.0383966,16.4572671 44.8171779,17.3055277 C45.5959592,18.1537882 45.9834159,19.2954488 45.8837713,20.4482987 C45.9837606,21.6042821 45.5939868,22.748889 44.8112813,23.5977648 C44.0285758,24.4466407 42.9263951,24.9201191 41.7785539,24.9005737 L4.1796952,24.9005737 C3.0066933,24.884944 1.8928295,24.3774691 1.1043798,23.499464 C0.3159302,22.6214589 -0.0762397,21.4518385 0.0216209,20.2702077 C-0.0924152,19.1460256 0.2837996,18.0274127 1.0520481,17.206402 C1.8202966,16.3853913 2.9043233,15.9434753 4.0211246,15.9960237 L4.0563625,15.9960237 Z M4.0563625,32.0242137 L41.7961728,32.0242137 C42.9393238,31.981804 44.0469591,32.4297346 44.8457023,33.2574514 C45.6444455,34.0851682 46.0598847,35.2155601 45.9894851,36.369634 C46.0721085,37.5596474 45.665084,38.7313565 44.8645753,39.6079331 C44.0640666,40.4845097 42.9410809,40.9881993 41.7609349,41 L4.2149332,41 C3.0419312,40.9843703 1.9280674,40.4768954 1.1396178,39.5988903 C0.3511681,38.7208852 -0.0410017,37.5512648 0.0568588,36.369634 C-0.0669754,35.2366234 0.3034979,34.1052755 1.0716438,33.2706927 C1.8397897,32.4361099 2.9294378,31.9810508 4.0563625,32.0242137 Z" id="navigator-icon" fill="#000000" fill-rule="nonzero"></path>' +
			'</g>' +
			'</g>' +
			'</svg>';
	} else if (text === 'Search') { // magnifying glass
		icon = '<svg>' +
			'<g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 20, h / 28) + ')">' +
			'<g fill="#000000" fill-rule="nonzero">' +
			'<path d="M12,18.4 L14.6,17 L20,25.8 C20,25.8 20,27.4 19,27.8 C18.3,28.3 16.8,27.6 16.8,27.6 L12,18.4 Z" id="Shape"></path><path d="M8.5,14 C5.5,14 3,11.6 3,8.6 C3,5.6 5.5,3 8.4,3 C11.4,3 14,5.6 14,8.6 C14,11.6 11.4,14 8.4,14 L8.5,14 Z M8.5,0 C3.7,0 0,4 0,8.6 C0,13.2 3.7,17 8.5,17 C13.3,17 17,13.3 17,8.6 C17,3.9 13.2,1.77635684e-15 8.5,0 Z" id="Shape"></path>' +
			'</g>' +
			'</g>' +
			'</svg>';
	} else if (text === 'Tasks') { // clipboard
		icon = '<svg>' +
			'<g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 32, h / 32) + ')">' +
			'<g fill="#000000" fill-rule="nonzero">' +
			'<g><path class="svg-shortcut" d="M28 42.5l-3 2.7v-1.7c-.4 0-1.4 0-2.5.6-1.3 1-1.5 1.6-1.5 1.6s-.4-1.2.8-2.7c1.2-1.6 2.6-1.7 3.2-1.6v-1.6l3 2.7z"/></g><g><path class="svg-cluster" d="M28.5 41.3c.6 0 1.2.5 1.2 1.2s-.6 1.2-1.2 1.2-1.2-.5-1.2-1.2.5-1.2 1.2-1.2zm-4 0c.6 0 1.2.5 1.2 1.2s-.6 1.2-1.2 1.2c-.7 0-1.2-.5-1.2-1.2s.5-1.2 1.2-1.2zm-4 0c.7 0 1.2.5 1.2 1.2s-.5 1.2-1.2 1.2-1.2-.5-1.2-1.2.5-1.2 1.2-1.2z"/></g><g><path class="svg-icon02" d="M33.2 38H14.7c-.7 0-1.7-1.3-1.7-2V17c0-.7 1-2 1.7-2H16v2h-1v19h18V17h-1v-2h1.2c.7 0 1.8 1.3 1.8 2v19c0 .7-1 2-1.8 2z"/></g><g><path class="svg-icon17" d="M18 17v-2c0-.8.3-1 1-1h2.2l-.2-1c0-1.7 1.3-3 3-3 1.6 0 3 1.3 3 3 0 .3 0 .7-.2 1H29c.7 0 1 .3 1 1v2H18zm6-5.5c-.8 0-1.5.7-1.5 1.5s.7 1.5 1.5 1.5 1.5-.7 1.5-1.5-.7-1.5-1.5-1.5z"/></g><g><path class="svg-icon12" d="M18 25h12v2H18v-2zm0-2v-2h12v2H18zm12 6v2H18v-2h12z"/></g><g><path class="svg-outline" d="M34.05 36.9h-20.1a1.98 1.98 0 0 1-1.64-1.68V15.09a1.99 1.99 0 0 1 1.7-1.63H17v2.35h14.03L31 13.46h3.15a1.85 1.85 0 0 1 1.54 1.66v20.2a1.88 1.88 0 0 1-1.63 1.59z"/></g><g><path class="svg-outline" d="M17 15.81v-2.7c0-.72 1-.93 1.73-.93l2.32-.02a3.09 3.09 0 0 1 2.98-3.06A3.12 3.12 0 0 1 27 12.19h2.3c.72 0 1.7.27 1.7 1v2.62H17z"/></g><g><path class="svg-outline" d="M30.02 25.18l-12.01-.01zm0-4.65l-12.01-.02zm0 9.37l-12.01-.01z"/></g>' +
			'</g>' +
			'</g>' +
			'</svg>';
	} else if (text === 'Headphones') { // call?
		icon = '<svg>' +
			'<g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 32, h / 32) + ')">' +
			'<g fill="#000000" fill-rule="nonzero">' +
			'<g><path class="svg-shortcut" d="M28 42.5l-3 2.7v-1.7c-.4 0-1.4 0-2.5.6-1.3 1-1.5 1.6-1.5 1.6s-.4-1.2.8-2.7c1.2-1.6 2.6-1.7 3.2-1.6v-1.6l3 2.7z"/></g><g><path class="svg-cluster" d="M28.5 41.3c.6 0 1.2.5 1.2 1.2s-.6 1.2-1.2 1.2-1.2-.5-1.2-1.2.5-1.2 1.2-1.2zm-4 0c.6 0 1.2.5 1.2 1.2s-.6 1.2-1.2 1.2c-.7 0-1.2-.5-1.2-1.2s.5-1.2 1.2-1.2zm-4 0c.7 0 1.2.5 1.2 1.2s-.5 1.2-1.2 1.2-1.2-.5-1.2-1.2.5-1.2 1.2-1.2z"/></g><g><path class="svg-icon04" d="M34 20h-2c0-5.5-4-7-8-7s-8 1.5-8 7h-2c0-5.7 3.5-10 10-10s10 4.4 10 10zM24 35h-3c-.5 0-.7.4-1 1h-1c-2.8-1-2.4-1-3-3h-2c0 .2-.6 3 5 5h7v-1c0-1.7-.5-2-2-2z"/></g><g><path class="svg-icon10" d="M14 22h1s2 0 2 1v7s-1.2 1-2 1h-1c-1.8 0-3-1.2-3-3v-3c0-1.8 1.2-3 3-3zm19 9c-.8 0-2-1-2-1v-7c0-1 2-1 2-1h1c1.8 0 3 1.4 3 3v3c0 1.8-1.2 3-3 3h-1z"/></g><g><path class="svg-outline" d="M34 22h-2c0-5.46-2.46-9-8-9s-8 3.54-8 9h-2v-2c0-5.7 3.55-10 10-10s10 4.3 10 10v2zM19 38c-5.64-1.93-5-6.83-5-7 .06.03 2-.03 2 0 .02 1.97.2 4.1 3 5a4.06 4.06 0 0 0 1 0l.15-.04A1.04 1.04 0 0 1 21 35h3c1.48-.06 1.94.3 2 2v1s-6.95.02-7 0z"/></g><g><path class="svg-outline" d="M14 22h1.5c.45 0 1.5-.04 1.5.97V30a1.5 1.5 0 0 1-1.27 1H14a2.82 2.82 0 0 1-3-3v-3a2.82 2.82 0 0 1 3-3zm20 9a2.82 2.82 0 0 0 3-3v-3a2.96 2.96 0 0 0-3-3h-1.7c.06 0-1.3 0-1.3 1v7a1.62 1.62 0 0 0 1.34 1H34z"/></g>' +
			'</g>' +
			'</g>' +
			'</svg>';
	} else if (text === 'Pencil') { // edit?
		icon = '<svg>' +
			'<g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" transform="translate(' + x + ',' + y + ') scale(' + Math.min(w / 32, h / 32) + ')">' +
			'<g fill="#000000" fill-rule="nonzero">' +
			'<g><path class="svg-shortcut" d="M28 42.5l-3 2.7v-1.7c-.4 0-1.4 0-2.5.6-1.3 1-1.5 1.6-1.5 1.6s-.4-1.2.8-2.7c1.2-1.6 2.6-1.7 3.2-1.6v-1.6l3 2.7z"/></g><g><path class="svg-cluster" d="M28.5 41.3c.6 0 1.2.5 1.2 1.2s-.6 1.2-1.2 1.2-1.2-.5-1.2-1.2.5-1.2 1.2-1.2zm-4 0c.6 0 1.2.5 1.2 1.2s-.6 1.2-1.2 1.2c-.7 0-1.2-.5-1.2-1.2s.5-1.2 1.2-1.2zm-4 0c.7 0 1.2.5 1.2 1.2s-.5 1.2-1.2 1.2-1.2-.5-1.2-1.2.5-1.2 1.2-1.2z"/></g><g><path class="svg-icon18" d="M16.5 35.5L9.8 38l2.6-6.8z"/></g><g><path class="svg-icon01" d="M17.7 34.3l-4.3-4.4L29.2 14l4.2 4.5z"/></g><g><path class="svg-icon07" d="M36.4 15.6l-1.7 1.6-4.2-4.3 1.8-1.8c.8-.8 1.5-1 2.3-.3l2.3 2.4c.8.9.2 1.6-.5 2.4z"/></g><g><path class="svg-outline" d="M34.7 10a1.6 1.6 0 0 0-1 .5L13.3 30.7 10 38l7.3-3.4 20.2-20.2a1.6 1.6 0 0 0 0-2.3L36 10.6a1.6 1.6 0 0 0-1.3-.5M17.2 34.7l-4-4M35 17.2l-4-4"/></g>' +
			'</g>' +
			'</g>' +
			'</svg>';
	}
	if (icon) {
		var svg = document.getElementById('asvg');
		svg.innerHTML = getSVGContents(svg.outerHTML) + getSVGContents(icon);
	}
}

// from: https://medium.com/front-end-hacking/layering-svgs-in-javascript-72c8cc7ba98d
function getSVGContents(inputString) {
	var svgDOM = (new DOMParser()).parseFromString(inputString, 'text/xml').getElementsByTagName('svg')[0];
	return svgDOM.innerHTML;
}

function getDims(el) {
	var rect = el.getBoundingClientRect();
	return {
		x: rect.left,
		y: rect.top,
		w: rect.width,
		h: rect.height
	};
}

function isVisible(original_el, dims) {
	if (!dims) {
		dims = getDims(original_el);
	}
	var mid_x = dims.x + dims.w / 2;
	var mid_y = dims.y + dims.h / 2;
	var my_el = document.elementFromPoint(mid_x, mid_y);
	while (my_el) {
		if (my_el === original_el) {
			return true;
		} else if (my_el.parentElement) {
			my_el = my_el.parentElement;
		} else {
			return false;
		}
	}
	return false;
}

function addScript(u, callback) {
	var e = document.createElement("script");
	e.type = "text/javascript";
	e.onload = function () { //was not working on Chromecast
		if (callback) {
			callback();
		}
	};
	e.src = u;
	document.head.appendChild(e);
}

function waitFor(toTest, toRun) {
	if (toTest()) {
		toRun();
	} else {
		setTimeout(function () {
			waitFor(toTest, toRun);
		}, 499);
	}
}
