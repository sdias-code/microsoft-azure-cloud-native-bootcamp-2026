using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;

namespace Api.Services;

public class BlobStorageService
{
    private readonly string _accountUrl;
    private readonly string _containerName;
    private readonly BlobServiceClient _blobServiceClient;

    public BlobStorageService(IConfiguration config)
    {
        var accountName = config["AZURE_ACCOUNT_NAME"] ?? throw new InvalidOperationException("AZURE_ACCOUNT_NAME não configurado.");
        _containerName = config["AZURE_CONTAINER_NAME"] ?? "fotos";
        _accountUrl = $"https://{accountName}.blob.core.windows.net";
        _blobServiceClient = new BlobServiceClient(new Uri(_accountUrl), new DefaultAzureCredential());
    }

    public async Task<string> UploadAsync(Stream stream, string fileName, string? contentType)
    {
        var container = _blobServiceClient.GetBlobContainerClient(_containerName);
        await container.CreateIfNotExistsAsync(PublicAccessType.None);

        var extension = Path.GetExtension(fileName);
        if (string.IsNullOrWhiteSpace(extension))
            extension = ".jpg";

        var blobName = $"{Guid.NewGuid():N}{extension}";
        var blob = container.GetBlobClient(blobName);

        var headers = new BlobHttpHeaders
        {
            ContentType = contentType ?? "application/octet-stream",
        };
        await blob.UploadAsync(stream, headers);

        return $"{_accountUrl}/{_containerName}/{blobName}";
    }

    public async Task DeleteIfExistsAsync(string imageUrl)
    {
        if (!Uri.TryCreate(imageUrl, UriKind.Absolute, out var uri))
            return;

        var container = _blobServiceClient.GetBlobContainerClient(_containerName);
        var blob = container.GetBlobClient(uri.Segments[^1]);
        await blob.DeleteIfExistsAsync();
    }
}
