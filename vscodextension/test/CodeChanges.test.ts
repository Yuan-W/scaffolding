import { expect } from 'chai';
import * as sinon from 'sinon';
import * as proxyquire from 'proxyquire';

import CodeChanges from '../src/CodeChanges';

suite('CodeChanges', () => {
    let codeChanges;
    setup( () => {
        codeChanges = new CodeChanges;
    });

    test('When CodeChanges is instantiated, it sets `hint` to {}', () => {
        expect(codeChanges.getHint()).to.deep.equal({});
    });

    test('When CodeChanges is instantiated, it sets `changes` to {}', () => {
        expect(codeChanges.getChanges()).to.deep.equal({});
    });

    suite('#updateChanges', () => {

        test('When called with documentId and newText and documentId is not in `changes` creates a new array of changes with element newText', () => {
            codeChanges.updateChanges('id', 'text');
            expect(codeChanges.getChanges().id).to.deep.equal([ 'text' ]);
        });

        test('When called with documentId and newText and documentId is in `changes` append to current array of changes', () => {
            codeChanges = new CodeChanges({ id: [ 'text' ]});
            codeChanges.updateChanges('id', 'newText');
            expect(codeChanges.getChanges().id).to.deep.equal([ 'text', 'newText' ]);
        });

        test('When called with documentId and newText, it does not mutate data under any other id', () => {
            const prevChanges = {
                foo: [ 'bar' ],
                baz: [ 'foobar' ]
            };
            codeChanges = new CodeChanges(prevChanges);
            codeChanges.updateChanges('id', 'newText');
            const { id, ...rest } = codeChanges.getChanges();
            expect(rest).to.deep.equal(prevChanges);
        });

    });

    suite('#updateHint', () => {

        test('When called with a hint saves it in state', () => {
            const newHint = { id: '0', text: 'blaaaa' };
            codeChanges.updateHint(newHint);
            expect(codeChanges.getHint()).to.deep.equal(newHint);
        });

        test('When called with a hint that has a different id to the previous hint, calls `showInformationMessage`', () => {
            const vscodeStub = { window: { showInformationMessage: sinon.stub() } };
            const CodeChanges = proxyquire.noCallThru().load('../src/CodeChanges', {
                'vscode': vscodeStub
            }).default;

            codeChanges = new CodeChanges(null, { id: '0' });

            codeChanges.updateHint({ id: '1' });
            expect(vscodeStub.window.showInformationMessage.called).to.equal(true);
        });

        test('When called with a new hint, calls `showInformationMessage`', () => {
            const vscodeStub = { window: { showInformationMessage: sinon.stub() } };
            const CodeChanges = proxyquire.noCallThru().load('../src/CodeChanges', {
                'vscode': vscodeStub
            }).default;

            codeChanges = new CodeChanges(null, null);

            codeChanges.updateHint({ id: '1' });
            expect(vscodeStub.window.showInformationMessage.called).to.equal(true);
        });
    });

});