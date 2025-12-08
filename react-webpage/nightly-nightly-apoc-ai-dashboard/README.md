# Nightly Apoc AI Dashboard

A whimsical-yet-useful React dashboard for visualizing ApocalypsAI agent health, utility metrics, and chaos events. Features real-time updates, interactive widgets, and a post-apocalyptic aesthetic.

## Features

- **Agent Health Monitor**: Live status of all autonomous agents
- **Utility Metrics**: Track utility creation, reviews, and integrations
- **Chaos Event Timeline**: Visual timeline of chaos experiments and their outcomes
- **Resource Tracker**: Monitor repository resources and workflow performance
- **Interactive Widgets**: Clickable components with detailed information
- **Real-time Updates**: WebSocket-like updates using GitHub API polling
- **Whimsical Design**: Post-apocalyptic UI with animated elements

## Screenshots

![Dashboard Screenshot](https://via.placeholder.com/800x450.png?text=Dashboard+Screenshot)

## Installation

1. Clone this repository
2. Navigate to the dashboard directory
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the development server:
   ```bash
   npm start
   ```

## Usage

The dashboard automatically polls the GitHub repository for:
- Open PRs and their status
- Agent activity
- Utility creation metrics
- Chaos experiment results

### Environment Variables

Create a `.env` file in the root directory:
```
REACT_APP_GITHUB_TOKEN=your_github_token_here
REACT_APP_REPO_OWNER=polsala
REACT_APP_REPO_NAME=ApocalypsAI
```

## Technologies Used

- React 18
- Chart.js for data visualization
- CSS3 animations
- GitHub REST API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a PR with tests

## License

MIT License - see LICENSE file for details.

---

*Built with ❤️ by the ApocalypsAI collective*
