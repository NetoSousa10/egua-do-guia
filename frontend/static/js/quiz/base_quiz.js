;(function(){
  class Quiz {
    constructor(questions, xpPerCorrect = 10, redirectTo = '/') {
      this.questions   = questions;
      this.current     = 0;
      this.score       = 0;
      this.total       = questions.length;
      this.xpPerCorrect = xpPerCorrect;
      this.redirectTo  = redirectTo;

      // DOM elements
      this.progressText   = document.getElementById('progress-text');
      this.progressFill   = document.getElementById('progress-fill');
      this.xpDisplay      = document.getElementById('xp-display');
      this.questionText   = document.getElementById('question-text');
      this.optionsContainer = document.querySelector('.options-container');
      this.feedbackModal  = document.getElementById('feedback-modal');
      this.feedbackCard   = document.getElementById('feedback-card');
      this.feedbackText   = document.getElementById('feedback-text');
      this.continueBtn    = document.getElementById('continue-btn');
      this.backBtn        = document.getElementById('back-btn');
      this.endModal       = document.getElementById('end-modal');
      this.endText        = document.getElementById('end-text');
      this.endContinueBtn = document.getElementById('end-continue-btn');

      // Esconde modais no início
      if (this.feedbackModal) this.feedbackModal.classList.add('hidden');
      if (this.endModal) this.endModal.classList.add('hidden');

      this._bindEvents();
      this._renderQuestion();
    }

    _bindEvents() {
      this.continueBtn.addEventListener('click', () => this._next());

      if (this.endContinueBtn) {
        this.endContinueBtn.addEventListener('click', () => {
          this.endModal.classList.add('hidden');
          window.location.href = this.redirectTo;
        });
      }

      if (this.backBtn) {
        this.backBtn.addEventListener('click', () => {
          if (this.feedbackModal) this.feedbackModal.classList.add('hidden');
          if (this.endModal) this.endModal.classList.add('hidden');
          window.location.href = '/menu/puzzle';
        });
      }
    }

    _renderQuestion() {
      this.progressText.textContent = `${this.current} de ${this.total}`;
      this.progressFill.style.width = `${(this.current / this.total) * 100}%`;
      this.xpDisplay.textContent = `${this.score}XP`;

      const q = this.questions[this.current];
      this.questionText.textContent = q.pergunta;
      this.optionsContainer.innerHTML = '';
      q.opcoes.forEach((texto, idx) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = texto;
        btn.disabled = false;
        btn.addEventListener('click', () => this._checkAnswer(idx));
        this.optionsContainer.appendChild(btn);
      });
    }

    _checkAnswer(choice) {
      Array.from(this.optionsContainer.children).forEach(b => b.disabled = true);
      const q = this.questions[this.current];
      const isCorrect = choice === q.correta;

      if (isCorrect) {
        this.score += this.xpPerCorrect;
        this.feedbackCard.className = 'feedback-card correct';
        this.feedbackText.textContent = '✅ Correta!';
      } else {
        this.feedbackCard.className = 'feedback-card incorrect';
        this.feedbackText.innerHTML = `❌ Incorreta!<br>Resposta correta: ${q.opcoes[q.correta]}`;
      }

      this.feedbackModal.classList.remove('hidden');
    }

    _next() {
      this.feedbackModal.classList.add('hidden');
      this.current++;

      if (this.current < this.total) {
        this._renderQuestion();
      } else {
        // Envia XP ao servidor antes de mostrar o modal final
        fetch('/api/user_stats/xp', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ xp: this.score })
        })
        .then(res => res.json())
        .then(data => {
          console.log('XP atualizado:', data);
          this._showEndModal();
        })
        .catch(err => {
          console.error('Erro ao atualizar XP:', err);
          this._showEndModal();
        });
      }
    }

    _showEndModal() {
      this.endText.textContent = `🎉 Quiz concluído! Você ganhou ${this.score} XP.`;
      this.endModal.classList.remove('hidden');
    }
  }

  window.startQuiz = function(questions, { xpPerCorrect = 10, redirectTo = '/menu/puzzle' } = {}) {
    document.addEventListener('DOMContentLoaded', () => {
      new Quiz(questions, xpPerCorrect, redirectTo);
    });
  };
})();
