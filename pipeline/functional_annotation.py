#!/usr/bin/env python2

##############################################################################################################################################################

#Execution: ./functional_annotation.py /home/projects/group-a/functional_annotation/clustering-tools/usearch11.0.667_i86linux32 -f /home/projects/group-a/functional_annotation/script_test -o scripty -e /home/projects/group-a/functional_annotation/homology-tools/eggnog/eggnog-mapper/emapper.py -p /home/projects/group-a/functional_annotation/ab-initio_tools/signalp-5.0b/bin/ -t /home/projects/group-a/functional_annotation/ab-initio_tools/tmhmm-2.0c/bin/ -s /home/projects/group-a/functional_annotation/homology-tools/interproscan/interproscan-5.41-78.0/interproscan.sh -d /home/projects/group-a/functional_annotation/homology-tools/deeparg/deeparg-ss/deepARG.py

#############################################################################################################################################################

import sys
from optparse import OptionParser
import os
import tempfile
import subprocess

def perform_clustering(path, files, prot_or_nucl, identity, tool, outpath):
	fh = open(outpath + "/combined_labelled_fasta.fna", "w")
	
	for i in files:
		reader = open(path+"/"+i, "r")
		
		for line in reader:
			if line.startswith(">"):
				segment = ">"+i+";"+line[1:]
				fh.write(segment)
			else:
				fh.write(line)
		reader.close()
	
	fh.close()
	
	#command on the server
	#clustering-tools/usearch11.0.667_i86linux32 -cluster_fast temp/combined_labelled_fasta.fna -id 0.7 -centroids temp/our_centroids.fa -uc temp/labeled_seqs.fa
	cmd = [tool, "-cluster_fast", outpath+"/combined_labelled_fasta.fna", "-id", str(identity), "-centroids", outpath+"/our_centroids.fa", "-uc", outpath+"/labeled_seqs.fa"]
	subprocess.call(cmd)

def do_interproscan(tool, centroids, outputPath):
	#homology-tools/interproscan/interproscan-5.41-78.0/interproscan.sh -i temp/our_centroids.fa -dp -d temp/interproscan_results
	if os.path.exists(centroids):
		directory = outputPath
		cmd = [tool, "-i", centroids,"-dp", "-d",directory]
		subprocess.call(cmd)
	else:
		print("Centroids fasta file doesn't exist")

def do_deeparg(tool,seqtype,centroids,outputPath):
	#conda activate python2.7
	#python homology-tools/deeparg/deeparg-ss/deepARG.py --align --genes --type prot --input temp/our_centroids.fa --output /temp/deeparg_results/our_centroids.fa.out
	if os.path.exists(centroids):
		#env= ["conda","activate","python2.7"]
		cmd= ["python2", tool,"--align", "--genes", "--type", seqtype, "--input", centroids, "--output", outputPath ]
		#subprocess.call(env)
		subprocess.call(cmd)
	else:
		print("Centroids fasta file doesn't exist")

def do_eggnog(tool,centroids,outputPath):
	if os.path.exists(centroiids):
		#env= ["conda","activate","python2.7"]
		cmd= ["python2", tool, "-i", centroids, "--output", "our_centroids", "-m", "diamond", "-d", "bact", "-o", outputPath]
		#subprocess.call(env)
		subprocess.call(cmd)
	else:
		print("Centroids fasta file doesn't exist")
		
def do_signalP5(tool, outputPath):
	
	#Note: If the tool is not on your path, it needs to be run from the directory where the executable script for the tool is present
	# the variable tool should contain the path to where the executable file is.

	#getting a list of input(.faa) files:
	path_to_gpresults = "/home/projects/group-a/Team1-GenePrediction/results/dfast_results/" #path to the gene prediction results directory
	input_files_command = 'ls '+ path_to_gpresults + '*.faa'
	input_files = subprocess.check_output(input_files_command,shell=True)
	input_files = input_files.split('\n')

	print("Running SignalP ...")

	change_dir = ["cd",tool]
	subprocess.call(change_dir)

	for file_name in input_files:
		output_file = outputPath+"/signalp_"+file_name.split("/")[-1].replace(".faa","")
		sp5_command = "signalp -fasta "+file_name+" -org gram- -format short -prefix "+output_file+" -gff3"
    		subprocess.call(sp5_command.split())

	print("Finished predicting signal peptides!")
	

