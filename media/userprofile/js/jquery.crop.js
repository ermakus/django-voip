// source image size
var crop_img_size = {
	width: 0,
	height: 0
};

function previewAvatar(img, selection) {
	var scaleX = DEFAULT_AVATAR_SIZE / (selection.width || 1);
	var scaleY = DEFAULT_AVATAR_SIZE / (selection.height || 1);
	$('#avatarimg').css({
		width: Math.round(scaleX * crop_img_size.width) + 'px',
		height: Math.round(scaleY * crop_img_size.height) + 'px',
		marginLeft: '-' + Math.round(scaleX * selection.x1) + 'px',
		marginTop: '-' + Math.round(scaleY * selection.y1) + 'px'
	});
}

function updateValues(img, selection) {
	$("input[name='left']").val(selection.x1);
	$("input[name='top']").val(selection.y1);
	$("input[name='right']").val(selection.x2);
	$("input[name='bottom']").val(selection.y2);
}

$(function() {
	// display legend (hidden if no js)
	$('form[name=cropavatar] legend').show();

	$("#cropimage").one("load", function() {

		//calculate source image size
		crop_img_size.width = $('#cropimage').width();
		crop_img_size.height = $('#cropimage').height();

		// calculate initial selection (maximum square)
		var selection = {
			x1: 0, x2: 0, y1: 0, y2: 0,
			width: 0, height: 0
		}
		if (crop_img_size.width > crop_img_size.height) {
			selection.width = selection.height = crop_img_size.height;
			var diff = (crop_img_size.width - crop_img_size.height) / 2;
			selection.x1 = diff;
			selection.x2 = crop_img_size.width - diff;
			selection.y2 = crop_img_size.height;
		} else {
			selection.width = selection.height = crop_img_size.width;
			var diff = (crop_img_size.height - crop_img_size.width) / 2;
			selection.x2 = crop_img_size.width;
			selection.y1 = diff;
			selection.y2 = crop_img_size.height - diff;
		}

		// prepare avatarimg and its container
		$('#avatarimg_container').css({
			position: 'relative',
			overflow: 'hidden',
			width: DEFAULT_AVATAR_SIZE + 'px',
			height: DEFAULT_AVATAR_SIZE + 'px',
			margin: 'auto',
			padding: '1px'
		});
		$('#avatarimg').attr('src', $("#cropimage").attr('src')).css({
			position: 'relative'
		}).removeClass('border');

		// simulate a first preview with initial selection
		previewAvatar($("#cropimage"), selection);
	
		// run imgAreaSelect
		$("#cropimage").imgAreaSelect({
			handles: 'corners',
			aspectRatio: "1:1",
			minHeight: MIN_AVATAR_SIZE,
			minWidth: MIN_AVATAR_SIZE,
			x1: selection.x1,
			x2: selection.x2,
			y1: selection.y1,
			y2: selection.y2,
			onSelectChange: previewAvatar,
			onSelectEnd: updateValues
		});
	})
	.each(function() {
		if (this.complete || (jQuery.browser.msie && parseInt(jQuery.browser.version) == 6))
		$(this).trigger("load");
	});
});

