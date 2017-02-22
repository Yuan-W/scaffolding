<?php
require './vendor/autoload.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

function dbConnect() {
    $MYSQL_URL = '127.0.0.1';
    $MYSQL_USER = 'root';
    $MYSQL_PASSWORD = '';
    // $MYSQL_PASSWORD = 'gs02Scaff!';
    $MYSQL_DATABASE = 'oauth';
    
    return new mysqli($MYSQL_URL, $MYSQL_USER, $MYSQL_PASSWORD, $MYSQL_DATABASE);
}

$app = new Silex\Application();

function createoAuthServer() {
    $dsn      = 'mysql:dbname=oauth;host=127.0.0.1';
    $username = 'root';
    $password = '';
    $storage = new OAuth2\Storage\Pdo(array('dsn' => $dsn, 'username' => $username, 'password' => $password));
    $oauthServer = new OAuth2\Server($storage);
    $oauthServer->addGrantType(new OAuth2\GrantType\ClientCredentials($storage));
    $oauthServer->addGrantType(new OAuth2\GrantType\AuthorizationCode($storage));
    return $oauthServer;
}

$app['oauthServer'] = createoAuthServer();

$app['debug'] = true;

$app->register(new Silex\Provider\SessionServiceProvider());

$app->get('/style.css', function() use ($app) {
    return $app->sendFile('./style.css', 200, array('Content-Type' => 'text/css'));
});

$app->get('/', function() use ($app) {
    return $app->sendFile('./views/index.html');
});

$app->get('/login', function() use ($app) {
    return $app->sendFile('./views/index.html');
});

$app->post('/login', function(Request $request) use ($app) {
    $user = $request->get('user');
    $password = $request->get('pass');
    if(empty($user) || empty($password)) {
        return $app->redirect('/login/error?error=empty');
    }
    $mysqli = dbConnect();
    $passcode = hash('sha256', $password);
    $stmt = $mysqli->prepare("SELECT * FROM users where username=? AND pass=?");
    $stmt->bind_param("ss", $user, $passcode);
    $stmt->execute();
    $stmt->store_result();
    $count = $stmt->num_rows;
    $stmt->close();

    if($count == 1) {
        $app['session']->set('login_user', $user);
        return $app->redirect('/login/success');
    } else {
        return $app->redirect('/login/error?error=fail');
    }
});

$app->get('/login/success', function() use ($app) {
    if($app['session']->has('login_user')) {
        return $app->redirect('/authorize?response_type=code&client_id=testclient&state=xyz');
    } else {
        return $app->redirect('/');
    }
});

$app->get('/login/error', function(Request $request) use ($app) {
    return file_get_contents('./views/loginError.html');
});

$app->get('/authorize', function(Request $request) use ($app) {
    if(!$app['session']->has('login_user')) {
        return $app->redirect('/');
    }


    return '
    <form method="post" action="/authorize">
        <label>Do You Authorize TestClient?</label><br />
        <input type="hidden" name="response_type" value="'. $request->get('response_type') . '">
        <input type="hidden" name="client_id" value="'. $request->get('client_id') . '">
        <input type="hidden" name="state" value="'. $request->get('state') . '">
        <input type="submit" name="authorized" value="yes">
        <input type="submit" name="authorized" value="no (will log you out)">
    </form>
    ';
});

$app->post('/authorize', function(Request $request) use ($app) {
    if(!$app['session']->has('login_user')) {
        return $app->redirect('/');
    }
    $response_type = $request->get('response_type');
    $client_id = $request->get('client_id');
    $state = $request->get('state');

    $oauthRequest = OAuth2\Request::createFromGlobals();
    $oauthResponse = new OAuth2\Response();
    if (!$app['oauthServer']->validateAuthorizeRequest($oauthRequest, $oauthResponse)) {
        $oauthResponse->send();
    }
    
    $userId = $app['session']->get('login_user');
    $isAuthorized = $request->get('authorized') === 'yes';
    if(!$isAuthorized) {
        $app['session']->clear();
        return $app->redirect('/');
    }

    $app['oauthServer']->handleAuthorizeRequest($oauthRequest, $oauthResponse, $isAuthorized, $userId);
    $code = substr($oauthResponse->getHttpHeader('Location'), strpos($oauthResponse->getHttpHeader('Location'), 'code=')+5, 40);
    return 'SUCCESS! Authorization Code: ' . $code;
});

$app->get('/token', function(Request $request) use ($app, $oauthServer) {
    $oauthServer->handleTokenRequest(OAuth2\Request::createFromGlobals())->send();
});

$app->get('/register', function() use ($app) {
    return $app->sendFile('./views/register.html');
});

$app->post('/register', function(Request $request) use ($app) {
    $user = $request->get('user');
    $password = $request->get('pass');
    $password_confirmation = $request->get('pass2');
    $instructor = $request->get('instr');
    $instructor_confirmation = $request->get('instr2');

    $isAnyInputEmpty = empty($user) || empty($password) || empty($instructor);

    if($isAnyInputEmpty) {
        return $app->redirect('/register/error?error=empty');
    }

    $passwordsMatch = $password === $password_confirmation;
    if(!$passwordsMatch) {
        return $app->redirect('/register/error?error=passMatch');
    }

    $instructorMatch = $instructor === $instructor_confirmation;
    if(!$instructorMatch) {
        return $app->redirect('/register/error?error=instrMatch');
    }

    $mysqli = dbConnect();

    $stmt = $mysqli->prepare("SELECT * FROM users where username=?");
    $stmt->bind_param("s", $user);
    $stmt->execute();
    $stmt->store_result();
    $userCount = $stmt->num_rows;
    $stmt->close();
    
    $userExists = $userCount != 0;
    if($userExists) {
        return $app->redirect('/register/error?error=user');
    }

    $passphrase = hash('sha256', $instructor);

    $stmt = $mysqli->prepare("SELECT username FROM instructors where passphrase=?");
    $stmt->bind_param("s", $passphrase);
    $stmt->execute();
    $stmt->store_result();
    $instructorCount = $stmt->num_rows;

    $instructorExists = $instructorCount != 0;
    if(!$instructorExists) {
        return $app->redirect('/register/error?error=instr');
    }
    
    $stmt->bind_result($instructorUsername);
    $stmt->fetch();
    $stmt->close();

    $passcode = hash('sha256', $password);

    $stmt = $mysqli->prepare("INSERT INTO users (username, pass, instructor) VALUES (?, ?, ?)");
    $stmt->bind_param("sss", $user, $passcode, $instructorUsername);
    $stmt->execute();
    $stmt->close();
    
    return $app->redirect('/register/success');
});

$app->get('/register/success', function(Request $request) use ($app) {
    return $app->sendFile('./views/registerSuccess.html');
});

$app->get('/register/error', function(Request $request) use ($app) {
    return $app->sendFile('./views/registerError.html');
});

$app->run();