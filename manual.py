import bpcs

alpha = 0.45
vslfile = "input/test.png"
msgfile = "input/message.txt"
encfile = "output/encoded.png"
msgfile_decoded = "output/message.txt"

bpcs.encode(vslfile, msgfile, encfile, alpha)
# embed msgfile in vslfile, write to encfile
bpcs.decode(encfile, msgfile_decoded, alpha)  # recover message from encfile

