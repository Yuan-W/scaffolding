import { expect } from 'chai';
import * as sinon from 'sinon';
import { TextDocumentChangeEvent } from 'vscode';

import { documentTextChangeHandler, activate } from '../src/extension';

// Defines a Mocha test suite to group tests of similar kind together
suite('Extension Tests', () => {
    
    suite('documentTextChangeHandler', () => {

        let codeChanges, sender, eventHandler, event;

        setup( () => {
            codeChanges = { updateChanges: sinon.stub() };
            sender = { resetSendInterval: sinon.stub() };
            eventHandler = documentTextChangeHandler(codeChanges, sender);
            event = {
                document: {
                    uri: 'foo',
                    getText: sinon.stub().returns('text')
                }
            };
        });
        
        test('When passed two objects as parameters returns eventHandler function', () => {
            expect(documentTextChangeHandler(undefined, undefined)).to.be.a('function');
        });

        test('When eventHandler is triggered calls `getText` on document in event passed', () => {
            eventHandler(event);
            expect(event.document.getText.called).to.equal(true);
        });
        
        test('When eventHandler is triggered calls `update` on codeChanges', () => {
            eventHandler(event);
            expect(codeChanges.updateChanges.called).to.equal(true);
        });
        
        test('When eventHandler is triggered calls `resetSendInterval` on sender', () => {
            eventHandler(event);
            expect(sender.resetSendInterval.called).to.equal(true);
        });

    });

});