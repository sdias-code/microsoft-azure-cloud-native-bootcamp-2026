# Query - Criar Tabela Fotos

```sql
IF OBJECT_ID('dbo.Fotos', 'U') IS NOT NULL
    DROP TABLE dbo.Fotos;

CREATE TABLE dbo.Fotos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo NVARCHAR(200) NOT NULL,
    descricao NVARCHAR(MAX) NOT NULL,
    data_upload DATETIME NOT NULL DEFAULT GETDATE(),
    imagem_url NVARCHAR(500) NOT NULL
);
```

## Observações

- `id`: chave primária autoincremental.
- `titulo`: título da foto, obrigatório.
- `descricao`: legenda/texto da foto, obrigatório.
- `data_upload`: data/hora do registro, preenchida automaticamente com `GETDATE()`.
- `imagem_url`: URL do blob no Azure Storage, obrigatória.
