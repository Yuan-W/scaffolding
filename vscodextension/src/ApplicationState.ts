class ApplicationState {
    tokens: any;
    isAuthenticated: boolean;
    startTime: number;
    exerciseId: number;
    constructor() {
        this.tokens = {};
        this.isAuthenticated = false;
        this.startTime = Date.now();
        this.exerciseId = 1;
    }
    setTokens(tokens) {
        console.log(tokens);
        this.tokens = tokens;
    }
    setAuthentication(isAuthenticated) {
        this.isAuthenticated = isAuthenticated;
    }
}
export default ApplicationState;