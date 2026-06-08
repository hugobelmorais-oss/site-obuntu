# Configuração: Produções do Google Drive

## Como funciona

O site lê automaticamente uma pasta do Google Drive e exibe todos os arquivos na seção **Produções**. Toda vez que você adicionar um arquivo na pasta, ele aparecerá no site na próxima visita.

---

## Passo 1 — Criar a pasta no Drive

1. No Google Drive, crie uma pasta chamada **"Produções OBUNTU"** (ou qualquer nome)
2. Clique com o botão direito → **Compartilhar** → mude para **"Qualquer pessoa com o link pode visualizar"**
3. Copie o **ID da pasta** da URL:
   ```
   https://drive.google.com/drive/folders/1ABC123xyz...
                                           ↑ esse é o ID
   ```

---

## Passo 2 — Criar o script no Google Apps Script

1. Acesse [script.google.com](https://script.google.com) com a conta **hugo.belarmino@academico.ufpb.br**
2. Clique em **"Novo projeto"**
3. Apague o código padrão e cole o seguinte:

```javascript
const FOLDER_ID = 'COLE_O_ID_DA_PASTA_AQUI'; // ← substitua

function doGet() {
  const folder = DriveApp.getFolderById(FOLDER_ID);
  const files  = folder.getFiles();
  const result = [];

  while (files.hasNext()) {
    const f = files.next();
    result.push({
      name:        f.getName(),
      url:         f.getUrl(),
      mimeType:    f.getMimeType(),
      createdTime: f.getDateCreated().toISOString(),
      size:        f.getSize()
    });
  }

  // mais recentes primeiro
  result.sort((a, b) => new Date(b.createdTime) - new Date(a.createdTime));

  return ContentService
    .createTextOutput(JSON.stringify({ files: result, updated: new Date() }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

4. Clique em **Salvar** (ícone de disquete) — dê um nome como "OBUNTU Drive API"

---

## Passo 3 — Publicar como aplicativo web

1. No Apps Script: **Implantar → Nova implantação**
2. Clique no ícone ⚙️ ao lado de "Selecionar tipo" → escolha **Aplicativo web**
3. Configure:
   - **Executar como:** Eu (sua conta)
   - **Quem tem acesso:** Qualquer pessoa
4. Clique em **Implantar**
5. Copie a **URL do aplicativo web** (começa com `https://script.google.com/macros/s/...`)

---

## Passo 4 — Colar a URL no site

Abra o arquivo `script.js` e encontre esta linha no topo:

```javascript
const DRIVE_API_URL = ''; // ← cole o URL do Apps Script aqui
```

Cole o URL entre as aspas:

```javascript
const DRIVE_API_URL = 'https://script.google.com/macros/s/SEU_ID_AQUI/exec';
```

Salve, faça commit e push. A seção Produções vai carregar os arquivos automaticamente.

---

## Como adicionar produções depois

Basta **arrastar o arquivo para a pasta no Drive**. Nenhuma alteração no site é necessária.

Para organizar por subcategorias, você pode criar **subpastas** dentro da pasta principal e adaptar o script para retornar `folder: f.getParents().next().getName()`.

---

## Publicação do site (GitHub Pages)

Para ter o site no ar gratuitamente:

1. No GitHub, vá em **Settings → Pages** do repositório `hugobelmorais-oss/claude`
2. Em **Source**, selecione o branch `main` e a pasta `/` (raiz)
3. Clique em **Save**
4. O site ficará disponível em: `https://hugobelmorais-oss.github.io/claude/`

Para um domínio personalizado (ex: `obuntu.ufpb.br`), basta criar um arquivo `CNAME` na raiz com o domínio desejado e configurar o DNS.
