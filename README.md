# DisProtEncoder
CLI tool for parsing DisProt annotations, retrieving UniProt sequences, and converting disorder regions into binary-encoded labels for protein disorder and IDR analysis.

## Usage Instructions

## Install to PATH

A shell installer is included to allow `DisProtEncoder` to be run from any directory.

### 1. Clone the Repository

```bash
git clone https://github.com/jcapecci09/DisProtEncoder.git
```

### 2. Change Into the Repository Directory

```bash
cd DisProtEncoder
```

### 3. Make the Installer Executable

```bash
chmod +x installer.sh
```

### 4. Run the Installer

```bash
./installer.sh
```

### 5. Reload Your Shell

```bash
source ~/.bashrc
```

### 6. Run DisProtEncoder From Anywhere

```bash
DisProtEncoder -i consensus_IDR.txt
```

