# Knowlift

A series of interactive games designed to boost your mood.  
Works great on both phones 📱 and computers 💻.

## 📊 Project Status

| Category           | Badge |
|--------------------|-------|
| **Master Branch**  | [![CI][ci-badge]][ci-link] |
| **Coverage**       | [![Coverage][cov-badge]][cov-link] |
| **Open Issues**    | [![Issues][issues-badge]][issues-link] |
| **Progress**       | [![Commits][commits-badge]][commits-link] |
| **Code of Conduct**| [![Covenant][covenant-badge]][covenant-link] |
| **License**        | [![License][license-badge]][license-link] |

## 📖 Contents

- [Architecture](#-architecture)  
- [Development](#-development)  
- [Contributing](#-contributing)  
- [Versioning](#-versioning)  
- [Code of Conduct](#-code-of-conduct)  

## 📐 Architecture

The project follows a layered architecture pattern where each layer only depends on the layer below it.  
The layers in the diagram below map directly to Python packages under `src/`, e.g. **Web** → `src/web`, etc.

![Architecture Diagram](./architecture.svg)

## 🛠 Development

To get the project running locally, follow the [setup instructions][setup].

## 🤝 Contributing

Contributions are welcome and greatly appreciated! 🙌  
Every little bit helps, and credit will always be given.  

- Read the [contribution guidelines][contributing] before opening issues or PRs.

## 📦 Versioning

This project follows [Semantic Versioning (SemVer)][semver].  
See available versions under the [repository tags][tags].  

- **Major**: Rare, planned well in advance.  
- **Minor**: Feature releases, shipped more frequently.  
- **Patch**: Bug fixes, released as needed.  

## 📜 Code of Conduct

We follow the [Contributor Covenant][coc].  
By participating, you are expected to uphold this code.  


[ci-badge]: https://github.com/mariusmucenicu/knowlift/actions/workflows/ci.yml/badge.svg
[ci-link]: https://github.com/mariusmucenicu/knowlift/actions/workflows/ci.yml?query=branch%3Amaster

[cov-badge]: https://codecov.io/gh/mariusmucenicu/knowlift/branch/master/graph/badge.svg
[cov-link]: https://codecov.io/gh/mariusmucenicu/knowlift

[issues-badge]: https://img.shields.io/github/issues/mariusmucenicu/knowlift.svg
[issues-link]: https://github.com/mariusmucenicu/knowlift/issues

[commits-badge]: https://img.shields.io/github/commits-since/mariusmucenicu/knowlift/2.1.0.svg
[commits-link]: https://github.com/mariusmucenicu/knowlift/compare/2.1.0...master

[covenant-badge]: https://img.shields.io/badge/Contributor%20Covenant-3.0-4baaaa.svg
[covenant-link]: https://www.contributor-covenant.org/version/3/0/code_of_conduct

[license-badge]: https://img.shields.io/badge/License-AGPL_v3-blue.svg
[license-link]: https://www.gnu.org/licenses/agpl-3.0

[setup]: ./SETUP.md
[contributing]: ./CONTRIBUTING.md
[coc]: ./CODE_OF_CONDUCT.md
[tags]: https://github.com/mariusmucenicu/knowlift/tags
[semver]: https://semver.org
