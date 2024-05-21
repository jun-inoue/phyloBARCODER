#!/usr/local/bin/python3.7

import subprocess,re,os,time,random,shutil,cgi,sys,glob,zipfile, datetime
import cgitb; cgitb.enable()
from collections import OrderedDict
from socket import gethostname

#time.sleep(3)


# coding: utf-8

print("Content-Type: text/html\n")
print("")


#print("hello, phyloBARCODER100")
#exit()

EMAIL_SUBJECT_PREFX = '[%s]' % gethostname()
#print("EMAIL_SUBJECT_PREFX:", EMAIL_SUBJECT_PREFX)
#exit()

#####

dirAddress = "../html/"

top_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html">
        <title>TITLE</title>
            <style type="text/css">
                .blackBG { background-color: #000000; color: white}
                .redBG { background-color: #FF0000; color: white}
                .blueBG { background-color: #000080; color: white}
                .grayBG { background-color: #808080; color: white}
            </style>
    </head>
<body>
<pre>
<span style="font-size: 120%;">
<b>phyloBARCODER </b>(ver.1.0)<br><br>'''

bottom_html = '''
</span></pre>
</body>
</html>'''

####


def retrieave_databaseVariables(release_MIDORI2DB):
    #print("release_MIDORI2DB", release_MIDORI2DB, "<br>")
    #exit()
    if "os3-373-19568.vs.sakura.ne.jp" in EMAIL_SUBJECT_PREFX:
        rscriptTMP = "Rscript"
        if release_MIDORI2DB == "GenBank254":
            database_address = "/var/www/html/dbb/database_phyloBARCODER/GB254_MIDORI/"
            database_species = "/var/www/html/dbb/database_phyloBARCODER/GB254_MIDORI/MIDORI2_LONGEST_NUC_GB254_15genes_RAW.fasta"
            database_haplotype = "/var/www/html/dbb/database_phyloBARCODER/GB254_MIDORI/MIDORI2_UNIQ_NUC_GB254_15genes_RAW1.fasta"
        elif release_MIDORI2DB == "GenBank259":
            #print("259")
            #exit()
            database_address = "/var/www/html/dbb/database_phyloBARCODER/GB259_MIDORI/"
            database_species = "/var/www/html/dbb/database_phyloBARCODER/GB259_MIDORI/MIDORI2_LONGEST_NUC_GB259_15genes_RAW.fasta"
            database_haplotype = "/var/www/html/dbb/database_phyloBARCODER/GB259_MIDORI/MIDORI2_UNIQ_NUC_GB259_15genes_RAW.fasta"
        ## osaka
    elif "rx1000.site" in EMAIL_SUBJECT_PREFX:
        rscriptTMP = "Rscript"
        if release_MIDORI2DB == "GenBank254":
            database_address = "/home1/dbb/database_phyloBARCODER/GB254_MIDORI/"
            database_species = "/home1/dbb/database_phyloBARCODER/GB254_MIDORI/MIDORI2_LONGEST_NUC_GB254_15genes_RAW.fasta"
            database_haplotype = "/home1/dbb/database_phyloBARCODER/GB254_MIDORI/MIDORI2_UNIQ_NUC_GB254_15genes_RAW1.fasta"
        elif release_MIDORI2DB == "GenBank259":
            database_address = "/home1/dbb/database_phyloBARCODER/GB259_MIDORI/"
            database_species = "/home1/dbb/database_phyloBARCODER/GB259_MIDORI/MIDORI2_LONGEST_NUC_GB259_15genes_RAW.fasta"
            database_haplotype = "/home1/dbb/database_phyloBARCODER/GB259_MIDORI/MIDORI2_UNIQ_NUC_GB259_15genes_RAW.fasta"
        else:
            print("Check release_MIDORI2DB:", release_MIDORI2DB, "\n")
            exit()
    else:
        print("Set up database address.")
        exit()
    return database_address, database_species, database_haplotype, rscriptTMP


def checkUploadFile(infileFN):

    if not text_area_anonSeq:
        print("(A) text area is empty.")
        exit()

    Infile = open(eachDirAddress + infileFN, "r")

    count = 0
    for Line in Infile:
        if re.search(">", Line):
            count += 1
        if re.search("=>", Line):
            print('Error: Remove "=>" from your query.<br>')
            exit()
        #if re.search(" ", Line):
        #    print('Error: Remove " "(space) from your query.<br>')
        #    exit()
    if count > 250000:
        print("Error: more than 250000 '>' were found in your uploaded eDNA file.<br>")
        print("phyloBARCODER allows less than 40000 sequences.<br>")
        exit()
    if count < 1:
        print("Error: No '>' was found in your query file.<br>")
        print("phyloBARCODER allows only fasta format.<br>")
        exit()

    Infile.close()

    recs_uploaded_eDNA_SEQ_fn = readFasta_dict(eachDirAddress, "000_uploaded_anonSeqs.txt")
    for name, seq in recs_uploaded_eDNA_SEQ_fn.items():
        if len(seq) > 3000:
            print("Error in your uploaded eDNA sequences.<br>")
            print("eDNA sequences should be less than 3000bp.<br>")
            print("The following query is " + str(len(seq)) + " bp.<br>")
            print(name + "<br>")
            exit()


def retrieave_topHTML_infor(query):
    #print("### retrieave_topHTML_infor() START ####<br>")
    #https://qiita.com/pythonista/items/ef1cbbf8991e3a5921ff
    #print("query", query, "<br>")
    query_sorted = sorted(query)
    #for html_name in query_sorted:
    #    print("html_name:", html_name, "<br>")
    #print("<br>")
    #exit()

    word_size = "11"

    if not os.path.exists(eachDirAddress):
        #print("making directory", eachDirAddress, "<br>")
        os.mkdir(eachDirAddress)

    mode_select = query.getvalue("mode_select")

    #word_size_yourseq = query.getvalue("word_size_yourseq")
    #print("word_size_yourseq", word_size_yourseq, "<br>")
    #exit()

    text_area_anonSeq = ""
    
    if mode_select == "mode_A":
        input_file_anonSeqs = query['input_file_anonSeqs']
        if (input_file_anonSeqs.filename):
            #print("Selected input_file_anonSeqs")
            text_area_anonSeq = input_file_anonSeqs.file.read().decode()
            if len(text_area_anonSeq) < 1:
                print("Error in your uploaded eDNA sequence file:<br>")
                print(input_file_spNameList.filename, "<br>")
                exit()
        else:
            text_area_anonSeq = query.getvalue("text_area_anonSeq")
        #exit()
        #text_area_anonSeq = query.getvalue("text_area_anonSeq")
        #print("text_area_anonSeq", text_area_anonSeq)
        #exit()

    num_queries = query.getvalue("num_queries")
    #genome_hits = query.getvalue("genome_hits")

    blastHits_anonDB = query.getvalue("blastHits_anonDB")

    blastEvalue_anonseq = query.getvalue("blastEvalue_anonseq")

    release_MIDORI2DB = query.getvalue("release_MIDORI2DB")

    blastHits_speciesDB = query.getvalue("blastHits_speciesDB")
    #print("blastHits_speciesDB", blastHits_speciesDB)
    #exit()
    blastHits_haplotypeDB = query.getvalue("blastHits_haplotypeDB")
    #print("blastHits_haplotypeDB", blastHits_haplotypeDB)
    #exit()
    blastEvalue_midori = query.getvalue("blastEvalue_midori")


    blastHits_userDB = query.getvalue("blastHits_userDB")
    blastEvalue_userDB = query.getvalue("blastEvalue_userDB")

    text_userDB = ""
    if mode_select == "mode_A":
        input_file_userDB = query['input_file_userDB']
        if (input_file_userDB.filename):
            #print("Selected input_file_anonSeqs")
            text_userDB = input_file_userDB.file.read().decode()
            #print("text_userDB", text_userDB)
            #exit()
            if len(text_userDB) < 1:
                print("Error in your uploaded user DB file:<br>")
                print(input_file_userDB.filename, "<br>")
                exit()


    num_bootstrap = query.getvalue("num_bootstrap")

    flankingSequence = query.getvalue("flankingSequence")
    #print("flankingSequence", flankingSequence)
    #exit()

    #taxon_rank_modeB = query.getvalue("taxon_rank_modeB")
    database_modeB = query.getvalue("database_modeB")
    gene_modeB = query.getvalue("gene_modeB")
    text_area_keyword_modeB = query.getvalue("text_area_keyword_modeB")

    #print("taxon_rank_modeB", taxon_rank_modeB)
    #exit()
    
    fh = open(eachDirAddress + "000_uploaded_anonSeqs.txt", "w")
    fh.write(text_area_anonSeq)
    fh.close()

    if text_userDB:
        #print("text_userDB present")
        fh = open(eachDirAddress + "000_uploaded_userDB.txt", "w")
        fh.write(text_userDB)
        fh.close()

    #print("blastHits_speciesDB", blastHits_speciesDB, "<br>")
    #exit()

    return mode_select, \
           word_size, \
           text_area_anonSeq, \
           num_queries, \
           blastHits_anonDB, \
           blastEvalue_anonseq, \
           release_MIDORI2DB, \
           blastEvalue_midori, \
           blastHits_speciesDB, \
           blastHits_haplotypeDB, \
           blastHits_userDB, \
           blastEvalue_userDB,\
           num_bootstrap, \
           flankingSequence, \
           database_modeB, \
           gene_modeB, \
           text_area_keyword_modeB



def delete_dirs():
    now = datetime.date.today()
    for dir in os.listdir(dirAddress + "phylobarcoderWork/"):
        if re.search("^\d", dir):
            mtime = datetime.date.fromtimestamp(int(os.path.getmtime(dirAddress + "phylobarcoderWork/" + dir)))
            base, ext = os.path.splitext(dir)
            if (now - mtime).days >= 3:
                rm_command = "rm -r " + dirAddress + "phylobarcoderWork/" + dir
                subprocess.call(rm_command, shell=True)

def makeCount():
    import fcntl
    
    dat = "./PHYLOBARCODERscripts/count.dat"
    
    fh = open(dat, "r+")
    fcntl.flock(fh.fileno(), fcntl.LOCK_EX)

    count = fh.read()
    count = int(count)
    count += 1
    count = str(count)

    fh.seek(0)
    fh.write(count)
    fcntl.flock(fh.fileno(), fcntl.LOCK_UN)

    fh.close()
    return count

def changeNameLine_trimalOutName (infile, outfile):
    recsFN = readFasta_dict(eachDirAddress, infile)
    out=open(eachDirAddress + "/" +outfile, "w")
    for name,seq in recsFN.items():
        name = re.sub(" .*$", "", name)
        out.write(name + "\n")
        out.write(seq + "\n")
    out.close()

def readFasta_dict(dirAddress, InfileNameFN):
    #print("dirAddress", dirAddress, "|<br>")
    #print("InfileNameFN111", InfileNameFN, "|<br>")
    #exit()
    Infile = open(dirAddress + InfileNameFN, "r")
    seqDictFN  = OrderedDict()
    for Line in Infile:
        Line = Line.rstrip("\n")
        #print("len(Line)", len(Line), "<br>")
        if len(Line) < 1:
            continue
        if Line[0] == ">":
            Name = Line
            Name = re.sub(" +$", "", Name)
            #print("Name", Name, "|<br>")
            #exit()
            seqDictFN[Name] = ""
        else:
            seqDictFN[Name] += Line
    Infile.close()
    return seqDictFN

def outGroupSelect (fastaFile):
    #recSeqFN = readPhy_dict(phyFileName)
    recsFN = readFasta_dict(eachDirAddress, fastaFile)

    #outgroupTMP = list(recsFN.keys())[-1]
    outgroupTMP = list(recsFN.keys())[0]
    return outgroupTMP[1:]

####
def makeSummary():

    uploaded_eDNA_SEQfn = readFasta_dict(eachDirAddress, "000_uploaded_anonSeqs.txt")
    cDNAfn = ""

    fs = open(eachDirAddress + "100_1stAnalysisSummary.txt", "w")

    #fs.write("################ Resultant tree ################\n\n")

    fs.write(">Gene_tree_newick\n")
    pathTMP = eachDirAddress + "085_NJBS1st.txt"
    if os.path.isfile(pathTMP):
        f1stTree = open(pathTMP)
        fs.write(list(f1stTree)[0])
        f1stTree.close()
    else:
        fs.write("Not_estimated.\n")
    #fs.write("\n")

    fs.write("\n")

    #fs.write("################ Settings ################\n\n")

    #print("num_queries", num_queries, "<br>")
    fs.write(">Queries\n")
    if num_queries == "NoBlastSearch":
        fs.write("Blast seaech was not conducted.\n")
    else:
        recsFN = readFasta_dict(eachDirAddress, "005_querySequences.txt")
        for name,seq in recsFN.items():
            fs.write(name[1:] + "\n")
            fs.write(seq + "\n")
    fs.write("\n")

    fs.write(">uploaded_anonymous_sequences\n")
    for name, seq in uploaded_eDNA_SEQfn.items():
        name = re.sub("[\n\r]", "", name)
        fs.write(name[1:] + "\n")
        fs.write(seq + "\n")
    fs.write("\n")

    #fs.write(">E-value threshold for reported sequences\n"  + str(blastEvalue_midori)  + "\n\n")
    #fs.write(">Number of hits to report per genome (num_alignments)\n" + str(num_alignments) + "\n\n")
    #fs.write(">Percent identity cutoff (perc_identity)\n" + str(perc_identity) + "\n\n")
    #fs.write(">Discontiguous MegaBLAST template length (template_length: only dc-megablast)\n" + str(template_length) + "\n\n")

    #fs.write(">TreeSearchMethod\n"   + "Neighbor-joining method (Saitou and Nei 1986)\n\n")

    #fs.write(">SubstitutionModel\n" + "TN93 (Tamura and Nei 1993) + gamma\n\n")

    #fs.write(">Dependencies\n")
    #fs.write("BLAST 2.7.1+\n")
    #fs.write("MAFFT v7.356b\n")
    #fs.write("trimAl 1.2rev59\n")
    #fs.write("ape in R, Version: 5.6.2\n")
    #fs.write("\n")

    fs.close()


def change_MIDORI_nameLine(nameline_fn):

    nameline_fn = re.sub(" incertae sedis", "", nameline_fn)

    #print("nameline_fn|", nameline_fn, "|<br>")
    #exit()
    ele = nameline_fn.split(";")

    gene_recordID = ele[0]
    gene_recordID = re.sub(":.*", "", gene_recordID)
    gene_recordID = re.sub(" .*", "", gene_recordID)
    match = re.search("^>([^\.]+)\.(.+)\.\d+", gene_recordID)

    gene_name = match.group(1)
    #gene_name = re.sub("SRRNA", "12S", gene_name)
    recordID = match.group(2)
    #print("gene_name|", gene_name, "|<br>")
    #print("recordID|", recordID, "|<br>")
    #exit()

    classification_large = "NONE"

    if re.search("_Salmonidae_", nameline_fn):
        classification_large = "Salmonidae"
    else:
        #print("len ele", len(ele))
        #exit()
        if len(ele) > 5:   # 13
            classification_large_tmp = ele[-4]    # ele[-12]
            if re.search("_([^_]+)_", classification_large_tmp):
                match = re.search("_([^_]+)_", classification_large_tmp)
                classification_large = match.group(1)
    #classification_large_tmp = ele[-4]
    #if re.search("_([^_]+)_", classification_large_tmp):
    #    match = re.search("_([^_]+)_", classification_large_tmp)
    #    classification_large = match.group(1)
    #print("classification_large", classification_large)
    #exit()

    classification_small = "NONE"
    if re.search("_Salmoninae_", nameline_fn):
        classification_small = "Salmoninae"
    else:
        classification_small_tmp = ele[-3]
        if re.search("_([^_]+)_", classification_small_tmp):
            match = re.search("_([^_]+)_", classification_small_tmp)
            classification_small = match.group(1)
    #classification_small_tmp = ele[-3]
    #if re.search("_([^_]+)_", classification_small_tmp):
    #    match = re.search("_([^_]+)_", classification_small_tmp)
    #    classification_small = match.group(1)
    #print("classification_small", classification_small)
    #exit()

    species = "NONE"
    speciesTMP = ele[-1]

    #if re.search(" subsp_[ _]+(.*)_+\d+", speciesTMP):
    if re.search(" subsp_ .*", speciesTMP):
        #print("speciesTMP", speciesTMP, "<br>")
        #speciesTMP = re.sub(" subsp_[ _]+(.*)_+\d+", r"-\1", speciesTMP)
        speciesTMP = re.sub(" subsp_ (.*$)", r"\1", speciesTMP)
        speciesTMP = re.sub("_([^_]+)_+\d+$", r"-\1_", speciesTMP)
        #print("speciesTMP", speciesTMP, "<br>")
        #exit()
    if re.search("sedis_([^_]+)_", speciesTMP):
        match = re.search("sedis_([^_]+)_", speciesTMP)
        species = match.group(1)
        species = re.sub(" ", "-", species)
    elif re.search("species_([^_]+)_", speciesTMP):
        match = re.search("species_([^_]+)_", speciesTMP)
        species = match.group(1)
        species = re.sub(" ", "-", species)

    #print("species", species)
    
    #revised_nameline = ">" + recordID + "_" + gene_name + "_" + classification_large + "_" + classification_mediam + "_" + classification_small + "_" + species
    revised_nameline = ">" + recordID + "_" + gene_name + "_" + classification_large + "_" + classification_small + "_" + species
    revised_nameline = re.sub(" ", "", revised_nameline)
    return revised_nameline


def make_querySequenceFile(inFileName, outFileName):
    #print("### make_querySequenceFile() ###<br>")
    #print("num_queries", num_queries, "<br>")
    #exit()
    recsFN = readFasta_dict(eachDirAddress, inFileName)
    out = open(eachDirAddress + outFileName, "w")
    count_nq = 1
    for name ,seq in recsFN.items():
        #print("name", name, "<br>")
        out.write(name + "\n")
        out.write(seq + "\n")
        if num_queries == "onlyFirstSeq":
            break
        if num_queries == "First2seqs" and count_nq == 2:
            break
        if num_queries == "First3seqs" and count_nq == 3:
            break
        if num_queries == "First4seqs" and count_nq == 4:
            break
        if num_queries == "First5seqs" and count_nq == 5:
            break
        if num_queries == "First6seqs" and count_nq == 6:
            break
        if num_queries == "First7seqs" and count_nq == 7:
            break
        if num_queries == "First8seqs" and count_nq == 8:
            break
        if num_queries == "First9seqs" and count_nq == 9:
            break
        if num_queries == "First10seqs" and count_nq == 10:
            break
        count_nq += 1
    out.close()


def change_nameLine(infile, prefix, out_namechanged_uploaded):
    #print("## change_nameLine() ##<br>")
    recsFN = readFasta_dict(eachDirAddress, infile)
    out = open(eachDirAddress + out_namechanged_uploaded, "w")
    count_yourseq = 1
    for name ,seq in recsFN.items():
        #if len(name) > 90:
        #    print("Error: Name line of query sequnece sjhould be less than 90.<br>")
        #    print("Submitted name line:", name, "<br>")
        #    exit()
        name_new =re.sub("\(", "", name)
        name_new =re.sub("\)", "", name_new)
        #name_new =re.sub("_", "-", name_new)
        name_new =re.sub(" ", "-", name_new)
        name_new =re.sub("\t", "-", name_new)
        name_new =re.sub(",", "-", name_new)
        #print("name_new", name_new, "|<br>")
        name_new =re.sub("\|", "_", name_new)
        name_new =re.sub(";", "_", name_new)
        name_new =re.sub("-+", "-", name_new)
        name_new =re.sub("_-", "_", name_new)
        name_new =re.sub("_+", "_", name_new)
        name_new =re.sub(":+", "_", name_new)
        #print("name_new", name_new, "|<br><br>")
        name_new = re.sub("(>.{60}).*", r"\1", name_new)

        #print("num_queries", num_queries,"<br>")
        #exit()

        #if count_yourseq == 1:
        #    name_new = re.sub("^>", ">YOURSEQ" + str(count_yourseq) + "_", name_new)
        #else:
        #if num_queries == "NoBlastSearch":
        #    pass
        #elif blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
        if blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
            pass
        else:
            name_new = re.sub("^>", prefix + str(count_yourseq) + "_", name_new)

        out.write(name_new + "\n")
        seq =re.sub(" ", "-", seq)
        seq =re.sub("-", "", seq)
        out.write(seq + "\n")
        count_yourseq += 1
    out.close()
        

def conduct_makeblastdb(eachDirAddressFN, database_selected, outfileFN):
    #./makeblastdb -dbtype nucl -parse_seqids -in MIDORI_UNIQ_GB238_15genes_RAW.fasta
    makeblastdbLineFN = "PHYLOBARCODERscripts/makeblastdb -dbtype nucl -parse_seqids -in " + eachDirAddressFN + database_selected + " > " + eachDirAddressFN + outfileFN
    #print("makeblastdbLineFN", makeblastdbLineFN, "<br>")
    #exit()
    blastRes = subprocess.call(makeblastdbLineFN, shell=True)


def conduct_blastn(eachDirAddressFN, querieSequenceFile, database_selected, num_alignments, outfile_blastn):
    #print("eachDirAddressFN", eachDirAddressFN, "<br>")
    #print("database_selected", database_selected, "<br>")
    #exit()
    blastLineFN = "PHYLOBARCODERscripts/blastn -num_descriptions 0 -task blastn -word_size " + word_size + " -query " + eachDirAddressFN + querieSequenceFile + " -db " + database_selected + " -num_alignments " + str(num_alignments) + " -evalue " + str(blastEvalue_midori) + " -out " + eachDirAddressFN + outfile_blastn
    #print("blastLineFN", blastLineFN, "<br><br>")
    #exit()
    blastRes = subprocess.call(blastLineFN, shell=True)
    #-num_descriptions 0


### blast res reader start ###
def clean_each_blasthit(list_each_query_fn):
    list_each_blasthit_fn = []
    query = ""
    nameline = ""
    for ele in list_each_query_fn:
        database = ele[0]
        lines = ele[1]
        for line in lines:
            if not line:
                continue
            if line.startswith("Query"):
                query = line
                nameline = ""
            elif line == "***** No hits found *****":
                list_each_blasthit_fn.append([database, query, ">" + line, ">" + line])
            elif line.startswith(">"):
                nameline = line
                #nameline = re.sub(" .*$", "", nameline)
                list_each_blasthit_fn.append([database, query, nameline, nameline])
            else:
                list_each_blasthit_fn.append([database, query, nameline, line])
    return list_each_blasthit_fn

def make_sbjct_stock(line_sbjct):
    #print("line_sbjct", line_sbjct)
    match = re.search("Sbjct +(\d+) +[^ ]+ +(\d+)$", line_sbjct)
    former = match.group(1)
    latter = match.group(2)
    return former, latter
    exit()

def clean_each_blasthit2(list_each_query_fn):
    list_each_query2_fn = []
    flag = 0
    database_stock = ""
    query_stock = ""
    nameline_stock = ""
    length_stock = ""
    score_stock = ""
    identity_stock = ""
    strand_stock = ""
    sbjct_stock = []
    for line in list_each_query_fn:
        database = line[0]
        query = line[1]
        content = line[3]
        #print(line)
        #continue
        #'''
        if content.startswith(">"):
            #print(content)
            if flag == 0:
                #print("flag == 0", content)
                #print("content", content)
                #exit()
                nameline_stock = content
                database_stock = database
                query_stock = query
                flag = 1
            else:
                #print("flag == 1", content)
                #print("database_stock", database_stock)
                #print("query_stock", query_stock)
                #print("nameline_stock", nameline_stock)
                #print("length_stock", length_stock)
                #print("score_stock", score_stock)
                #print("identity_stock", identity_stock)
                #print("strand_stock", strand_stock)
                #print("sbjct_stock", sbjct_stock)
                #print()
                list_each_query2_fn.append([database_stock, query_stock, nameline_stock, length_stock,score_stock, identity_stock, strand_stock, sbjct_stock])
                database_stock = database
                query_stock = query
                nameline_stock = content
                length_stock = ""
                score_stock = ""
                identity_stock = ""
                strand_stock = ""
                sbjct_stock = []
        elif content.startswith("Length="):
            length_stock = content
        elif content.startswith(" Score ="):
            score_stock = content
        elif content.startswith(" Identities ="):
            identity_stock = content
        elif content.startswith(" Strand="):
            strand_stock = content
        elif content.startswith("Sbjct  "):
            sbjct_1, sbjct_2 = make_sbjct_stock(content)
            #print(sbjct_1, sbcjt_2)
            #exit()
            sbjct_stock.append(sbjct_1)
            sbjct_stock.append(sbjct_2)
        #'''
    #print("database_stock", database_stock)
    #print("query_stock", query_stock)
    #print("nameline_stock", nameline_stock)
    #print("length_stock", length_stock)
    #print("score_stock", score_stock)
    #print("identity_stock", identity_stock)
    #print("strand_stock", strand_stock)
    #print("sbjct_stock", sbjct_stock)
    list_each_query2_fn.append([database_stock, query_stock, nameline_stock, length_stock, score_stock, identity_stock, strand_stock, sbjct_stock])
    
    return list_each_query2_fn

def get_each_database(lines_fn):
    dic_each_database_fn = OrderedDict()
    flag = 0
    database = ""
    lines_stock = []
    nameline = ""
    flag_nameline = 0
    for line in lines_fn:
        line = line.rstrip("\n")
        if line.startswith("Database:"):
            if flag == 1:
                 dic_each_database_fn[database] = lines_stock
                 database = line
                 lines_stock = []
            if flag == 0:
                database = line
                flag = 1
        else:
            if line.startswith("Query=") or line.startswith(" Score") or line.startswith(" Identities") or line.startswith(" Strand") or line.startswith("Sbjct") or line.startswith("***** No hits found *****"):
                lines_stock.append(line)

            if flag_nameline == 1:
                if line.startswith("Length"):
                    lines_stock.append(nameline)
                    nameline = ""
                    lines_stock.append(line)
                    flag_nameline = 0
                else:
                    nameline += line
            else:
                if line.startswith(">"):
                    nameline = line
                    flag_nameline = 1
                
    dic_each_database_fn[database] = lines_stock

    list_each_query_fn = []
    for database, recs in dic_each_database_fn.items():
        list_each_query_fn.append([database, recs])

    return list_each_query_fn

def read_blastnRes2(infileFN):
    f = open(eachDirAddress + infileFN)
    lines = list(f)
    f.close()

    list_each_database = get_each_database(lines)
    list_each_blasthit_raw = clean_each_blasthit(list_each_database)
    #print("list_each_blasthit_raw", list_each_blasthit_raw)
    #exit()
    list_each_blasthit = clean_each_blasthit2(list_each_blasthit_raw)
    '''
    for recs in list_each_blasthit:
        database_stock = recs[0]
        query_stock = recs[1]
        nameline_stock = recs[2]
        length_stock = recs[3]
        score_stock = recs[4]
        identity_stock = recs[5]
        strand_stock = recs[6]
        sbjct_stock = recs[7]
        print("database_stock", database_stock)
        print("query_stock", query_stock)
        print("nameline_stock", nameline_stock)
        print("length_stock", length_stock)
        print("score_stock", score_stock)
        print("identity_stock", identity_stock)
        print("strand_stock", strand_stock)
        print("sbjct_stock", sbjct_stock)
        if sbjct_stock:
            print(min(sbjct_stock), max(sbjct_stock))
        print()
    '''
    return list_each_blasthit

### blast res reader end ###


def combine_2retrievedSeqFiles(infileG, infileP, outfileName):
    #print(infileG)
    #print(infileP)
    #print(outfileName)
    recs_G = readFasta_dict(eachDirAddress, infileG)
    recs_P = readFasta_dict(eachDirAddress, infileP)
    seqDictFN  = OrderedDict()
    for name, seq in recs_G.items():
        seqDictFN[name] = seq
    for name, seq in recs_P.items():
        seqDictFN[name] = seq
    out = open(eachDirAddress + outfileName, "w")
    for name, seq in seqDictFN.items():
        out.write(name + "\n")
        out.write(seq + "\n")
    out.close()


def get_bitScore(bitScore_line):
    matchBS = re.search("= ([^ ]+) bits", bitScore_line)
    bitScore_fn = matchBS.group(1)
    return float(bitScore_fn)

def retrieve_seqInformation(nameLineFN, contentsNF):
    #print("nameLineFN", nameLineFN, "<br>")
    #print("contentsNF", contentsNF, "<br>")
    #exit()
    nameLineFN = re.sub(" .*$", "", nameLineFN)
    #print("nameLineFN", nameLineFN, "<br>")
    #exit()
    database_fn = contentsNF[0]
    database_fn = re.sub("Database: ", "", database_fn)
    recordID = nameLineFN[1:]
    #print("nameLineFN", nameLineFN, "<br>")
    #print("recordID", recordID, "<br>")
    #for content in contentsNF:
    #    print(content)

    strand = re.sub("^.*\/","",contentsNF[6]).lower()

    sbjct_tmp = contentsNF[7]
    sbjct = [int(s) for s in sbjct_tmp]
    start_hit = min(sbjct)
    stop_hit = max(sbjct)
    Length = re.sub("Length=", "", contentsNF[3])
    
    #print("database_fn", database_fn)
    #print("recordID", recordID)
    #print("strand", strand)
    #print("start_hit", start_hit)
    #print("stop_hit", stop_hit)
    #print("Length", Length)
    #exit()
    #print("flankingSequence", flankingSequence)
    start = start_hit - int(flankingSequence)
    stop = stop_hit + int(flankingSequence)
    #print("start", start)
    #print("stop", stop)
    if start < 1:
        start = 1
    if stop > int(Length):
        stop = Length
    #print("start", start)
    #print("stop", stop)
    #exit()
    return database_fn, recordID, strand, str(start), str(stop)


def conduct_blastdbcmd(infile_blastres_FN, outfileName):
    #print("eachDirAddress", eachDirAddress)
    '''
    for rec in infile_blastres_FN:
        print("database_selected", rec[0], "<br>")
        print("Query", rec[1], "<br>")
        print("nameline", rec[2], "<br>")
        #print("length", rec[3])
        #print("score", rec[4])
        #print("identity", rec[5])
        #print("strand", rec[6])
        #print("sbjct", rec[7])
        print()
    print("XXXX")
    exit()
    '''

    ### Delete duplicated blast hits
    recs_blastnRes = OrderedDict()
    for rec in  infile_blastres_FN:
        nameline = rec[2]
        if nameline == ">***** No hits found *****":
            continue
        if nameline not in recs_blastnRes.keys():
            recs_blastnRes[nameline] = rec
    #exit()

    recs_cmdResOD = OrderedDict()
    for nameLine, contents in recs_blastnRes.items():
        #print("################################ <br>")
        #print("nameLine", nameLine, "<br>")
        #print("contents", contents, "<br>")
        #continue
        database_selected, recordID, strand, start, stop = retrieve_seqInformation(nameLine, contents)
        #exit()

        #print("#### database_selected ####", database_selected, "<br>")
        if database_selected.startswith("MIDORI"):
            line_blastdbcmd = "PHYLOBARCODERscripts/blastdbcmd -entry " + recordID + " -db " + database_address + database_selected + " -dbtype nucl -strand " + strand + " -range " + start + "-" + stop
        else:
            line_blastdbcmd = "PHYLOBARCODERscripts/blastdbcmd -entry " + recordID + " -db " + database_selected + " -dbtype nucl -strand " + strand + " -range " + start + "-" + stop
        #print("line_blastdbcmd", line_blastdbcmd, "<br><br>")
        #exit()
        res_blastdbcmd_TMP = subprocess.Popen(line_blastdbcmd, stdout=subprocess.PIPE,shell=True).communicate()[0]
        res_blastdbcmd = res_blastdbcmd_TMP.decode('utf-8').split("\n")
        
        #print("res_blastdbcmd", res_blastdbcmd, "<br><br>")
        #exit()

        nameLineBDC = ""
        for line in res_blastdbcmd:
            if line.startswith(">"):
                #print("nameLine", nameLine, "<br>")
                #print("11line", line)
                if database_selected.startswith("MIDORI"):
                    nameLineBDC = change_MIDORI_nameLine(nameLine)
                else:
                    nameLineBDC = line
                #print("nameLineBDC", nameLineBDC, "<br><br>")
                #nameLineBDC = change_MIDORI_nameLine(line)
                recs_cmdResOD[nameLineBDC] = ""
            else:
                recs_cmdResOD[nameLineBDC] += line
                #print("nameLineBDC", nameLineBDC, "<br>")
                #print("line", line, "<br><br>")
    #exit()

    out = open(eachDirAddress + "/" + outfileName, "w")
    #for name, ele in rev_recs_cmdResOD.items():
    for name, ele in reversed(list(recs_cmdResOD.items())):
        out.write(name + "\n")
        out.write(ele + "\n")
    #print("<br><br><br>")
    out.close()


def check_blasthits(eachDirAddressFN, infileName):
    recs_fn = readFasta_dict(eachDirAddressFN + "/", infileName)
    #print("check_blasthits<br>")
    if len(recs_fn) < 3:
        print("Blast hits was less than 3. Stopped. <bf>")
        exit()


def reverse_sequence_file(uploadedSequencesFile, outfile):
    #print("uploadedSequencesFile", uploadedSequencesFile, "<br>")
    #print("retrievedSequencesFile", retrievedSequencesFile, "<br>")
    #print("outfile", outfile, "<br>")
    out = open(eachDirAddress + outfile, "w")

    recs_uploaded_seqs = readFasta_dict(eachDirAddress, uploadedSequencesFile)
    #count = len(recs_uploaded_seqs)
    for name, seq in reversed(recs_uploaded_seqs.items()):
        #name = re.sub(">", ">YOURSEQ" + str(count) + "_", name)
        name = re.sub(":", "-", name)
        #name = name[0:66]
        out.write(name + "\n")
        out.write(seq + "\n")
        #count -= 1
    out.close()


def addQuery2recFile_then_reverse(uploadedSequencesFile, retrievedSequencesFile, outfile):
    #print("## addQuery2recFile_then_reverse ## <br>")
    #print("uploadedSequencesFile", uploadedSequencesFile, "<br>")
    #print("retrievedSequencesFile", retrievedSequencesFile, "<br>")
    #print("outfile", outfile, "<br>")
    out = open(eachDirAddress + outfile, "w")
    pathTMP = eachDirAddress + retrievedSequencesFile
    if os.path.isfile(pathTMP):
        recs_retrieved_seqs = readFasta_dict(eachDirAddress, retrievedSequencesFile)
        for name, seq in recs_retrieved_seqs.items():
            out.write(name + "\n")
            out.write(seq + "\n")

    recs_uploaded_seqs = readFasta_dict(eachDirAddress, uploadedSequencesFile)
    #count = len(recs_uploaded_seqs)
    for name, seq in reversed(recs_uploaded_seqs.items()):
        #name = re.sub(">", ">YOURSEQ" + str(count) + "_", name)
        name = re.sub(":", "-", name)
        #name = name[0:66]
        out.write(name + "\n")
        out.write(seq + "\n")
        #count -= 1
    out.close()


def firstSpeciesPicker(recsFN):
    flag = "notFound"
    for name, seq in recsFN.items():
        if re.search("ANON1_", name):
            keyNameFN = name
            keySequenceFN = seq
            flag = "found"
            break
    if flag == "notFound":
        for name, seq in recsFN.items():
            if re.search("Used4treeSearch", name):
                continue
            keyNameFN = name
            keySequenceFN = seq
            break
        
    return keyNameFN, keySequenceFN


def trimAlresReader(inFileAAFN):
    aafile = open(eachDirAddress + inFileAAFN, "r")
    aafileLines = list(aafile)
    aafile.close()
    
    sequenceTMP = ""
    name_firstRec = ""
    for line in aafileLines:
        #print("line", line)
        if re.search("    <span class=sel>[^<]+<", line):
            match = re.search("    <span class=sel>([^<]+)<", line)
            name_firstRec = match.group(1)
            break
    for line in aafileLines:
        if re.search("<span class=sel>" + name_firstRec + "<", line):
            line = re.sub("^ +<span class=sel>" + name_firstRec + "</span> +", "", line).rstrip("\n")
            line = re.sub("<span class=sel>.</span>", "#", line)
            sequenceTMP += line

    sequence = ""
    for chr in sequenceTMP:
        chr2 = ""
        if chr == "#":
            chr2 = "1"
        else:
            chr2 = "0"
        sequence += chr2

    if sequence:
        return sequence
    else:
        print("No key sequence line in :", inFileAAFN)
        print("  searched by :", topHitName_1stQuery[1:])
        exit()

def addSiteNotes(inFileAAFN, recsFN):
    seqDictFN  = OrderedDict()
    sequence_tm = trimAlresReader(inFileAAFN)
    seqDictFN[">Used4treeSearch"] = sequence_tm
    for name, value in recsFN.items():
      seqDictFN[name] = value
    return seqDictFN

def whiteSpaceAdd(recsFN1):
    longestNameLen = len(max(recsFN1.keys(), key = len))
    recsFN2        = OrderedDict()
    for name,value in recsFN1.items():
        nameWhiteSpace = name[1:] + " " * (longestNameLen - len(name) + 2)
        recsFN2[nameWhiteSpace] = value
    return recsFN2

def add_NCBI_link(lineFN):

    #linFN_mod = lineFN
    #linFN_mod = re.sub("<", "[", linFN_mod)
    #linFN_mod = re.sub(">", "]", linFN_mod)
    #print("linFN_mod:", linFN_mod, "|<br>")

    line_mod = ""
    if re.search("^ ", lineFN) or re.search("ANON\d+", lineFN) or re.search("USERDB\d+", lineFN) or re.search("Used4treeSearch", lineFN):
        #print("No")
        line_mod = lineFN
    else:
        #print("Modified")
        line_mod = re.sub("^([^_]+)_(.*)$", r'<a href="https://www.ncbi.nlm.nih.gov/nuccore/\1" target="_blank">\1</a>_\2', lineFN)
    #print("line_mod:", line_mod, "|<br>")
    #print("")
    return line_mod

def addColor_nameline(recsFN1, summaryFile):
    species_color = make_species_color(summaryFile)
    recsFN2 = OrderedDict()
    for name_seq, seq in recsFN1.items():
        #print("A name_seq|", name_seq, "|")
        for name_color, color in species_color.items():
            if name_seq.startswith("ANON") or name_seq.startswith("Used4treeSearch"):
                recsFN2[name_seq] = seq
                break
            if name_seq.startswith(name_color):
                #print(name_seq + ":" + color + "<br>")
                color = color.rstrip("\n")
                match = re.search("^([^ ]+)( +)$", name_seq)
                content = match.group(1)
                space_after = match.group(2)
                #print("content|", content, "|")
                #print("space_after|", space_after, "|")
                #name_seq2 = "<font color=" + color + ">" + name_seq + "</font>"
                name_seq2 = "<font color=" + color + ">" + content + "</font>" + space_after
                recsFN2[name_seq2] = seq
                #print("B name_seq2|", name_seq2, "|")
                break
    return recsFN2


def matchFirst_sameEachCharacter(keyNameFN, keySpcharacterFN, nameFN, characterFN):
    #print("keyNameFN", keyNameFN, "<br>")
    #print("keySpcharacterFN", keySpcharacterFN, "<br>")
    #print("nameFN", nameFN, "<br>")
    #print("characterFN", keySpcharacterFN, "<br>")
    #print("<br>")
    #exit()
    characterFN_mod = ""
    nameFN = ">" + nameFN
    
    if keyNameFN[1:] in nameFN:
        #print("keyNameFN", keyNameFN, "<br>")
        #print("keySpcharacterFN", keySpcharacterFN, "<br>")
        #print("nameFN", nameFN, "<br>")
        #print("characterFN1", keySpcharacterFN, "<br>")
        #print("<br>")
        characterFN_mod += characterFN
    else:
        if characterFN == "X" or characterFN == "-" or characterFN == "N":
            characterFN_mod += characterFN
        elif keySpcharacterFN.upper() == characterFN:
            #characterFN_mod += "<span class=blackBG>" + characterFN + "</span>"
            characterFN_mod += "."
        else:
            characterFN_mod += characterFN

    return characterFN_mod


def black_sameEachCharacter(keyNameFN, keySpcharacterFN, nameFN, characterFN):
    #print("keyNameFN", keyNameFN, "<br>")
    #print("keySpcharacterFN", keySpcharacterFN, "<br>")
    #print("nameFN", nameFN, "<br>")
    #print("characterFN", keySpcharacterFN, "<br>")
    #print("<br>")
    #exit()
    characterFN_mod = ""
    nameFN = ">" + nameFN
    
    if keyNameFN[1:] in nameFN:
        #print("keyNameFN", keyNameFN, "<br>")
        #print("keySpcharacterFN", keySpcharacterFN, "<br>")
        #print("nameFN", nameFN, "<br>")
        #print("characterFN1", keySpcharacterFN, "<br>")
        #print("<br>")
        if characterFN.islower():
            characterFN_mod += '<span class="redBG">' + characterFN + '</span>'
        elif characterFN == 'X' or characterFN == '-' or characterFN == 'N':
            characterFN_mod += characterFN
        else:
            characterFN_mod += '<span class="blackBG">' + characterFN + '</span>'
    else:
        if characterFN == 'X' or characterFN == '-' or characterFN == 'N':
            characterFN_mod += characterFN
        elif keySpcharacterFN.upper() == characterFN:
            characterFN_mod += '<span class="blackBG">' + characterFN + '</span>'
        else:
            characterFN_mod += characterFN

    return characterFN_mod


def recOneLinesMaker(startPosNF, stopPosNF, recsFN):
    keyNameFN, keySequenceFN = firstSpeciesPicker(recsFN)
    htmlOneLines = []

    longestName = max(recsFN.keys(), key = len)
    longestName = re.sub("<[^>]+>", "", longestName)
    #print("longestName", longestName)
    longestNameLen = len(longestName)
    #print("longestNameLen", longestNameLen)
    NumberLine = " " * (longestNameLen) + str(startPosNF+1) + "\n"
    htmlOneLines.append(NumberLine)

    #print("startPosNF", startPosNF)
    for name in recsFN.keys():
        nameLine = ""
        #if startPosNF == 0:
        #    htmlOneLine = link_genomeLocation(name)
        #else:
        #    htmlOneLine = name
        htmlOneLine = name

        for p in range(startPosNF, stopPosNF):
            character_keySpecies = keySequenceFN[p]
            character      = recsFN[name][p]
            if characters_total > 70000: 
                character_HTML  = matchFirst_sameEachCharacter (keyNameFN, character_keySpecies, name, character)
            else:
                character_HTML  = black_sameEachCharacter (keyNameFN, character_keySpecies, name, character)
            htmlOneLine += character_HTML
        
        keyNameFN_NS = re.sub("^>", "", keyNameFN)
        #print("keyNameFN_NS<br>")
        #print("|", keyNameFN_NS, "|<br>")
        #print("name", "<br>")
        #print("|", name, "|<br>")
        if re.search(keyNameFN_NS, name):
            #print("found<br>")
            htmlOneLine = "<u>" + htmlOneLine + "</u>"
        #else:
        #    print("not found<br>")
        #print("<br>")
        
        htmlOneLine += "\n"
        htmlOneLines.append(htmlOneLine)

    return htmlOneLines


def higlightQuery_in_html(recsFN1):
    recsFN = OrderedDict()
    if os.path.isfile(eachDirAddress + "005_querySequences.txt"):
        recs_querySeqs = readFasta_dict(eachDirAddress, "005_querySequences.txt")
        names_querySeqs = list(recs_querySeqs.keys())
        for name, seq in recsFN1.items():
            name_modified = name
            if name.startswith("ANON"):
                match = re.search("^ANON(\d+)_", name)
                num_yourseq = match.group(1)
                if int(num_yourseq) == 1:
                    #print("YOURSEQ1_ name", name,"<br>")
                    name_modified = '<span class="redBG">' + name + '</span>'
                elif int(num_yourseq) <= int(len(recs_querySeqs)):
                    #print("YOURSEQ2,3_ name", name,"<br>")
                    name_modified = '<span class="blueBG">' + name + '</span>'
                else:
                    #print("YOURSEQ_ name", name,"<br>")
                    name_modified = '<span class="grayBG">' + name + '</span>'
            recsFN[name_modified] = recsFN1[name]
    else:
        for name, seq in recsFN1.items():
            #print("name", name, "<br>")
            name_modified = name
            if name.startswith("UPLOAD1_"):
                name_modified = '<span class="redBG">' + name + '</span>'
            recsFN[name_modified] = recsFN1[name]
    return recsFN


def interleavedMake(oneLineLength, recsFN1):
    
    recsFN = higlightQuery_in_html(recsFN1)

    siteNum  = 1
    startPos = 0
    stopPos  = 0
    sequenceLengthFN = len(list(recsFN.values())[0])
    linesFN  = []
    for i in range(sequenceLengthFN):
        if i > 1 and i % oneLineLength == 0:
            startPos = i - oneLineLength
            stopPos = startPos + oneLineLength
            #print("i :", i, "<br>")
            #print("oneLineLength :", oneLineLength, "<br>")
            #print("siteNum :", startPos + 1, "<br>")
            #print("startPos:", startPos, "<br>")
            #print("stopPos :", stopPos, "<br>")
            #print("<br>")
            #for j in range(startPos, stopPos):
            #    print(str(j) + ",", end="")
            #print()
            recOneLines = recOneLinesMaker(startPos, stopPos, recsFN)
            for line in recOneLines:
                if startPos == 0:
                    line = add_NCBI_link(line)
                linesFN.append(line)
            linesFN.append("\n")

    #print("siteNum :", stopPos + 1)
    #print("startPos:", stopPos)
    #print("stopPos :", sequenceLengthFN)
    #for i in range(stopPos, sequenceLengthFN):
    #    print(str(i) + ",", end="")
    #print()
    recOneLines = recOneLinesMaker(stopPos, sequenceLengthFN, recsFN)
    for line in recOneLines:
        linesFN.append(line)

    linesFN.append("\n")
    return(linesFN)


def deleteReturns_from_seqs(recsFN):
    seqDictFN  = OrderedDict()
    for name, seq in recsFN.items():
        seq = re.sub("\r", "", seq)
        seqDictFN[name] = seq
    return seqDictFN

def make_lines_table_contents(lines_taxon_assignment_fn):
    lines_table_contents_fn = []
    #print("lines_taxon_assignment_fn", lines_taxon_assignment_fn)
    #exit()
    for line in lines_taxon_assignment_fn:
        #print("line", line, "<br>")
        line = line.rstrip("\n")
        lines_table_contents_fn.append('    <tr valign="top">\n')
        #eles  = line.split("\t")
        eles  = line.split(",")
        #print("eles", eles, "<br>")
        if re.search("no_hits_found", line):
            lines_table_contents_fn.append("        <td>" + eles[0] + "</td>\n")
            lines_table_contents_fn.append("        <td>&nbsp;</td>\n")
            lines_table_contents_fn.append("        <td>" + "no_hits_found" + "</td>\n")
            lines_table_contents_fn.append("        <td>&nbsp;</td>\n")
            lines_table_contents_fn.append("        <td>&nbsp;</td>\n")
            lines_table_contents_fn.append("        <td>&nbsp;</td>\n")
        elif re.search("No_tree_estimated", line):
            lines_table_contents_fn.append("        <td>" + eles[0] + "</td>\n")
            lines_table_contents_fn.append("        <td>&nbsp;</td>\n")
            lines_table_contents_fn.append("        <td>" + "No_tree_estimated" + "</td>\n")
            lines_table_contents_fn.append("        <td>&nbsp;</td>\n")
            lines_table_contents_fn.append("        <td>&nbsp;</td>\n")
            lines_table_contents_fn.append("        <td>&nbsp;</td>\n")
        else:

            lines_table_contents_fn.append("        <td>" + eles[0] + "</td>\n")

            largeGrouping = eles[1]
            largeGrouping = re.sub("\/", "/<br>", largeGrouping)
            lines_table_contents_fn.append("        <td>" + largeGrouping + "</td>\n")

            middleGrouping = eles[2]
            middleGrouping = re.sub("\/", "/<br>", middleGrouping)
            lines_table_contents_fn.append("        <td>" + middleGrouping + "</td>\n")

            genus = eles[3]
            genus = re.sub("\/", "/<br>", genus)
            lines_table_contents_fn.append('        <td>' + genus + '</td>\n')

            species = eles[4]
            species = re.sub("\/", "/<br>", species)
            lines_table_contents_fn.append("        <td>" + species + "</td>\n")
            lines_table_contents_fn.append("        <td>" + eles[5] + "</td>\n")
        lines_table_contents_fn.append('    </tr>\n')
    return lines_table_contents_fn


def htmlFileMake(linesFN, queryFile, outFileFN):
    #print("queryFile", queryFile, "<br>")
    #exit()
    
    recs = readFasta_dict(eachDirAddress + "/", queryFile)
    recs = deleteReturns_from_seqs(recs)
           
    #print("outFileFN", outFileFN)
    out = open(eachDirAddress + "/" + outFileFN, "w")

    dirname_rand_TMP = dirname_rand
    dirname_rand_TMP = re.sub("-.*$", "", dirname_rand_TMP)
    top1_html = re.sub("TITLE", dirname_rand_TMP, top_html)
    out.write(top1_html)

    out.write("\n")
    out.write("Download:")
    out.write('<a href="result'+ num_dir +'_phyloBARCODER.zip">result' + num_dir + '_phyloBARCODER.zip</a>\n')
    out.write("\n")

    #out.write('<pre>\n')
    #out.write('<span style="font-size: 120%;">\n')

    if os.path.isfile(eachDirAddress + "115_tree_rooted.png"):
        #if num_queries == "NoBlastSearch":
        #    out.write("Unrooted phylogenetic tree:\n")
        #    out.write('<img src="115_tree_unrooted.png">')
        #    out.write("\n")
        #if blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
        #    out.write("Unrooted phylogenetic tree:\n")
        #    out.write('<img src="115_tree_unrooted.png">')
        #    out.write("\n")
        out.write("Phylogenetic tree:\n")
        out.write('<img src="115_tree_rooted.png">')
        out.write("\n")
    else:
        out.write("Phylogenetic tree:\n")
        out.write('Not estimated.\n')
        out.write("\n")


    out.write("Alignment of blast hits:\n")

    #out.write(str(sequenceLength) + "\n")
    count0 = 0 
    count1 = 0 
    for line in linesFN:
        if line.startswith("Used4treeSearch"):
            count0tmp = line.count('0')
            count0 += count0tmp
            count1tmp = line.count('1')
            count1 += count1tmp
    out.write(str(count1) + " sites (1) were used for tree reconstruction by excluding " + str(count0)+ " sites (0).\n")

    #out.write("</span></pre>")


    for line in linesFN:
        out.write(line)

    
    if num_queries == "NoBlastSearch":
        pass
    elif blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
        pass
    else:
        lines_table_contents = []
    
        #if os.path.isfile(eachDirAddress + "085_NJBS1st.txt"):
        if os.path.isfile(eachDirAddress + "100_taxon_assignment_tree.txt"):
            out.write("Tree identification:\n")
            f = open(eachDirAddress + "100_taxon_assignment_tree.txt")
            lines_taxon_assignment = list(f)
            f.close()
            lines_table_contents = make_lines_table_contents(lines_taxon_assignment)
        #else:
        #    out.write("Blast assignment:\n")
        #    f = open(eachDirAddress + "100_taxon_assignment_blast.txt")
        #    lines_taxon_assignment = list(f)
        #    f.close()
        #    lines_table_contents = make_lines_table_contents(lines_taxon_assignment)
        #out.write("</span></pre>")
        out.write('<table width="80%" border="1">\n')
        out.write("  <tbody>\n")
        for line in lines_table_contents:
            out.write(line)
        out.write('  </tbody>\n')
        out.write('</table>\n')
        out.write("\n")


    out.write("\n################ Settings ################\n\n")

    # Number of queries
    out.write("> Number of queries\n"  + str(num_queries)  + "\n")
    out.write("\n")

    out.write("# Anonymous DB\n")
    out.write(">Number of hits for each query\n" + str(blastHits_anonDB) + "\n")
    out.write(">E-value threshold for reported sequences\n"  + str(blastEvalue_anonseq)  + "\n")
    out.write("\n")

    out.write("# Pre-installed DB\n")
    out.write(">MIDORI2 (Leray et al. 2022) database version\n")
    #out.write(release_MIDORI2DB + "\n")
    #if release_MIDORI2DB == "GenBank254": 
    #out.write("GenBank254\n")
    #out.write("Species DB: 598,328 sequences\n")
    #out.write("Haplotype DB: 2,604,499 sequences\n")

    #elif release_MIDORI2DB == "GenBank259": 
    out.write(release_MIDORI2DB + "\n")
    #out.write("Species DB: 793,068 sequences\n")
    #out.write("Haplotype DB: 3,375,571 sequences\n")
    #out.write("\n")

    out.write(">Number of hits (SpeciesDB) \n" + str(blastHits_speciesDB) + "\n")
    out.write(">Number of hits (HaplotypeDB) \n" + str(blastHits_haplotypeDB) + "\n")
    out.write(">E-value\n"  + str(blastEvalue_midori)  + "\n")
    out.write("\n")

    out.write("# User DB\n")
    out.write(">Number of hits\n" + str(blastHits_userDB) + "\n")
    out.write(">E-value\n"  + str(blastEvalue_userDB)  + "\n")
    out.write("\n")

    out.write(">TreeSearchMethod\n"   + "Neighbor-joining method (Saitou and Nei 1986)\n\n")

    out.write(">SubstitutionModel\n" + "TN93 (Tamura and Nei 1993) + gamma\n\n")

    out.write(">Dependencies\n")
    out.write("BLAST 2.7.1+\n")
    out.write("MAFFT v7.356b\n")
    out.write("trimAl 1.2rev59\n")
    out.write("ape in R, Version: 5.6.2\n")
    out.write("\n")

    out.write(">Version\n")
    out.write("phyloBARCODER 1.0.0\n")
    out.write("\n")


    elapsed_time = round((time.time() - startTime),1)
    out.write("Analysis time: {0}".format(elapsed_time) + " seconds\n")
    out.write("\n\n")


    out.write(bottom_html)
    out.write("\n")
    out.close()

def make_species_color(summaryFile):
    Infile = open(eachDirAddress + summaryFile, "r")
    species_color_FN = {}
    flag = 0
    for line in Infile:
        if flag == 1:
            if line[0] == ">":
                break
            #if re.search("([^ ]+) +([^ ]+)", line):
            #    match = re.search("([^ ]+) +([^ ]+)", line)
            if re.search("^[^_]+_[^_]+$", line):
                match = re.search("^([^_]+)_([^_]+)$", line)
                species = match.group(1)
                color = match.group(2)
                species_color_FN[species] = color
        if re.search(">taxonSampling_color", line):
            flag = 1
    return species_color_FN

def get_leaves(tree_fn):
    #print(tree_fn)
    #print()
    #### Delete branch lengths
    tree_fn = tree_fn.rstrip("\n")
    tree_fn = re.sub(":-", ":", tree_fn)
    tree_fn = re.sub("e-\d+\)", ")", tree_fn)
    tree_fn = re.sub("e-\d+,", ",", tree_fn)
    tree_fn = re.sub(":[\d\.]+\)", ")", tree_fn)
    tree_fn = re.sub(":[\d\.]+,", ",", tree_fn)
    #print()
    #### Delete BS values
    tree_fn = re.sub("\)\d+\)", "))", tree_fn)
    tree_fn = re.sub("\)\d+\)", "))", tree_fn)
    tree_fn = re.sub("\)\d+,", "),", tree_fn)
    tree_fn = re.sub("\)\d+;", ");", tree_fn)
    #print(tree_fn)
    #exit()
    #### Delete comman and parenthass
    tree_fn = re.sub("[\)\(]+", ",", tree_fn)
    tree_fn = re.sub(",+", ",", tree_fn)
    tree_fn = re.sub("^,", "", tree_fn)
    tree_fn = re.sub(",;", "", tree_fn)
    #print(tree_fn)
    #exit()
    leaves_list = tree_fn.split(",")
    return leaves_list


def reorder_seq_by_tree(recs_fn):
    #print("## reorder_seq_by_tree ##<br>")
    #print("recs_fn<br>")
    #for name, con, in recs_fn.items():
    #    print("name", name, "|<br>")
    #    #print("con", con, "|<br>")
    #    print("<br>")
    #exit()
    seqDict_ordered  = OrderedDict()
    f = open(eachDirAddress + "/" + "100_1stAnalysisSummary.txt")
    lines= list(f)
    f.close()
    flag = 0
    tree = ""
    
    for line in lines:
        if flag == 1:
            if line.startswith("("):
                tree = line
            else:
                break
        if line.startswith(">Gene_tree_newick"):
            flag = 1
            
    #print("tree", tree, "<br>")
    #exit()
    if tree:
        leaves_list = get_leaves(tree)
        for leaf in leaves_list:
            #print("leaf", leaf, "<br><br>")
            if ">" + leaf in recs_fn.keys():
                #print("Found <br>")
                pass
            else:
                print("Error: Leaf name, |", leaf, "|, cannot be found in recs_fn.keys().<br><br>")
                print("recs_fn.keys()<br>")
                for name_rec in recs_fn.keys():
                    print("name_rec|", name_rec, "|<br>")
                print("<br><br>")
                print("tree:", tree, "<br>")
                exit()
            seqDict_ordered[">" + leaf] = recs_fn[">" + leaf]
        #exit()
        return seqDict_ordered
    else:
        return recs_fn


def make_resHTMLfile(infile, queryFile, outfile):
    oneLineLength = 90         ## For cDNA, needs to be a multiple of 3
    recs = readFasta_dict(eachDirAddress + "/", infile)
    recs = reorder_seq_by_tree(recs)
    #yourRecName, yourRecSequence = firstSpeciesPicker(recs)
    recs = addSiteNotes("030_trimalOut.fas.trm.html", recs)
    #for name, sec in recs.items():
    #    print(name + "<br>")
    #    print(sec + "<br>")
    recs = whiteSpaceAdd(recs)
    #recs = add_NCBI_link(recs)
    lines = interleavedMake(oneLineLength, recs)
    htmlFileMake(lines, queryFile, outfile)


def compression():

    resDirName = eachDirAddress + "result" + str(num_dir)
    os.mkdir (resDirName)
    if os.path.isfile(eachDirAddress + "115_tree_rooted.pdf"):
        shutil.copy(eachDirAddress + "115_tree_rooted.pdf", resDirName)
        shutil.copy(eachDirAddress + "115_tree_rooted.png", resDirName)
        shutil.copy(eachDirAddress + "115_tree_rooted_noBranchLengths.pdf", resDirName)
    #if os.path.isfile(eachDirAddress + "115_tree_unrooted.pdf"):
    #    shutil.copy(eachDirAddress + "115_tree_unrooted.png", resDirName)
    #    shutil.copy(eachDirAddress + "115_tree_unrooted.pdf", resDirName)
    #    shutil.copy(eachDirAddress + "115_tree_unrooted.png", resDirName)
    #    #shutil.copy(eachDirAddress + "115_tree_unrooted_noBranchLengths.pdf", resDirName)

    if os.path.isfile(eachDirAddress + "210_aln_nucl.html"):
        shutil.copy(eachDirAddress + "210_aln_nucl.html", resDirName + "/000_results.html")

    if os.path.isfile(eachDirAddress + "130_mafOut_tree_order.txt"):
        shutil.copy(eachDirAddress + "130_mafOut_tree_order.txt", resDirName + "/020_alignment.txt")
        #shutil.copy(eachDirAddress + "140_uploadSeqs_tree_order.txt", resDirName + "/000_uploadedSeqs_treeOrder.txt")

    if os.path.isfile(eachDirAddress + "000_uploaded_anonSeqs.txt"):
        shutil.copy(eachDirAddress + "000_uploaded_anonSeqs.txt", resDirName + "/010_anonymousSeqs.txt")

    if os.path.isfile(eachDirAddress + "085_NJBS1st.txt"):
        shutil.copy(eachDirAddress + "085_NJBS1st.txt", resDirName + "/020_tree.txt")
    if os.path.isfile(eachDirAddress + "000_uploaded_userDB.txt"):
        shutil.copy(eachDirAddress + "000_uploaded_userDB.txt", resDirName + "/000_uploadedUserREFseqs.txt")
    #if os.path.isfile(eachDirAddress + "seq_selected.html"):
    #    shutil.copy(eachDirAddress + "seq_selected.html", resDirName + "/result" + num_dir + "_phyloBARCODER_seqs.html")
    if mode_select == "mode_B" and os.path.isfile(eachDirAddress + "seq_selected.html"):
        shutil.copy(eachDirAddress + "seq_selected.html", resDirName + "/seq_selected.html")

    if mode_select == "mode_B":
        pass
    elif num_queries == "NoBlastSearch":
        pass
    elif blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
        pass
    else:
        shutil.copy(eachDirAddress + "100_taxon_assignment_tree.txt", resDirName + "/030_taxon_assignment.csv")
        #shutil.copy(eachDirAddress + "100_taxon_assignment_blast.txt", resDirName + "/030_taxon_assignment_blastHits.txt")

    # by zip with glob in html directory
    zipfiles = glob.glob(resDirName + '/*')
    fzip = zipfile.ZipFile(resDirName + '_phyloBARCODER.zip', 'w', zipfile.ZIP_DEFLATED)
    for file in zipfiles:
        fzip.write(file, os.path.basename(file))
    fzip.close()


def change_resHTMLfile(infile200, outfile210):
    f = open(eachDirAddress + infile200)
    lines = list(f)
    out = open(eachDirAddress + "/" + outfile210, "w")
    for line in lines:
        line = line.rstrip("\n")
        #if re.search("Download:", line) or re.search("Phylogenetic tree", line) or re.search("115_1stGeneTree.png", line):
        if re.search("Download:", line):
            continue
        else:
            out.write(line + "\n")
    out.close()


def orderedDict2phyFile(recs, outfile):
    secLength     = len(sorted(recs.values())[0])
    spSeqSizeLine = str(len(recs)) + " " + str(secLength)

    recs = whiteSpaceAdd(recs)
    out = open(eachDirAddress + outfile, "w")
    out.write(spSeqSizeLine + "\n")
    for name,value in recs.items():
        out.write(name + value + "\n")
    out.close()

def fas2phy(fastaFileName, outPhyFileName):
    recs = readFasta_dict(eachDirAddress,fastaFileName)
    orderedDict2phyFile(recs, outfile = outPhyFileName)
    num_OTUs = len(recs)
    len_sequence = len(list(recs.values())[0])
    #print("num_OTUs", num_OTUs)
    return num_OTUs * len_sequence

def fas_reorder_by_tree(inFileName, outFileName):
    #print("### fas_reorder_by_tree ###<br>")
    #print("inFileName", inFileName, "<br>")
    recs = readFasta_dict(eachDirAddress, inFileName)
    recs = reorder_seq_by_tree(recs)

    out = open(eachDirAddress + outFileName, "w")
    for name, value in recs.items():
        out.write(name + "\n")
        out.write(value + "\n")
    out.close()

    num_OTUs = len(recs)
    len_sequence = len(list(recs.values())[0])
    #print("num_OTUs", num_OTUs)
    return num_OTUs * len_sequence

def save_uploadSeqs(inFileName, outFileName):
    recs = readFasta_dict(eachDirAddress, inFileName)

    out = open(eachDirAddress + outFileName, "w")
    for name, seqs in recs.items():
        if name.startswith(">ANON"):
            name = re.sub(">ANON\d+_", ">", name)
            out.write(name + "\n")
            seqs = re.sub("-", "", seqs)
            out.write(seqs + "\n")
    out.close()

def complex_kewWordSearch():
    #print("outFileNamefn", outFileNamefn)
    #exit()

    num_keywordHit = search_keyword()

    if num_keywordHit:
        htmlAddress = '<br>Finished: <a href="../phylobarcoderWork/' + str(dirname_rand) + '/seq_selected.html" target="_blank">' + str(dirname_rand) + '</a><br><br>'
        #print("outFileNamefn:" + outFileNamefn + "|<br>")
        elapsed_time = round((time.time() - startTime),1)
        print ("Analysis time: {0}".format(elapsed_time) + " seconds")
        print(htmlAddress)
    else:
        print("No hit for: " + text_area_keyword_modeB)
    
    compression()


def search_keyword():

    database_selected_fn = ""
    if database_modeB == "Long_MIDORI":
        database_selected_fn = database_species
    else:
        database_selected_fn = database_haplotype
    
    #print("database_selected_fn", database_selected_fn, "<br>")
    #exit()
    #print("gene_modeB", gene_modeB, "<br>")
    #print("taxon_rank_modeB", taxon_rank_modeB, "<br>")
    #print("text_area_keyword_modeB", text_area_keyword_modeB, "<br>")
    #exit()
    recs_OD = readFasta_dict("", database_selected_fn)
    #print("recs_OD", len(recs_OD))
    #exit()
    recs_OD_selected = OrderedDict()
    for name, seq in recs_OD.items():
        #if taxon_rank_modeB == "genus_name":
        keyLine = "^>ref\|" + gene_modeB + "\..*_" + text_area_keyword_modeB + "_"
        #print("keyLine", keyLine)
        #exit()
        if re.search(keyLine, name):
                recs_OD_selected[name] = seq

    num_keywordHit = len(recs_OD_selected)
    #print("eachDirAddress", eachDirAddress, "<br>")
    #exit()
    if num_keywordHit == 0:
        print("NONE")
    else:
        recs_OD_selected_mod = add_NCBIacc_nameline(recs_OD_selected)
        #recs_OD_selected_mod = recs_OD_selected

        out = open(eachDirAddress + "seq_selected.html", "w")
        
        out.write(top_html)

        out.write("\n")
        out.write("Download:")
        out.write('<a href="result'+ num_dir +'_phyloBARCODER.zip">result' + num_dir + '_phyloBARCODER.zip</a>\n')
        out.write("\n")


        if database_modeB == "Long_MIDORI":
            out.write("### Database:       " + database_modeB + "(species) \n")
        else:
            out.write("### Database:       " + database_modeB + "(haplotype) \n")
        out.write("### Gene:           " + gene_modeB + "\n")
        out.write("### Taxonomic name: " + text_area_keyword_modeB + "\n")
        if database_modeB == "Long_MIDORI":
            out.write("### Hits:           " + str(num_keywordHit) + " species\n")
        else:
            out.write("### Hits:           " + str(num_keywordHit) + " haplotypes\n")
        out.write("\n")

        for name, seq in recs_OD_selected_mod.items():
            out.write(name + "\n")
            out.write(seq + "\n")
        out.write(bottom_html)

        out.close()

    return num_keywordHit


def add_NCBIacc_nameline(recs_OD_selected):
    recs_OD_selected_mod = OrderedDict()
    for name, seq in recs_OD_selected.items():
        recs = name.split(";")
        #print("recs", recs)
        number_accession = recs[0]
        #print("number_accession", number_accession, "<br>")
        number_accession = re.sub("\| .[^\|]+$", "", number_accession)
        #print("number_accession", number_accession, "<br>")
        #number_accession = re.sub(r'\| ([^\.]+)\.', r'| <a href="https://www.ncbi.nlm.nih.gov/nuccore/\1" target="_blank">\1</a>.', number_accession)
        number_accession = re.sub(r'\|([^\.]+)\.([^\.]+)\.', r'|\1.<a href="https://www.ncbi.nlm.nih.gov/nuccore/\2" target="_blank">\2</a>.', number_accession)
        #print("number_accession", number_accession, "<br>")
        #exit()
        number_accession = re.sub(r"<(\d\.)>", r"\1", number_accession)
        #print("number_accession", number_accession)
        #exit()
        
        name_species = recs[-1]
        #print("name_species", name_species, "<br>")
        #print("name_species", name_species, "<br>")
        name_species = re.sub("^[^_]+_", "", name_species)
        name_species = re.sub("_[^_]+$", "", name_species)
        #print("name_species", name_species, "<br>")
        
        nameLine_mod = number_accession + "_" + name_species
        nameLine_mod = re.sub("\|", "_", nameLine_mod)
        
        recs_OD_selected_mod[nameLine_mod] = seq

    return recs_OD_selected_mod


##################### Tree START #####################
def taxonAssignment_from_tree(allNodes_decrement, outfile):
    #print("#### taxonAssignment_from_tree ####<br>")
    #exit()

    #list_leaves_all = allNodes_decrement[0][2]
    f = open(eachDirAddress + "085_NJBS1st.txt")
    treeFN = list(f)[0]
    f.close

    list_leaves_all = get_leaves(treeFN)

    #print("list_leaves_all", list_leaves_all)
    
    list_queryLeaves = []
    for leaf in list_leaves_all:
        #print("leaf", leaf, "<br>")
        if leaf.startswith("ANON"):
            match = re.search("ANON(\d+)_", leaf)
            number = match.group(1)
            list_queryLeaves.append([int(number), leaf])
    #list_queryLeaves = sorted(list_queryLeaves, key=lambda x: x[1])

    fh = open(eachDirAddress + outfile, "w")
    #fh.write("Num_UPLOAD\tUploadedName\tSpecies\tGenus\tMiddle_grouping\tLarge_grouping\n")    
    fh.write("Num_UPLOAD,UploadedName,Species,Genus,Middle_grouping,Large_grouping\n")    
    for queryLeaf_TMP in list_queryLeaves:
        queryLeaf = queryLeaf_TMP[1]
        #print("queryLeaf", queryLeaf, "<br>")

        #queryLeaf = "YOURSEQ1"
    
        speciesNode = speciesNodeIdentify(allNodes_decrement, queryLeaf)
        sister_leaves = sisterLeafIdentify(allNodes_decrement, speciesNode)
        
        #print("sister_leaves", sister_leaves)
        
        #cousin_leaves = ""
        #parentalNode = ""
        if sister_leaves:
            cousin_leaves, cousin_node_TMP = cousinLeafIdentify(allNodes_decrement, speciesNode)
            #parentalNode = parentNodeIdentify(allNodes_decrement, speciesNode)
        else:
            sister_leaves, cousin_node = cousinLeafIdentify(allNodes_decrement, speciesNode)
            #cousin_leaves, cousin_node_TMP = cousinLeafIdentify(allNodes_decrement, cousin_node)
            #parentalNode = parentNodeIdentify(allNodes_decrement, cousin_node)
            #if not sister_leaves:
            #    print("No sister_leaves")
        
        
        #print("## sister_leaves")
        #for leaf in sister_leaves:
        #    print(leaf)
        #print("## cousin_leaves")
        #for leaf in cousin_leaves:
        #    print(leaf)
        
        #print("######################")
        #combined_leaves = sister_leaves + cousin_leaves
        combined_leaves = sister_leaves
        line_large_taxon, line_middle_taxon, line_genus_taxon, line_species_taxon = taxon_assignment(combined_leaves)
        #print("Large grouping:  ", line_large_taxon)
        #print("Middle grouping: ", line_middle_taxon)
        #print("Genus:           ", line_genus_taxon)
        #print("Species:         ", line_species_taxon)    
        #exit()

        #parentalNode_bs = parentalNode[0]

        #fh.write(queryLeaf + "\tNA\t" + line_large_taxon + "\t" + line_middle_taxon + "\t" + line_genus_taxon + "\t" + line_species_taxon + "\n")

        match = re.search("(ANON\d+)_(.*$)", queryLeaf)
        Num_UPLOAD = match.group(1)
        UploadedName = match.group(2)
        #fh.write(Num_UPLOAD + "\t" + UploadedName + "\t" + line_species_taxon + "\t" + line_genus_taxon + "\t" + line_middle_taxon + "\t" + line_large_taxon + "\n")
        fh.write(Num_UPLOAD + "," + UploadedName + "," + line_species_taxon + "," + line_genus_taxon + "," + line_middle_taxon + "," + line_large_taxon + "\n")

    fh.close()


def nodesCollectFromNewick(tree_file):

    f = open(eachDirAddress + tree_file)
    treeFN = list(f)[0]
    f.close

    treeFN = treeFN.rstrip("\n")
    treeFN = re.sub(":-", ":", treeFN)
    treeFN = re.sub("e-\d+\)", ")", treeFN)
    treeFN = re.sub("e-\d+,", ",", treeFN)
    treeFN = re.sub(":[\d\.]+\)", ")", treeFN)
    treeFN = re.sub(":[\d\.]+,", ",", treeFN)
    
    #print(treeFN)
    #exit()

    nodes = []     # 2D array for nodes
    if int(num_bootstrap) > 0:
        nodeReg = "\(([^\(\)]+)\)([^\),]+)"
        while re.search(nodeReg, treeFN):
            treeFN = treeFN.rstrip("\n")
            match = re.search(nodeReg, treeFN)     # Pick up the smallest and leftmost node for the following analysis
            leavesString = match.group(1)
            BSvalue = match.group(2)
            leaves = set(leavesString.split(","))
            #print("len(leaves):", len(leaves))
            #print("BSvalue:", BSvalue)
            #for leaf in leaves:
            #    print("leaf:", leaf)
            #print()
            #exit()
            treeFN = re.sub(nodeReg, r"\1", treeFN, 1)  # Delete the outer parentheses from the analyzed node
            nodes.append([BSvalue, len(leaves), leaves])
    else:
        nodeReg = "\(([^\(\)]+)\)"
        while re.search(nodeReg, treeFN):
            treeFN = treeFN.rstrip("\n")
            match = re.search(nodeReg, treeFN)     # Pick up the smallest and leftmost node for the following analysis
            leavesString = match.group(1)
            leaves = set(leavesString.split(","))
            #print("len(leaves):", len(leaves))
            #print("BSvalue:", BSvalue)
            #for leaf in leaves:
            #    print("leaf:", leaf)
            #print()
            #exit()
            treeFN = re.sub(nodeReg, r"\1", treeFN, 1)  # Delete the outer parentheses from the analyzed node
            nodes.append([1, len(leaves), leaves])
    #exit()

    sortedNodes = sorted(nodes, key=lambda x:x[1], reverse=True)

    ### Attache clade numbers at list position 0
    #count = 1
    #for node in sortedNodes:
    #    node.insert(0, count)
    #    count += 1
    #for node in sortedNodes:
    #    print("node", node, "<br>")
    #exit()

    ## Add spacies node (leaf) as a node
    largestNode = sortedNodes[0];
    #print("largestNode", largestNode)
    #exit()
    Leaves_all = largestNode[2]
    Leaves_all = sorted(Leaves_all)
    for leaf in Leaves_all:
        #print ("leaf:", leaf)
        match = re.search(r"([^_]+)_", leaf)
        BSvlue = 0
        tempLeafNode = {leaf}
        #sortedNodes.append([BSvlue, count, 1, tempLeafNode])
        sortedNodes.append([BSvlue, 1, tempLeafNode])
        #count += 1

    return sortedNodes

def speciesNodeIdentify(allNodes_decrement, queryLeaf_fn):
    speciesNode = []
    for node in allNodes_decrement:
        #if node[1] == 1 and re.search(queryLeaf_fn + "_", list(node[2])[0]):
        if node[1] == 1 and queryLeaf_fn == list(node[2])[0]:
            speciesNode = node
    if not speciesNode:
        print ("Stopped. No speciesNode was found for ", queryLeaf_fn)
        exit()
    return speciesNode

def sisterLeafIdentify(allNodes_decrement, node_focal):
    #print("############ cousinNodeIdentify ##########")
    sisterNode_FN = sisterNodeIdentify(allNodes_decrement, node_focal)
    sister_leaves_FN = []
    if sisterNode_FN:
        sister_leaves_FN = get_speciesNode_from_leaves(sisterNode_FN)
    return sister_leaves_FN

def sisterNodeIdentify(allNodes_decrement, node_focal):
    sisterNode_FN = []

    #print("sisterNodeIdentify")
    #print("node_focal", node_focal)
    parentNode_focal = parentNodeIdentify(allNodes_decrement, node_focal)

    if not parentNode_focal:
        #print("XXXXX")
        return sisterNode_FN

    childNodes_decrement = childNodesCollect(allNodes_decrement, parentNode_focal)
    #print("ignore_start_word", ignore_start_word)
    #exit()
    daughterNode2ndSR = ""
    leaves_node_focal = node_focal[2]
    for eachChildNode in childNodes_decrement:
        #print("eachChildNode[2]", eachChildNode[2])
        leaves_eachChildNode = eachChildNode[2]
        #print()
        #exit()
        #continue
        if isIndependent(leaves_eachChildNode, leaves_node_focal):
            sisterNode_FN = eachChildNode;
            break

    return sisterNode_FN

def parentNodeIdentify(allNodes_decrement, node_focal):
    #print("parentNodeIdentify")
    #print("node_focal", node_focal)
    #exit()
    ancestralNodes_decrement_fn = ancestralNodesCollect(allNodes_decrement, node_focal)
    #print("#### ancestralNodes_decrement_fn")
    parentalNode_FN = "";
    if len(ancestralNodes_decrement_fn) > 0:
        parentalNode_FN = ancestralNodes_decrement_fn[-1]
    return parentalNode_FN

def ancestralNodesCollect(allNodes_decrement, node_focal):
    #print("ancestralNodesCollect START")
    #print("node_focal", node_focal)
    ancestralNodes_decrement = []
    for eachNode in allNodes_decrement:
        #print("eachNode[2]", eachNode[2])
        if node_focal == eachNode:
            #print("node_focal == eachNode")
            continue
        elif node_focal[2].issubset(eachNode[2]):
            ancestralNodes_decrement.append(eachNode)
        #print()
    #print("@@@@ancestralNodes_decrement")
    #for node in ancestralNodes_decrement:
    #    print(node)
    ##print("ancestralNodesCollect END")
    #exit()
    return ancestralNodes_decrement

def childNodesCollect(allNodes_decrement, node_focal):
    childNodes = []
    for eachNode in allNodes_decrement:
        if eachNode == node_focal:
            continue
        if eachNode[2].issubset(node_focal[2]):
            childNodes.append(eachNode)
    return childNodes;

def isIndependent(checkNodeLeave, focalNodeLeave):
    for ckeckNodeLeaf in checkNodeLeave:
        if [focalNodeLeaf for focalNodeLeaf in focalNodeLeave if re.search(ckeckNodeLeaf, focalNodeLeaf)]:
            return 0;
    return 1;

def get_speciesNode_from_leaves(node_focal):
    #print("get_speciesNode_from_leaves")
    speciesNode_FN = ""
    leavesTMP = list(node_focal[2])
    leavesTMP2 = []
    for leaf in leavesTMP:
        if not re.search("^" + ignore_start_word + "\d+_", leaf):
            leavesTMP2.append(leaf)
    #if leavesTMP2:
    #    leaves = sorted(leavesTMP2)
    #    speciesNode_FN = leaves[0]
    return leavesTMP2

def cousinLeafIdentify(allNodes_decrement, node_focal):
    #print("############ cousinNodeIdentify ##########")
    cousin_node_fn = cousinNodeIdentify(allNodes_decrement,node_focal)
    #if cousinNode:
    #    print ("cousinNode:")
    #    print ("  Node name:#", cousinNode[0])
    #    print ("  BS value", cousinNode[-1])
    ##    print ("  Num of leaves:", len(cousinNode[2]))
    #    print ("  Leaves:", cousinNode[2])
    #    print ()

    cousin_leaf_FN = ""
    if cousin_node_fn:
        cousin_leaf_FN = get_speciesNode_from_leaves(cousin_node_fn)
        if not (cousin_leaf_FN):
            return cousin_leaf_FN

    return cousin_leaf_FN, cousin_node_fn

def cousinNodeIdentify(allNodes_decrement, node_focal):
    #print("cousinNodeIdentify")
    #print("node_focal", node_focal)
    #exit()
    #print()
    cousinNode_FN =[]
    ancestralNodes_decrement_fn = ancestralNodesCollect(allNodes_decrement, node_focal)
    ancestralNodes_increment_fn = sorted(ancestralNodes_decrement_fn, key=lambda x:x[1], reverse=False)
    #print("@@@ ancestralNodes_increment_fn")
    for eachNode in ancestralNodes_increment_fn:
        #print("eachNode", eachNode)
        cousinNode_FN = sisterNodeIdentify(allNodes_decrement, eachNode)
        #print("cousinNode_FN1", cousinNode_FN)
        if not cousinNode_FN:
            return cousinNode_FN
        num_nonignore_leaves = check_non_UPLOAD_leaves(cousinNode_FN)
        #print("num_nonignore_leaves", num_nonignore_leaves)
        #exit()
        if num_nonignore_leaves > 0:
            #print("cousinNode_FN > 0", cousinNode_FN)
            return cousinNode_FN
            #exit()
        #else:
        #    print("cousinNode_FN = 0", cousinNode_FN)
        #print()
    #print()
    #exit()
    return cousinNode_FN

def check_non_UPLOAD_leaves(node_focal):
    #print("check_non_YOURSEQ_leaves")
    num_non_UPLOAD_leaves = 0
    leaves_node_focal = node_focal[2]
    for leaf in leaves_node_focal:
        if not re.search("^" + ignore_start_word + "\d+_", leaf):
            num_non_UPLOAD_leaves += 1
    return num_non_UPLOAD_leaves

def taxon_assignment(leaves_FN):
    #print("### taxon_assignment START ###")
    #for leaf in leaves_FN:
    #    print(leaf)
    #exit()
    dic_large_taxon_FN = {}
    dic_middle_taxon_FN = {}
    dic_genus_taxon_FN = {}
    dic_species_taxon_FN = {}
    for leaf in leaves_FN:
        #print("leaf", leaf, "<br><br>")
        if leaf.startswith("USERDB"):
            continue
        leaf = re.sub("_[^_]+$", "", leaf)
        gene_ID_TMP, gene_name_TMP, large_taxon_FN, middle_taxon_FN, species_taxon_TMP_FN = leaf.split("_")
        #print("species_taxon_TMP_FN", species_taxon_TMP_FN)
        
        genus_taxon_FN = "NONE"
        if re.search("^([^-]+)-(.*)$", species_taxon_TMP_FN):
            match = re.search("^([^-]+)-(.*)$", species_taxon_TMP_FN)
            genus_taxon_FN = match.group(1)
        #species_taxon_FN = match.group(2)
        #print("dic_genus_taxon_FN", dic_genus_taxon_FN)
        #print("species_taxon_FN", species_taxon_FN)
        #exit()

        dic_large_taxon_FN[large_taxon_FN] = 1
        dic_middle_taxon_FN[middle_taxon_FN] = 1
        dic_genus_taxon_FN[genus_taxon_FN] = 1
        dic_species_taxon_FN[species_taxon_TMP_FN] = 1
        
        #print("END\n")
    
    line_large_taxon_FN = make_line(dic_large_taxon_FN)
    line_middle_taxon_FN = make_line(dic_middle_taxon_FN)
    line_genus_taxon_FN = make_line(dic_genus_taxon_FN)
    line_species_taxon_FN = make_line(dic_species_taxon_FN)
    
    #print("### taxon_assignment END ###")

    return line_large_taxon_FN, line_middle_taxon_FN, line_genus_taxon_FN, line_species_taxon_FN


def make_line(dic_fn):
    line_FN = ""
    
    if len(dic_fn) == 1:
        line_FN = list(dic_fn.keys())[0]
        return line_FN
    
    list_fn = dic_fn.keys()
    list_fn = sorted(list_fn)

    for name in list_fn:
        #print(name)
        if name == "NONE":
            continue
        line_FN += name + "/"
    line_FN = re.sub("/$", "", line_FN)
    print()
    return line_FN



##################### Taxon assignment #####################

def make_taxonAssignmentFile_from_tree(treeFile, outfile_assign_tree):
    #print("## make_taxonAssignmentFile_from_tree ##<br>")
    #exit()
    #print("treeFile", treeFile,"<br>")
    #print("outfile_assign_tree", outfile_assign_tree,"<br>")
    pathTMP = eachDirAddress + treeFile
    #print("pathTMP", pathTMP, "<br>")
    #exit()
    if os.path.isfile(pathTMP):
        #print("tree file exists<br>")
        #exit()
        allNodes_decrement = nodesCollectFromNewick(treeFile)
        #print("allNodes_decrement", allNodes_decrement, "<br>")
        taxonAssignment_from_tree(allNodes_decrement, outfile = outfile_assign_tree)
    else:
        #print("no tree file<br>")
        #exit()
        fh = open(eachDirAddress + outfile_assign_tree, "w")
        fh.write("No_tree_estimated\n")
        fh.close()

def make_recs_query_blasttophit(recs_blastnRes_fn):
    recs_query_blasttophit_fn = OrderedDict()
    for rec in  recs_blastnRes_fn:
        #print("rec", rec, "<br>")
        database = rec[0]
        query = rec[1]
        #print("database", database, "<br>")
        #print("query", query, "<br><br>")
        #print("")
        if not database.startswith("Database: MIDORI"):
            continue
        if not query in list(recs_query_blasttophit_fn.keys()):
            recs_query_blasttophit_fn[query] = rec
    return recs_query_blasttophit_fn

def make_recs_query_blastAllhit_for_UPLOAD1(recs_blastnRes_fn):
    recs_query_blastAllhit_fn = []
    for rec in  recs_blastnRes_fn:
        #print("rec", rec, "<br>")
        database = rec[0]
        query = rec[1]
        blastHit = rec[2]
        #print("database", database, "<br>")
        #print("query", query, "<br>")
        #print("rec", rec, "<br><br>")
        #print("")
        if query.startswith("Query= UPLOAD1_"):
            recs_query_blastAllhit_fn.append(rec)
    return recs_query_blastAllhit_fn


def add_recs_blastout_sequenceID(filename_blastout):
    #print("### add_recs_blastout_sequenceID ####<br>")
    #print("filename_blastout", filename_blastout, "<br>")

    recs_blastnRes = read_blastnRes2(filename_blastout)
    recs_blastout_sequenceID = []
    for rec in  recs_blastnRes:
        #for rec in recs:
        #    print("rec", rec, "<br>")
        #exit()
        database = rec[0]
        query = rec[1]
        blastHit = rec[2]
        length = rec[3]
        score = rec[4]
        identity = rec[5]
        strand = rec[6]
        position = rec[7]
        #print("database", database, "<br>")
        #print("query", query, "<br>")
        #print("blastHit", blastHit, "<br>")
        #print("length", length, "<br>")
        #print("score", score, "<br>")
        #print("identity", identity, "<br>")
        #print("strand", strand, "<br>")
        #print("position", position, "<br>")

        #print("blastHit", blastHit, "<br>")

        sequenceID = ""
        if blastHit.startswith(">ANON") or blastHit.startswith(">USERDB") :
            match = re.search("^>([^_]+)_", blastHit)
            sequenceID = match.group(1)
            #print("sequenceID", sequenceID, "<br><br>")
        else:
            match = re.search("^>[^\.]+\.([^\.]+\.\d+)\.", blastHit)
            sequenceID = match.group(1)
            #print("sequenceID", sequenceID, "<br><br>")
            #exit()
        recs_blastout_sequenceID.append([database, query, blastHit, length, score, identity, strand, position, sequenceID])
    return recs_blastout_sequenceID


def choose_recs_blastout_ANON1(recs_blastout):
    #print("#### choose_recs_blastout_ANON1 ####<br>")
    recs_blastout_ANON1 = []
    for rec in  recs_blastout:
        #for rec in recs:
        #    print("rec", rec, "<br>")
        #exit()
        database = rec[0]
        query = rec[1]
        blastHit = rec[2]
        length = rec[3]
        score = rec[4]
        identity = rec[5]
        strand = rec[6]
        position = rec[7]
        #print("database", database, "<br>")
        #print("query", query, "<br>")
        #print("blastHit", blastHit, "<br>")
        #print("length", length, "<br>")
        #print("score", score, "<br>")
        #print("identity", identity, "<br>")
        #print("strand", strand, "<br>")
        #print("position", position, "<br>")

        #print("blastHit", blastHit, "<br>")

        if query.startswith("Query= ANON1_"):
            recs_blastout_ANON1.append(rec)

    return recs_blastout_ANON1


def make_list_print_taxonomic_lines(list_modifiedNames_fn, recs_query_blasttophit_fn):

    list_print_taxonomic_lines_TMP = []
    for query, rec in recs_query_blasttophit_fn.items():
        #print("query", query, "<br>")
        #print("rec", rec, "<br><br>")
        query = re.sub("Query= ", "", query)

        nameline_blasttop = rec[2]
        
        if nameline_blasttop == ">***** No hits found *****":
            list_print_taxonomic_lines_TMP.append(query + "\tno_hits_found")
        else: 
            nameline_blasttop = re.sub(" .*$", "", nameline_blasttop)
            #print("nameline_blasttop1", nameline_blasttop)  ## >SRRNA.AB032554.1.14397
            nameline_blasttop_keyword = re.sub(">([^\.]+)\.([^\.]+\.\d+)\.\d+", r">\2_\1_", nameline_blasttop)
            #print("nameline_blasttop_keyword", nameline_blasttop_keyword)  ## >SRRNA.AB032554.1.14397
            #exit()

            identityTMP = rec[5]
            #print(identityTMP)
            identity = identityTMP
            identity = re.sub("\).*$", "", identity)
            identity = re.sub("^.*\(", "", identity)
    
            #for line in list_modifiedNames_fn:
            #    print(line)
            #exit()
    
            for modifiedNameLine in list_modifiedNames_fn:
                #print("modifiedNameLine", modifiedNameLine)
                #continue
                #exit()
                name_blastTopHit = "NONE"
                if re.search(nameline_blasttop_keyword, modifiedNameLine):
                    name_blastTopHit = modifiedNameLine
                    #print("nameline_blasttop_keyword", nameline_blasttop_keyword)
                    #print("name_blastTopHit", name_blastTopHit)
                    #exit()
                    line_large_taxon, line_middle_taxon, line_genus_taxon, line_species_taxon = taxon_assignment([name_blastTopHit])
                    #print()
                    #print(queryTMP + "\t" + identity + "\t"+ line_large_taxon + "\t" + line_middle_taxon + "\t" + line_genus_taxon + "\t" + line_species_taxon)
                    list_print_taxonomic_lines_TMP.append(query + "\t" + identity + "\t"+ line_large_taxon + "\t" + line_middle_taxon + "\t" + line_genus_taxon + "\t" + line_species_taxon)
                    break

    #exit()
    return list_print_taxonomic_lines_TMP



def add_nameline_identities(recs_blastout, fastafile, outfile):
    #print("## add_nameline_identities ##<br>")
    #print("recs_blastout", recs_blastout, "<br>")
    #exit()
    #print("outfile", outfile, "<br>")

    recs_fastafile = readFasta_dict(eachDirAddress, fastafile)

    recs_fastafile_identity = OrderedDict()
    for nameline_fasta, sequence in recs_fastafile.items():
        #print("nameline_fasta", nameline_fasta, "<br>")
        match = re.search("^>([^_]+)_", nameline_fasta)
        sequenceID_fasta = match.group(1)
        #print("sequenceID_fasta", sequenceID_fasta, "<br>")
        #exit()

        rec_sameSeqID = []
        for rec in recs_blastout:
            #database = rec[0]
            #query = rec[1]
            #query = re.sub("Query= ", "", query)
            #blasthit = rec[2]
            identyty = rec[5]
            sequenceID_blastout = rec[8]
            #print("sequenceID_blastout", sequenceID_blastout, "<br>")
            
            if sequenceID_fasta == sequenceID_blastout:
                #print("sequenceID_blastout", sequenceID_blastout, identyty, "<br>")
                rec_sameSeqID.append(rec)
        
        identity = ""
        if len(rec_sameSeqID):
            #print("Found<br>")
            #print("rec_sameSeqID", rec_sameSeqID, "<br>")
            identityTMP = rec_sameSeqID[0][5]
            match = re.search("Identities = \d+\/\d+ \((\d+%)\), Gaps = ", identityTMP)
            identity = match.group(1)
            #exit()
        #if len(rec_sameSeqID) > 1:
        #    print("rec_sameSeqID", rec_sameSeqID, "<br>")
        #    print("#### More than 2 same blast hits were found for UPLOAD1. Stopped. #####<br>")
        #    exit()
        else:
            #print("Not found<br>")
            identity = "BlueHit"

        #print("identity", identity, "<br>")
        nemalineNEW = nameline_fasta + "_" + identity
        #nemalineNEW = nameline_fasta
        #print("nemalineNEW", nemalineNEW, "<br>")
        recs_fastafile_identity[nemalineNEW] = sequence
        #print("<br><br>")

    #print("outfile name<br>")
    out = open(eachDirAddress + "/" + outfile, "w")
    for name, seq in recs_fastafile_identity.items():
        out.write(name + "\n")
        out.write(seq + "\n")
    out.close()
    #exit()


def reorder_by_treetopology(list_print_taxonomic_lines_fn, treefile):
    pathTMP = eachDirAddress + treefile
    if os.path.isfile(pathTMP):
        list_print_lines2_reordered_by_tree = []
        f = open(eachDirAddress + "085_NJBS1st.txt")
        treeFN = list(f)[0]
        f.close
        list_leaves_all = get_leaves(treeFN)
        for nameline_tree in list_leaves_all:
            #print("nameline_tree", nameline_tree, "<br>")
            if nameline_tree.startswith("ANON"):
                for line_assigned_res in list_print_taxonomic_lines_fn:
                    #print("line_assigned_res", line_assigned_res, "<br>")
                    if re.search(nameline_tree, line_assigned_res):
                        list_print_lines2_reordered_by_tree.append(line_assigned_res)
        return list_print_lines2_reordered_by_tree
    else:
        return list_print_taxonomic_lines_fn



#def make_taxonAssignment_from_blast(uploadedFile, blastRefFile, mafoutFile, outfile):
#    #print("### make_taxonAssignment_from_blast ###<br>")
#    #print("blastRefFile", blastRefFile, "<br>")
#    #print("eachDirAddress", eachDirAddress, "<br><br>")
#    #exit()
#    recs_blastnRes = read_blastnRes2(blastRefFile)
#    #print("recs_blastnRes", recs_blastnRes, "<br><br>")
#    #exit()
#
#    #recs_query_blasttophit = make_recs_query_blasttophit(recs_blastnRes)
#    recs_query_blastAllhit_for_UPLOAD1 = make_recs_query_blastAllhit_for_UPLOAD1(recs_blastnRes)
#    #print("#### recs_query_blastAllhit<br><br>")
#    #for name, recs in recs_query_blastAllhit_for_UPLOAD1.items():
#    #    print("name", name, "<br>")
#    #    print("recs1", recs, "<br><br>")
#    #print("#### recs_query_blasttophit<br><br>")
#    #for name, recs in recs_query_blasttophit.items():
#    #    print("name", name, "<br>")
#    #    print("recs", recs, "<br><br>")
#    #exit()
#
#    recs_mafoutFile = readFasta_dict(eachDirAddress, mafoutFile)
#    #for name, seq in recs_mafoutFile.items():
#    #    print("name", name, "<br>")
#    #    print("seq", seq, "<br>")
#    #exit()
#    #list_mafftOut_modifiedNames = recs_mafoutFile.keys()
#    #for line in list_mafftOut_modifiedNames:
#    #    print("line", line, "<br><br>")
#    #exit()
#
#    #list_print_taxonomic_lines = make_list_print_taxonomic_lines(list_mafftOut_modifiedNames, recs_query_blasttophit)
#    list_print_taxonomic_lines = make_list_print_taxonomic_lines_for_allBlastHits(list_mafftOut_modifiedNames, recs_query_blastAllhit_for_UPLOAD1)
#    #for line in list_print_taxonomic_lines:
#    #    print("line", line, "<br><br>")
#    #exit()
#
#    list_print_lines2 = reorder_by_treetopology(list_print_taxonomic_lines, "085_NJBS1st.txt")
#    #for line in list_print_lines2:
#    #    print(line)
#    #exit()
#
#    fh = open(eachDirAddress + outfile, "w")
#    fh.write("ANON\tidentity\tLarge grouping\tMiddle grouping\tGenus\tSpecies\tnameline\n") 
#    if list_print_lines2:
#        for line in list_print_lines2:
#            fh.write(line + "\n")
#    else:
#        for line in list_print_taxonomic_lines:
#            fh.write(line + "\n")
#    fh.close()





###############################################################
##################### Main program #####################

#'''##############################
#blastEvalue_midori = "1"  # 1e-3
#blastHits_speciesDB = "3"
#blastHits_haplotypeDB = "3"
#flankingSequence = 0
#word_size = "11"
#'''##############################



startTime = time.time()
dirName_count = makeCount()
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters_rand = ''.join([random.choice(letters) for _ in range(6)])

dirname_rand = dirName_count + "-" + letters_rand
#dirname_rand = "995-nKvMnm"   ## 18S
#dirname_rand = "1125-oTdKAB"  ## example


eachDirAddress = dirAddress + "phylobarcoderWork/" + str(dirname_rand) + "/"
num_dir = re.sub("-.*$", "", dirname_rand)

delete_dirs()

########################################################
########################################################
########################################################

mode_select, \
word_size, \
text_area_anonSeq, \
num_queries, \
blastHits_anonDB, \
blastEvalue_anonseq, \
release_MIDORI2DB, \
blastEvalue_midori, \
blastHits_speciesDB, \
blastHits_haplotypeDB, \
blastHits_userDB, \
blastEvalue_userDB,\
num_bootstrap, \
flankingSequence, \
database_modeB, \
gene_modeB, \
text_area_keyword_modeB \
= retrieave_topHTML_infor(cgi.FieldStorage())

database_address, \
database_species, \
database_haplotype, \
rscriptTMP \
= retrieave_databaseVariables(release_MIDORI2DB)



'''

#print("mode_select", mode_select, "<br>")
#print("blastHits_anonDB", blastHits_anonDB, "<br>")
#print("blastEvalue_anonseq", blastEvalue_anonseq, "<br>")
#print("word_size", word_size, "<br>")
##print("text_area_anonSeq", text_area_anonSeq, "<br>")
#print("num_queries", num_queries, "<br>")
#print("release_MIDORI2DB", release_MIDORI2DB, "<br>")
#exit()
#print("blastHits_speciesDB", blastHits_speciesDB, "<br>")
#print("blastHits_haplotypeDB", blastHits_haplotypeDB, "<br>")
#print("blastHits_userDB", blastHits_userDB, "<br>")
#print("blastEvalue_midori", blastEvalue_midori, "<br>")
#print("word_size", word_size, "<br>")
#print("flankingSequence", flankingSequence, "<br>")
#print("num_bootstrap", num_bootstrap, "<br>")
#print("database_modeB", database_modeB, "<br>")
#print("gene_modeB", gene_modeB, "<br>")
#print("text_area_keyword_modeB", text_area_keyword_modeB, "<br>")
#exit()

print("#### Now running only .phy script. ####")
mode_select = "mode_A"
blastHits_anonDB = "20"
blastEvalue_anonseq = "1e-3"
word_size_yourseq = ['11', '11'] 
num_queries = "First3seqs"
blastHits_speciesDB = "5"
blastHits_haplotypeDB = "10"
blastHits_userDB = "5" 
blastEvalue_midori = "1e-3"
word_size = "11"
text_area_anonSeq = "DAMMY"
flankingSequence = "0"
num_bootstrap = "100"
database_modeB = "Long_MIDORI "
gene_modeB = "srRNA"
text_area_keyword_modeB = ""
########################################################
########################################################
########################################################
'''



if mode_select == "mode_B":
    if not text_area_keyword_modeB:
        print("(B) Text area is empty.")
        exit()
    complex_kewWordSearch()
    exit()


####################### 
checkUploadFile(infileFN = "000_uploaded_anonSeqs.txt")
change_nameLine("000_uploaded_anonSeqs.txt", prefix=">ANON", out_namechanged_uploaded = "003_annonymousDB.txt")
if os.path.isfile(eachDirAddress + "000_uploaded_userDB.txt"):
    #print("000_uploaded_userDB.txt found.<br>")
    #exit()
    checkUploadFile(infileFN = "000_uploaded_userDB.txt")
    change_nameLine("000_uploaded_userDB.txt", prefix=">USERDB", out_namechanged_uploaded = "004_userDB.txt")
if num_queries == "NoBlastSearch":
    pass
elif blastHits_anonDB == "NotSelected" and blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
    #print("pass2")
    pass
else:
    make_querySequenceFile(inFileName = "003_annonymousDB.txt", outFileName = "005_querySequences.txt")


####################### BLAST: makeblastdb
if blastHits_anonDB != "NotSelected":
    conduct_makeblastdb(eachDirAddressFN=eachDirAddress, database_selected="003_annonymousDB.txt", outfileFN="003_annonymousDB.txt.n.scout.txt")
if os.path.isfile(eachDirAddress + "004_userDB.txt"):
    conduct_makeblastdb(eachDirAddressFN=eachDirAddress, database_selected="004_userDB.txt", outfileFN="004_userDB.txt.n.scout.txt")


####################### BLAST: blastn
#print("blastHits_anonDB", blastHits_anonDB, "<br>")
#print("blastHits_speciesDB", blastHits_speciesDB, "<br>")
#print("blastHits_haplotypeDB", blastHits_haplotypeDB, "<br>")
#print("blastHits_userDB", blastHits_userDB, "<br>")
#exit()
if num_queries == "NoBlastSearch":
    print("1 pass<br>")
    pass
elif blastHits_anonDB == "NotSelected" and blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
    print("2 pass<br>")
    pass
    #print("Select values at least one of WHOLE or PARTIAL<br>")
    #exit()
else:
    if blastHits_anonDB != "NotSelected":
        #print("blastHits_anonDB != NotSelected<br>")
        #exit()
        #print("Blast only for uploaded your seqs.<br>")
        #print('blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected"<br>')
        #print("eachDirAddress", eachDirAddress, "<br>")
        database_yourseq = eachDirAddress + "003_annonymousDB.txt"
        conduct_blastn(eachDirAddressFN=eachDirAddress, querieSequenceFile="005_querySequences.txt", database_selected=database_yourseq, num_alignments=blastHits_anonDB, outfile_blastn="010_blast_resut_uploadedDB.txt")
        #elapsed_time_yourseq_hits = round((time.time() - startTime),1)
        #print ("blastHits_anonDB analysis time: {0}".format(elapsed_time_yourseq_hits) + " seconds<br>")

    if blastHits_speciesDB != "NotSelected":
        #print("database_species", database_species, "<br>")
        conduct_blastn(eachDirAddressFN=eachDirAddress, querieSequenceFile="005_querySequences.txt", database_selected=database_species, num_alignments=blastHits_speciesDB, outfile_blastn="010_blast_resut_speciesDB.txt")
        #elapsed_time_species_hits = round((time.time() - startTime),1)
        #print ("blastHits_speciesDB analysis time: {0}".format(elapsed_time_species_hits) + " seconds<br>")

    if blastHits_haplotypeDB != "NotSelected":
        conduct_blastn(eachDirAddressFN=eachDirAddress, querieSequenceFile="005_querySequences.txt", database_selected=database_haplotype, num_alignments=blastHits_haplotypeDB, outfile_blastn="010_blast_resut_haplotypeDB.txt")
        #elapsed_time_haplotype_hits = round((time.time() - startTime),1)
        #print ("blastHits_haplotypeDB analysis time: {0}".format(elapsed_time_haplotype_hits) + " seconds<br>")

    if blastHits_userDB != "NotSelected":
        #print("blastHits_userDB != NotSelected<br>")
        #exit()
        database_yourRefSeq = eachDirAddress + "004_userDB.txt"
        conduct_blastn(eachDirAddressFN=eachDirAddress, querieSequenceFile="005_querySequences.txt", database_selected=database_yourRefSeq, num_alignments=blastHits_userDB, outfile_blastn="010_blast_resut_yourRefDB.txt")
        elapsed_time_yourref_hits = round((time.time() - startTime),1)
        #print ("blastHits_userDB analysis time: {0}".format(elapsed_time_yourref_hits) + " seconds<br>")
        #exit()


#print("## making 012_blast_resut_all.txt ##<br>")
out = open(eachDirAddress + "012_blast_resut_all.txt", "w")
out.write("")
out.close
#if os.path.isfile(eachDirAddress + "010_blast_resut_uploadedDB.txt"):
if blastHits_anonDB != "NotSelected":
    cat_line = "cat " + eachDirAddress + "010_blast_resut_uploadedDB.txt >> " + eachDirAddress + "012_blast_resut_all.txt"
    subprocess.call(cat_line, shell=True)
#if os.path.isfile(eachDirAddress + "010_blast_resut_haplotypeDB.txt"):
if blastHits_userDB != "NotSelected":
    cat_line = "cat " + eachDirAddress + "010_blast_resut_yourRefDB.txt >> " + eachDirAddress + "012_blast_resut_all.txt"
    subprocess.call(cat_line, shell=True)
if blastHits_haplotypeDB != "NotSelected":
    cat_line = "cat " + eachDirAddress + "010_blast_resut_haplotypeDB.txt >> " + eachDirAddress + "012_blast_resut_all.txt"
    subprocess.call(cat_line, shell=True)
#if os.path.isfile(eachDirAddress + "010_blast_resut_speciesDB.txt"):
if blastHits_speciesDB != "NotSelected":
    cat_line = "cat " + eachDirAddress + "010_blast_resut_speciesDB.txt >> " + eachDirAddress + "012_blast_resut_all.txt"
    subprocess.call(cat_line, shell=True)

#conduct_blastdbcmd(eachDirAddressFN=eachDirAddress, infile_blastres="010G_blast_resut.txt", database_selected=database_species, num_alignments=blastHits_speciesDB, outfileName= "012G_retrievedSequences.txt")
#conduct_blastdbcmd(eachDirAddressFN=eachDirAddress, infile_blastres="010P_blast_resut.txt", database_selected=database_haplotype, num_alignments=blastHits_haplotypeDB, outfileName= "012P_retrievedSequences.txt")
#combine_2retrievedSeqFiles(infileG = "012G_retrievedSequences.txt", infileP = "012P_retrievedSequences.txt", outfileName= "012retrievedSequences.txt")


####################### BLAST: blastdbcmd

if num_queries == "NoBlastSearch":
    pass
elif blastHits_anonDB == "NotSelected" and blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
    pass
else:
    #print("to read_blastnRes2<br>")
    #exit()
    list_recs_blastnRes = read_blastnRes2("012_blast_resut_all.txt")
    #for rec in list_recs_blastnRes:
    #    print("rec", rec, "<br><br>")
    #exit()
    conduct_blastdbcmd(list_recs_blastnRes, outfileName= "012_BLASThits.txt")


####################### Make multiple fast file

#print("blastHits_userDB", blastHits_userDB, "<br>")
if num_queries == "NoBlastSearch":
    #print("1111<br>")
    reverse_sequence_file(uploadedSequencesFile = "003_annonymousDB.txt", outfile = "015_queries_BLASThits.txt")
elif blastHits_anonDB == "NotSelected" and blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
    #print("2222<br>")
    reverse_sequence_file(uploadedSequencesFile = "003_annonymousDB.txt", outfile = "015_queries_BLASThits.txt")
else:
    #print("3333<br>")
    #addQuery2recFile_then_reverse(uploadedSequencesFile = "003_annonymousDB.txt", retrievedSequencesFile = "012_BLASThits.txt", outfile = "015_queries_BLASThits.txt")
    addQuery2recFile_then_reverse(uploadedSequencesFile = "005_querySequences.txt", retrievedSequencesFile = "012_BLASThits.txt", outfile = "015_queries_BLASThits.txt")

check_blasthits(eachDirAddressFN=eachDirAddress, infileName="015_queries_BLASThits.txt")



####################### Alignment

#print("num_queries", num_queries, "<br>")
#exit()
if num_queries != "NoBlastSearch":
    #print("num_queries != NoBlastSearch <br>")
    recs_blastout = add_recs_blastout_sequenceID("012_blast_resut_all.txt")
    recs_blastout_ANON1 = choose_recs_blastout_ANON1(recs_blastout)
    #for rec in recs_blastout_ANON1:
    #    print("rec", rec, "<br>")
    #exit()
    add_nameline_identities(recs_blastout_ANON1, fastafile="015_queries_BLASThits.txt", outfile="015_queries_BLASThits_identities.txt")
    maffLine1 = "PHYLOBARCODERscripts/mafft --preservecase " + eachDirAddress + "015_queries_BLASThits_identities.txt > " + eachDirAddress + "020_mafOut.txt"
else:
    print("else: num_queries != NoBlastSearch <br>")
    maffLine1 = "PHYLOBARCODERscripts/mafft --preservecase " + eachDirAddress + "015_queries_BLASThits.txt > " + eachDirAddress + "020_mafOut.txt"
####
#print("maffLine1", maffLine1, "<br>")
subprocess.call(maffLine1, shell=True)

trimLine1 = "PHYLOBARCODERscripts/trimal -out " + eachDirAddress + "030_trimalOut.fas.trm -htmlout " + eachDirAddress + "030_trimalOut.fas.trm.html -in " + eachDirAddress + "020_mafOut.txt -gappyout"
#print("trimLine1:", trimLine1, "\n");
subprocess.call(trimLine1, shell=True)

changeNameLine_trimalOutName(infile="030_trimalOut.fas.trm", outfile="035_trimalOut.fas.nameChanged.trm")


####################### Tree search

outgroup1 = outGroupSelect("035_trimalOut.fas.nameChanged.trm")
#print("outgroup1", outgroup1)
NJBSline1 = "PHYLOBARCODERscripts/" + rscriptTMP + " PHYLOBARCODERscripts/085_NJBSa.R " + eachDirAddress + "035_trimalOut.fas.nameChanged.trm " + outgroup1 + " TN93 " + num_bootstrap + " " + eachDirAddress + "085_NJBS1st.txt > " + eachDirAddress + "085_log.txt"
#print("NJBSline1", NJBSline1)
subprocess.call(NJBSline1, shell=True)
#exit()


####################### Taxon assignment

ignore_start_word = "ANON"
if num_queries == "NoBlastSearch":
    pass
elif blastHits_anonDB == "NotSelected" and blastHits_speciesDB == "NotSelected" and blastHits_haplotypeDB == "NotSelected" and blastHits_userDB == "NotSelected":
    pass
else:
    #print("## to make_taxonAssignmentFile_from_tree ##<br>")
    #make_taxonAssignment_from_blast(uploadedFile = "003_annonymousDB.txt", blastRefFile = "012_blast_resut_all.txt", mafoutFile="020_mafOut.txt", outfile = "100_taxon_assignment_blast.txt")
    #recs_blastIdentiries_UPLOAD1_vs_others_With_MaffoutName = make_recs_blastIdentiries_UPLOAD1_vs_others_With_MaffoutName(blastRefFile = "012_blast_resut_all.txt", mafoutFile="020_mafOut.txt")
    make_taxonAssignmentFile_from_tree(treeFile = "085_NJBS1st.txt", outfile_assign_tree = "100_taxon_assignment_tree.txt")
    #exit()


####################### Make summary

makeSummary()


####################### Tree plot

treePlotR = "PHYLOBARCODERscripts/" + rscriptTMP + " PHYLOBARCODERscripts/115_treePlot_pSCOPE.R " + eachDirAddress + "100_1stAnalysisSummary.txt " + eachDirAddress + "115_ > " + eachDirAddress + "115_logTreePlotB.txt"
#print("treePlotR: ", treePlotR)
#exit()
subprocess.call(treePlotR, shell=True)


#characters_total = fas2phy(fastaFileName = "020_mafOut.txt", outPhyFileName="130mafOutPhy.txt" )
characters_total = fas_reorder_by_tree(inFileName = "020_mafOut.txt", outFileName="130_mafOut_tree_order.txt")
#exit()
save_uploadSeqs(inFileName = "130_mafOut_tree_order.txt", outFileName="140_uploadSeqs_tree_order.txt")

make_resHTMLfile(infile = "020_mafOut.txt", queryFile = "003_annonymousDB.txt", outfile = "200_aln_nucl.html")

change_resHTMLfile(infile200 = "200_aln_nucl.html", outfile210 = "210_aln_nucl.html")


####################### Make download files

compression()



####################### Make result messages

elapsed_time = round((time.time() - startTime),1)
print ("Analysis time: {0}".format(elapsed_time) + " seconds")


htmlAddress = '<br>Finished: <a href="../phylobarcoderWork/' + str(dirname_rand) + '/200_aln_nucl.html" target="_blank">' + str(dirname_rand) + '</a>'
#htmlAddress = '<br>Finished: <a href="http://localhost/phylobarcoderWork/'              + str(dirname_rand) + '/200_aln_nucl.html" target="_blank">' + str(dirname_rand) + '</a><br><br>'

print(htmlAddress)
#print ("Analysis finished.<br>")

#resHtmlMaker()


exit()
