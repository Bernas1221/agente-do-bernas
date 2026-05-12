# OpenClaw Agent

## Visão geral
Este repositório contém um agente de IA escrito em Python que roda 24/7 no Moltbook. Ele pode:
- Conversar com outras IAs no Moltbook.
- Detectar oportunidades de criptomoedas em mensagens.
- Proteger contra **prompt injection** usando um escudo simples.
- (Opcional) gerar respostas inteligentes via **Claude API**.
- Ser implantado gratuitamente na **Render.com** com configuração automática.

## Estrutura do projeto
```
openclaw_agent_advanced.py   # Código principal do agente
prompt_injection_shield.py    # Função de proteção contra prompt injection
requirements.txt              # Dependências Python
render.yaml                    # Configuração do serviço Render.com
.env.example                   # Template de variáveis de ambiente (copiar para .env)
README.md                      # Esta documentação
```

## Como começar
1. **Clone o repositório**
   ```bash
   git clone <repo-url>
   cd <repo-dir>
   ```
2. **Criar o arquivo de ambiente**
   ```bash
   cp .env.example .env
   ```
   Preencha `MOLTBOOK_API_TOKEN` (obrigatório) e `CLAUDE_API_KEY` (opcional).
3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```
4. **Rodar localmente** (para teste)
   ```bash
   python openclaw_agent_advanced.py
   ```
   O agente ficará em loop aguardando mensagens do Moltbook.

## Deploy na Render.com (gratuito)
1. Crie uma conta em <https://render.com> (plano gratuito).
2. No dashboard, clique em **New** → **Web Service**.
3. Selecione o repositório que contém este código.
4. Render detectará o `render.yaml` e usará as instruções:
   - `pip install -r requirements.txt`
   - `python openclaw_agent_advanced.py`
5. Defina as variáveis de ambiente (`MOLTBOOK_API_TOKEN`, `CLAUDE_API_KEY`, `AGENT_NAME`).
6. Salve – o serviço será implantado e mantido ativo 24/7 (com pings diários).

## Scripts de deploy automatizado
Para CI/CD ou re‑deploy manual, você pode usar o comando abaixo (já incluso no `render.yaml` através de `autoDeploy`).
```bash
# Re‑deploy manual no Render via CLI (necessita do Render CLI instalado)
render services restart openclaw-agent
```

## Segurança – Prompt‑Injection Shield
A função `sanitize_prompt` em `prompt_injection_shield.py` remove padrões de código e rejeita mensagens suspeitas. Ela é usada antes de gerar qualquer resposta, garantindo que o agente não execute código arbitrário.

## Integração opcional com Claude API
Se `CLAUDE_API_KEY` estiver definido, o agente usará o SDK `anthropic` para gerar respostas contextuais. Caso contrário, ele responde com um eco simples.

## Licença
Este projeto está disponível sob a licença MIT. Sinta‑se livre para adaptar e melhorar.
