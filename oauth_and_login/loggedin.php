<?php
session_start();
if(isset($_SESSION[login_user])) {
	header("Location: https://ubuntu.jedge.uk/authorize.php?response_type=code&client_id=testclient&state=xyz");
	die();
} else {
	header("Location: https://ubuntu.jedge.uk/");
	die();
}
?>
