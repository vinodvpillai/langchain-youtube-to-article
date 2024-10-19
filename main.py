from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
#from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import whisper
from pytube import YouTube
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Loading the environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Step 1: Function to Fetch Transcript from YouTube
def fetch_transcript(video_url):
    try:
        video_id = extract_video_id_from_url(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t['text'] for t in transcript])
        return text
    except Exception as e:
        print(f"Transcript not available: {str(e)}")
        return None

# Step 2: Convert Audio to Text using Whisper (if transcript not available)
def convert_audio_to_text(video_url):
    # Download audio from YouTube video
    audio_file = download_youtube_audio(video_url)
    
    # Use Whisper ASR model to convert audio to text
    model = whisper.load_model("base")
    result = model.transcribe(audio_file) # type: ignore
    return result['text']

# Step 3: Summarize Text into Article Format
def summarize_to_article(text):
    # llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5)
    llm = ChatOpenAI(temperature=0, model=os.environ.get('OPENAI_MODEL'), api_key=os.environ.get('OPENAI_API_KEY'), base_url=os.environ.get('OPENAI_API_HOST'))  # type: ignore
    prompt_template = """
    Convert the following transcript into a well-structured article:
    
    Transcript:
    {transcript}
    
    Article:
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["transcript"])
    
    # Parser
    parser = StrOutputParser()
    chain = prompt|llm|parser
    
    article = chain.invoke(input={'transcript':text})
    return article

# Full pipeline
def youtube_to_article(video_url):
    # Step 1: Try fetching the transcript
    transcript = fetch_transcript(video_url)
    
    if not transcript:
        # Step 2: Convert audio to text if transcript isn't available
        transcript = convert_audio_to_text(video_url)
    
    # Step 3: Summarize the transcript into an article
    article = summarize_to_article(transcript)
    
    return article

# Helper function to extract YouTube video ID from URL
def extract_video_id_from_url(url):
    import re
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.match(regex, url)
    return match.group(1) if match else None

# Placeholder function to download audio (you can use youtube-dl or pytube)
def download_youtube_audio(video_url):
    try:
        # Initialize the YouTube object with the video URL
        yt = YouTube(video_url)
        
        # Select the audio stream with the highest bitrate
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Download the audio file and save it as mp4
        audio_file = audio_stream.download(filename="audio.mp4") #type: ignore
        
        return audio_file
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None

# Main function
def main():
    # Example YouTube URL (replace with any valid URL)
    video_url = input("Please enter the YouTube video URL: ")

    # Convert the YouTube video into an article format
    article = youtube_to_article(video_url)
    
    # Output the article to a file
    if article:
        # Ask user for the output file name
        file_name = input("Please enter the name of the file to save the article (e.g., article.txt): ")

        # Write the article to the file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(article)
        
        print(f"\nThe article has been saved to {file_name}.")
    else:
        print("No article was generated.")

# Main Method
if __name__ == "__main__":
    main()
