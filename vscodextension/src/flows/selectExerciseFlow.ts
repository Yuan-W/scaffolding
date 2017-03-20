import ApplicationState from '../ApplicationState';
import {
    fetchExercises,
    showExerciseSelect
} from '../actions';

export function selectExerciseFlow(vscode, state: ApplicationState) {
    return fetchExercises()
        .then((exercises) => {
            return showExerciseSelect(vscode, exercises);
        })
        .then((exerciseId) => {
            console.log(exerciseId)
            state.setExercise(exerciseId);
        });
}

export default selectExerciseFlow;