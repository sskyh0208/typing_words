class Game {
    constructor (words, wordbook) {
        this.words = words;
        this.wordbook = wordbook;

        // 既にタイプされたwordのnameを表示するタグ要素
        this.typingWordChar = document.getElementById('name');
        // タイプしているwordのdescriptionを表示するタグ要素
        this.typingWordDescription = document.getElementById('description');
        // タイプに成功した回数を表示するタグ要素
        this.successCount = document.getElementById('success');
        // タイプに失敗した回数を表示するタグ要素
        this.failedCount = document.getElementById('failed');
        // タイプ中のwordの文字列を格納する
        this.checkWords = [];

        this.totalSuccessCount = 0;
        this.totalFailedCount = 0;

        this.gameOver = false;
        this.successCount.textContent = this.totalSuccessCount;
        this.failedCount.textContent = this.totalFailedCount;

        this.typingWordId = '';

        this.wordScores = [];
        this.typingWordScoreDict = {};
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

        // ボタン表示
        var scoreBtn = document.createElement('div');
        scoreBtn.classList.add('score-btn');
        typing.appendChild(scoreBtn);

        // 戻るボタン
        var backBtn = document.createElement('a');
        backBtn.classList.add('red-link');
        backBtn.id = "back";
        backBtn.href = document.referrer;
        scoreBtn.appendChild(backBtn);
        var backIcon = document.createElement('i');
        backIcon.classList.add('fas');
        backIcon.classList.add('fa-arrow-left');
        backBtn.appendChild(backIcon);
        
        // タイトル表示
        var scoreTitle = document.createElement('h1');
        scoreTitle.classList.add('score-title');
        scoreTitle.textContent = 'スコア';
        typing.appendChild(scoreTitle);
        
        if (this.totalFailedCount > 0) {
            // ミスがある場合はスコア表示
            // テーブル作成
            var scoreTable = document.createElement('div');
            scoreTable.classList.add('score-table');
            typing.appendChild(scoreTable);
    
            // テーブルヘッダー作成
            var scoreTableHeader = this.createScoreTableHeader();
            scoreTable.appendChild(scoreTableHeader);
            
            // スコアをミス回数の降順に並べ替え
            this.scoreSortDesc();
    
            // 10個のみ表示
            if (this.wordScores.length > 10) {
                this.wordScores = this.wordScores.slice(0, 10);
            }
            
            // テーブル行作成
            for (const score of this.wordScores) {
                var scoreTableRow = this.createScoreTableRow(score);
                scoreTable.appendChild(scoreTableRow);
            }
        } else {
            var perfect = document.createElement('h1');
            perfect.classList.add('score-perfect');
            perfect.textContent = 'パーフェクト!';
            typing.appendChild(perfect);
        }
    };

    // スコアテーブルのヘッダー行を作成する
    createScoreTableHeader() {
        // テーブルヘッダー
        var dlHead = document.createElement('dl');
        dlHead.classList.add('score-table-head');

        // 単語列
        var dt = document.createElement('dt');
        dlHead.appendChild(dt);
        var spanName = document.createElement('span');
        spanName.textContent = '単語';
        dt.appendChild(spanName);
        
        // 意味列
        var dd1 = document.createElement('dd');
        dlHead.appendChild(dd1);
        var spanDescription = document.createElement('span');
        spanDescription.textContent = '意味';
        dd1.appendChild(spanDescription);

        // ミス回数
        var dd2 = document.createElement('dd');
        dlHead.appendChild(dd2);
        var spanMiss = document.createElement('span');
        spanMiss.textContent = 'ミス';
        dd2.appendChild(spanMiss);

        return dlHead;
    };

    // スコアテーブルのスコア行を作成する
    createScoreTableRow(score) {
        // テーブルロウ
        var dlRow = document.createElement('dl');
        dlRow.classList.add('score-table-row');

        // 単語列
        var dt = document.createElement('dt');
        dlRow.appendChild(dt);
        var spanName = document.createElement('span');
        spanName.textContent = score.name;
        dt.appendChild(spanName);
        
        // 意味列
        var dd1 = document.createElement('dd');
        dlRow.appendChild(dd1);
        var spanDescription = document.createElement('span');
        spanDescription.textContent = score.description;
        dd1.appendChild(spanDescription);

        // ミス回数
        var dd2 = document.createElement('dd');
        dlRow.appendChild(dd2);
        var spanMiss = document.createElement('span');
        spanMiss.textContent = score.count;
        dd2.appendChild(spanMiss);

        return dlRow;
    };

    // タイピングスコアの降順ソート
    scoreSortDesc() {
        this.wordScores.sort(function(a, b) {
            if(a.count < b.count) return 1;
            if(a.count > b.count) return -1;
            return 0;
        });
    };

    // タイピング文字の作成
    createText(){
        this.typingWordChar.textContent = '';
        this.typingWordDescription.textContent = this.words[0].description;
        this.typingWordScoreDict = {};
        this.typingWordScoreDict.id = this.words[0].id;
        this.typingWordScoreDict.name = this.words[0].name;
        this.typingWordScoreDict.description = this.words[0].description;
        this.typingWordScoreDict.count = 0;
        // wordのnameを１文字ずつspan要素にする。
        var wordChars = this.words[0].name.split('');
        for (const char of wordChars) {
            var span = this.generateSpanElement(char);
            this.typingWordChar.appendChild(span);
            // 空文字でなければタイプチェック用の配列にcharを入れる
            if(char != ' ') {
                this.checkWords.push(span);
            };
        };
    };

    // spanタグを作成
    generateSpanElement(char) {
        var span = document.createElement('span');
        span.textContent = char;
        span.style.visibility = 'hidden';
        return span
    };

    // タイプされたキーを判定
    checkTypedKey(event) {
        if(event.key === this.checkWords[0].textContent) {
            this.typedSuccess();
        } else if(event.key !== this.checkWords[0].textContent && event.code.startsWith('Key')) {
            this.typedMiss();
        };
    };

    // 次の単語を確認
    nextWordCheck() {
        this.words.shift();
        // wordの残り数判定
        if(!this.words.length) {
            this.gameOver = true
        } else {
            // すぐ切り替えると最後のタイプ文字が確認できないため
            setTimeout(() =>{
                this.createText();
            }, 300)
        };
    };

    // タイプ成功時に文字を赤く変える
    changeCheckWordsFont(){
        this.checkWords[0].style.visibility = 'visible';
        this.checkWords[0].className = "add-red";
    };

    // タイプ成功
    typedSuccess() {
        this.changeCheckWordsFont();
        this.checkWords.shift();
        this.successCount.textContent ++;
        if(!this.checkWords.length) {
            this.addSuccessCount();
            this.nextWordCheck()
        };
    };

    // タイプ失敗
    typedMiss() {
        this.addFailedCount();
    }

    // 1単語タイプ完了時
    addSuccessCount() {
        this.totalSuccessCount ++;
        // this.successCount.textContent = this.totalSuccessCount;
        if (this.typingWordScoreDict.count > 0) {
            this.wordScores.push(this.typingWordScoreDict);
        }
    }

    // タイプ失敗時
    addFailedCount() {
        this.totalFailedCount ++;
        this.failedCount.textContent = this.totalFailedCount;
        this.typingWordScoreDict.count ++;
    }
}



