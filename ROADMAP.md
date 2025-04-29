# ROADMAP

Este documento lista as melhorias planejadas para o projeto **Égua do Guia**, organizadas em categorias e prioridades.

---

## 🚀 Funcionalidades de Cadastro/Login

- **Campo “Confirmar Senha”**
  - Adicionar input para confirmação de senha no front-end e validação no back-end.
- **Validação de formato de e-mail reforçada**
  - Regex mais robusto e feedback inline para e-mails mal formatados.
---

## 🔒 Segurança e Autenticação

- **Proteção CSRF com Flask-WTF**
  - Incluir tokens CSRF em todos os formulários POST.
- **Confirmação de conta por e-mail**
  - Gerar token, enviar link de ativação e bloquear login até confirmação.
- **Rate-limiting de login**
  - Implementar limite de tentativas (flask-limiter).
- **Cookies mais seguros**
  - Configurar `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE` e `SESSION_COOKIE_SAMESITE`.

---

## 🛠 Infraestrutura e Deploy

- **Migrations com Alembic/Flask-Migrate**
  - Versionar alterações de schema em vez de scripts manuais.
- **Docker + docker-compose**
  - Containerizar app e banco para desenvolvimento e produção.

---

## 🧪 Testes e Qualidade

- **Testes end-to-end (Cypress/Selenium)**
  - Automatizar fluxo de cadastro e login via browser.
- **Cobertura de testes unitários**
  - Completar cenários faltantes em `tests/`, incluindo validações de e-mail e senha.
- **Análise de qualidade (CI)**
  - Configurar linters (flake8, eslint) e GitHub Actions para integração contínua.

---

## 🖥 Front-end e UX

### Telas e Componentes

- **Tela de Cadastro**
  - Estender `base.html` para herdar layout e bloco de flashes.
  - Erros inline claros e toasts automáticos.
  - Validação on-the-fly: e-mail, senha, confirmar senha, >=14 anos.
- **Tela de Login**
  - Mesmos padrões de validação e mensagens.
  - Spinner ou indicador de loading ao submeter.
  - Opção “mostrar/ocultar senha”.
- **Componentização**
  - Criar componentes reutilizáveis: Input, Button, Select.
  - Padronizar via CSS variables ou framework (Tailwind).

### Interações e Feedback

- **Animações suaves**
  - Transição de telas com fade.
  - Feedback de clique com classe `btn--pressed`.
- **Skeleton/Placeholder**
  - Mostrar carregamento ao aguardar resposta.
- **Toasts & Flashes**
  - Container fixo e desaparecimento automático.
  - Uso de ARIA-live para acessibilidade.

### Acessibilidade (A11Y)

- **Labels e ARIA**
  - Inputs com `<label>` e atributos `aria-invalid`, `aria-describedby`.
- **Navegação por teclado**
  - Tabindex lógico e estilo de foco visível.
- **Contraste de cores**
  - Garantir mínimo de 4.5:1 para texto.

### Responsividade e Mobile

- **Layout fluído**
  - Flex/Grid adaptativos para mobile.
- **Botões Touch-friendly**
  - Tamanho e espaçamento adequados.
- **Dark Mode (opcional)**
  - Suporte a `prefers-color-scheme`.

---
