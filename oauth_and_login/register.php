<?php
function Register() {
	$mysqli = new mysqli("127.0.0.1", "root", "gs02Scaff!", "oauth");
	session_start();
	if(!empty($_POST['user']) || !empty($_POST['pass']) || !empty($_POST['inst']))
	{
		$username = $_POST[user];
		$passcode = hash('sha256', $_POST[pass]);
		$passcode2 = hash('sha256', $_POST[pass2]);
		$instructor = hash('sha256', $_POST[instr]);
		$instructor2 = hash('sha256', $_POST[instr2]);
		if ($passcode === $passcode2) {
			if ($instructor === $instructor2) {
				$stmt = $mysqli->prepare("SELECT * FROM users where username=?");
				$stmt->bind_param("s", $username);
				$stmt->execute();
				$stmt->store_result();
				$count = $stmt->num_rows;
				if ($count == 0) {
					$stmt2 = $mysqli->prepare("SELECT username FROM instructors where passphrase=?");
					$stmt2->bind_param("s", $instructor);
					$stmt2->execute();
					$stmt2->store_result();
					$count2 = $stmt2->num_rows;
					if ($count2 == 1) {
						$stmt2->bind_result($instructorusername);
      					$stmt2->fetch();
						$stmt3 = $mysqli->prepare("INSERT INTO users (username, pass, instructor) VALUES (?, ?, ?)");
						$stmt3->bind_param("sss", $username, $passcode, $instructorusername);
						$stmt3->execute();
						header("Location: https://ubuntu.jedge.uk/registerSuccess.html");
						die();
					}
					else {
						header("Location: https://ubuntu.jedge.uk/registerError.html?error=instr");
						die();
					}
				}
				else {
					header("Location: https://ubuntu.jedge.uk/registerError.html?error=user");
					die();
				}
			}
			else {
				header("Location: https://ubuntu.jedge.uk/registerError.html?error=instrMatch");
				die();
			}
		}
		else {
			header("Location: https://ubuntu.jedge.uk/registerError.html?error=passMatch");
			die();
		}
	}
	else {
		header("Location: https://ubuntu.jedge.uk/registerError.html?error=empty");
		die();
	}
}
if(isset($_POST['submit']))
	{
		Register();
	}
?>