def do_TMHMM(tool, outputPath):
	
	#Note: If the tool is not on your path, it needs to be run from the directory where the executable script for the tool is present
	#the variable tool should contain the path to where the executable file is.

	#getting a list of input(.faa) files:
	path_to_gpresults = "/home/projects/group-a/Team1-GenePrediction/results/dfast_results/" #path to the gene prediction results directory
	input_files_command = 'ls '+ path_to_gpresults + '*.faa'
	input_files = subprocess.check_output(input_files_command,shell=True)
	input_files = input_files.split('\n')

	change_dir = ["cd",tool]
	subprocess.call(change_dir)

	print("Running TMHMM...")

	for file_name in input_files:
		output_file = outputPath+"/tmhmm_"+file_name.split("/")[-1].replace(".faa","")
		tmhmm_command = "tmhmm "+file_name+" | tee "+output_file+".gff3"
	   	os.system(tmhmm_command)

def do_pilercr(outputPath):
	### Note:
	### PilerCR has to be in the path
	### path = /home/projects/group-a/functional_annotation/ab-initio_tools/pilercr/pilercr1.06/pilercr

	########################
	print('Beginning PilerCR')
	########################

	### This portion captures the assembled isolate genome fasta files in a list
	pathToGenomeAssemblyResults = '/home/projects/group-a/Team1-GenomeAssembly/assembled_output/'
	command = 'ls '+ pathToGenomeAssemblyResults + '*CGT*'
	isolateList = subprocess.check_output(command,shell=True)
	isolateList = isolateList.split('\n')
	########################

	### This portion runs PilerCR on every isolate file,
	### and places the output file in the given PilerCR directory
	for isolateFile in isolateList:
		if isolateFile != '':
			isolateFileName = isolateFile.split('/')
			isolateFileName = isolateFileName[6].split('_')[0]
			command = 'pilercr -in ' + isolateFile + ' -out ' + PilerCR_results_path + isolateFileName + '_pilercrResults.out -noinfo -quiet'
			print(command)
			subprocess.call(command,shell=True)
	########################

	### This part captures all the PilerCR output files in a list
	command = 'ls '+PilerCR_results_path + '*pilercrResults.out*'
	pilercrFiles = subprocess.check_output(command,shell=True)
	pilercrFiles = pilercrFiles.split('\n')
	########################

	### This part takes the information from the PilerCR output files,
	###     and writes the information to a gff file in the same directory
	for pilercrOutput in pilercrFiles:
		if pilercrOutput != '':
			pilerCRName = pilercrOutput.split('/')[7].split('_')[0]
			handle = open(pilercrOutput,'r')
			newHandle = open(PilerCR_results_path+pilerCRName+'_pilercrResults.gff','w')
			newHandle.write('##gff-version 3\n')
			switch = False
			info = []
			for line in handle:
				line = line.strip()
				if '0 putative CRISPR arrays found' in line:
					newHandle.write(pilerCRName+'\t'+'PilerCR'+'\t'+'.'+'\t'+'.'+'\t'+'.'+'\t'+'.'+'\t'+'.'+'\t'+'.'+'\t'+'Description="No CRISPRs found in '+pilerCRName+' isolate file." ')
					newHandle.close()
					break
				elif 'SUMMARY BY SIMILARITY' in line:
					switch = True
				elif 'SUMMARY BY POSITION' in line:
					switch = False
				elif switch == True and line != '' and '=====' not in line and 'Consensus' not in line and '*****' not in line:
					info.append(line)
					newline = line.split()
					array = newline[0]
					sequence = newline[1]+' '+newline[2] #ID
					position = newline[3]
					length = newline[4]
					noCopies = newline[5]
					repeat = newline[6]
					spacer = newline[7]
					strand = newline[8]
					consensus = newline[9]
					end = str(int(position) + int(length))
					newHandle.write(pilerCRName+'\t'+'PilerCR'+'\t'+'CRISPR'+'\t')
					newHandle.write(position+'\t'+ end + '\t')
					newHandle.write('.'+'\t'+'.'+'\t'+'.'+'\t')
					newHandle.write('ArrayID='+array+';')
					newHandle.write('SequenceID="'+sequence+'";')
					newHandle.write('CRISPR_consensus_seq='+consensus+';')
					newHandle.write('Num.Copies='+noCopies+';')
					newHandle.write('RepeatLength='+repeat+';')
					newHandle.write('SpacerLength='+spacer+'\n')
				else:
					'nothing happens'
			handle.close()
			newHandle.close()
	########################

	### This part removes the original PilerCR output files,
	###     and leaves only the gff files
	command = 'rm '+PilerCR_results_path + '*pilercrResults.out*'
	subprocess.call(command,shell=True)
	########################

	########################
	print('PilerCR done')
	########################

	return True


