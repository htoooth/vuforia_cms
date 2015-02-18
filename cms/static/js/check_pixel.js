var img2 = new Image();


$("#afile").onchange = function(evt){
	var files = evt.target.files;
	if(files.length == 0) return;

	var file = files[0];
	if(!file.type.match(/image/)) {
		alert('画像ファイルを選んでください');
		return;
	}

	// 変更されたファイルを読み込む。
	var reader = new FileReader();
	// 読み込まれた時のイベントハンドラー
	reader.onload = function(evt) {
		$("#new_image").src = reader.result;

		img1 = $("#new_image");

		// img2 = new Image();
		img2.src = img1.src;
		
		// JS実行中は、img2.widthがセットされないので待つ。
		setTimeout( 'alert_pixel()', 1000 );

	}

	reader.readAsDataURL(file);

}


function showImage(b) {
	var val = b ? "block" : "none";
	// $("#up_btn").style.display = val;
	$("#new_image").style.display = val;
}

function $(id) {
	return document.querySelector(id);
}



function alert_pixel() {
	// alert(img2.width + "," + img2.height);
	if( img2.width != 0 && img2.height != 0 ) {
		if( img2.width < 600 || img2.height < 600 ) {
			alert("600ピクセルより小さい画像の場合、認識されにくくなります。");
			// alert(img2.width + "," + img2.height);
		} else {
			// alert("ピクセル数が十分あります。");
		}
	} else {
		// alert("ピクセル数は取得できませんでした。");
	}
}

