import { window, MessageItem } from 'vscode';

class CodeChanges {
    private changes: any;
    private hint: any;
    constructor(changes = {}, hint = {}) {
        this.changes = changes || {};
        this.hint = hint || {};
    }
    getChanges() {
        return this.changes;
    }
    getHint() {
        return this.hint;
    }
    updateChanges(documentId: string, newText: string) {
        const prev = this.changes[documentId];
        this.changes = {
            ...this.changes,
            [ documentId ]: Array.isArray(prev) ? [ ...prev, newText ] : [ newText ]
        };
    }
    updateHint(hint) {
        if(this.hint.id !== hint.id) {
            window.showInformationMessage('Try XYZ');
        }
        this.hint = hint;
    }
}

export default CodeChanges;