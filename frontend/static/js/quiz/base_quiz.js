;(function(){
  class Quiz {
    constructor(questions, xpPerCorrect = 10, redirectTo = '/') {
      this.questions = questions;
      this.current = 0;
      this.score = 0;
      this.total = questions.length;
      this.xpPerCorrect = xpPerCorrect;
      this.redirectTo = redirectTo;

      // DOM elements
      this.progressText = document.getElementById('progress-text');
      this.progressFill = document.getElementById('progress-fill');
      this.xpDisplay = document.getElementById('xp-display');
      this.questionText = document.getElementById('question-text');
      this.optionsContainer = document.querySelector('.options-container');
      this.feedbackModal = document.getElementById('feedback-modal');
      this.feedbackCard = document.getElementById('feedback-card');
      this.feedbackText = document.getElementById('feedback-text');
      this.continueBtn = document.getElementById('continue-btn');
      this.backBtn = document.getElementById('back-btn');
      
      // End-of-quiz modal elements
      this.endModal = document.getElementById('end-modal');
      this.endText = document.getElementById('end-text');
      this.endContinueBtn = document.getElementById('end-continue-btn');

      // Ensure modals start hidden
      if (this.feedbackModal) this.feedbackModal.classList.add('hidden');
      if (this.endModal) this.endModal.classList.add('hidden');

      this._bindEvents();
      this._renderQuestion();
    }

    _bindEvents() {
      // Continue after feedback
      this.continueBtn.addEventListener('click', () => this._next());

      // End-of-quiz continue
      if (this.endContinueBtn) {
        this.endContinueBtn.addEventListener('click', () => {
          this.endModal.classList.add('hidden');
          window.location.href = this.redirectTo;
        });
      }

      // Back button always returns to puzzle
      if (this.backBtn) {
        this.backBtn.addEventListener('click', () => {
          // Hide any open modals
          if (this.feedbackModal) this.feedbackModal.classList.add('hidden');
          if (this.endModal) this.endModal.classList.add('hidden');
          window.location.href = '/menu/puzzle';
        });
      }
    }

    _renderQuestion() {
      // Update progress and XP
      this.progressText.textContent = `${this.current} de ${this.total}`;
      this.progressFill.style.width = `${(this.current / this.total) * 100}%`;
      this.xpDisplay.textContent = `${this.score}XP`;

      // Load question
      const q = this.questions[this.current];
      this.questionText.textContent = q.pergunta;

      // Generate options
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
      // Disable all options
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

      // Show feedback modal
      this.feedbackModal.classList.remove('hidden');
    }

    _next() {
      // Hide feedback modal
      this.feedbackModal.classList.add('hidden');
      this.current++;
      if (this.current < this.total) {
        this._renderQuestion();
      } else {
        // Show end-of-quiz pop-up
        this.endText.textContent = `🎉 Quiz concluído! Você ganhou ${this.score} XP.`;
        this.endModal.classList.remove('hidden');
      }
    }
  }

  /**
   * Initialize a quiz.
   * @param {Array} questions — list of {pergunta, opcoes, correta}
   * @param {Object} options — xpPerCorrect, redirectTo
   */
  window.startQuiz = function(questions, { xpPerCorrect = 10, redirectTo = '/menu/puzzle' } = {}) {
    document.addEventListener('DOMContentLoaded', () => {
      new Quiz(questions, xpPerCorrect, redirectTo);
    });
  };
})();
