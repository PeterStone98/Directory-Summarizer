import os,sys,subprocess,tarfile,glob,re

#get directory path
dir_path = sys.argv[1]

#sort files alphabetically
file_list = sorted(os.listdir(dir_path))

#for each file in directory make summary file
file_count=0 
for file in file_list:
	if(file[:9] != 'summary_a' and file != 'index.html' and file !=  'csc344.tar.gz' and file != 'body.txt') : 
		file_count += 1
		#gets all words
		regex = '(\w+)'
		#gets words contained in "", '', numbers, #.., /.., and %..
		anti_regex = '(\".*\"|\'.*\'|\d+|#.*|/.*|%.*)'				
		
		#get line count and idnetifiers
		line_count = 0
		match_list = []
	       	lines = open(file)
		for line in lines:
			#find all matches and anti matches
			anti_match_list = []
			match = re.findall(regex, line)
			anti_match = re.findall(anti_regex, line)
			if(anti_match != []):
				#split the list because it can be one big string right now
				anti_match = anti_match[0].split(' ')	
				for a in anti_match:
					#gets rid of all non alpha characters aka ./:#
					a = re.sub('[^a-zA-Z0-9]','',a)
					anti_match_list.append(a)
			if(match != []):
				for m in list(set(match) - set(anti_match_list)):
					match_list.append(m)
			line_count += 1
	
		#remove all strings that are composed of numbers
		match_list = [x for x in match_list if not x.isdigit()]	
	
		#open summary file and write to it
		summary_file = open('summary_a%s.html' % str(file_count),'w')
		summary_file.write("<html><body bgcolor = '#21DC97'><h1>")
		summary_file.write("Summary for A" + str(file_count))
		summary_file.write("</h1><br>File: ")
		summary_file.write("<a href='"+file+"'>"+file+"</a><br>")
		summary_file.write("</h1><br>Line count: ")
		summary_file.write(str(line_count))
		summary_file.write("<br>Summary:<br>")
		for string in sorted(set(match_list),key=lambda v: v.upper()):
			summary_file.write(string + '<br>')
		summary_file.write("</body></html>")
		summary_file.close()			


#create index file
index_file = open('%s.html' % 'index','w')
index_file.write("<html><body bgcolor='#21DCB9'><h1>Project Index for CSC344</h1><br>")

#for each file hyperlink summary file in index file
file_count=0
for file in file_list:
	if(file[:9] == 'summary_a'):
		index_file.write("<a href='"+file+"'>"+file+"</a><br>")
index_file.write("</body></html>")
index_file.close()

#tar directory
tar_file = tarfile.open("csc344.tar.gz","w:gz")
for file in file_list:
	tar_file.add(file)
tar_file.close()

#get tar file and recipient and send email
tar_file = dir_path + '/csc344.tar.gz'
recipient = raw_input("Please enter an email recipient: ")
os.system('echo "" | mutt -s "CSC Tar File" -a %s -- %s < body.txt' %(tar_file, recipient))
print("Email sent!")
