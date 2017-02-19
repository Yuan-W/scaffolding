import { expect } from 'chai';
import request from 'supertest';
import app from 'app';

describe('Test Runner API', () => {
    it('should respond 200 OK if sent code and testCode', (done) => {
        request(app)
            .post('/test')
            .send({ code: 'print \'hello\'', testCode: 'print \'world\'' })
            .expect(200)
            .end((err, res) => {
                if(err) throw err;
                done();
            });
    });
    it('should respond 400 if sent nothing', (done) => {
        request(app)
            .post('/test')
            .send({})
            .expect(400)
            .end((err, res) => {
                if(err) throw err;
                done();
            });
    });
    it('should respond 400 if sent only code', (done) => {
        request(app)
            .post('/test')
            .send({ code: 'print \'hello\''})
            .expect(400)
            .end((err, res) => {
                if(err) throw err;
                done();
            });
    });
    it('should respond 400 if sent only testCode', (done) => {
        request(app)
            .post('/test')
            .send({ testCode: 'print \'hello\''})
            .expect(400)
            .end((err, res) => {
                if(err) throw err;
                done();
            });
    });
})
