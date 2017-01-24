import { expect } from 'chai';
import * as sinon from 'sinon';

import CodeChangeSender from '../src/CodeChangeSender';
import CodeChanges from '../src/CodeChanges';

suite('CodeChangeSender', () => {

    let sender, setIntervalStub, clearIntervalStub;
    setup( () => {
        sender = new CodeChangeSender(new CodeChanges);
        global.setInterval = sinon.stub();
        setIntervalStub = global.setInterval;
        setIntervalStub.onCall(0).returns(1);
        setIntervalStub.onCall(1).returns(2);
        global.clearInterval = sinon.stub();
        clearIntervalStub = global.clearInterval;
    });

    suite('#resetSendInterval', () => {

        test('When called, calls clearInterval', () => {
            sender.resetSendInterval();
            expect(clearIntervalStub.called).to.equal(true);
        });

        test('When called, updates `sendInterval`', () => {
            const oldSendInterval = sender.getSendInterval();
            sender.resetSendInterval();
            expect(sender.getSendInterval()).to.not.equal(oldSendInterval);
        });

        test('When called, calls setInterval with time param', () => {
            sender.resetSendInterval(1000);
            expect(setIntervalStub.getCall(0).args[1]).to.equal(1000);
        });

    });

    suite('#send', () => {

        let fetch, thenStub, catchStub;

        setup( () => {
            thenStub = {
                then: sinon.stub()
            };
            catchStub = {
                catch: sinon.stub()
            }
            fetch = {
                post: sinon.stub()
            };

            fetch.post.returns(thenStub);
            thenStub.then.returns(catchStub);
        });

        test('When called, calls clearInterval before initiating request', () => {
            sender.send();
            expect(clearIntervalStub.called).to.equal(true);
        });

        test('When called, calls fetch.post', () => {
            sender.send(fetch);
            expect(fetch.post.called).to.equal(true);
        });

    });


});