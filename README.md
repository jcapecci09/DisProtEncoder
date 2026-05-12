# DisProtEncoder

## Overview
CLI tool for parsing DisProt annotations, retrieving UniProt sequences, and converting disorder regions into binary-encoded labels for protein disorder and IDR analysis.

## Installation

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

## Command-line arguments
| Flag | Description | Required | Default |
|---|---|---|---|
| `-i` | Input consensus sequence file from [DisProt](https://disprot.org) | Yes | — |
| `-o` | Name of output directory | No | `Data/` |
| `-t` | Output type: `0` = both outputs, `1` = UniProt FASTA only, `2` = recoded FASTA only | No | `0` |
| `-w` | Number of workers used for UniProt downloads | No | `16` |

## Usage Example

The user must provide consensus IDR data from DisProt (e.g. `consensus_IDR.txt`). The expected input format is shown below:

```text
>disprot|DP00074|full acc=P03372
TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
TTTTTTTTTTTTTTTTTTTTTTTT-----------------------------DDDDDDDDDDDDDDDDDDDDDDD----
------------DDDDDDDDDD------------------------TTTTTTTTTTTTTTTTTTT---------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
-----------------------------------
```

Ensure the tool is installed, then run:

```bash
DisProtEncoder -i consensus_IDR.txt -o output
```

The tool will generate the following files in the output directory.

### `consensus_IDR_recoded.txt`

Disordered regions (`D`) are encoded as `1`, while transition regions (`T`) and ordered regions (`-`) are encoded as `0`.

```text
>disprot|DP00074|full acc=P03372
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000111111111111111111111110000
00000000000011111111110000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000
```

### `UniProt.fasta`

FASTA sequence downloaded from UniProt associated with the accession number in the DisProt file.

```text
>sp|P03372|ESR1_HUMAN Estrogen receptor OS=Homo sapiens OX=9606 GN=ESR1 PE=1 SV=2
MTMTLHTKASGMALLHQIQGNELEPLNRPQLKIPLERPLGEVYLDSSKPAVYNYPEGAAY
EFNAAAAANAQVYGQTGLPYGPGSEAAAFGSNGLGGFPPLNSVSPSPLMLLHPPPQLSPF
LQPHGQQVPYYLENEPSGYTVREAGPPAFYRPNSDNRRQGGRERLASTNDKGSMAMESAK
ETRYCAVCNDYASGYHYGVWSCEGCKAFFKRSIQGHNDYMCPATNQCTIDKNRRKSCQAC
RLRKCYEVGMMKGGIRKDRRGGRMLKHKRQRDDGEGRGEVGSAGDMRAANLWPSPLMIKR
SKKNSLALSLTADQMVSALLDAEPPILYSEYDPTRPFSEASMMGLLTNLADRELVHMINW
AKRVPGFVDLTLHDQVHLLECAWLEILMIGLVWRSMEHPGKLLFAPNLLLDRNQGKCVEG
MVEIFDMLLATSSRFRMMNLQGEEFVCLKSIILLNSGVYTFLSSTLKSLEEKDHIHRVLD
KITDTLIHLMAKAGLTLQQQHQRLAQLLLILSHIRHMSNKGMEHLYSMKCKNVVPLYDLL
LEMLDAHRLHAPTSRGGASVEETDQSHLATAGSTSSHSLQKYYITGEAEGFPATV
```

## Data Sources

- [DisProt](https://disprot.org/) — database of intrinsically disordered proteins and regions
- [UniProt](https://www.uniprot.org/) — protein sequence and functional information database
