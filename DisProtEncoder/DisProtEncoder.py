#!/usr/bin/env python3
"""Script to extract data from DisProt and create two files: 

1. Recoded DisProt fasta file
2. corresponding UniProt fasta file

Author: jcapecci09
"""

from pathlib import Path
import os
from concurrent.futures import ThreadPoolExecutor
import requests
import time
import argparse
import sys

class  DisProtEncoderError(Exception):
    """Special DisProtEncoder error to prompt user when given wrong input"""
    pass


def parse_consensus(fasta: str) -> tuple[list[str], dict[str, str]]:
    """Parses consensus IDR data from DisProt. Consensus sequences have the
    following format.

    >disprot|DP00004|full acc=P49913
    --------------------------------------------------------------------------------
    -----------------------------------------------------TTTTTTTTTTTTTTTTTTTTTTTTTTT
    TTTTTTTTTT


    :param fasta: multi-fasta file with consensus seqeunces
    :param recoded_fasta: recoded consensus multi fasta file with D replaced with 1 and [T, -] replaced with 0
    :return: list of UniProt accession numbers
    """

    # List to contain accessions number
    acc = []
    fastas_recoded = {}

    # Open fasta file for reading and new recoded file for 
    # recoding
    with open(fasta, 'r') as f:
        
        # For each line in fasta 
        for line in f:

            # collect accessions and headers
            if line.startswith('>'):
                fastas_recoded[line] = ''   # Add header to dictionary 
                current_header = line       # track current headers
                line_split = line.split(' ')    # split by spaces
                acc.append(line_split[1].replace('acc=', '').strip())   # grab UniProt accessions and add to list
            
            # recode sequences and save in dictionary
            else:
                line_recoded = line.replace('-', '0').replace('D', '1').replace('T', '0')       # Replace line with 0's and 1's
                fastas_recoded[current_header] += line_recoded                                  # map line with current header in  dictionary
    
    return acc, fastas_recoded


def download(url: str):
    """Download fasta data from a UniProt URL.

    :param url: UniProt fasta URL
    :return: Fasta text if successful, otherwise None
    """

    # Extract filename from URL
    filename = url.split('/')[-1]
    
    try:

        # Send GET request with timeout to avoid hanging forever
        r = requests.get(url, timeout=10)
        
        # Check if request succeeded and response contains data
        if r.status_code == 200 and r.content:

            # Print successful download
            print(f"downloading data from: {url}")

            # Return fasta text
            return r.text
        else:

            # Print failed request status code
            print(f"Failed: {url} ({r.status_code})")
            return None
         
    except Exception as e:

        # Catch connection/time out errors without crashing program
        print(f"Error: {url} -> {e}. Try reducing number of workers (-w) if errors persist.")
        return None
        
                
def main():

    # Set up parser for command line support
    parser = argparse.ArgumentParser(description='Recodes DisProt consensus sequences ' \
                                    'AND obtains corresponding UniProt sequences')
    parser.add_argument('-i', '--input', help='input file', required=True)
    parser.add_argument('-o', '--output', help='output directory', default='Data')
    parser.add_argument('-t', '--type', help='output type', default=0)
    parser.add_argument('-w', '--workers', help='Number of workers', default=16)

    # define infile, outfile, and type
    args = parser.parse_args(sys.argv[1:])
    infile = args.input
    directory = args.output
    output_type = int(args.type) # defines what outputs the user desires
    num_workers = int(args.workers) # Number of workers to generate output

    # If user gives invalid output raise error
    if not output_type in [0, 1, 2]:
        raise DisProtEncoderError('Output type error: User must specify 0 for both outputs, 1 for ONLY UniProt.fasta,' \
        'or 2 for ONLY recoded fasta')


    # Make directory to hold data
    os.makedirs(directory, exist_ok=True)

    # Parse consensus fasta to grab accessions and recode fasta
    accs, recoded = parse_consensus(infile)

    # Only perform operations if user specifies 0 or 2 for output type
    if output_type == 0 or output_type == 2:

        # Write recoded to fasta file
        with open(f'{directory}/consensus_IDR_recoded.txt', 'w') as f:
            for key in recoded:
                f.write(key)
                f.write(recoded[key])

    # Collect URLS in list
    urls = [f'https://rest.uniprot.org/uniprotkb/{acc}.fasta' for acc in accs]

    # Only perform operations if user specifies 0 or 1 for output type
    if output_type == 0 or output_type == 1:

        # Download data faster
        # Program spends most of its time waiting for network responses
        # ThreadPoolExecutor allows multiple URL downloads to happen concurrently
        # While one thread waits for a response, another can download data
        if not Path(f'{directory}/UniProt.fasta').exists():

            # benchmark  tool
            start = time.perf_counter()

            # Create a pool of worker threads to download URL's concurrently
            with ThreadPoolExecutor(max_workers=num_workers) as executer:

                # Map each URL to the download function
                # Returns downloaded fasta contents in order
                results = list(executer.map(download, urls))

            end = time.perf_counter()

            # Print total download time
            print(f'Time to download data: {(end - start):.2f}s with {num_workers} workers')

            # Combine all fasta data into one fasta file
            with open(f'{directory}/UniProt.fasta', 'w') as f:
                for fasta in results:

                    # Skip failed downloads that returned None
                    if fasta:
                        f.write(fasta)

            print('data retrieved')
        
        # If directory already contains data, don't bother downloading
        else:
            print('Data already retrieved')
            print(f'look for UniProt.fasta in {directory}')


if __name__ == '__main__':
    main()
