class ApplicationState {
    tokens: any;
    isAuthenticated: boolean;
    startTime: number;
    exerciseId: number;
    studentId: number;
    code: string;
    hints_number: number;
    constructor() {
        this.tokens = {};
        this.isAuthenticated = false;
        this.startTime = Date.now();
        this.exerciseId = 1;
        this.studentId = 1;
        this.code = '';
        this.hints_number = 0;
    }
    setTokens(tokens) {
        this.tokens = tokens;
        // this.tokens = {
        //     access_token: '7f05ad622a3d32a5a81aee5d73a5826adb8cbf64'
        // };
    }
    setAuthentication(isAuthenticated) {
        this.isAuthenticated = isAuthenticated;
    }
    setStudent(studentId) {
        this.studentId = studentId;
    }
    setExercise(exerciseId) {
        this.exerciseId = exerciseId;
    }
    setCode(code) {
        this.code = code;
    }
    incrementHintsNumber() {
        this.hints_number += 1;
    }
}
export default ApplicationState;