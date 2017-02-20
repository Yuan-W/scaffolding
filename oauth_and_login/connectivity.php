<?php
function SignIn() {
	$mysqli = new mysqli("127.0.0.1", "root", "gs02Scaff!", "oauth");
	session_start();
	if(!empty($_POST['user']))
	{
		$username = $_POST[user];
		$passcode = hash('sha256', $_POST[pass]);
		$stmt = $mysqli->prepare("SELECT * FROM users where username=? AND pass=?");
		$stmt->bind_param("ss", $username, $passcode);
//		echo $username;
//		$username = $_POST[user];
//		$passcode = hash('sha256', $_POST[pass]);
//		$result = $mysqli->query("SELECT * FROM users where username = '$username' AND pass = '$passcode'");
		$stmt->execute();
		$stmt->store_result();
		$count = $stmt->num_rows;
    		$stmt->close();
		if($count == 1) {
			$_SESSION[login_user] = $username;
			header("Location: https://ubuntu.jedge.uk/loggedin.php");
			die();
//			echo "SUCCESSFULLY LOGIN TO USER PROFILE PAGE...";
		}
		else {
			echo "SORRY... YOU ENTERD WRONG ID AND PASSWORD... PLEASE RETRY...";
		}
	}
}
if(isset($_POST['submit']))
	{
		SignIn();
	}
?>
