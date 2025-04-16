# MemePoster

**MemePoster** is an automated meme distribution tool that fetches trending memes from Reddit and posts them to platforms like X (formerly Twitter) and Instagram. Designed with flexibility in mind, it supports multiple content sources and destinations, making it a versatile solution for meme enthusiasts and social media managers.

## 🚀 Features

- **Automated Meme Collection**: Retrieves popular memes from Reddit's top lists.
- **Multi-Platform Posting**: Currently supports posting to X and Instagram, with the potential to add more platforms.
- **Extensible Architecture**: Built to easily incorporate additional content sources and destinations.
- **Scheduled Posting**: Set up to post memes at regular intervals, keeping your audience engaged.

## 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pexmee/MemePoster.git
   cd MemePoster
   ```
2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure Environment Variables**
    Make sure to export and populate the following environment variables:
    ```text
    REDDIT_CLIENT_ID=your_reddit_client_id
    REDDIT_CLIENT_SECRET=your_reddit_client_secret
    REDDIT_USER_AGENT=your_user_agent

    TWITTER_API_KEY=your_twitter_api_key
    TWITTER_API_SECRET=your_twitter_api_secret
    TWITTER_ACCESS_TOKEN=your_access_token
    TWITTER_ACCESS_SECRET=your_access_secret

    INSTAGRAM_USERNAME=your_instagram_username
    INSTAGRAM_PASSWORD=your_instagram_password
    ```

    Either in a session:
    ```bash
    export ENV_VARIABLE_NAME=<insert thing here>
    ```

    Or for persistance add it to your config file (**~/.bashrc**, **~/.zshrc** or similar).

## 🤝 Contributing
Contributions are welcome! If you have suggestions for new features, improvements, or bug fixes, please fork the repo and open a pull request.