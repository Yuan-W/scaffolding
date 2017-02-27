<?php
require './vendor/autoload.php';
require_once './Connections.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

use App\Connections;

$app = new Silex\Application();

$app->register(new Silex\Provider\SessionServiceProvider(), [
    'session.test' => false !== getenv('TEST')
]);

$app->register(new Silex\Provider\TwigServiceProvider(), array(
    'twig.path' => __DIR__.'/views',
));

$app->before(function () use ($app) {
    $app['twig']->addGlobal('layout', null);
    $app['twig']->addGlobal('layout', $app['twig']->loadTemplate('layout.twig'));
});

$app['oauthServer'] = Connections::createoAuthServer();

$app['debug'] = true;

$app->get('/', function () use ($app) {
    return $app['twig']->render('login.twig');
});

$app->get('/login', function () use ($app) {
    return $app['twig']->render('login.twig');
});

$app->post('/login', function (Request $request) use ($app) {
    $user = $request->get('user');
    $password = $request->get('pass');
    if (empty($user) || empty($password)) {
        $app['session']->getFlashBag()->set('error', 'Username or Password empty.');
        return $app->redirect('/login');
    }
    $mysqli = Connections::dbConnect();
    $passcode = hash('sha256', $password);
    $stmt = $mysqli->prepare("SELECT * FROM users where username=? AND pass=?");
    $stmt->bind_param("ss", $user, $passcode);
    $stmt->execute();
    $stmt->store_result();
    $count = $stmt->num_rows;
    $stmt->close();

    if ($count == 1) {
        $app['session']->set('login_user', $user);
        return $app->redirect('/authorize?response_type=code&client_id=testclient&state=xyz');
    } else {
        $app['session']->getFlashBag()->set('error', 'Username or Password incorrect.');
        return $app->redirect('/login');
    }
});

$app->get('/authorize', function (Request $request) use ($app) {
    if (!$app['session']->has('login_user')) {
        $app['session']->getFlashBag()->set('error', 'Not logged in.');
        return $app->redirect('/');
    }

    $response_type = $request->get('response_type');
    $client_id = $request->get('client_id');
    $state = $request->get('state');

    return $app['twig']->render('authorize.twig', compact('response_type', 'client_id', 'state'));
});

$app->post('/authorize', function (Request $request) use ($app) {
    if (!$app['session']->has('login_user')) {
        $app['session']->getFlashBag()->set('error', 'Not logged in.');
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
    if (!$isAuthorized) {
        $app['session']->clear();
        $app['session']->getFlashBag()->set('error', 'Not authorized.');
        return $app->redirect('/');
    }

    $app['oauthServer']->handleAuthorizeRequest($oauthRequest, $oauthResponse, $isAuthorized, $userId);
    $code = substr($oauthResponse->getHttpHeader('Location'), strpos($oauthResponse->getHttpHeader('Location'), 'code=')+5, 40);

    return $app['twig']->render('authorizeSuccess.twig', compact('code'));
});

$app->get('/token', function (Request $request) use ($app) {
    $app['oauthServer']->handleTokenRequest(OAuth2\Request::createFromGlobals())->send();
});

$app->get('/register', function () use ($app) {
    return $app['twig']->render('register.twig');
});

$app->post('/register', function (Request $request) use ($app) {
    $user = $request->get('user');
    $password = $request->get('pass');
    $password_confirmation = $request->get('pass2');
    $instructor = $request->get('instr');
    $instructor_confirmation = $request->get('instr2');

    $isAnyInputEmpty = empty($user) || empty($password) || empty($instructor);

    if ($isAnyInputEmpty) {
        $app['session']->getFlashBag()->set('error', 'Username, Password or Instructor empty.');
        return $app->redirect('/register');
    }

    $passwordsMatch = $password === $password_confirmation;
    if (!$passwordsMatch) {
        $app['session']->getFlashBag()->set('error', 'Passwords don\'t match.');
        return $app->redirect('/register');
    }

    $instructorMatch = $instructor === $instructor_confirmation;
    if (!$instructorMatch) {
        $app['session']->getFlashBag()->set('error', 'Passphrases don\'t match.');
        return $app->redirect('/register');
    }

    $mysqli = Connections::dbConnect();

    $stmt = $mysqli->prepare("SELECT * FROM users where username=?");
    $stmt->bind_param("s", $user);
    $stmt->execute();
    $stmt->store_result();
    $userCount = $stmt->num_rows;
    $stmt->close();
    
    $userExists = $userCount != 0;
    if ($userExists) {
        $app['session']->getFlashBag()->set('error', 'Username already in use.');
        return $app->redirect('/register');
    }

    $passphrase = hash('sha256', $instructor);

    $stmt = $mysqli->prepare("SELECT username FROM instructors where passphrase=?");
    $stmt->bind_param("s", $passphrase);
    $stmt->execute();
    $stmt->store_result();
    $instructorCount = $stmt->num_rows;

    $instructorExists = $instructorCount != 0;
    if (!$instructorExists) {
        $app['session']->getFlashBag()->set('error', 'Instructor doesn\'t exist.');
        return $app->redirect('/register');
    }
    
    $stmt->bind_result($instructorUsername);
    $stmt->fetch();
    $stmt->close();

    $passcode = hash('sha256', $password);

    $stmt = $mysqli->prepare("INSERT INTO users (username, pass, instructor) VALUES (?, ?, ?)");
    $stmt->bind_param("sss", $user, $passcode, $instructorUsername);
    $stmt->execute();
    $stmt->close();
    
    return $app['twig']->render('registerSuccess.twig');
});

$app->run();

return $app;
