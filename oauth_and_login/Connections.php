<?php
namespace App;

$dotenv = new \Dotenv\Dotenv(__DIR__);
$dotenv->load();

function env($name, $defaultValue)
{
    $envValue = getenv($name);
    return ($envValue || $envValue === '') ? $envValue : $defaultValue;
}

class Connections
{
    public static function dbConnect()
    {
        $MYSQL_URL = env('MYSQL_URL', '');
        $MYSQL_USER = env('MYSQL_USER', '');
        $MYSQL_PASSWORD = env('MYSQL_PASSWORD', '');
        $MYSQL_DATABASE = env('MYSQL_DATABASE', '');
    
        return new \mysqli($MYSQL_URL, $MYSQL_USER, $MYSQL_PASSWORD, $MYSQL_DATABASE);
    }

    public static function createoAuthServer()
    {
        $host = env('MYSQL_URL', '');
        $dbname = env('MYSQL_DATABASE', '');
        $dsn = "mysql:dbname={$dbname};host={$host}";
        $username = env('MYSQL_USER', '');
        $password = env('MYSQL_PASSWORD', '');
        $storage = new \OAuth2\Storage\Pdo(compact('dsn', 'username', 'password'));
        $oauthServer = new \OAuth2\Server($storage);
        $oauthServer->addGrantType(new \OAuth2\GrantType\ClientCredentials($storage));
        $oauthServer->addGrantType(new \OAuth2\GrantType\AuthorizationCode($storage));
        return $oauthServer;
    }
}
