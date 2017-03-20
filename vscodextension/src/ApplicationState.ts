class ApplicationState {
    tokens: any;
    isAuthenticated: boolean;
    startTime: number;
    exerciseId: number;
    studentId: number;
    code: string;
    constructor() {
        this.tokens = {};
        this.isAuthenticated = false;
        this.startTime = Date.now();
        this.exerciseId = 1;
        this.studentId = 1;
        this.code = '';
    }
    setTokens(tokens) {
        console.log(tokens);
        this.tokens = tokens;
    }
    setAuthentication(isAuthenticated) {
        this.isAuthenticated = isAuthenticated;
    }
    setCode(code) {
        this.code = code;
    }
    setExercise(exerciseId) {
        this.exerciseId = exerciseId;
    }
}
export default ApplicationState;