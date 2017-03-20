import ApplicationState from '../ApplicationState';
import {
    fetchExercises,
    showExerciseSelect
} from '../actions';

export function selectExerciseFlow(vscode, state: ApplicationState) {
    const { tokens } = state;
    const { access_token } = tokens;
    return fetchExercises(access_token)
        .then((exercises) => {
            return showExerciseSelect(vscode, exercises);
        })
        .then(({ label: exerciseId } = {}) => {
            if(exerciseId === undefined) {
                return vscode.window.showWarningMessage('Please select an exercise if you wish to receive hints');
            }
            state.setExercise(exerciseId);
        });
}

export default selectExerciseFlow;