#!/bin/bash

# Three-Component Memory System - Environment Setup Script
# Version: 1.1.0

set -e

echo "🚀 Setting up Three-Component Memory System"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check Python version
echo "🔍 Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(echo "$PYTHON_VERSION < 3.8" | bc -l 2>/dev/null || echo "0") -eq 1 ]]; then
    print_error "Python 3.8 or higher is required (found $PYTHON_VERSION)"
    exit 1
fi
print_status "Python $PYTHON_VERSION detected"

# Check if running in virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Not running in a virtual environment"
    read -p "Create virtual environment? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 -m venv venv
        source venv/bin/activate
        print_status "Virtual environment created and activated"
    fi
else
    print_status "Running in virtual environment: $VIRTUAL_ENV"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip

if [[ -f "../requirements.txt" ]]; then
    pip install -r ../requirements.txt
elif [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
else
    # Install core dependencies
    pip install lancedb networkx sentence-transformers numpy
fi

print_status "Dependencies installed"

# Check OpenClaw installation
echo "🔍 Checking OpenClaw..."
if command -v openclaw &> /dev/null; then
    OPENCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")
    print_status "OpenClaw found: $OPENCLAW_VERSION"
else
    print_warning "OpenClaw not found in PATH"
    print_warning "The memory system will work as a standalone library"
    print_warning "For OpenClaw integration, install OpenClaw first"
fi

# Create data directory
echo "📁 Creating data directory..."
DATA_DIR="$HOME/.openclaw/memory/three_component"
mkdir -p "$DATA_DIR"
print_status "Data directory: $DATA_DIR"

# Test the installation
echo "🧪 Testing installation..."
TEST_SCRIPT=$(cat << 'PYTHON_EOF'
import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

try:
    from three_component_memory import MemorySystem
    
    # Test with temporary directory
    import tempfile
    test_dir = tempfile.mkdtemp()
    
    memory = MemorySystem({'data_path': test_dir, 'debug': False})
    print("✅ MemorySystem imported successfully")
    
    # Test basic functionality
    memory_id = memory.add("Test memory", category="test", importance=1)
    if memory_id:
        print("✅ Memory added successfully")
    else:
        print("⚠️  Memory addition returned None")
    
    stats = memory.get_stats()
    print(f"✅ System status: {stats.get('status', 'unknown')}")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    print("🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON_EOF
)

python3 -c "$TEST_SCRIPT"

# Create configuration example
echo "⚙️  Creating configuration example..."
CONFIG_EXAMPLE=$(cat << 'JSON_EOF'
{
  "skills": {
    "three-component-memory": {
      "enabled": true,
      "auto_record": true,
      "importance_threshold": 3,
      "data_path": "~/.openclaw/memory/three_component",
      "search": {
        "default_type": "hybrid",
        "default_limit": 5,
        "min_score": 0.3
      }
    }
  }
}
JSON_EOF
)

echo "$CONFIG_EXAMPLE" > openclaw_config_example.json
print_status "OpenClaw configuration example created: openclaw_config_example.json"

# Create quick test script
echo "📝 Creating quick test script..."
cat > quick_test.py << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Quick test script for Three-Component Memory System.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from three_component_memory import MemorySystem

def main():
    print("🚀 Quick Test - Three-Component Memory System")
    print("=" * 50)
    
    # Initialize with test directory
    import tempfile
    test_dir = tempfile.mkdtemp()
    
    try:
        memory = MemorySystem({'data_path': test_dir, 'debug': True})
        print("✅ System initialized")
        
        # Test basic operations
        memory_id = memory.add(
            content="Quick test memory",
            category="test",
            importance=2
        )
        print(f"✅ Memory added: {memory_id}")
        
        # Test search
        results = memory.search("test", search_type="hybrid")
        print(f"✅ Search found {len(results)} results")
        
        # Test stats
        stats = memory.get_stats()
        print(f"✅ System status: {stats['status']}")
        print(f"✅ Memory count: {stats['memory_count']}")
        
        print("\n🎉 All quick tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
PYTHON_EOF

chmod +x quick_test.py
print_status "Quick test script created: quick_test.py"

echo ""
echo "🎉 Setup Complete!"
echo "================="
echo ""
echo "📋 Next Steps:"
echo "1. Run the quick test: ./quick_test.py"
echo "2. Check the examples: python examples/basic_usage.py"
echo "3. Read the documentation: docs/getting-started.md"
echo ""
echo "🔧 For OpenClaw Integration:"
echo "1. Copy the skill to OpenClaw skills directory:"
echo "   cp -r src ~/.openclaw/skills/three-component-memory"
echo "2. Add configuration to ~/.openclaw/config.json"
echo "3. Restart OpenClaw: openclaw gateway restart"
echo ""
echo "📚 Documentation:"
echo "• Getting Started: docs/getting-started.md"
echo "• API Reference: docs/api-reference.md"
echo "• Architecture: docs/architecture.md"
echo "• Troubleshooting: docs/troubleshooting.md"
echo ""
echo "💡 Need help? Check the troubleshooting guide or open an issue on GitHub."
