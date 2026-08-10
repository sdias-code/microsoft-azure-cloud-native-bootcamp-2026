namespace Api.Models;

public class Photo
{
    public int Id { get; set; }
    public string Titulo { get; set; } = string.Empty;
    public string? Descricao { get; set; }
    public string ImagemUrl { get; set; } = string.Empty;
    public DateTime DataUpload { get; set; }
}

public record PhotoUpdateRequest(string Titulo, string? Descricao);
