import { expect } from 'chai';
import * as sinon from 'sinon';
import { TextDocumentChangeEvent } from 'vscode';

import { documentTextChangeHandler } from '../src/actions';

suite('Action Tests', () => {

    suite('documentTextChangeHandler', () => {

        let state, eventHandler, event;

        setup(() => {
            state = {};
            eventHandler = documentTextChangeHandler(state);
            event = {
                document: {
                    getText: sinon.stub().returns('text')
                }
            };
        });

        test('When passed two objects as parameters returns eventHandler function', () => {
            expect(documentTextChangeHandler(undefined)).to.be.a('function');
        });

        test('When eventHandler is triggered calls `getText` on document in event passed', () => {
            eventHandler(event);
            expect(event.document.getText.called).to.equal(true);
        });

    });

});