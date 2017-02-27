<?php
use Silex\WebTestCase;

class LoginTest extends WebTestCase
{
    public function createApplication()
    {
        $app = require __DIR__.'/../app.php';
        unset($app['debug']);
        unset($app['exception_handler']);
        return $app;
    }
    public function testLoginPage()
    {
        $client = $this->createClient();
        $crawler = $client->request('GET', '/login');
        
        $this->assertTrue($client->getResponse()->isOk());
        $this->assertCount(1, $crawler->filter('form'));
        $this->assertCount(3, $crawler->filter('input'));
    }
    
    public function testLoginSubmit()
    {
        $client = $this->createClient();
        $crawler = $client->request('POST', '/login');

        $client->getResponse();
        
        // $this->assertTrue($client->getResponse()->isOk());
    }

}