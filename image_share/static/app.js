// Global image file.
var IMAGE_FILE;

function sendFileFromPaste() {
	var file = IMAGE_FILE;
	sendFileGivenFile(file);
}

function sendFileCallback(response) {
	console.log(response);
	var $imageUrl = $('#image-url');
	response = JSON.parse(response);
	console.log(response.url);

	let a = $("<a></a>").text(response.url);
	a.attr('href', response.url);
	a.attr('id', 'image-url-link')
	$imageUrl.html(a);
}

function sendFileGivenFile(file) {
	var formData = new FormData();
	formData.append('file', file);

	console.log(file);

	var xhr = new XMLHttpRequest();

	xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      sendFileCallback(xhr.response);
    }
	}

	// Add any event handlers here...
	xhr.open('POST', '/uploader', true);
	xhr.send(formData);
}

function sendFile() {
	console.log("Send Files");
	// The Javascript
	var fileInput = document.getElementById('the-file');
	var file = fileInput.files[0];
	sendFileGivenFile(file);
}

$(document).ready(function() {

	var $content = $('.content');

	var $message = $('.message');
	var timeoutId;
	function showMessage(message, reset) {
		if (timeoutId) clearTimeout(timeoutId);
		$message.html(message);
		if (reset) {
			timeoutId = setTimeout(function() {
				$message.html('Paste (Ctrl+v) your image');
				timeoutId = undefined;
			}, 2000);
		}
	}

	var $img = $('img').hide();
	function loadImage(file) {
		var deferred = new $.Deferred();
		var reader = new FileReader();

		showMessage('Loading image...');
		reader.onload = function(e) {
			$img.show();
			$img.attr('src', e.target.result);
			$canvas.hide();
			$content.addClass('has-image');
			showMessage('Image pasted. You can paste again to replace.');
			setTimeout(function() {
				deferred.resolve();
			}, 25);
		};
		reader.readAsDataURL(file);
		return deferred;
	};

	var $canvas = $('canvas').hide();
	var $size = $('.image-size');
	function copyImageInCanvas() {
		var canvas = $canvas[0];
		var ctx = canvas.getContext("2d");
		var image = $img[0];

		showMessage('Copying to canvas...');
		canvas.width = image.naturalWidth;
		canvas.height = image.naturalHeight;
		ctx.drawImage(image, 0, 0);
		$img.hide();
		$canvas.show();
		showMessage('Image pasted. You can paste again to replace.');
		$size.html(image.naturalWidth + ' x ' + image.naturalHeight);
	}

	var IMAGE_MIME_REGEX = /^image\/(p?jpeg|gif|png)$/i;
	$(document).on('paste', function(e) {
    if (!e.originalEvent.clipboardData || !e.originalEvent.clipboardData.items) return;

		var items = e.originalEvent.clipboardData.items;
		for (var i = 0; i < items.length; i++) {
			if (IMAGE_MIME_REGEX.test(items[i].type)) {
				loadImage(items[i].getAsFile()).done(copyImageInCanvas);
				console.log(items[i].getAsFile());
				var file = items[i].getAsFile();
				IMAGE_FILE = file;
				// sendFileGivenFile(file);
				return;
			}
			showMessage('No image found on your Clipboard!', true);
		}
	});

	var $mouse = $('.mouse-position');
	$canvas.on('mousemove', function(e) {
		var x = Math.round(e.pageX - $(this).offset().left);
		var y = Math.round(e.pageY - $(this).offset().top);
		$mouse.html(x + ', ' + y);
	});

	$message.first().html('Copy your screen by pressing on the Print Screen key. Then paste (Ctrl+v) it here as an image.');
});