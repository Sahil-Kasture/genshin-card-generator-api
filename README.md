# Genshin Card Generator API

A FastAPI-based service that generates beautiful character and profile cards for Genshin Impact players using data from the Enka Network API.

## Features

- **Character Cards**: Generate detailed character cards with stats, artifacts, and weapons
- **Profile Cards**: Create comprehensive player profile cards
- **Multiple Templates**: Support for different card designs and layouts
- **Real-time Data**: Uses Enka Network API for up-to-date player information
- **FastAPI**: Modern, fast web framework with automatic API documentation

## API Endpoints

### Base URL
```
https://your-domain.com
```

### Available Endpoints

#### Health Check
- `GET /` - Check if the API is running
- `GET /update` - Update assets and data

#### Character Cards
- `GET /character_card/{uid}/{character_id}` - Generate character card 

#### Profile Cards
- `GET /profile_card/{uid}` - Generate player profile card

### Parameters
- `uid`: Player's UID (User ID)
- `character_id`: Character index in the player's roster (0-based)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MR-LORD-REX-123/card-api.git
cd card-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python ENKA_CARD/main.py
```

The API will be available at `http://localhost:8000`

## Deployment

This project includes a `render.yaml` configuration file for easy deployment on Render.com.

### Environment Variables
- `PORT`: Server port (default: 8000)
- `PYTHON_VERSION`: Python version (default: 3.12.0)

## Project Structure

```
enka_project/
├── ENKA_CARD/
│   ├── main.py                 # FastAPI application
│   ├── character_card/         # Character card generation
│   └── profile_card/           # Profile card generation
├── enkanetwork/               # Enka Network API client
├── requirements.txt           # Python dependencies
├── render.yaml               # Render deployment config
└── README.md                 # This file
```

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pillow**: Image processing
- **EnkaNetworkAPI**: Genshin Impact data API

## Usage Examples

### Generate a Character Card
```bash
curl "http://localhost:8000/character_card1/123456789/0" -o character_card.png
```

### Generate a Profile Card
```bash
curl "http://localhost:8000/profile_card/123456789" -o profile_card.png
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Enka Network](https://enka.network/) for providing Genshin Impact player data
- [Genshin Impact](https://genshin.hoyoverse.com/) for the game assets and data 
