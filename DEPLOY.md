# 🐳 Guia de Deploy com Docker

## Pré-requisitos
- Docker instalado
- Docker Compose instalado (opcional, mas recomendado)

## Método 1: Docker Compose (Recomendado)

### Build e execução
```bash
# Criar o banco de dados de exemplo (se ainda não existir)
python create_sample_db.py

# Build e iniciar o container
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar o container
docker-compose down
```

### Acessar o dashboard
Abra o navegador em: `http://localhost:8501`

## Método 2: Docker CLI

### Build da imagem
```bash
docker build -t bi-dashboard .
```

### Executar o container
```bash
# Criar o banco de dados de exemplo (se ainda não existir)
python create_sample_db.py

# Executar o container
docker run -d \
  --name bi-dashboard \
  -p 8501:8501 \
  -v $(pwd)/sample_database.db:/app/sample_database.db:ro \
  bi-dashboard
```

### Comandos úteis
```bash
# Ver logs
docker logs -f bi-dashboard

# Parar o container
docker stop bi-dashboard

# Remover o container
docker rm bi-dashboard

# Reiniciar
docker restart bi-dashboard
```

## Deploy em Produção

### Render.com (Gratuito)
1. Crie uma conta em [render.com](https://render.com)
2. Conecte seu repositório GitHub
3. Crie um novo "Web Service"
4. Configure:
   - Environment: Docker
   - Build Command: (deixe vazio, usará o Dockerfile)
   - Start Command: (deixe vazio, usará o CMD do Dockerfile)
5. Deploy!

### Fly.io (Gratuito)
```bash
# Instalar fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Lançar a aplicação
fly launch

# Deploy
fly deploy
```

### Railway (Gratuito)
1. Instale o Railway CLI: `npm i -g @railway/cli`
2. Faça login: `railway login`
3. Inicialize: `railway init`
4. Deploy: `railway up`

## Otimizações

### Tamanho da imagem
A imagem usa `python:3.11-slim` para manter o tamanho reduzido (~150MB).

### Cache de camadas
O Dockerfile está otimizado para aproveitar o cache do Docker:
1. Dependências do sistema
2. Requirements Python (muda raramente)
3. Código da aplicação (muda frequentemente)

### Segurança
- Não execute como root em produção
- Use volumes read-only para o banco de dados
- Configure variáveis de ambiente sensíveis via secrets

## Troubleshooting

### Container não inicia
```bash
# Verificar logs
docker logs bi-dashboard

# Verificar se a porta está em uso
lsof -i :8501
```

### Banco de dados não encontrado
Certifique-se de que `sample_database.db` existe antes de iniciar o container:
```bash
python create_sample_db.py
```

### Permissões de arquivo
```bash
# Ajustar permissões do banco de dados
chmod 644 sample_database.db
```

## Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| STREAMLIT_SERVER_PORT | 8501 | Porta do servidor |
| STREAMLIT_SERVER_ADDRESS | 0.0.0.0 | Endereço de bind |
| STREAMLIT_SERVER_HEADLESS | true | Modo headless |
| STREAMLIT_BROWSER_GATHER_USAGE_STATS | false | Desabilita telemetria |

## Recursos

- **CPU**: ~0.5 cores
- **RAM**: ~256-512MB
- **Disco**: ~200MB (imagem + banco de dados)

---

**Desenvolvido para o trabalho de BI da Faculdade** 🎓
