class BoggleGame {
    constructor(boardId, sec = 60) {
        this.board = $('#' + boardId);
        this.score = 0;
        this.sec = sec;
        this.timer = setInterval(this.calculateTime.bind(this), 1000);

        $('#guess-form', this.board).on('submit', this.handleSubmit.bind(this));
    }

    displayMessage(message, cls) {
        $('.msg', this.board).text(message).removeClass().addClass(`msg ${cls}`);
    }

    displayScore() {
        $('.score', this.board).text(this.score);
    }

    displayTimer() {
        $('.timer', this.board).text(this.sec);
    }

    async calculateTime() {
        this.sec -= 1;
        this.displayTimer();

        if (this.sec === 0) {
            clearInterval(this.timer);
            $('#guess-form', this.board).hide();
            this.displayMessage('Time is up!', 'ok');
        }
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
                    this.displayMessage(`Found a word: ${word}!`, 'ok');
                    this.score += word.length;
                    this.displayScore();
                    break;
                default:
                    this.displayMessage(`Word ${word} is not on board or is not valid. Try again!`, 'err');
            }
        }
        $word.val('').focus();
    }
}