#A function for reading args
def opts():
	parser = OptionParser()
	parser.add_option("-i", "--identity", default = 0.7, dest="clust_id", help = "clustering identity")
	parser.add_option("-f", "--files", dest="files", help = "protein sequences directory")
	#parser.add_option("-p", "--protein", action='store_true', dest="prot", help = "use this if seqs are protein")
	parser.add_option("-u", "--usearch", dest="usearch_loc", help = "usearch absolute path")
	parser.add_option("-o", "--output", default = "temp", dest="outpath", help = "output_file_path")
	parser.add_option("-s", "--interproscan", dest="ips", help = "interproscan absolute path")
	parser.add_option("-d", "--deeparg", dest="deeparg", help = "deeparg absolute path")
	parser.add_option("-e", "--eggnog", dest="eggnog", help = "eggnog absolute path")
	parser.add_option("-p", "--signalp", dest="sigp", help = "signalP absolute path")
	parser.add_option("-t", "--tmhmm", dest="tm", help = "tmhmm absolute path")
	parser.add_option("-r", "--pilercr",dest="pilercr",help='pilercr output path, must end in "/" ')
	

	return(parser.parse_args())
	
#Main should be at bottom.
def main():
	options, args = opts()
	
	file_path = options.files
	
	clust_identity = options.clust_id
	#We decided against nucleotide
	is_protein = True
	
	input_files = os.listdir(file_path)
	
	usearch = options.usearch_loc
	interpro = options.ips
	deeparg = options.deeparg
	eggnog = options.eggnog
	pilercrOutputPath = options.pilercr
	sigP = options.sigp

	print(sigP)
	
	tm = options.tm
	
	out = options.outpath
	
	#location for middle files
	if not os.path.exists(out):
		os.makedirs(out)
		
	homology_root = out+"/homology"
	initio_root = out+"/initio"
	
	deeparg_dir = homology_root + "/deeparg/"
	interpro_dir = homology_root + "/interpro/"
	eggnog_dir = homology_root + "/eggnog/"

	if not os.path.exists(out):
		os.makedirs(out)
		
	if not os.path.exists(homology_root):
		os.makedirs(homology_root)
		
	if not os.path.exists(initio_root):
		os.makedirs(initio_root)
		
	if not os.path.exists(deeparg_dir):
		os.makedirs(deeparg_dir)
		
	if not os.path.exists(interpro_dir):
		os.makedirs(interpro_dir)
		
	if not os.path.exists(eggnog_dir):
		os.makedirs(eggnog_dir)
	
	if is_protein:
		print("Clustering proteins...")
		perform_clustering(file_path, input_files, is_protein, clust_identity, usearch, out)
	else:
		print("Clustering nucleotides...")
		perform_clustering(file_path, input_files, is_protein, clust_identity, usearch, out)
		
	centroids_loc = out+"/our_centroids.fa"
	
	
	
	do_signalP5(sigP, initio_root)
	do_TMHMM(tm, initio_root)
	do_pilercr(pilercrOutputPath)
	do_interproscan(interpro, centroids_loc, interpro_dir)
	do_deeparg(deeparg, "prot", centroids_loc, deeparg_dir+"our_centroids.fa.out")
	do_eggnog(eggnog, centroids_loc, eggnog_dir)
	
	
#Just runs main.
if __name__ == "__main__":main()
