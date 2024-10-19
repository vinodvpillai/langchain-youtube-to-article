# YouTube to Article Converter

This is a Python program that takes a YouTube video URL and generates a well-structured article based on the video's transcript or audio. The process involves fetching the transcript if available or downloading and converting the audio to text using Whisper, followed by summarizing the text into an article using OpenAI's GPT model via LangChain.

## Features

- **Transcript Extraction**: If available, the YouTube video transcript is fetched via the YouTube Data API.
- **Audio to Text Conversion**: If the transcript is not available, the program downloads the video's audio and converts it to text using the Whisper ASR model.
- **Article Generation**: The generated text (from either the transcript or audio) is formatted into an article using OpenAI's GPT model.
- **File Output**: The generated article is saved as a text file specified by the user.

## Requirements

To run this program, you need to install the following Python libraries:

### Core Libraries:
- **LangChain**: Used for chain management and interacting with OpenAI models.
- **OpenAI**: Used to interact with OpenAI's GPT-3.5 Turbo model.
- **YouTube Transcript API**: Fetches transcripts from YouTube videos.
- **Whisper**: Converts audio to text if no transcript is available.
- **pytube**: Downloads audio from YouTube videos.

### Installation

Use the following command to install all the required libraries:

```
pip install langchain openai youtube-transcript-api whisper pytube regex
```

Additionally, **Whisper** relies on `ffmpeg` for audio processing. You need to install `ffmpeg`:

- On Ubuntu:
  ```
  sudo apt update && sudo apt install ffmpeg
  ```

- On macOS using Homebrew:
  ```
  brew install ffmpeg
  ```

## How to Run the Program

1. Clone or download the repository to your local machine.
2. Ensure all dependencies are installed as mentioned above.
3. Run the program using Python:

   ```
   python main.py
   ```

4. When prompted, enter a valid YouTube video URL.
5. The program will attempt to fetch the transcript or convert the audio to text, summarize the content, and generate an article.
6. You will be prompted to provide a file name where the generated article will be saved.
7. The article will be saved in the specified file.

### Example

```
$ python main.py
Please enter the YouTube video URL: https://www.youtube.com/watch?v=exampleID
Please enter the name of the file to save the article (e.g., article.txt): my_article.txt

The article has been saved to my_article.txt.
```

## Project Structure

```
.
├── main.py  # Main program file
├── README.md              # Project documentation (this file)
```

## Customization

### Change the OpenAI Model
If you want to change the model or fine-tune the GPT prompt, you can modify the `summarize_to_article` function inside the `main.py` file. You can also adjust the temperature or use another model from OpenAI.

```python
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5)
```

### Modify the Output
The generated article is saved to a text file. You can change the file format or output method as needed, such as saving to a PDF or directly displaying the output in a web interface.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

