# Sibila Dependency Migration Guide

## 🎯 Overview

This guide provides step-by-step instructions for updating Sibila's dependencies to the latest secure versions and testing the application.

## 📋 Prerequisites

- Python 3.8+ (current: 3.12.3)
- Git (for version control)
- Internet connection (for package downloads)

## 🚀 Quick Migration

### Option 1: Automated Update (Recommended)

```bash
# Run the automated update script
./update_dependencies.sh
```

### Option 2: Manual Update

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install updated dependencies
pip install -r requirements.txt

# 4. Test the application
python tests/test_application.py

# 5. Start the application
python main.py
```

## 📦 Dependency Changes Summary

| Package | Old Version | New Version | Risk Level | Notes |
|---------|-------------|-------------|------------|-------|
| Flask | 3.0.3 | 3.1.1 | 🟢 Low | Security patches, no breaking changes |
| Werkzeug | 3.0.4 | 3.1.3 | 🟢 Low | Compatible with Flask 3.1.x |
| python-dotenv | 1.0.1 | 1.1.1 | 🟢 Low | Minor improvements |
| pdfplumber | 0.11.1 | 0.11.7 | 🟢 Low | Bug fixes for text extraction |
| PyPDF2 | 3.0.1 | 3.0.1 | 🟢 None | Already latest |
| ollama | 0.3.3 | 0.5.1 | 🟡 Medium | New features, test integration |
| openai | 1.10.0 | 1.97.1 | 🟡 Medium | Major update, but code compatible |
| requests | 2.31.0 | 2.32.4 | 🟠 High | **Security fixes - CRITICAL** |
| chromadb | 0.5.3 | 0.5.20 | 🟡 Medium | Performance improvements |
| chroma-hnswlib | 0.7.3 | 0.7.6 | 🟡 Medium | Bug fixes |

## 🔒 Security Improvements

### Critical Security Updates:
1. **requests**: Fixes for CVE vulnerabilities in HTTP handling
2. **Flask/Werkzeug**: Security patches for web framework
3. **OpenAI**: Latest security patches and API improvements

## 🧪 Testing Strategy

### 1. Automated Testing
```bash
# Run comprehensive tests
python tests/test_application.py
```

### 2. Manual Testing Checklist

#### Basic Functionality:
- [ ] Application starts without errors
- [ ] Web interface loads at http://localhost:5000
- [ ] Environment variables load correctly

#### Document Processing:
- [ ] PDF upload works
- [ ] Text extraction functions
- [ ] Document indexing completes

#### LLM Integration:
- [ ] OpenAI API calls work (if configured)
- [ ] Ollama integration works (if installed)
- [ ] Question answering functions

#### Database Operations:
- [ ] ChromaDB initialization
- [ ] Vector storage/retrieval
- [ ] Search functionality

### 3. Performance Testing
- [ ] Memory usage normal
- [ ] Response times acceptable
- [ ] No memory leaks during operation

## 🐛 Troubleshooting

### Common Issues and Solutions:

#### Import Errors
```bash
# If modules not found
pip install --force-reinstall -r requirements.txt
```

#### OpenAI API Issues
```python
# Test OpenAI connection
python -c "
import openai
client = openai.OpenAI(api_key='your-key')
print('OpenAI client works!')
"
```

#### Ollama Connection Issues
```bash
# Check Ollama status
curl http://localhost:11434/api/tags
```

#### ChromaDB Issues
```bash
# Clear ChromaDB data if corrupted
rm -rf data/chromadb/
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required for OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Required for Ollama (if using)
OLLAMA_PROXY_URL=http://localhost:11434
```

### Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# Download model (in another terminal)
ollama pull llama3
```

## 📈 Performance Monitoring

### Key Metrics to Monitor:
- Application startup time
- PDF processing speed
- Query response time
- Memory usage
- Error rates

### Monitoring Commands:
```bash
# Check application health
curl http://localhost:5000/health

# Monitor system resources
htop
```

## 🔄 Rollback Plan

If issues occur, rollback to previous versions:

```bash
# Restore original requirements
cp requirements.txt.backup requirements.txt

# Reinstall old versions
pip install --force-reinstall -r requirements.txt
```

## 📝 Post-Migration Checklist

- [ ] All tests pass
- [ ] Application starts successfully
- [ ] Core functionality verified
- [ ] Performance acceptable
- [ ] Error logs clean
- [ ] Documentation updated
- [ ] Team notified of changes

## 🎉 Success Indicators

✅ Application runs without errors  
✅ All imports successful  
✅ Web interface responsive  
✅ PDF processing works  
✅ LLM integration functional  
✅ Database operations normal  

## 📞 Support

If you encounter issues:
1. Check the logs: `tail -f logs/application.log`
2. Run diagnostics: `python tests/test_application.py`
3. Review error messages carefully
4. Consult the dependency documentation for breaking changes

---

**Migration completed successfully!** 🎊

Your Sibila application is now running with the latest secure dependencies.