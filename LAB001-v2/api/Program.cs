using DotNetEnv;
using Api.Models;
using Api.Services;

const long MaxFileBytes = 1 * 1024 * 1024;

var cwd = Directory.GetCurrentDirectory();
var envPath = new[]
    {
        Path.Combine(cwd, ".env"),
        Path.Combine(cwd, "api", ".env"),
    }
    .FirstOrDefault(File.Exists);

if (envPath is not null)
    Env.Load(envPath, LoadOptions.NoClobber());

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors(o =>
{
    o.AddPolicy("Front", p => p
        .WithOrigins(
            "http://localhost:5173",
            "http://127.0.0.1:5173")
        .AllowAnyHeader()
        .AllowAnyMethod());
});

builder.Services.AddSingleton<BlobStorageService>();
builder.Services.AddSingleton<SqlPhotoRepository>();

var app = builder.Build();

app.UseCors("Front");

var photos = app.MapGroup("/api/photos");

photos.MapGet("/", async (SqlPhotoRepository repo) =>
    Results.Ok(await repo.ListAsync()));

photos.MapGet("/{id:int}", async (int id, SqlPhotoRepository repo) =>
{
    var photo = await repo.GetByIdAsync(id);
    return photo is null ? Results.NotFound() : Results.Ok(photo);
});

photos.MapPost("/", async (HttpRequest request, BlobStorageService storage, SqlPhotoRepository repo) =>
{
    if (!request.HasFormContentType)
        return Results.BadRequest(new { error = "Envie os dados como multipart/form-data." });

    var form = await request.ReadFormAsync();
    var titulo = form["titulo"].ToString();
    var descricao = form["descricao"].ToString();
    var file = form.Files.GetFile("imagem");

    if (string.IsNullOrWhiteSpace(titulo) || file is null)
        return Results.BadRequest(new { error = "O título e a imagem são obrigatórios." });

    if (file.Length > MaxFileBytes)
        return Results.BadRequest(new
        {
            error = $"Arquivo excede o limite de {MaxFileBytes / (1024 * 1024)} MB. Escolha uma imagem menor."
        });

    var imageUrl = await storage.UploadAsync(file.OpenReadStream(), file.FileName, file.ContentType);
    var photo = await repo.CreateAsync(titulo.Trim(), descricao, imageUrl);

    return Results.Created($"/api/photos/{photo.Id}", photo);
});

photos.MapPut("/{id:int}", async (int id, PhotoUpdateRequest req, SqlPhotoRepository repo) =>
{
    if (string.IsNullOrWhiteSpace(req.Titulo))
        return Results.BadRequest(new { error = "O título não pode ficar vazio." });

    var updated = await repo.UpdateAsync(id, req.Titulo.Trim(), req.Descricao);
    return updated ? Results.NoContent() : Results.NotFound();
});

photos.MapDelete("/{id:int}", async (int id, SqlPhotoRepository repo, BlobStorageService storage) =>
{
    var photo = await repo.GetByIdAsync(id);
    if (photo is null)
        return Results.NotFound();

    await repo.DeleteAsync(id);
    await storage.DeleteIfExistsAsync(photo.ImagemUrl);
    return Results.NoContent();
});

app.Run();
