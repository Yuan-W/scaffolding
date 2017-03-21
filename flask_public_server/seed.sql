INSERT INTO oauth_clients (client_id, client_secret, redirect_uri) VALUES ("testclient", "testpass", "http://fake/");
INSERT INTO instructors (username, pass, passphrase) VALUES ("test", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08");
INSERT INTO instructorMaster (passphrase) VALUES ("1e089e3c5323ad80a90767bdd5907297b4138163f027097fd3bdbeab528d2d68");

INSERT INTO users VALUES ('1', 'chris.teague', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d15','test');
INSERT INTO users VALUES ('2', 'michael.crouch', '7njaau28ndwawdjwijc629279323ndsjbdjanu2aw9222jwj8wmd82dim3','test');
INSERT INTO users VALUES ('3', 'matt.hemus', '1smdasd29mwdm9928dksadiad82mkamma2mif9fm2m99mmwdwdk29dfk949','test');
INSERT INTO oauth_access_tokens VALUES ('5f05ad622a3d32a5a81aee5d73a5826adb8cbf64','testclient','chris.teague' ,'2017-02-24 12:30:00', NULL);
INSERT INTO oauth_access_tokens VALUES ('6f05ad622a3d32a5a81aee5d73a5826adb8cbf63','testclient','chris.teague' ,'2017-02-24 12:30:00', NULL);
INSERT INTO oauth_access_tokens VALUES ('6f05ad622a3d32a5a81aee5d73a5826adb8cbf64','testclient','chris.teague' ,'2017-06-18 12:30:00', NULL);
INSERT INTO oauth_access_tokens VALUES ('7f05ad622a3d32a5a81aee5d73a5826adb8cbf64','testclient','chris.teague' ,'2017-06-13 12:30:00', NULL);
