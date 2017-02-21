import { window, MessageItem } from 'vscode';

class CodeChanges {
    private changes: any;
    private hint: any;
    private startTime: any;
    constructor(changes = [], hint = {}, startTime = Date.now()) {
        this.changes = changes;
        this.hint = hint;
        this.startTime = startTime;
    }
    getChanges() {
        return this.changes;
    }
    getStartTime() {
        return this.startTime;
    }
    getHint() {
        return this.hint;
    }
    updateChanges(newText: string, date: number) {
        const newChange = {
            date,
            code: newText
        };

        this.changes = [
            ...this.changes,
            newChange
        ];
    }
    updateHint(hint) {
        if(!this.hint || this.hint.id !== hint.id) {
            window.showInformationMessage('Try XYZ');
        }
        this.hint = hint;
    }
}

export default CodeChanges;