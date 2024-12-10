using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Azure;
using Azure.AI.OpenAI;
using OpenAI.Images;

class Program
{
    static async Task Main(string[] args)
    {
        string endpoint = "AZURE_OPENAI_ENDPOINT";
        string apiKey = "AZURE_OPENAI_APIKEY";

        // Create a client to connect to the Azure OpenAI service
       

        AzureOpenAIClient azureClient = new(
        new Uri(endpoint),
        new AzureKeyCredential(apiKey));

        // This must match the custom deployment name you chose for your model
        ImageClient chatClient = azureClient.GetImageClient("dall-e-3");

        string[] treeTypes = { "Natural Pine", "Artificial Pre-Lit", "Post-Modern", "Snow-Covered Artificial", "Vintage Aluminum" };
        Console.WriteLine("Choose the type of Christmas tree:");
        for (int i = 0; i < treeTypes.Length; i++)
        {
            Console.WriteLine($"{i + 1}. {treeTypes[i]}");
        }

        int treeChoice = int.Parse(Console.ReadLine());
        string selectedTreeType = treeTypes[treeChoice - 1];

        string[] additionalDetailsOptions = { "Snow-covered branches", "Gold and silver ornaments", "Multicolored string lights", "Candy cane decorations", "Star topper" };
        List<string> selectedDetails = new List<string>();
        Console.WriteLine("Choose additional details for your tree (enter numbers separated by commas):");
        for (int i = 0; i < additionalDetailsOptions.Length; i++)
        {
            Console.WriteLine($"{i + 1}. {additionalDetailsOptions[i]}");
        }

        string[] detailChoices = Console.ReadLine().Split(',');
        foreach (string choice in detailChoices)
        {
            int detailChoice = int.Parse(choice.Trim());
            selectedDetails.Add(additionalDetailsOptions[detailChoice - 1]);
        }

        string additionalDetails = string.Join(", ", selectedDetails);

        Console.WriteLine("Enter any text you would like to include in the image (e.g., Merry Christmas):");
        string textLayout = Console.ReadLine();

        var imageGeneration = await chatClient.GenerateImageAsync(
            $"a beautiful {selectedTreeType} Christmas tree with colorful decorations and lights, {additionalDetails}. Text: {textLayout}",
        new ImageGenerationOptions()
            {
                Size = GeneratedImageSize.W1024xH1024 // Default size
            }
        );

        Console.WriteLine(imageGeneration.Value.ImageUri);
    }
}
