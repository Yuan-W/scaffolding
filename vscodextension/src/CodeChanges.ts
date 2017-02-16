import { window, MessageItem } from 'vscode';

class CodeChanges {
    private changes: any;
    private hint: any;
    private startTime: any;
    constructor(changes = {}, hint = {}, startTime = Date.now()) {
        this.changes = changes;
        this.hint = hint;
        this.startTime = startTime;
    }
    getChanges() {
        return this.changes;
    }
    getChangesPayload() {
        return {
            ...this.changes,
            startTime: this.startTime
        };
    }
    getHint() {
        return this.hint;
    }
    updateChanges(documentId: string, newText: string, date: number) {
        const prev = this.changes[documentId] || [];

        const newChange = {
            date,
            text: newText
        };

        this.changes = {
            ...this.changes,
            [ documentId ]: Array.isArray(prev) ? [ ...prev, newChange ] : [ newChange ]
        };
    }
    updateHint(hint) {
        if(!this.hint || this.hint.id !== hint.id) {
            window.showInformationMessage('Try XYZ');
        }
        this.hint = hint;
    }
}

export default CodeChanges;