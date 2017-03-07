'use strict';

import * as vscode from 'vscode';
import ApplicationState from './ApplicationState';
import { documentTextChangeHandler } from './actions';
import {
    loginFlow,
    createAccountFlow,
    requestHintFlow
} from './flows';

export function activate(context: vscode.ExtensionContext) {
    const state = new ApplicationState;

    let documentChange = vscode.workspace.onDidChangeTextDocument(documentTextChangeHandler(state));

    let scaffoldBegin = vscode.commands.registerCommand('extension.scaffoldBegin', () => {
        if (!state.isAuthenticated) {
            return vscode.window.showInformationMessage('Do you have an account?', 'Yes', 'No')
                .then(option => {
                    if (option === 'Yes') {
                        return loginFlow(vscode, state);
                    }
                    return createAccountFlow(vscode);
                });
        }
        vscode.window.showInformationMessage('Start Coding, you can request a hint any time');
    });

    let requestHint = vscode.commands.registerCommand('extension.requestHint', () => {
        if (!state.isAuthenticated) {
            return vscode.window.showWarningMessage('Please run \'Scaffolding: begin exercise\' first');
        }
        return requestHintFlow(vscode, state);
    });

    context.subscriptions.push(documentChange);
    context.subscriptions.push(scaffoldBegin);
    context.subscriptions.push(requestHint);
}

// this method is called when your extension is deactivated
export function deactivate() {
}