import ApplicationState from '../ApplicationState';
import {
    fetchHints,
    showHint
} from '../actions';

export function requestHintFlow(vscode, state: ApplicationState) {
    const { code } = state;
    if(code === '') {
        return vscode.window.showWarningMessage('Write some code before requesting a hint :)');
    }
    const { exerciseId, studentId, startTime, tokens, hints_number } = state;
    const { access_token } = tokens;
    const timeSpent = Date.now() - startTime;

    const payload = {
        headers: {
            access_token,
            'Content-Type': 'application/json'
        },
        data: {
            code: JSON.stringify(code).slice(1, -1),
            time_spent: timeSpent,
            exercise_id: exerciseId,
            hints_number
        }
    };

    return fetchHints(payload)
        .then((data) => {
            const { hints = 'This is a hint', student_id } = data;
            state.setStudent(student_id);
            state.incrementHintsNumber();
            return hints;
        })
        .then((message) => {
            return showHint(vscode, message);
        });
}

export default requestHintFlow;