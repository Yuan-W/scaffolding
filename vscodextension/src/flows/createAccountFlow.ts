import {
    LOGIN_URL
} from '../constants';

export default function createAccountFlow(vscode) {
    return vscode.window
        .showInformationMessage('You can create an account here', 'Create Account')
        .then(option => {
            if (option === 'Create Account') {
                return vscode.commands.executeCommand('vscode.open', vscode.Uri.parse(LOGIN_URL));
            }
            return vscode.window.showErrorMessage('You must have an account to start coding');
        });
}
