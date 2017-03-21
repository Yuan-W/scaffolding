import LoginSteps from './LoginSteps';

export default function loginFlow(
    vscode,
    state,
    steps = new LoginSteps(vscode, state)
) {
    return steps.getUsername()
        .then(steps.addPassword)
        .then(steps.addConfirmation)
        .then(steps.checkConfirmation)
        .then(steps.getAuthorizationCode)
        .then(steps.getRawTokens)
        .then(steps.selectTokens)
        .then(steps.commitTokens);
}