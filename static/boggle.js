class BoggleGame {
    constructor(boardId) {
        this.board = $('#' + boardId);
        this.score = 0;
        $('#guess-form', this.board).on('submit', this.handleSubmit.bind(this));
    }

    displayGuessResult(message, cls) {
        $('.msg', this.board).text(message).removeClass().addClass(`msg ${cls}`);
    }

    displayScore() {
        $('.score', this.board).text(this.score);
    }

    async handleSubmit(evt) {
        evt.preventDefault();

        const $word = $('.word', this.board);
        let word = $word.val();
        const resp = await axios.get('/check-word', {
            params: { word: word }
        });
        let result = resp.data.result;
        if (result) {
            switch (result) {
                case 'ok':
                    this.displayGuessResult(`Found a word: ${word}!`, 'ok');
                    this.score += word.length;
                    this.displayScore();
                    break;
                default:
                    this.displayGuessResult(`Word ${word} is not on board or is not valid. Try again!`, 'err');
            }
        }
    }
}