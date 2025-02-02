# Bookmark Search

## Description

_Bookmark Search_ is a Python **RAG application** that allows users to **store** the contents of their bookmarked
websites and
automatically **search** for matching websites based on their query they enter in the URL bar.

When a matching website is found (based on cosine similarity), a link to the bookmarked website pops up, allowing users
to quickly navigate.

**The purpose** of this application is to provide users with a more efficient way to search within their bookmarked
websites as the number of bookmarks grows and becomes difficult to sort through manually.

## Features

- OCR: JinaAI for reading text from the bookmarked websites.
- LLM: Sentence-transformers for embedding text.
- Vector DB: PGVector for storing indexed bookmarks as documents.

## Installation (for development)

### Prerequisites

Ensure you have the following installed:

- Brave Browser
- Python3.10


### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/project-name.git
   ```
2. Navigate to the project directory:
   ```sh
   cd bookmark-search
   ```

3. Install dependencies:
   ```sh
   poetry install
   ```

## Usage

Run the application with:

```sh
python main.py
```

## Configuration

If your application requires configuration, mention how to set it up. Example:

- Edit the `.env` file with appropriate values.

## Testing

Run tests using:

```sh
pytest
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make changes and commit (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a pull request

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contact

For any questions or support, contact [your email] or create an issue in the repository.
