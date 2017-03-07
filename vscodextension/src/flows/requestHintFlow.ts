import ApplicationState from '../ApplicationState';
import {
    sendCodeChanges,
    showHint
} from '../actions';

export function requestHintFlow(vscode, state: ApplicationState) {
    const { code, exerciseId, studentId, startTime, tokens } = state;
    const { access_token } = tokens;
    const timeSpent = Date.now() - startTime;

    const payload = {
        data: `code=${code}&time_spent=${timeSpent}&exercise_id=${exerciseId}&student_id=${studentId}`,
        headers: {
            access_token
        }
    }

    return sendCodeChanges(payload)
        .then(({ message = 'This is a hint' }) => {
            return message;
        }).then((message) => {
            return showHint(vscode, message);
        });
}

export default requestHintFlow;