class Tap {
    constructor (words) {
        this.words = words;

        // 既にタイプされたwordのnameを表示するタグ要素
        this.typingWordChar = document.getElementById('name');
        // タイプしているwordのdescriptionを表示するタグ要素
        this.typingWordDescription = document.getElementById('description');
        // タップするword
        this.tapWord = [];

        this.tapCount = 0;

        this.gameOver = false;
    };

    // ゲーム開始
    startGame() {
        this.createText();
    };

    // ゲーム終了
    endGame() {
        this.displayScore();
    };

    displayScore() {
        // タイプ画面のメインタグ
        var typing = document.getElementById('typing');
        while(typing.firstChild) {
            typing.removeChild(typing.firstChild);
        }
        
        // タイトル表示
        var scoreTitle = document.createElement('h1');
        scoreTitle.classList.add('score-title');
        scoreTitle.textContent = '終了';
        typing.appendChild(scoreTitle);
    };

    // タイピング文字の作成
    createText(){
        this.typingWordChar.textContent = '';
        this.typingWordDescription.textContent = this.words[0].description;
        var span = this.generateSpanElement(words[0].name)
        this.typingWordChar.appendChild(span);
        this.tapWord.push(span);
    };

    // spanタグを作成
    generateSpanElement(word) {
        var span = document.createElement('span');
        span.textContent = word;
        // span.style.color = '#fff';
        // span.style.visibility = 'hidden';
        return span
    };

    // 次の単語を確認
    tapCard() {
        if (this.tapCount == 0) {
            this.tapWord[0].style.visibility = 'visible';
            this.tapWord[0].className = "add-red";
            this.tapWord.shift();
        }
        this.tapCount ++;
        
        if (this.tapCount == 2) {
            this.words.shift();
            this.tapCount = 0;
            if(!this.words.length) {
                this.gameOver = true
            } else {
                setTimeout(() =>{
                    this.createText();
                }, 300)
            }
        };
    };
}



