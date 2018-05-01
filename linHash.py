#linear Hashing
#Kritika Prakash
import sys
i = 0		#splitting round (determines hash function - h0 and h1 ... hi and h_i+1 )
p = 0		#which bucket needs to be split next p_sequence = {0,1; 0,1,2,3; 0,1,2,3,4,5,6,7; 0,1,2,3,4...15; 0,..31; ...}
S = 0		#total number of records
b = 2		#initial hash function modulo 2
b_new = 4
bucket_count = 2
linHash = {}	#global hash data structure - each bucket is a list of blocks, where each block is a list and of size B
block_count = {}
total_block_count = 2
block_count[0] = 1
block_count[1] = 1

########################################################################

#taking input parameters: filename, M, B
#filename = "input.txt"
filename = sys.argv[1]
M = int(sys.argv[2])		#number of buffers >=2, M-1 input buffers, 1 output buffer
B = int(sys.argv[3])		#buffer size = bucket size, M*B<=10^6
if B <= 4:
	B = 4					#min block size
if M <= 2:
	M = 2
output_buffer = []

########################################################################

#inserting the integer to the hash
def insertion (num):
	global S
	global total_block_count
	global output_buffer

	hash_val = num % b
	if hash_val < p:
		hash_val = num % b_new
	if hash_val not in linHash:
		linHash[hash_val] = [[] for _ in range(1)]

	flag = 0
	for i in range(block_count[hash_val]):
		if num in linHash[hash_val][i]:
			flag = 1
	if flag == 0:
		S += 1
		temp = block_count[hash_val] - 1
		if len(linHash[hash_val][temp]) >= (B * 0.25):
			total_block_count += 1
			temp += 1
			block_count[hash_val] += 1
			l = []
			linHash[hash_val].append(l)
		linHash[hash_val][temp].append(num)
		#print str(num)
		output_buffer.append(num)
		if len(output_buffer) >= ((B * 1.0) / 4.0):
			for val in output_buffer:
				print str(val)
			output_buffer = []

	if hash_table_too_full():
		create_new_bucket()

########################################################################

def hash_table_too_full():
	global b

	density = ( S * 400.0 ) / (B * total_block_count)
	if density > 75.0:
		return 1
	return 0

########################################################################

def create_new_bucket():
	global bucket_count
	global p
	global b
	global b_new
	global total_block_count

	bucket_count += 1
	#rehash values
	replace_array = []

	for i in range(block_count[p]):
		for value in linHash[p][i]:
			replace_array.append(value)

	total_block_count -= block_count[p]

	linHash[p] = [[] for _ in range(1)]
	block_count[p] = 1
	total_block_count += 1

	linHash[bucket_count - 1] = [[] for _ in range(1)]
	block_count[bucket_count - 1] = 1
	total_block_count += 1

	for value in replace_array:
		hash_val = value % b_new

		if hash_val not in linHash:
			linHash[hash_val] = [[] for _ in range(1)]
			block_count[hash_val] = 1
			total_block_count += 1

		flag = 0
		for j in range(block_count[hash_val]):
			if value in linHash[hash_val][j]:
				flag = 1

		if flag == 0:
			temp = block_count[hash_val] - 1
			if len(linHash[hash_val][temp]) >= (B * 0.25):
				temp += 1
				block_count[hash_val] += 1
				total_block_count += 1
				l = []
				linHash[hash_val].append(l)
			linHash[hash_val][temp].append(value)
	p += 1

	if bucket_count == b_new:
		b = b * 2
		b_new = 2 * b
		p = 0

	return 1

########################################################################

#reading from input file
input_buffer = []
fh = open(filename)
for line in fh:
	num = int(line.strip())
	input_buffer.append(num)
	if len(input_buffer) >= (((M-1) * B * 1.0) / 4.0) :
		for val in input_buffer:
			insertion(val)
		input_buffer = []

for val in input_buffer:
	insertion(val)
input_buffer = []
fh.close()

for val in output_buffer:
	print str(val)
output_buffer = []

#print linHash