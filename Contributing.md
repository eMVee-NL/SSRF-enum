# Contributing to SSRF-enum

First off, thank you for considering contributing to this project! It's people like you that make this tool better for the security research and CTF community.
When contributing to this repository, please first discuss the change you wish to make via an Issue before making a change. 
Please note we have a strict code of conduct, and we expect all contributors to follow it to maintain a welcoming and safe environment.

## How Can I Contribute?

### Reporting Bugs
If you encounter a bug or unexpected behavior (such as false positives on a specific type of server reflection), please open an Issue and include:
* Your Python version.
* The target environment type (if known/authorized, e.g., Apache, Nginx, built-in PHP server).
* A clear description of the issue and steps to reproduce.
* Any relevant error messages or console logs (ensuring no sensitive corporate or personal data is exposed).

### Suggesting Enhancements
We welcome ideas to make the tool faster or more robust! If you have a feature request:
* Open an Issue describing the feature and why it would be useful.
* Explain the problem it solves and provide examples if possible.

### Pull Requests (PRs)
Ready to make a change? Follow these steps to ensure a smooth review process:

1. **Fork the repository** and create your branch from `main`.
2. Ensure your code follows clean Python style guidelines (PEP 8 preferred).
3. Keep your commits clean, well-structured, and descriptive.
4. Update the `README.md` documentation if your changes introduce new interactive prompts or arguments.
5. Submit your Pull Request with a comprehensive description of the changes made.

## Code Style & Standards

To maintain code clarity and project integrity:
* Ensure all comments and documentation are written in **English**.
* Do not introduce third-party library requirements unless absolutely necessary and discussed beforehand.
* Make sure error handling (e.g., `requests.exceptions`) remains robust so network timeouts don't crash long-running recursive scans.

Thank you for your dedication to keeping the security community secure and well educated!
