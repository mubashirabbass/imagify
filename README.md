```markdown
# Imagify - Image Downloader

![Imagify Logo](https://via.placeholder.com/150)  <!-- Replace with actual logo if available -->

Imagify is a user-friendly desktop application built with Python and CustomTkinter that allows you to download high-quality images from Bing's image search API with ease.

## Features

- 🖼️ Download multiple images simultaneously with multi-threading
- 🔍 Search for any type of images using keywords
- 📂 Choose custom save location
- 🎚️ Select number of images to download (1-1000)
- 📊 Real-time progress tracking with progress bar
- 👀 Image preview during download
- 🌓 Light/Dark mode support
- 🚀 Fast and efficient downloads

## Requirements

- Python 3.7+
- Required Python packages (install via `pip install -r requirements.txt`):
  ```
  customtkinter
  Pillow
  requests
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mubashirabbass/imagify.git
   cd imagify
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Get a Bing Image Search API key from [Microsoft Azure](https://azure.microsoft.com/en-us/services/cognitive-services/bing-image-search-api/)

4. Replace `"Your api key "` in `imagify.py` with your actual Bing API key

5. Run the application:
   ```bash
   python imagify.py
   ```

## Usage

1. Enter your search term (e.g., "nature", "animals", "technology")
2. Specify the number of images to download (1-1000)
3. Choose a save location
4. Click "Download Images"
5. View progress and image previews as downloads complete

## Screenshots

![Main Window](https://via.placeholder.com/600x400)  <!-- Replace with actual screenshot -->
![Download Progress](https://via.placeholder.com/600x400)  <!-- Replace with actual screenshot -->

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Developed by Mubashir Abbas

---

**Note:** This application uses the Bing Image Search API which may have usage limits. Please check Microsoft's terms of service for API usage.
```
