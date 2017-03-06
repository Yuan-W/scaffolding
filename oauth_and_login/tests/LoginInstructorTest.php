<?php
use Silex\WebTestCase;

class LoginInstructorTest extends WebTestCase
{
    public function createApplication()
    {
        $app = require __DIR__.'/../app.php';
        unset($app['debug']);
        unset($app['exception_handler']);
        return $app;
    }
    public function testInstructorPage()
    {
        $client = $this->createClient();
        $crawler = $client->request('GET', '/login/instructor');
        
        $this->assertTrue($client->getResponse()->isOk());
        $this->assertCount(1, $crawler->filter('form'));
        $this->assertCount(2, $crawler->filter('input'));
    }
    
    public function testInstructorSubmit()
    {
        $client = $this->createClient();
        $crawler = $client->request('POST', '/login/instructor');

        $client->getResponse();
        
        // $this->assertTrue($client->getResponse()->isOk());
    }

}