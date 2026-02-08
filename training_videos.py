import streamlit as st
import json
import os
from pathlib import Path

def load_training_videos():
    """Load training videos from JSON file."""
    json_path = Path(__file__).parent / "training_videos.json"
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Training videos data file not found.")
        return []
    except json.JSONDecodeError:
        st.error("Error reading training videos data.")
        return []

def get_youtube_embed_url(url):
    """Convert YouTube URL to embed URL."""
    if "youtu.be" in url:
        video_id = url.split("/")[-1].split("?")[0]
    elif "youtube.com/watch" in url:
        video_id = url.split("v=")[1].split("&")[0]
    else:
        return None
    return f"https://www.youtube.com/embed/{video_id}"

def run():
    """Main function for Training Videos page."""
    st.header("📹 Staff Training Videos")
    st.write("Browse and watch previous training videos for staff development.")
    
    # Load training videos
    videos = load_training_videos()
    
    if not videos:
        st.warning("No training videos available at the moment.")
        return
    
    # Display count
    st.info(f"📊 Total Training Videos: {len(videos)}")
    
    # Create tabs or sections for each video
    st.markdown("---")
    
    # Option to view videos in grid or list
    view_mode = st.radio(
        "View Mode:",
        ["List View", "Grid View"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if view_mode == "Grid View":
        # Display videos in a grid (2 columns)
        cols = st.columns(2)
        for idx, video in enumerate(videos):
            with cols[idx % 2]:
                st.markdown(f"### 🎬 {video['title']}")
                
                # Embed YouTube video
                embed_url = get_youtube_embed_url(video['url'])
                if embed_url:
                    st.markdown(
                        f"""
                        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
                            <iframe 
                                src="{embed_url}" 
                                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                                frameborder="0" 
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                allowfullscreen>
                            </iframe>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Display description
                st.markdown(f"**Description:** {video['description']}")
                
                # Link to open in new tab
                st.markdown(f"🔗 [Open in YouTube]({video['url']})", unsafe_allow_html=True)
                st.markdown("---")
    
    else:  # List View
        for idx, video in enumerate(videos, 1):
            with st.expander(f"📼 {idx}. {video['title']}", expanded=False):
                # Create two columns for video and details
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Embed YouTube video
                    embed_url = get_youtube_embed_url(video['url'])
                    if embed_url:
                        st.markdown(
                            f"""
                            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
                                <iframe 
                                    src="{embed_url}" 
                                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                                    frameborder="0" 
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                    allowfullscreen>
                                </iframe>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                with col2:
                    st.markdown("### 📝 Details")
                    st.markdown(f"**Title:** {video['title']}")
                    st.markdown(f"**Description:** {video['description']}")
                    st.markdown(f"🔗 [Open in YouTube]({video['url']})")
                    
            st.markdown("")  # Add some spacing
    
    # Add admin section for future enhancement
    st.markdown("---")
    with st.expander("ℹ️ How to add new training videos"):
        st.markdown("""
        To add new training videos, edit the `training_videos.json` file with the following format:
        
        ```json
        {
            "title": "Your Video Title",
            "url": "https://www.youtube.com/watch?v=VIDEO_ID",
            "description": "Brief description of the video content"
        }
        ```
        
        The system supports both YouTube formats:
        - `https://www.youtube.com/watch?v=VIDEO_ID`
        - `https://youtu.be/VIDEO_ID`
        """)

if __name__ == "__main__":
    run()
