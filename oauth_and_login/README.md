# oAuth and Login Service

## Installation

Install composer, PHP7, MySQL and PHP command line tools.

Create `oauth` database in MySQL and run:
```sql
CREATE TABLE oauth_clients (client_id VARCHAR(80) NOT NULL, client_secret VARCHAR(80), redirect_uri VARCHAR(2000) NOT NULL, grant_types VARCHAR(80), scope VARCHAR(100), user_id VARCHAR(80), CONSTRAINT clients_client_id_pk PRIMARY KEY (client_id));
CREATE TABLE oauth_access_tokens (access_token VARCHAR(40) NOT NULL, client_id VARCHAR(80) NOT NULL, user_id VARCHAR(255), expires TIMESTAMP NOT NULL, scope VARCHAR(2000), CONSTRAINT access_token_pk PRIMARY KEY (access_token));
CREATE TABLE oauth_authorization_codes (authorization_code VARCHAR(40) NOT NULL, client_id VARCHAR(80) NOT NULL, user_id VARCHAR(255), redirect_uri VARCHAR(2000), expires TIMESTAMP NOT NULL, scope VARCHAR(2000), CONSTRAINT auth_code_pk PRIMARY KEY (authorization_code));
CREATE TABLE oauth_jwt (client_id VARCHAR(80) NOT NULL, subject VARCHAR(80), public_key VARCHAR(2000), CONSTRAINT jwt_client_id_pk PRIMARY KEY (client_id));
CREATE TABLE oauth_refresh_tokens (refresh_token VARCHAR(40) NOT NULL, client_id VARCHAR(80) NOT NULL, user_id VARCHAR(255), expires TIMESTAMP NOT NULL, scope VARCHAR(2000), CONSTRAINT refresh_token_pk PRIMARY KEY (refresh_token));
CREATE TABLE oauth_scopes (scope TEXT, is_default BOOLEAN);

CREATE TABLE users (id int(6) NOT NULL AUTO_INCREMENT, username VARCHAR(255) NOT NULL, pass VARCHAR(255) NOT NULL, instructor VARCHAR(255) NOT NULL, PRIMARY KEY (id));
CREATE TABLE instructors (id int(6) NOT NULL AUTO_INCREMENT, username VARCHAR(255) NOT NULL, pass VARCHAR(255) NOT NULL, passphrase VARCHAR(255) NOT NULL, PRIMARY KEY (id));
CREATE TABLE instructorMaster (passphrase VARCHAR(255) NOT NULL, PRIMARY KEY (passphrase));
```

Create an oauth client with id 'testclient' and an instructor with name and passphrase 'test':
```sql
INSERT INTO oauth_clients (client_id, client_secret, redirect_uri) VALUES ("VSCode", "password", "http://");
INSERT INTO oauth_clients (client_id, client_secret, redirect_uri) VALUES ("Dashboard", "password", "http://");
INSERT INTO instructors (instructor, pass, passphrase) VALUES ("test", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08");
INSERT INTO instructorMaster (passphrase) VALUES ("1e089e3c5323ad80a90767bdd5907297b4138163f027097fd3bdbeab528d2d68");
```

Copy `.env.example` to `.env` and modify with the correct MySQL local login credentials.

Run `composer install`.

Use `php -S localhost:5000 app.php` to run the server locally on `http://localhost:5000`.

## Testing

You need `phpunit` installed.

Run `phpunit`.
