import subprocess

import os

import ast

# Function to extract chapter data from YouTube video
def extract_chapters(video_url):
    try:
        # Run yt-dlp command to get chapter information
        result = subprocess.run(
            ['yt-dlp', '--print', '%(chapters)s', video_url],
            stdout=subprocess.PIPE,
            text=True
        )

        # Check if the output is empty or None
        if not result.stdout.strip() or result.stdout.strip() == "None":
            print("No chapters found for this video.")
            return []

        # Parse the output as a Python literal (list of dictionaries)
        chapters = ast.literal_eval(result.stdout.strip())
        return chapters

    except (SyntaxError, ValueError) as e:
        print(f"Error: Unable to evaluate the chapter data. The output may not be in the correct format. Details: {e}")
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error: yt-dlp command failed with error: {e}")
        return []

# Function to fetch the video title and uploader
def get_video_info(video_url):
    try:
        # Get video title and uploader using yt-dlp
        title_result = subprocess.run(
            ['yt-dlp', '--print', '%(title)s', video_url],
            stdout=subprocess.PIPE,
            text=True
        )
        uploader_result = subprocess.run(
            ['yt-dlp', '--print', '%(uploader)s', video_url],
            stdout=subprocess.PIPE,
            text=True
        )

        title = title_result.stdout.strip()
        uploader = uploader_result.stdout.strip()

        print(f"Video Title: {title}, Uploader: {uploader}")
        return title, uploader

    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to retrieve video info. Details: {e}")
        return None, None

# Function to save song-artist pairs to a .txt file
def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

def save_song_artist_list(chapters, file_name):
    directory = os.path.expanduser("~/Documents/projects/playlistGen/playlists/")
    ensure_directory_exists(directory)
    full_path = os.path.join(directory, file_name)
    with open(full_path, 'w') as f:
        for chapter in chapters:
            title = chapter.get('title', '')
            if title:
                f.write(f"{title}\n")
    return full_path

# Main function
def main():
    # Prompt the user for the YouTube video URL
    video_url = input("Enter the YouTube video URL: ")

    # Extract video title and uploader
    title, uploader = get_video_info(video_url)

    if title and uploader:
        # Generate the file name in "Uploader - Title.txt" format
        file_name = f"{uploader} - {title}.txt"

        # Extract chapters
        chapters = extract_chapters(video_url)

        if chapters:
            # Save to text file
            full_path = save_song_artist_list(chapters, file_name)
            print(f"Song-Artist list saved to {full_path}")
            print("Please check the ~/playlistGen/playlists/ directory for your playlist file.")
        else:
            print("No song-artist pairs could be extracted.")
    else:
        print("Unable to get video information. File will not be saved.")

if __name__ == "__main__":
    main()
