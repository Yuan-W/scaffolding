<?php
use Silex\WebTestCase;

class RegisterTest extends WebTestCase
{
    public function createApplication()
    {
        $app = require __DIR__.'/../app.php';
        unset($app['debug']);
        unset($app['exception_handler']);
        return $app;
    }

    public function testRegisterPage()
    {
        $client = $this->createClient();
        $crawler = $client->request('GET', '/register');
        
        $this->assertTrue($client->getResponse()->isOk());
        $this->assertCount(1, $crawler->filter('form'));
        $this->assertCount(6, $crawler->filter('input'));
    }
}