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
        .then(steps.getData)
        .then(steps.getRawTokens)
        .then(steps.getData)
        .then(steps.selectTokens)
        .then(steps.commitTokens);
}