'use strict';
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

import CodeChanges from './CodeChanges';
import CodeChangeSender from './CodeChangeSender';

export function documentTextChangeHandler(codeChanges, sender) {
    return (e) => {
        const { document } = e;
        const id = document.uri.toString();
        const text = document.getText();
        codeChanges.updateChanges(id, text);
        sender.resetSendInterval(5000);
    };
}

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Scaffolding is active!');

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with  registerCommand
    // The commandId parameter must match the command field in package.json

    let disposable = vscode.commands.registerCommand('extension.scaffoldStart', () => {
        // The code you place here will be executed every time your command is executed

        // Display a message box to the user
        vscode.window.showInformationMessage('Start Coding');

        const codeChanges = new CodeChanges;
        const sender = new CodeChangeSender(codeChanges);

        let listener = vscode.workspace.onDidChangeTextDocument(documentTextChangeHandler(codeChanges, sender));

        context.subscriptions.push(listener);
    });

    context.subscriptions.push(disposable);
}

// this method is called when your extension is deactivated
export function deactivate() {
}