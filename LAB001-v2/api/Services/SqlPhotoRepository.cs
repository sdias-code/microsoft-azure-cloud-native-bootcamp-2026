using Microsoft.Data.SqlClient;
using Api.Models;

namespace Api.Services;

public class SqlPhotoRepository
{
    private readonly string _connectionString;

    public SqlPhotoRepository(IConfiguration config)
    {
        var connectionStringBuilder = new SqlConnectionStringBuilder
        {
            DataSource = config["AZURE_SQL_SERVER"],
            InitialCatalog = config["AZURE_SQL_DATABASE"],
            UserID = config["AZURE_SQL_USERNAME"],
            Password = config["AZURE_SQL_PASSWORD"],
            ConnectTimeout = 30,
            TrustServerCertificate = true,
            Encrypt = true,
        };
        _connectionString = connectionStringBuilder.ConnectionString;
    }

    public async Task<List<Photo>> ListAsync()
    {
        var photos = new List<Photo>();
        await using var conn = new SqlConnection(_connectionString);
        await conn.OpenAsync();

        const string query = """
            SELECT id, titulo, descricao, data_upload, imagem_url
            FROM dbo.Fotos
            ORDER BY data_upload DESC
            """;

        await using var cmd = new SqlCommand(query, conn);
        await using var reader = await cmd.ExecuteReaderAsync();
        while (await reader.ReadAsync())
        {
            photos.Add(new Photo
            {
                Id = reader.GetInt32(0),
                Titulo = reader.GetString(1),
                Descricao = reader.IsDBNull(2) ? null : reader.GetString(2),
                DataUpload = reader.GetDateTime(3),
                ImagemUrl = reader.GetString(4),
            });
        }
        return photos;
    }

    public async Task<Photo?> GetByIdAsync(int id)
    {
        await using var conn = new SqlConnection(_connectionString);
        await conn.OpenAsync();

        const string query = """
            SELECT id, titulo, descricao, data_upload, imagem_url
            FROM dbo.Fotos
            WHERE id = @Id
            """;

        await using var cmd = new SqlCommand(query, conn);
        cmd.Parameters.AddWithValue("@Id", id);

        await using var reader = await cmd.ExecuteReaderAsync();
        if (!await reader.ReadAsync())
            return null;

        return new Photo
        {
            Id = reader.GetInt32(0),
            Titulo = reader.GetString(1),
            Descricao = reader.IsDBNull(2) ? null : reader.GetString(2),
            DataUpload = reader.GetDateTime(3),
            ImagemUrl = reader.GetString(4),
        };
    }

    public async Task<Photo> CreateAsync(string titulo, string? descricao, string imagemUrl)
    {
        await using var conn = new SqlConnection(_connectionString);
        await conn.OpenAsync();

        const string query = """
            INSERT INTO dbo.Fotos (titulo, descricao, imagem_url)
            OUTPUT INSERTED.id, INSERTED.data_upload
            VALUES (@Titulo, @Descricao, @ImagemUrl)
            """;

        await using var cmd = new SqlCommand(query, conn);
        cmd.Parameters.AddWithValue("@Titulo", titulo);
        cmd.Parameters.AddWithValue("@Descricao", (object?)descricao ?? DBNull.Value);
        cmd.Parameters.AddWithValue("@ImagemUrl", imagemUrl);

        await using var reader = await cmd.ExecuteReaderAsync();
        await reader.ReadAsync();

        return new Photo
        {
            Id = reader.GetInt32(0),
            Titulo = titulo,
            Descricao = descricao,
            ImagemUrl = imagemUrl,
            DataUpload = reader.GetDateTime(1),
        };
    }

    public async Task<bool> UpdateAsync(int id, string titulo, string? descricao)
    {
        await using var conn = new SqlConnection(_connectionString);
        await conn.OpenAsync();

        const string query = """
            UPDATE dbo.Fotos
            SET titulo = @Titulo, descricao = @Descricao
            WHERE id = @Id
            """;

        await using var cmd = new SqlCommand(query, conn);
        cmd.Parameters.AddWithValue("@Titulo", titulo);
        cmd.Parameters.AddWithValue("@Descricao", (object?)descricao ?? DBNull.Value);
        cmd.Parameters.AddWithValue("@Id", id);

        return await cmd.ExecuteNonQueryAsync() > 0;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        await using var conn = new SqlConnection(_connectionString);
        await conn.OpenAsync();

        const string query = "DELETE FROM dbo.Fotos WHERE id = @Id";
        await using var cmd = new SqlCommand(query, conn);
        cmd.Parameters.AddWithValue("@Id", id);

        return await cmd.ExecuteNonQueryAsync() > 0;
    }
}
