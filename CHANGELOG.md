# Changelog

## [1.0.1] - 2026-02-16

### Fixed
- Fixed Dockerfile module path from `main:app` to `app.main:app`
- Added `curl` installation in Dockerfile for healthcheck functionality
- Fixed `load_docs_from_file` in RAG module to handle both array and object JSON formats
- Fixed LangGraph workflow node return types (nodes must return state dict, not strings)
- Fixed workflow edge logic to properly route between agents
- Fixed main.py to use the compiled workflow instead of manual routing
- Added proper Python package structure with `__init__.py`

### Added
- Created `start.bat` for Windows users
- Created `start.sh` for Linux/Mac users
- Added `.env.example` for environment configuration
- Added `test_api.py` for API testing
- Enhanced `.gitignore` with more comprehensive patterns
- Improved README with detailed setup instructions
- Added proper API endpoint documentation

### Changed
- Updated README Quick Start section with multiple setup options
- Updated API endpoints documentation to reflect actual endpoints
- Enhanced RAG retriever initialization to load from data file automatically

## [1.0.0] - Initial Release

### Features
- Multi-agent support system with FAQ, Technical, Billing, and Escalation agents
- RAG (Retrieval-Augmented Generation) implementation using FAISS
- LangGraph workflow for agent orchestration
- FastAPI REST API
- Docker support
- AWS ECS deployment ready
