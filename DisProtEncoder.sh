#!/usr/bin/env bash

# Create local bin if needed
mkdir -p ~/.local/bin

# Copy executable
cp DisProtEncoder.py ~/.local/bin/DisProtEncoder

# Make executable
chmod +x ~/.local/bin/disprotencoder

# Add ~/.local/bin to PATH if missing
if ! grep -q 'HOME/.local/bin' ~/.bashrc; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

echo "Installation complete!"
echo "Run:"
echo "source ~/.bashrc"
echo "Then:"
echo "DisProtEncoder --help"