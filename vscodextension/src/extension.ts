'use strict';

import * as vscode from 'vscode';
import ApplicationState from './ApplicationState';
import { documentTextChangeHandler } from './actions';
import loginFlow from './loginFlow';
import createAccountFlow from './createAccountFlow';

export function activate(context: vscode.ExtensionContext) {
    console.log('Scaffolding is active!');

    const state = new ApplicationState;
    vscode.workspace.onDidChangeTextDocument(documentTextChangeHandler(state));

    let disposable = vscode.commands.registerCommand('extension.scaffoldBegin', () => {
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

    vscode.commands.registerCommand('extension.requestHint', () => {
        if (!state.isAuthenticated) {
            vscode.window.showWarningMessage('Please run \'Scaffolding: begin exercise\' first');
        } else {
            vscode.window.showInformationMessage('This is a hint')
                .then(console.log);
        }
    });

    context.subscriptions.push(disposable);
}

// this method is called when your extension is deactivated
export function deactivate() {
}