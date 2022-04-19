class BoggleGame {
  constructor(time = 60) {
    this.board = $("#boggle");
    this.score = 0;
    this.words = new Set();
    this.time = time;
    this.showTimer();
    this.timer = setInterval(this.tick.bind(this), 1000);
    $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    $(".new-game", this.board).on("submit", this.handleNewGame.bind(this));
  }


  showWord(word) {
    $(".words", this.board).append($("<li>", { text: word }));
  }


  showScore() {
    $(".score", this.board).text(this.score);
  }


  showMessage(msg, cls) {
    $(".msg", this.board)
      .text(msg)
      .removeClass()
      .addClass(`msg ${cls}`);
  }


  async handleNewGame(evt) {
    location.reload();
  }


  async handleSubmit(evt) {
    evt.preventDefault();
    const $word = $(".word", this.board);

    let word = $word.val();
    if (!word) return;

    if (this.words.has(word)) {
      this.showMessage(`Already found ${word}`, "err");
      return;
    }


    const resp = await axios.get("/check-word", { params: { word: word }});
    if (resp.data.result === "not-word") {
      this.showMessage(`${word} is not a valid English word`, "err");
    } else if (resp.data.result === "not-on-board") {
      this.showMessage(`${word} is not a valid word on this board`, "err");
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
      this.showMessage(`Added: ${word}`, "ok");
    }

    $word.val("").focus();
  }


  showTimer() {
    $(".timer", this.board).text(this.time);
  }


  async tick() {
    this.time -= 1;
    this.showTimer();

    if (this.time === 0) {
      clearInterval(this.timer);
      await this.scoreGame();
    }
  }


  async scoreGame() {
    $(".add-word", this.board).hide();
    $(".new-game", this.board).show();
    const resp = await axios.post("/update-score", { score: this.score });
    if (resp.data.brokeRecord) {
      this.showMessage(`New record: ${this.score}`, "ok");
    } else {
      this.showMessage(`Final score: ${this.score}`, "ok");
    }
  }
}
